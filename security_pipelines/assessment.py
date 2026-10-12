"""Generate an evidence-linked assessment pack without inventing AI test results."""

import hashlib
import json
from pathlib import Path

from .assessment_content import documents
from .assessment_view import render


def write_assessment(result: dict, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    entries = []
    for name, title, content in documents(result):
        text = (f"# {title}\n\nRun UTC: {result['timestamp_utc']}\n\n"
                f"Evidence: `../report.json` · Suite SHA-256: `{result['suite_sha256']}`\n\n"
                + content + "\n")
        (destination / name).write_text(text, encoding="utf-8")
        entries.append({"file": name, "title": title,
                        "sha256": hashlib.sha256((destination / name).read_bytes()).hexdigest()})
    (destination / "index.html").write_text(render(result, entries), encoding="utf-8")
    manifest = {"schema_version": 1, "timestamp_utc": result["timestamp_utc"],
                "suite_sha256": result["suite_sha256"], "evaluation_verdict": result["verdict"],
                "source_sha256": result["source_sha256"], "python_version": result["python_version"],
                "assessment_scope": "synthetic offline tool-boundary replay",
                "production_readiness": "NOT ASSESSED", "reviewer_signoff": "PENDING",
                "model_used": None, "documents": entries,
                "index_sha256": hashlib.sha256((destination / "index.html").read_bytes()).hexdigest(),
                "report_sha256": hashlib.sha256(
                    (destination.parent / "report.json").read_bytes()).hexdigest()}
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
