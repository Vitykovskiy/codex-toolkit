#!/usr/bin/env python3
"""Normalize saved native event streams for conservative token accounting.

The adapter deliberately understands only observed CLI-style event shapes.  It
binds terminal events without repeated IDs to the preceding ``thread.started``
and active ``turn.started``. Such a request is labelled with a local,
stream-scoped provenance key; it is never presented as a provider request ID.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from tools.token_usage import UsageError, summarize
except ModuleNotFoundError:  # pragma: no cover
    from token_usage import UsageError, summarize


class NativeUsageError(ValueError):
    """The native trace cannot prove the requested accounting coverage."""


TERMINAL = {"turn.completed": "completed", "turn.failed": "failed",
            "turn.interrupted": "interrupted", "turn_complete": "completed"}


def _mapping(value, label):
    if not isinstance(value, dict):
        raise NativeUsageError(f"{label} must be an object")
    return value


def _identifier(event, key, nested):
    value = event.get(key)
    if isinstance(value, str) and value.strip():
        return value
    for parent, child in nested:
        data = event.get(parent)
        if isinstance(data, dict):
            value = data.get(child)
            if isinstance(value, str) and value.strip():
                return value
    return None


def _usage(event):
    value = event.get("usage")
    if value is None and isinstance(event.get("turn"), dict):
        value = event["turn"].get("usage")
    if value is None:
        return None
    data = _mapping(value, "usage")
    aliases = {
        "input_tokens": ("input_tokens", "input"),
        "output_tokens": ("output_tokens", "output"),
        "cached_input_tokens": ("cached_input_tokens", "cached_input"),
        "cache_write_input_tokens": ("cache_write_input_tokens", "cache_write_input"),
        "reasoning_tokens": ("reasoning_tokens", "reasoning_output_tokens", "reasoning"),
    }
    normalized = {}
    for target, candidates in aliases.items():
        actual = next((data[name] for name in candidates if name in data), None)
        if actual is None:
            if target in {"input_tokens", "output_tokens"}:
                raise NativeUsageError(f"usage lacks {target}")
            continue
        if type(actual) is not int or actual < 0:
            raise NativeUsageError(f"usage.{target} must be a non-negative integer")
        normalized[target] = actual
    if "cached_input_tokens" in normalized:
        normalized["cached_input_semantics"] = "included"
    if "reasoning_tokens" in normalized:
        normalized["reasoning_semantics"] = "included"
    return normalized


def normalize(events, expected_threads=(), stream_identity="capture"):
    """Return normalized terminal turns plus evidence-based coverage facts.

    ``expected_threads`` is a required lineage, not a claim that an event stream
    contains all children. An unfinished observed turn, empty stream, absent
    expected thread, malformed terminal event, or unknown usage is partial.
    """
    if not isinstance(stream_identity, str) or not stream_identity.strip():
        raise NativeUsageError("stream_identity must be a nonblank string")
    records, threads, active, notes = {}, set(), {}, []
    current_thread, ordinal, terminal_seen = None, 0, False
    for sequence, raw in enumerate(events, 1):
        event = _mapping(raw, f"event {sequence}")
        event_type = event.get("type")
        thread_id = _identifier(event, "thread_id", (("thread", "id"),))
        if event_type == "thread.started":
            if thread_id is None:
                notes.append(f"event {sequence} thread.started lacks thread_id")
                current_thread = None
            else:
                threads.add(thread_id)
                current_thread = thread_id
            continue
        if thread_id is not None:
            threads.add(thread_id)
            current_thread = thread_id
        if event_type == "turn.started":
            if current_thread is None:
                notes.append(f"event {sequence} turn.started lacks thread context")
                continue
            supplied = _identifier(event, "turn_id", (("turn", "id"), ("turn", "turn_id")))
            ordinal += 1
            active[current_thread] = supplied or f"local:{stream_identity}:turn:{ordinal}"
            continue
        if event_type not in TERMINAL:
            continue
        terminal_seen = True
        if current_thread is None:
            notes.append(f"event {sequence} terminal turn lacks thread context")
            continue
        supplied = _identifier(event, "turn_id", (("turn", "id"), ("turn", "turn_id")))
        turn_id = supplied or active.get(current_thread)
        if turn_id is None:
            notes.append(f"event {sequence} terminal turn lacks active turn context")
            continue
        try:
            usage = _usage(event)
        except NativeUsageError as error:
            notes.append(f"event {sequence}: {error}")
            usage = None
        outcome = event.get("status") if isinstance(event.get("status"), str) else TERMINAL[event_type]
        record = {
            "schema": "token_usage/v1", "scope": current_thread, "request_id": turn_id,
            "coverage": "complete" if usage is not None else "unknown", "outcome": outcome,
            "aggregate_of": [], "usage": usage,
            "provenance": {"stream": stream_identity, "sequence": sequence,
                           "request_id_kind": "provider" if supplied else "local",
                           "counter_kind": "turn_delta"},
        }
        key = (current_thread, turn_id)
        if key in records:
            previous = dict(records[key])
            current = dict(record)
            previous.pop("provenance")
            current.pop("provenance")
            if previous != current:
                raise NativeUsageError(f"conflicting terminal values for {current_thread}/{turn_id}")
        else:
            records[key] = record
        active.pop(current_thread, None)
    missing = sorted(set(expected_threads) - threads)
    if not terminal_seen:
        notes.append("capture has no terminal turn event")
    for thread_id, turn_id in sorted(active.items()):
        notes.append(f"thread {thread_id} has unterminated turn {turn_id}")
    for thread_id in missing:
        notes.append(f"missing expected thread: {thread_id}")
    if not records:
        notes.append("capture has no attributable terminal usage")
    coverage = "complete" if not notes and all(record["usage"] is not None for record in records.values()) else "partial"
    return {"events": list(records.values()), "coverage": coverage,
            "observed_threads": sorted(threads), "missing_threads": missing, "notes": notes}


def load_jsonl(path):
    events = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise NativeUsageError(f"line {number}: invalid JSON: {error.msg}") from error
    return events


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path, help="raw native JSONL trace")
    parser.add_argument("--expected-thread", action="append", default=[])
    parser.add_argument("--stream-identity", default="capture")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        normalized = normalize(load_jsonl(args.trace), args.expected_thread, args.stream_identity)
        accounting = summarize(normalized["events"])
    except (OSError, NativeUsageError, UsageError) as error:
        print(json.dumps({"status": "unsupported", "detail": str(error)}))
        return 2
    if args.output:
        args.output.write_text("".join(json.dumps(event, sort_keys=True) + "\n" for event in normalized["events"]), encoding="utf-8")
    if normalized["coverage"] != "complete":
        accounting = {**accounting, "status": "unknown", "coverage": "partial",
                      "logical_tokens_total": None, "notes": accounting["notes"] + normalized["notes"]}
    print(json.dumps({**normalized, "accounting": accounting}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
