import unittest

from tools.token_usage import UsageError, summarize


def event(request_id, **changes):
    value = {
        "schema": "token_usage/v1", "scope": "run-1", "request_id": request_id,
        "coverage": "complete", "outcome": "accepted", "aggregate_of": [],
        "usage": {"input_tokens": 10, "output_tokens": 5},
    }
    value.update(changes)
    return value


class TokenUsageTests(unittest.TestCase):
    def test_manual_arithmetic_and_nested_categories(self):
        result = summarize([event("a", usage={
            "input_tokens": 10, "output_tokens": 5,
            "cached_input_tokens": 4, "cached_input_semantics": "included",
            "reasoning_tokens": 3, "reasoning_semantics": "included",
        }), event("b", usage={
            "input_tokens": 2, "output_tokens": 1,
            "cached_input_tokens": 7, "cached_input_semantics": "separate",
        })])
        self.assertEqual(25, result["logical_tokens_total"])
        self.assertEqual(12.5, result["logical_tokens_per_accepted"])

    def test_exact_duplicate_is_idempotent_and_conflict_is_rejected(self):
        first = event("a")
        self.assertEqual(15, summarize([first, dict(first)])["logical_tokens_total"])
        with self.assertRaisesRegex(UsageError, "conflicting duplicate"):
            summarize([first, event("a", outcome="failed")])

    def test_parent_child_aggregate_uses_children_once(self):
        parent = event("parent", usage={"input_tokens": 100, "output_tokens": 100}, aggregate_of=["child"])
        result = summarize([parent, event("child")])
        self.assertEqual(15, result["logical_tokens_total"])
        self.assertEqual(1, result["counted_requests"])

    def test_direct_and_long_aggregate_cycles_are_rejected(self):
        direct = event("a", aggregate_of=["b"])
        with self.assertRaisesRegex(UsageError, "aggregate cycle"):
            summarize([direct, event("b", aggregate_of=["a"])])
        with self.assertRaisesRegex(UsageError, "aggregate cycle"):
            summarize([
                event("a", aggregate_of=["b"]),
                event("b", aggregate_of=["c"]),
                event("c", aggregate_of=["a"]),
            ])

    def test_missing_child_or_usage_makes_total_unknown(self):
        result = summarize([event("parent", aggregate_of=["missing"])])
        self.assertIsNone(result["logical_tokens_total"])
        self.assertEqual("unknown", result["status"])
        result = summarize([event("missing-usage", usage=None, outcome="failed")])
        self.assertIsNone(result["logical_tokens_total"])
        self.assertEqual(1, result["missing_usage_requests"])

    def test_partial_failed_resume_and_compaction_remain_accounted(self):
        result = summarize([
            event("failed", outcome="failed"),
            event("resume", outcome="resumed"),
            event("compaction", coverage="partial", outcome="completed"),
        ])
        self.assertEqual(45, result["logical_tokens_known"])
        self.assertIsNone(result["logical_tokens_total"])

    def test_zero_accepted_has_no_ratio(self):
        result = summarize([event("failed", outcome="failed")])
        self.assertEqual(0, result["accepted_requests"])
        self.assertIsNone(result["logical_tokens_per_accepted"])

    def test_unsupported_schema_is_rejected(self):
        with self.assertRaisesRegex(UsageError, "unsupported schema"):
            summarize([event("a", schema="provider-payload")])
