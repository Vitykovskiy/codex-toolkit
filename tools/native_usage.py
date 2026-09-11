#!/usr/bin/env python3
"""Normalize Codex ``exec --json`` turn events for campaign accounting.

This adapter is intentionally local and offline.  It preserves the raw trace,
does not infer missing child usage, and writes only the documented
``token_usage/v1`` records consumed by :mod:`tools.token_usage`.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:  # ``python tools/native_usage.py`` and ``python -m tools.native_usage``.
    from tools.token_usage import UsageError, summarize
except ModuleNotFoundError:  # pragma: no cover - exercised by the CLI itself.
    from token_usage import UsageError, summarize


class NativeUsageError(ValueError):
    """The native trace cannot prove the requested accounting coverage."""


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
    # Codex CLI's turn usage counters include cached/reasoning values in input
    # and output unless a native trace states otherwise.  Do not double count.
    if "cached_input_tokens" in normalized:
        normalized["cached_input_semantics"] = "included"
    if "reasoning_tokens" in normalized:
        normalized["reasoning_semantics"] = "included"
    return normalized


def normalize(events, expected_threads=()):
    """Return normalized events and coverage facts from parsed native JSONL.

    A completed turn is one accounting record.  Repeated cumulative updates for
    the same ``thread_id``/``turn_id`` replace the earlier record rather than
    being added.  Missing expected threads or a completed turn with unknown
    usage force partial coverage; they are represented, never treated as zero.
    """
    records = {}
    observed_threads = set()
    malformed = []
    for sequence, raw in enumerate(events, 1):
        event = _mapping(raw, f"event {sequence}")
        event_type = event.get("type")
        if event_type not in {"turn.completed", "turn.updated", "turn_complete"}:
            continue
        thread_id = _identifier(event, "thread_id", (("thread", "id"),))
        turn_id = _identifier(event, "turn_id", (("turn", "id"), ("turn", "turn_id")))
        if thread_id is None or turn_id is None:
            malformed.append(f"event {sequence} lacks thread_id or turn_id")
            continue
        observed_threads.add(thread_id)
        try:
            usage = _usage(event)
        except NativeUsageError as error:
            malformed.append(f"event {sequence}: {error}")
            usage = None
        outcome = event.get("status") if isinstance(event.get("status"), str) else "completed"
        records[(thread_id, turn_id)] = {
            "schema": "token_usage/v1",
            "scope": thread_id,
            "request_id": turn_id,
            "coverage": "complete" if usage is not None else "unknown",
            "outcome": outcome,
            "aggregate_of": [],
            "usage": usage,
        }
    missing = sorted(set(expected_threads) - observed_threads)
    result = list(records.values())
    coverage = "complete" if not malformed and not missing else "partial"
    return {
        "events": result,
        "coverage": coverage,
        "observed_threads": sorted(observed_threads),
        "missing_threads": missing,
        "notes": malformed + [f"missing expected thread: {thread}" for thread in missing],
    }


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
    parser.add_argument("trace", type=Path, help="raw Codex exec --json JSONL")
    parser.add_argument("--expected-thread", action="append", default=[], help="thread ID that must be observed")
    parser.add_argument("--output", type=Path, help="normalized token_usage/v1 JSONL output")
    args = parser.parse_args(argv)
    try:
        normalized = normalize(load_jsonl(args.trace), args.expected_thread)
        accounting = summarize(normalized["events"])
    except (OSError, NativeUsageError, UsageError) as error:
        print(json.dumps({"status": "unsupported", "detail": str(error)}))
        return 2
    if args.output:
        args.output.write_text("".join(json.dumps(event, sort_keys=True) + "\n" for event in normalized["events"]), encoding="utf-8")
    if normalized["coverage"] != "complete":
        accounting = {
            **accounting,
            "status": "unknown",
            "coverage": "partial",
            "logical_tokens_total": None,
            "notes": accounting["notes"] + normalized["notes"],
        }
    result = {**normalized, "accounting": accounting}
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
