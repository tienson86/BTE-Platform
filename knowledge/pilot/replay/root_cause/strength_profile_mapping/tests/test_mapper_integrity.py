"""Mapper integrity tests for PILOT-1J."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
EXAMPLES = ROOT / "examples"

REQUIRED_MD = [
    "README.md",
    "REFERENCE_MAPPER_SPEC.md",
    "MAPPING_RULES.md",
    "SOURCE_FIELD_CATALOG.md",
    "FIELD_AVAILABILITY_MATRIX.md",
    "INFORMATION_PRESERVATION_REPORT.md",
    "INFORMATION_LOSS_REPORT.md",
    "REFERENCE_IMPLEMENTATION_LIMITS.md",
    "PROFILE_MAPPING_REPORT.md",
    "PILOT_1J_SUMMARY.md",
]


def test_required_docs_exist() -> None:
    for name in REQUIRED_MD:
        assert (ROOT / name).exists(), name


def test_23_results_exist() -> None:
    paths = list(RESULTS.glob("*.json"))
    assert len(paths) == 23
    assert (RESULTS / "REAL_CAL-000001.json").exists()
    assert (RESULTS / "REAL_CAL-000006.json").exists()
    assert (RESULTS / "SYN-STR-000001.json").exists()
    assert (RESULTS / "SYN-STR-000021.json").exists()


def test_reference_flags() -> None:
    for path in RESULTS.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["reference_only"] is True
        assert data["production_ready"] is False
        assert data["taxonomy_implemented"] is False
        assert data["calibration_implementation"] is False


def test_summary_status() -> None:
    text = (ROOT / "PILOT_1J_SUMMARY.md").read_text(encoding="utf-8")
    assert "REFERENCE_MAPPER_CREATED: YES" in text
    assert "TOTAL_CASES_MAPPED: 23" in text
    assert "TAXONOMY_V2_IMPLEMENTED: NO" in text
    assert "Final Decision:\nREFERENCE_MAPPING_COMPLETE" in text


def test_examples_present() -> None:
    for name in (
        "real_cal_000001_profile.json",
        "real_cal_000006_profile.json",
        "synthetic_000001_profile.json",
        "synthetic_000010_profile.json",
        "synthetic_000019_profile.json",
    ):
        assert (EXAMPLES / name).exists(), name
