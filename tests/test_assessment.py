import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from security_pipelines.cli import main
from security_pipelines.assessment import write_assessment
from security_pipelines.policy import Session
from security_pipelines.replay import replay
from security_pipelines.reports import write_reports
from security_pipelines.suite import load_suite


class AssessmentTests(unittest.TestCase):
    def setUp(self):
        self.cases = load_suite(Path("suites/agent-boundaries.json"))

    def test_pack_is_bound_to_actual_evidence(self):
        with tempfile.TemporaryDirectory() as root:
            out = Path(root)
            self.assertEqual(main(["demo", "--out", str(out)]), 0)
            report = json.loads((out / "report.json").read_text())
            pack = out / "assessment"
            manifest = json.loads((pack / "manifest.json").read_text())
            self.assertEqual(manifest["suite_sha256"], report["suite_sha256"])
            self.assertEqual(manifest["source_sha256"], report["source_sha256"])
            self.assertEqual(manifest["timestamp_utc"], report["timestamp_utc"])
            self.assertEqual(manifest["report_sha256"], hashlib.sha256((out / "report.json").read_bytes()).hexdigest())
            self.assertEqual(manifest["index_sha256"], hashlib.sha256((pack / "index.html").read_bytes()).hexdigest())
            self.assertEqual(len(manifest["documents"]), 10)
            for entry in manifest["documents"]:
                data = (pack / entry["file"]).read_bytes()
                self.assertEqual(entry["sha256"], hashlib.sha256(data).hexdigest())
                self.assertIn(report["suite_sha256"], data.decode())
            self.assertEqual(manifest["production_readiness"], "NOT ASSESSED")
            self.assertEqual(manifest["reviewer_signoff"], "PENDING")
            self.assertIsNone(manifest["model_used"])

    def test_failed_run_stays_failed_in_pack(self):
        result = replay(self.cases, Session(verified=False))
        with tempfile.TemporaryDirectory() as root:
            out = Path(root)
            write_reports(result, out)
            write_assessment(result, out / "assessment")
            manifest = json.loads((out / "assessment/manifest.json").read_text())
            self.assertEqual(manifest["evaluation_verdict"], "FAIL")
            self.assertIn("Offline evaluation: FAIL", (out / "assessment/index.html").read_text())
            self.assertIn("NOT RUN", (out / "assessment/06-evaluation-plan-and-results.md").read_text())

    def test_report_write_error_fails_command(self):
        with tempfile.TemporaryDirectory() as root:
            out = Path(root) / "occupied"
            out.write_text("not a directory")
            self.assertEqual(main(["demo", "--out", str(out)]), 2)

    def test_context_requires_verified_boolean(self):
        for value in ("true", 1, [], None):
            result = replay(self.cases, Session(verified=value))
            self.assertEqual(result["verdict"], "FAIL")
            self.assertEqual(result["runs"]["governed"]["forbidden_allowed"], 0)

    def test_invalid_suite_labels_and_schema_are_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "suite.json"
            for data in ({"schema_version": True, "cases": self.cases},
                         {"schema_version": 1, "cases": [{**self.cases[0], "id": "<script>"}, *self.cases[1:]]}):
                path.write_text(json.dumps(data), encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_suite(path)


if __name__ == "__main__":
    unittest.main()
