"""One explicit pipeline command; malformed inputs return an error, never PASS."""

import argparse
import json
import sys
from pathlib import Path

from .replay import replay
from .reports import write_reports
from .suite import load_suite
from .assessment import write_assessment


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline agent boundary security pipeline")
    parser.add_argument("command", choices=["demo"])
    parser.add_argument("--suite", type=Path, default=Path("suites/agent-boundaries.json"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/agent-boundaries"))
    args = parser.parse_args(argv)
    try:
        result = replay(load_suite(args.suite))
        write_reports(result, args.out)
        write_assessment(result, args.out / "assessment")
    except (OSError, ValueError, TypeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(json.dumps({"verdict": result["verdict"], "case_count": result["case_count"],
                      "report": str(args.out / "report.html"), "model_used": None}))
    return 0 if result["verdict"] == "PASS" else 1
