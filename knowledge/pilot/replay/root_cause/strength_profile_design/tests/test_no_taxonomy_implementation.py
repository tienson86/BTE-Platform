"""Ensure PILOT-1I remains design-only (no taxonomy runtime implementation)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_RUNTIME_PATTERNS = [
    re.compile(r"def\s+classify_taxonomy_v2\b"),
    re.compile(r"TAXONOMY_V2_THRESHOLDS\s*="),
    re.compile(r"\bT1\s*=\s*0\."),
    re.compile(r"\bT6\s*=\s*0\."),
]


def test_no_python_runtime_classifier_modules() -> None:
    py_files = list(ROOT.rglob("*.py"))
    # allow builder and tests only
    for path in py_files:
        if path.name in {"build_design_package.py"} or "tests" in path.parts:
            continue
        raise AssertionError(f"unexpected python module in design package: {path}")


def test_no_threshold_constants_in_schemas() -> None:
    for path in (ROOT / "schemas").glob("*.json"):
        text = path.read_text(encoding="utf-8")
        assert '"t1"' not in text.lower()
        assert '"t6"' not in text.lower()
        assert "threshold" not in text.lower() or "thresholds" not in path.name


def test_guardrails_forbid_taxonomy_v2() -> None:
    data = json.loads((ROOT / "reports" / "implementation_guardrails.json").read_text(encoding="utf-8"))
    assert "implement_taxonomy_v2" in data["do_not"]
    assert "replace_v1_score" in data["do_not"]
    assert "preserve_unknown" in data["must"]


def test_docs_may_mention_taxonomy_but_summary_says_not_implemented() -> None:
    text = (ROOT / "PILOT_1I_SUMMARY.md").read_text(encoding="utf-8")
    assert "TAXONOMY_V2_IMPLEMENTED: NO" in text
    assert "TAXONOMY_THRESHOLDS_IMPLEMENTED: NO" in text


def test_builder_has_no_forbidden_runtime_patterns() -> None:
    builder = (ROOT / "build_design_package.py").read_text(encoding="utf-8")
    for pattern in FORBIDDEN_RUNTIME_PATTERNS:
        assert pattern.search(builder) is None, pattern.pattern
