"""Replay tests for PILOT-1G synthetic Strength stress dataset."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
HARNESS_PARENT = ROOT

# Ensure repo root + harness package importable when pytest changes cwd.
REPO_ROOT = ROOT.parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from knowledge.pilot.replay.synthetic_strength.harness.replay import (  # noqa: E402
    list_case_ids,
    load_case,
    replay_all,
    replay_case,
)
from knowledge.pilot.replay.synthetic_strength.harness.compare import (  # noqa: E402
    MISMATCH_CATEGORIES,
    expected_v1_band,
)


def test_list_case_ids_count() -> None:
    assert len(list_case_ids()) == 21


def test_replay_single_case_structure() -> None:
    case = load_case("SYN-STR-000001")
    result = replay_case(case)
    assert result["case_id"] == "SYN-STR-000001"
    assert "runtime" in result
    assert "comparison" in result
    assert result["runtime"]["success"] is True
    assert 0.0 <= float(result["runtime"]["score"]) <= 1.0
    assert result["runtime"]["v1_band"] in {"weak", "balanced", "strong"}
    assert result["comparison"]["mismatch_category"] in MISMATCH_CATEGORIES
    assert result["calibration_eligible"] is False
    assert result["golden_eligible"] is False


def test_replay_all_writes_21_results(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Replay into real results/ to keep artifacts current for report consumers.
    outputs = replay_all(write_results=True)
    assert len(outputs) == 21
    paths = sorted(RESULTS.glob("SYN-STR-*.json"))
    assert len(paths) == 21
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["case_id"] == path.stem
        assert data["comparison"]["mismatch_category"] in MISMATCH_CATEGORIES


def test_expected_v1_projection_table() -> None:
    assert expected_v1_band("very_weak") == "weak"
    assert expected_v1_band("slightly_weak") == "weak"
    assert expected_v1_band("balanced") == "balanced"
    assert expected_v1_band("slightly_strong") == "strong"
    assert expected_v1_band("very_strong") == "strong"


def test_extreme_cases_present_in_results() -> None:
    for case_id in (
        "SYN-STR-000001",
        "SYN-STR-000002",
        "SYN-STR-000003",
        "SYN-STR-000019",
        "SYN-STR-000020",
        "SYN-STR-000021",
    ):
        path = RESULTS / f"{case_id}.json"
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["runtime"]["success"] is True
