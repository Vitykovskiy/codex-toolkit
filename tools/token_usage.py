#!/usr/bin/env python3
"""Read-only accounting for documented local ``token_usage/v1`` JSONL events.

This tool deliberately accepts no provider, SDK, or OpenTelemetry payload.  It
normalizes only the small local format documented in docs/token-accounting.md.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


SCHEMA = "token_usage/v1"
SEMANTICS = {"included", "separate"}
COVERAGE = {"complete", "partial", "unknown"}


class UsageError(ValueError):
    """A malformed or mutually conflicting normalized event."""


def _integer(value, name):
    if type(value) is not int or value < 0:
        raise UsageError(f"{name} must be a non-negative integer")
    return value


def _event(value):
    if not isinstance(value, dict):
        raise UsageError("event must be an object")
    if value.get("schema") != SCHEMA:
        raise UsageError("unsupported schema")
    for name in ("scope", "request_id", "coverage", "outcome"):
        if not isinstance(value.get(name), str) or not value[name].strip():
            raise UsageError(f"{name} must be a nonblank string")
    if value["coverage"] not in COVERAGE:
        raise UsageError("coverage must be complete, partial, or unknown")
    aggregate_of = value.get("aggregate_of", [])
    if not isinstance(aggregate_of, list) or any(not isinstance(item, str) or not item for item in aggregate_of):
        raise UsageError("aggregate_of must be a list of nonblank request IDs")
    if len(set(aggregate_of)) != len(aggregate_of) or value["request_id"] in aggregate_of:
        raise UsageError("aggregate_of must not repeat or contain request_id")
    usage = value.get("usage")
    if usage is not None:
        if not isinstance(usage, dict):
            raise UsageError("usage must be an object or null")
        for name in ("input_tokens", "output_tokens"):
            _integer(usage.get(name), f"usage.{name}")
        for name, semantic in (("cached_input_tokens", "cached_input_semantics"),
                               ("reasoning_tokens", "reasoning_semantics")):
            if name in usage:
                _integer(usage[name], f"usage.{name}")
                if usage.get(semantic) not in SEMANTICS:
                    raise UsageError(f"usage.{semantic} must be included or separate")
            elif semantic in usage:
                raise UsageError(f"usage.{semantic} requires {name}")
    return value


def _logical_tokens(usage):
    total = usage["input_tokens"] + usage["output_tokens"]
    for name, semantic in (("cached_input_tokens", "cached_input_semantics"),
                           ("reasoning_tokens", "reasoning_semantics")):
        if usage.get(semantic) == "separate":
            total += usage[name]
    return total


def _reject_aggregate_cycles(requests):
    """Reject cycles before aggregate parents can be excluded from accounting."""
    visiting = set()
    visited = set()

    def visit(key):
        if key in visiting:
            raise UsageError(f"aggregate cycle: {key[1]}")
        if key in visited:
            return
        visiting.add(key)
        event = requests[key]
        for child_id in event["aggregate_of"]:
            child = (event["scope"], child_id)
            if child in requests:
                visit(child)
        visiting.remove(key)
        visited.add(key)

    for key in requests:
        visit(key)


def summarize(events):
    """Return accounting result for normalized event mappings.

    Identical duplicate events are idempotent. Conflicting values for one
    request ID raise UsageError. Aggregate parents are excluded when every
    listed child is present in the same scope; otherwise coverage is unknown.
    """
    requests = {}
    for raw in events:
        event = _event(raw)
        key = (event["scope"], event["request_id"])
        if key in requests:
            if requests[key] != event:
                raise UsageError(f"conflicting duplicate request ID: {event['request_id']}")
            continue
        requests[key] = event

    _reject_aggregate_cycles(requests)

    excluded = set()
    incomplete = False
    notes = []
    for key, event in requests.items():
        if not event["aggregate_of"]:
            continue
        children = [(event["scope"], child) for child in event["aggregate_of"]]
        if all(child in requests for child in children):
            excluded.add(key)
        else:
            incomplete = True
            notes.append(f"aggregate {event['request_id']} has missing child coverage")

    known_total = 0
    accepted = 0
    missing_usage = 0
    partial = incomplete
    counted = 0
    for key, event in requests.items():
        if key in excluded:
            continue
        counted += 1
        if event["coverage"] != "complete":
            partial = True
        if event["usage"] is None:
            missing_usage += 1
            partial = True
            continue
        known_total += _logical_tokens(event["usage"])
        if event["outcome"] == "accepted":
            accepted += 1

    coverage = "complete" if not partial else "partial"
    return {
        "schema": SCHEMA,
        "status": "complete" if coverage == "complete" else "unknown",
        "logical_tokens_known": known_total,
        "logical_tokens_total": known_total if coverage == "complete" else None,
        "coverage": coverage,
        "unique_requests": len(requests),
        "counted_requests": counted,
        "missing_usage_requests": missing_usage,
        "accepted_requests": accepted,
        "logical_tokens_per_accepted": known_total / accepted if accepted else None,
        "notes": notes,
    }


def load_jsonl(path):
    events = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise UsageError(f"line {number}: invalid JSON: {error.msg}") from error
    return events


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path, help="normalized token_usage/v1 JSONL file")
    args = parser.parse_args(argv)
    try:
        result = summarize(load_jsonl(args.events))
    except (OSError, UsageError) as error:
        print(json.dumps({"schema": SCHEMA, "status": "unsupported", "detail": str(error)}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
