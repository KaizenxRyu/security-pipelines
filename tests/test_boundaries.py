import json
import tempfile
import unittest
from pathlib import Path

from security_pipelines.cli import main
from security_pipelines.policy import Session, authorize
from security_pipelines.replay import replay
from security_pipelines.reports import write_reports
from security_pipelines.suite import load_suite


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.cases = load_suite(Path("suites/agent-boundaries.json"))

    def test_entire_registered_suite(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(authorize(Session(), case["call"]).allowed, case["expect_allowed"])

    def test_unverified_context_cannot_be_overridden_by_arguments(self):
        for verified in ("true", True, 1):
            call = {"tool": "read_invoice", "args": {"account_id": "demo-account", "verified": verified}}
            self.assertFalse(authorize(Session(verified=False), call).allowed)

    def test_all_tools_deny_missing_identity(self):
        for case in self.cases:
            self.assertFalse(authorize(Session(account_id=""), case["call"]).allowed)

    def test_unknown_structure_fails_closed(self):
        for call in (None, [], {}, {"tool": "read_invoice"}, {"tool": None, "args": {}},
                     {"tool": "read_invoice", "args": []}):
            self.assertFalse(authorize(Session(), call).allowed)

    def test_same_fixture_digest_and_distinct_metrics(self):
        result = replay(self.cases)
        self.assertEqual(result["suite_sha256"], replay(self.cases)["suite_sha256"])
        self.assertEqual(result["verdict"], "PASS")
        self.assertGreater(result["runs"]["baseline"]["forbidden_allowed"], 0)
        self.assertEqual(result["runs"]["governed"]["forbidden_allowed"], 0)
        self.assertEqual(result["runs"]["governed"]["legitimate_blocked"], 0)
        self.assertIsNone(result["model_used"])

    def test_overrefusal_is_failure(self):
        result = replay(self.cases, Session(verified=False))
        self.assertEqual(result["verdict"], "FAIL")
        self.assertGreater(result["runs"]["governed"]["legitimate_blocked"], 0)

    def test_suite_change_changes_digest(self):
        self.assertNotEqual(replay(self.cases)["suite_sha256"], replay(self.cases[:-1])["suite_sha256"])

    def test_schema_errors_never_return_success(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "suite.json"
            bad = ({}, {"schema_version": 1, "cases": []},
                   {"schema_version": 1, "cases": [self.cases[0], self.cases[0]]},
                   {"schema_version": 1, "cases": [{**self.cases[0], "expect_allowed": "false"}]})
            for data in bad:
                path.write_text(json.dumps(data), encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_suite(path)
                self.assertEqual(main(["demo", "--suite", str(path), "--out", str(Path(root)/"out")]), 2)
            self.assertFalse((Path(root) / "out/report.json").exists())

    def test_report_roundtrip_and_no_tool_arguments(self):
        with tempfile.TemporaryDirectory() as root:
            result = replay(self.cases)
            write_reports(result, Path(root))
            self.assertEqual(json.loads((Path(root)/"report.json").read_text()), result)
            self.assertIn("Synthetic policy", (Path(root)/"report.html").read_text())
            self.assertNotIn("tool", result["runs"]["governed"]["cases"][0])

    def test_report_escapes_custom_case_labels(self):
        result = replay(self.cases, Session(verified=False))
        result["runs"]["governed"]["cases"][0]["id"] = "<script>bad()</script>"
        with tempfile.TemporaryDirectory() as root:
            write_reports(result, Path(root))
            content = (Path(root)/"report.html").read_text()
            self.assertNotIn("<script>", content)
            self.assertIn("&lt;script&gt;", content)


if __name__ == "__main__":
    unittest.main()
