"""Validate an explicit case list before executing any replay."""

import json
import re
from pathlib import Path


def load_suite(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(data, dict) or type(data.get("schema_version")) is not int
            or data["schema_version"] != 1):
        raise ValueError("Unsupported suite schema")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Suite must contain cases")
    seen = set()
    kinds = set()
    for case in cases:
        if not isinstance(case, dict) or set(case) != {"id", "expect_allowed", "call"}:
            raise ValueError("Each case needs id, expect_allowed and call")
        identity = case["id"]
        if (not isinstance(identity, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,79}", identity)
                or identity in seen):
            raise ValueError("Case IDs must be unique short lowercase slugs")
        if type(case["expect_allowed"]) is not bool:
            raise ValueError("expect_allowed must be a boolean")
        if not isinstance(case["call"], dict):
            raise ValueError("call must be an object")
        seen.add(identity)
        kinds.add(case["expect_allowed"])
    if kinds != {False, True}:
        raise ValueError("Include both forbidden and legitimate cases")
    return cases
