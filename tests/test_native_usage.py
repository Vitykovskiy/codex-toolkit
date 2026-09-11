import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from tools.native_usage import NativeUsageError, main, normalize
from tools.token_usage import summarize


def event(kind, **values):
    return {"type": kind, **values}


class NativeUsageTests(unittest.TestCase):
    def test_real_cli_shape_binds_to_thread_and_local_turn(self):
        result = normalize([
            event("thread.started", thread_id="root"), event("turn.started"),
            event("turn.completed", usage={"input_tokens": 468271, "cached_input_tokens": 427520,
                                           "cache_write_input_tokens": 0, "output_tokens": 2514,
                                           "reasoning_output_tokens": 692}),
        ], ["root"], "fixture")
        self.assertEqual("complete", result["coverage"])
        self.assertEqual("local:fixture:turn:1", result["events"][0]["request_id"])
        self.assertEqual("local", result["events"][0]["provenance"]["request_id_kind"])
        self.assertEqual(470785, summarize(result["events"])["logical_tokens_total"])

    def test_failed_interrupted_resumed_and_unknown_usage_are_retained(self):
        result = normalize([
            event("thread.started", thread_id="child"), event("turn.started", turn_id="one"),
            event("turn.failed", turn_id="one", usage={"input_tokens": 2, "output_tokens": 1}),
            event("turn.started", turn_id="two"), event("turn.interrupted", turn_id="two"),
            event("turn.started", turn_id="three"),
            event("turn.completed", turn_id="three", usage={"input_tokens": 4, "output_tokens": 1}, status="resumed"),
        ], ["child"])
        self.assertEqual("partial", result["coverage"])
        self.assertEqual(["failed", "interrupted", "resumed"], [x["outcome"] for x in result["events"]])
        self.assertEqual(2, result["events"][0]["usage"]["input_tokens"])
        self.assertIsNone(result["events"][1]["usage"])

    def test_exact_duplicate_terminal_is_idempotent_but_conflict_errors(self):
        first = event("turn.completed", thread_id="root", turn_id="one", usage={"input_tokens": 2, "output_tokens": 1})
        result = normalize([event("thread.started", thread_id="root"), event("turn.started", turn_id="one"), first, dict(first)])
        self.assertEqual(1, len(result["events"]))
        conflict = dict(first, usage={"input_tokens": 3, "output_tokens": 1})
        with self.assertRaisesRegex(NativeUsageError, "conflicting terminal"):
            normalize([event("thread.started", thread_id="root"), event("turn.started", turn_id="one"), first, conflict])

    def test_progress_empty_missing_child_and_unfinished_turn_are_partial(self):
        progress = normalize([event("thread.started", thread_id="root"), event("turn.started"), event("turn.updated")], ["root", "child"])
        self.assertEqual("partial", progress["coverage"])
        self.assertEqual([], progress["events"])
        self.assertIn("child", progress["missing_threads"])
        self.assertEqual("partial", normalize([])["coverage"])

    def test_cli_never_reports_partial_trace_as_complete_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            trace = Path(directory) / "trace.jsonl"
            trace.write_text(json.dumps(event("turn.updated")) + "\n", encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(0, main([str(trace)]))
        result = json.loads(output.getvalue())
        self.assertEqual("partial", result["accounting"]["coverage"])
        self.assertIsNone(result["accounting"]["logical_tokens_total"])

    def test_non_mapping_event_is_rejected(self):
        with self.assertRaisesRegex(NativeUsageError, "must be an object"):
            normalize([[]])
