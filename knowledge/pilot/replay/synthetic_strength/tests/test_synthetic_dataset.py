"""Validation tests for PILOT-1G synthetic Strength stress dataset."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATASETS = ROOT / "datasets"
INDEX_PATH = ROOT / "SYNTHETIC_DATASET_INDEX.json"

LEVELS = [
    "very_weak",
    "weak",
    "slightly_weak",
    "balanced",
    "slightly_strong",
    "strong",
    "very_strong",
]

HAN_OR_CJK = re.compile(r"[\u3400-\u9FFF\uF900-\uFAFF\u3040-\u30FF\uAC00-\uD7AF]")
NON_ASCII = re.compile(r"[^\x00-\x7F]")


def _load_cases() -> list[dict]:
    paths = sorted(DATASETS.glob("SYN-STR-*.json"))
    return [json.loads(p.read_text(encoding="utf-8")) for p in paths]


def test_exactly_21_cases() -> None:
    cases = _load_cases()
    assert len(cases) == 21


def test_ids_unique_and_syn_str_prefix() -> None:
    cases = _load_cases()
    ids = [c["case_id"] for c in cases]
    assert len(ids) == len(set(ids))
    assert all(i.startswith("SYN-STR-") for i in ids)
    assert ids == [f"SYN-STR-{n:06d}" for n in range(1, 22)]


def test_no_cal_identifiers() -> None:
    cases = _load_cases()
    blob = json.dumps(cases, ensure_ascii=True)
    assert "CAL-" not in blob
    assert "CALIBRATION_CASE" not in blob


def test_seven_levels_three_each() -> None:
    cases = _load_cases()
    counts = Counter(c["synthetic_expected_taxonomy"] for c in cases)
    assert set(counts) == set(LEVELS)
    assert all(counts[level] == 3 for level in LEVELS)


def test_eligibility_flags_false() -> None:
    for case in _load_cases():
        assert case["calibration_eligible"] is False
        assert case["golden_eligible"] is False
        assert case["expert_calibration_eligible"] is False
        assert case["production_expected"] is False
        assert case["synthetic_pillars"] is True
        assert case["calendar_verified"] is False
        assert case["birth_datetime"] is None
        assert case["birth_location"] is None
        assert case["timezone"] is None
        assert case["dataset_type"] == "SYNTHETIC_STRENGTH_STRESS"


def test_ascii_machine_fields_no_han() -> None:
    for case in _load_cases():
        text = json.dumps(case, ensure_ascii=True)
        assert HAN_OR_CJK.search(text) is None
        for key in ("case_id", "day_master", "synthetic_expected_taxonomy"):
            assert NON_ASCII.search(str(case[key])) is None
        for pillar in case["pillars"].values():
            assert NON_ASCII.search(pillar) is None
            assert "_" in pillar


def test_index_matches_datasets() -> None:
    cases = _load_cases()
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    assert index["case_count"] == 21
    assert index["calibration_eligible"] is False
    assert index["golden_eligible"] is False
    assert [c["case_id"] for c in index["cases"]] == [c["case_id"] for c in cases]


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c["case_id"])
def test_day_master_matches_day_pillar(case: dict) -> None:
    day_stem = case["pillars"]["day"].split("_", 1)[0]
    assert case["day_master"] == day_stem
