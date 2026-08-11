"""Expert-B blinding validation tests."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from .helpers import ROOT, TEMPLATES, VALIDATION, load_json


def _load_blinding():
    path = ROOT / "blinding_check.py"
    spec = importlib.util.spec_from_file_location("blinding_check", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_blinding_rules_list_forbidden_tokens() -> None:
    text = (ROOT / "BLINDING_RULES.md").read_text(encoding="utf-8")
    for token in (
        "expert_a",
        "expert_a_label",
        "expert_a_rationale",
        "expert_a_evidence",
        "adjudication",
        "runtime_score",
        "runtime_band",
        "future_taxonomy",
        "T1",
        "T6",
    ):
        assert token in text


def test_clean_expert_b_template_passes_blinding() -> None:
    mod = _load_blinding()
    packet = load_json(TEMPLATES / "expert_b_review.json")
    # Template must not embed Expert-A / runtime leak keys.
    leaks = mod.validate_expert_b_packet(packet)
    assert leaks == []


def test_leaky_packet_fails_blinding() -> None:
    mod = _load_blinding()
    packet = {
        "reviewer_id": "expert_b",
        "strength_level": "balanced",
        "expert_a_label": "weak",
        "runtime_score": 0.5,
    }
    leaks = mod.validate_expert_b_packet(packet)
    assert "expert_a_label" in leaks
    assert "runtime_score" in leaks


def test_taxonomy_threshold_keys_fail_blinding() -> None:
    mod = _load_blinding()
    packet = {"T3": 0.5, "future_taxonomy": True}
    leaks = mod.validate_expert_b_packet(packet)
    assert "t3" in leaks
    assert "future_taxonomy" in leaks


def test_validation_marks_blinding_validated() -> None:
    data = load_json(VALIDATION / "VALIDATION.json")
    assert data["blinding_validated"] is True
    assert "forbidden_blinding_tokens" in data
