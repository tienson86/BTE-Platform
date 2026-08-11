"""Population separation tests — no CAL/SYN mutations."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAL_DIR = ROOT.parents[0] / "strength_taxonomy_v2" / "calibration" / "cases"
SYN_DIR = ROOT.parents[1] / "synthetic_strength" / "datasets"


def test_no_new_cal_ids() -> None:
    assert sorted(p.stem for p in CAL_DIR.glob("CAL-*.json")) == [f"CAL-{n:06d}" for n in range(1, 8)]


def test_syn_count_unchanged() -> None:
    assert len(list(SYN_DIR.glob("SYN-STR-*.json"))) == 21


def test_examples_are_design_only() -> None:
    import json

    for path in (ROOT / "examples").glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data.get("design_marker") == "design_only"
