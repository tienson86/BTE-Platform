"""Integrity tests for PILOT-1H strength model diagnostic package."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
VALIDATION = ROOT / "validation"

REQUIRED_MD = [
    "README.md",
    "STRENGTH_EVIDENCE_DIMENSION_MATRIX.md",
    "SCORE_TRACE_ANALYSIS.md",
    "SCORE_SATURATION_ANALYSIS.md",
    "VERY_WEAK_BOUNDARY_ANALYSIS.md",
    "BALANCED_PROFILE_ANALYSIS.md",
    "TAXONOMY_RESOLUTION_ANALYSIS.md",
    "SCORE_COLLISION_ANALYSIS.md",
    "SUPPORT_PRESSURE_DIAGNOSTIC.md",
    "SEASONAL_WEIGHTING_DIAGNOSTIC.md",
    "ROOTING_DIAGNOSTIC.md",
    "STRENGTH_PROFILE_REQUIREMENTS.md",
    "TAXONOMY_BOUNDARY_ANALYSIS.md",
    "V1_TO_V2_PROJECTION_ANALYSIS.md",
    "CONFIDENCE_MODEL_DIAGNOSTIC.md",
    "SYNTHETIC_EXPECTATION_AUDIT.md",
    "REAL_CALIBRATION_DIAGNOSTIC.md",
    "STRENGTH_MODEL_DIAGNOSTIC_SUMMARY.md",
    "PRE_IMPLEMENTATION_RECOMMENDATIONS.md",
    "PILOT_1H_SUMMARY.md",
]

REQUIRED_JSON = [
    "evidence_matrix.json",
    "score_trace.json",
    "saturation.json",
    "boundary_analysis.json",
    "collision_analysis.json",
    "profile_requirements.json",
    "confidence_analysis.json",
    "synthetic_audit.json",
]

HAN_OR_CJK = re.compile(r"[\u3400-\u9FFF\uF900-\uFAFF\u3040-\u30FF\uAC00-\uD7AF]")


def test_required_markdown_present() -> None:
    for name in REQUIRED_MD:
        assert (ROOT / name).exists(), name


def test_required_json_present() -> None:
    for name in REQUIRED_JSON:
        assert (REPORTS / name).exists(), name
    assert (VALIDATION / "VALIDATION.json").exists()
    assert (VALIDATION / "profile.json").exists()


def test_validation_decision() -> None:
    data = json.loads((VALIDATION / "VALIDATION.json").read_text(encoding="utf-8"))
    assert data["final_decision"] == "DIAGNOSTIC_COMPLETE"
    assert data["taxonomy_boundaries_frozen"] is False
    assert data["no_production_mutations"] is True
    assert data["cal_records_unchanged"] is True
    assert data["syn_records_unchanged"] is True


def test_summary_status_block() -> None:
    text = (ROOT / "PILOT_1H_SUMMARY.md").read_text(encoding="utf-8")
    assert "REAL_DUAL_REVIEWED_CASES: 2" in text
    assert "SYNTHETIC_CASES_ANALYZED: 21" in text
    assert "TAXONOMY_BOUNDARIES_FROZEN: NO" in text
    assert "CALIBRATION_DATA_CHANGED: NO" in text
    assert "Final Decision:\nDIAGNOSTIC_COMPLETE" in text
    assert "NEXT_ACTION: Continue real expert case acquisition" in text


def test_no_han_in_machine_json() -> None:
    for path in list(REPORTS.glob("*.json")) + list(VALIDATION.glob("*.json")):
        text = path.read_text(encoding="utf-8")
        assert HAN_OR_CJK.search(text) is None, path.name


def test_saturation_mechanisms_distinct() -> None:
    data = json.loads((REPORTS / "saturation.json").read_text(encoding="utf-8"))
    assert data["mechanism_a_score_saturation"] is True
    assert data["mechanism_b_taxonomy_projection_collapse"] is True
    assert data["mechanisms_are_distinct"] is True
    assert data["published_distinguishable"] is False


def test_profile_required() -> None:
    data = json.loads((REPORTS / "profile_requirements.json").read_text(encoding="utf-8"))
    assert data["profile_required"] is True
    assert "Score" in data["stack"]
    assert "Profile" in data["stack"]
    collision = json.loads((REPORTS / "collision_analysis.json").read_text(encoding="utf-8"))
    assert collision["score_only_sufficient"] is False


def test_forbidden_final_decisions_absent() -> None:
    text = (ROOT / "PILOT_1H_SUMMARY.md").read_text(encoding="utf-8")
    assert "CALIBRATION_COMPLETE" not in text
    assert "IMPLEMENTATION_READY" not in text
    assert "TAXONOMY_V2_FROZEN" not in text
