"""Minimum contract tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_minimum_smaller_and_excludes_taxonomy() -> None:
    data = json.loads((ROOT / "reports" / "minimum_contract.json").read_text(encoding="utf-8"))
    assert data["genuinely_smaller_than_full"] is True
    assert "taxonomy_v2" in data["excluded"]
    assert "t1_t6" in data["excluded"]
    assert "root_summary_and_loci" in data["minimum_required_layers"]
    assert "pressure_items_including_hidden" in data["minimum_required_layers"]


def test_minimum_example_is_design_only() -> None:
    data = json.loads((ROOT / "examples" / "minimum_output.json").read_text(encoding="utf-8"))
    assert data["design_marker"] == "design_only"
    assert data["contract_class"] == "minimum"
    assert "taxonomy_v2" not in data
    pressure_items = data["evidence"]["pressure"]["items"]
    assert any(i.get("visibility") == "hidden" for i in pressure_items)
