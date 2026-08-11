"""Taxonomy firewall tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

FORBIDDEN = (
    "taxonomy_v2",
    "taxonomy_v2_label",
    "future_taxonomy_label",
    "t1",
    "t2",
    "t3",
    "t4",
    "t5",
    "t6",
    "seven_band",
)


def test_no_taxonomy_fields_in_profiles() -> None:
    for path in RESULTS.glob("*.json"):
        text = path.read_text(encoding="utf-8").lower()
        for token in FORBIDDEN:
            # allow mentions only if somehow in notes? require exact json keys absent in profile
            pass
        data = json.loads(path.read_text(encoding="utf-8"))
        profile = data["profile"]
        for token in FORBIDDEN:
            assert token not in profile
        # external labels may hold synthetic/expert strings but not taxonomy_v2 keys
        ext = profile.get("external_labels") or {}
        assert "taxonomy_v2" not in ext
        assert "t1" not in ext


def test_current_v1_band_allowed() -> None:
    data = json.loads((RESULTS / "SYN-STR-000001.json").read_text(encoding="utf-8"))
    assert data["profile"]["score_reference"]["current_v1_band"] in {"weak", "balanced", "strong", "unknown"}


def test_synthetic_expected_outside_taxonomy_fields() -> None:
    data = json.loads((RESULTS / "SYN-STR-000001.json").read_text(encoding="utf-8"))
    assert data["profile"]["external_labels"]["synthetic_expected_taxonomy"] == "very_weak"
    assert "taxonomy_level" not in data["profile"]
