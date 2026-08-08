"""Capability adapter tests — Career Selection production allow-list."""

from __future__ import annotations

from engines.commercial_knowledge import (
    CAREER_SELECTION_ALLOW_LIST,
    PRODUCTION_ALLOW_LIST,
    WAVE_1_1_ALLOW_LIST,
    CommercialKnowledgeAdapter,
)

from .conftest import strong_employee_chart


def test_production_allow_list_is_wave_plus_career_selection_only() -> None:
    """Production allow-list = Wave 1.1 ∪ SEL — no LED/BU Domain 01 units."""
    assert PRODUCTION_ALLOW_LIST == WAVE_1_1_ALLOW_LIST | CAREER_SELECTION_ALLOW_LIST
    assert "KU-CN-LE-000001" not in PRODUCTION_ALLOW_LIST
    assert "KU-AC-BU-000001" not in PRODUCTION_ALLOW_LIST
    assert len(CAREER_SELECTION_ALLOW_LIST) == 11


def test_adapter_with_production_allow_list_selects_career_units() -> None:
    """Production allow-list selects Career Selection Assessment units."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(
        analysis=strong_employee_chart(),
        allow_list_ids=PRODUCTION_ALLOW_LIST,
        run_id="cap-1",
    )
    selected = {item.knowledge_unit_id for item in bundle.selected_units}
    assert selected.issubset(PRODUCTION_ALLOW_LIST)
    career_selected = selected & CAREER_SELECTION_ALLOW_LIST
    assert career_selected
    assert "KU-CN-CA-000001" in career_selected
    assert "KU-AC-CA-000001" in career_selected
    assert "KU-CN-LE-000001" not in selected
    assert "KU-AC-BU-000001" not in selected


def test_adapter_default_remains_wave_1_1_compatible() -> None:
    """Default adapter path stays Wave 1.1 (no Domain LED/BU leakage)."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(analysis=strong_employee_chart())
    selected = {item.knowledge_unit_id for item in bundle.selected_units}
    assert selected.issubset(WAVE_1_1_ALLOW_LIST)
    assert not (selected & CAREER_SELECTION_ALLOW_LIST)
