"""Taxonomy firewall tests."""

from __future__ import annotations

import re

from .helpers import ROOT, VALIDATION, load_json

FORBIDDEN_RUNTIME = [
    re.compile(r"def\s+classify_taxonomy_v2\b"),
    re.compile(r"TAXONOMY_V2_THRESHOLDS\s*="),
    re.compile(r"\btaxonomy_classifier\b"),
]


def test_summary_firewall_flags() -> None:
    text = (ROOT / "PILOT_1M_SUMMARY.md").read_text(encoding="utf-8")
    assert "TAXONOMY_V2_IMPLEMENTED: NO" in text
    assert "T1_T6_FROZEN: NO" in text


def test_validation_firewall() -> None:
    data = load_json(VALIDATION / "VALIDATION.json")
    assert data["taxonomy_v2_implemented"] is False
    assert data["t1_t6_frozen"] is False


def test_no_runtime_taxonomy_classifier_in_package_python() -> None:
    for path in ROOT.rglob("*.py"):
        if "tests" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_RUNTIME:
            assert pattern.search(text) is None, (path, pattern.pattern)


def test_expert_labels_marked_annotation_only() -> None:
    text = (ROOT / "EXPERT_A_EXECUTION.md").read_text(encoding="utf-8")
    assert "research annotations" in text.lower()
