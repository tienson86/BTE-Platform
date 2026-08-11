"""Ensure execution package does not import production engines."""

from __future__ import annotations

import re

from .helpers import ROOT

FORBIDDEN_IMPORTS = [
    re.compile(r"^\s*from\s+engines\b", re.M),
    re.compile(r"^\s*import\s+engines\b", re.M),
    re.compile(r"^\s*from\s+applications\b", re.M),
    re.compile(r"^\s*from\s+pipelines\b", re.M),
]


def test_no_production_imports_in_package_python() -> None:
    for path in ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_IMPORTS:
            assert pattern.search(text) is None, (path, pattern.pattern)


def test_lifecycle_states_documented() -> None:
    text = (ROOT / "EXECUTION_WORKFLOW.md").read_text(encoding="utf-8")
    for state in (
        "intake_pending",
        "ready_for_expert_a",
        "ready_for_expert_b",
        "agreement_review",
        "adjudication_required",
        "calibration_complete",
    ):
        assert f"`{state}`" in text
