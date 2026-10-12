"""Compare the exact same calls with/without the boundary. No actions execute."""

import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

from .policy import Session, authorize


def replay(cases: list[dict], session: Session | None = None) -> dict:
    session = session or Session()
    digest = hashlib.sha256(json.dumps(cases, sort_keys=True).encode()).hexdigest()
    runs = {}
    for variant in ("baseline", "governed"):
        rows = []
        for case in cases:
            decision = authorize(session, case["call"])
            # Deliberately insecure baseline dispatches every synthetic call.
            allowed = True if variant == "baseline" else decision.allowed
            rows.append({"id": case["id"], "expect_allowed": case["expect_allowed"],
                         "allowed": allowed, "reason": "no-control" if variant == "baseline"
                         else decision.reason, "passed": allowed == case["expect_allowed"]})
        forbidden = [row for row in rows if not row["expect_allowed"]]
        legitimate = [row for row in rows if row["expect_allowed"]]
        runs[variant] = {"cases": rows,
            "forbidden_allowed": sum(row["allowed"] for row in forbidden),
            "forbidden_total": len(forbidden),
            "legitimate_blocked": sum(not row["allowed"] for row in legitimate),
            "legitimate_total": len(legitimate)}
    passed = all(row["passed"] for row in runs["governed"]["cases"])
    source = hashlib.sha256()
    for path in sorted(Path(__file__).parent.glob("*.py")):
        source.update(path.name.encode() + b"\0" + path.read_text(encoding="utf-8").encode() + b"\0")
    return {"schema_version": 1, "kind": "offline-policy-replay", "model_used": None,
            "source_sha256": source.hexdigest(), "python_version": platform.python_version(),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "suite_sha256": digest, "case_count": len(cases),
            "verdict": "PASS" if passed else "FAIL", "runs": runs,
            "limits": "Synthetic policy checks only. No LLM, tool execution, real files or network."
    }
