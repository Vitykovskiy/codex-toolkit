import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from tools.native_usage import NativeUsageError, main, normalize


def turn(thread, turn_id, usage=None, event_type="turn.completed", **extra):
    event = {"type": event_type, "thread_id": thread, "turn_id": turn_id}
    if usage is not None:
        event["usage"] = usage
    event.update(extra)
    return event


class NativeUsageTests(unittest.TestCase):
    def test_root_and_two_children_have_complete_coverage(self):
        result = normalize([
            turn("root", "r1", {"input_tokens": 10, "output_tokens": 2}),
            turn("child-a", "a1", {"input_tokens": 3, "output_tokens": 1}),
            turn("child-b", "b1", {"input_tokens": 4, "output_tokens": 1}),
        ], ["root", "child-a", "child-b"])
        self.assertEqual("complete", result["coverage"])
        self.assertEqual([], result["missing_threads"])
        self.assertEqual(3, len(result["events"]))

    def test_cumulative_update_and_duplicate_count_once(self):
        result = normalize([
            turn("child", "t1", {"input_tokens": 2, "output_tokens": 1}, "turn.updated"),
            turn("child", "t1", {"input_tokens": 8, "output_tokens": 3}),
            turn("child", "t1", {"input_tokens": 8, "output_tokens": 3}),
        ], ["child"])
        self.assertEqual(1, len(result["events"]))
        self.assertEqual(8, result["events"][0]["usage"]["input_tokens"])

    def test_resume_is_separate_turn_and_failed_known_usage_is_retained(self):
        result = normalize([
            turn("child", "before-restart", {"input_tokens": 2, "output_tokens": 1}, status="failed"),
            turn("child", "after-restart", {"input_tokens": 4, "output_tokens": 1}, status="resumed"),
        ], ["child"])
        self.assertEqual(2, len(result["events"]))
        self.assertEqual(["failed", "resumed"], [event["outcome"] for event in result["events"]])

    def test_failed_unknown_usage_and_missing_child_are_partial(self):
        result = normalize([turn("root", "r1", None, status="failed")], ["root", "child"])
        self.assertEqual("partial", result["coverage"])
        self.assertEqual(["child"], result["missing_threads"])
        self.assertIsNone(result["events"][0]["usage"])

    def test_missing_identity_is_not_silently_counted(self):
        result = normalize([{"type": "turn.completed", "usage": {"input_tokens": 1, "output_tokens": 1}}])
        self.assertEqual([], result["events"])
        self.assertEqual("partial", result["coverage"])
        self.assertIn("lacks thread_id", result["notes"][0])

    def test_bad_usage_is_preserved_as_unknown_coverage(self):
        result = normalize([turn("root", "r1", {"input_tokens": True, "output_tokens": 1})], ["root"])
        self.assertEqual("partial", result["coverage"])
        self.assertIsNone(result["events"][0]["usage"])

    def test_codex_reasoning_output_alias_is_included_once(self):
        result = normalize([turn("root", "r1", {
            "input_tokens": 10, "output_tokens": 2, "reasoning_output_tokens": 3,
        })], ["root"])
        self.assertEqual("included", result["events"][0]["usage"]["reasoning_semantics"])

    def test_cache_write_usage_is_retained_separately(self):
        result = normalize([turn("root", "r1", {
            "input_tokens": 10, "output_tokens": 2, "cache_write_input_tokens": 7,
        })], ["root"])
        self.assertEqual(7, result["events"][0]["usage"]["cache_write_input_tokens"])

    def test_non_mapping_event_is_rejected(self):
        with self.assertRaisesRegex(NativeUsageError, "must be an object"):
            normalize([[]])

    def test_cli_does_not_report_complete_zero_for_partial_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            trace = Path(directory) / "trace.jsonl"
            trace.write_text(json.dumps({"type": "turn.completed", "usage": {"input_tokens": 1, "output_tokens": 1}}) + "\n")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(0, main([str(trace)]))
            result = json.loads(output.getvalue())
        self.assertEqual("partial", result["accounting"]["coverage"])
        self.assertIsNone(result["accounting"]["logical_tokens_total"])
