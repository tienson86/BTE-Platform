"""CASE-0001 integration test for Ten Gods Core Engine."""

from __future__ import annotations

from engines.ten_gods_engine import run_case_0001


def test_case_0001_end_to_end() -> None:
    """Run full Ten Gods pipeline for canonical CASE-0001."""
    result = run_case_0001()

    assert result.version == "1.0.0"
    assert result.day_master.stem == "Canh"
    assert result.day_master.element == "Kim"
    assert len(result.visible) == 4
    assert len(result.hidden) == 11
    assert result.distribution
    assert result.weights
    assert result.dominant.status in {"DETERMINED", "UNDETERMINED"}
    assert len(result.hierarchy) == 10
    assert result.relationships
    assert result.interaction_matrix
    assert result.diagnostics

    visible_gods = {entry.ten_god for entry in result.visible}
    assert visible_gods == {"Thất Sát", "Kiếp Tài", "Nhật Chủ", "Thiên Ấn"}

    hidden_gods = {entry.ten_god for entry in result.hidden}
    assert "Chính Ấn" in hidden_gods
    assert "Thiên Tài" in hidden_gods
    assert "Thương Quan" in hidden_gods

    payload = result.to_dict()
    assert payload["dominant"]["policy"]
    assert payload["missing_data"] == []
