"""Profile compatibility tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_profile_compatibility_taxonomy_unavailable() -> None:
    data = json.loads((ROOT / "reports" / "profile_compatibility.json").read_text(encoding="utf-8"))
    assert data["mapping"]["taxonomy"] == "unavailable_by_design"
    assert "score_reference" in data["mapping"]
    assert "rooting_state" in data["mapping"]


def test_v1_gaps_trace_to_pilot_1j() -> None:
    data = json.loads((ROOT / "reports" / "v1_gap_analysis.json").read_text(encoding="utf-8"))
    fields = {g["field"] for g in data["gaps"]}
    assert "root_loci" in fields
    assert "sitting_hidden_pressure" in fields
    assert "clash_punishment_harm_destruction" in fields
    assert "follow_pattern" in fields
