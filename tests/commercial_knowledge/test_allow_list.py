"""Allow-list tests for Wave 1.1 commercial retrieval."""

from __future__ import annotations

from engines.commercial_knowledge import WAVE_1_1_ALLOW_LIST, CommercialKnowledgeAdapter
from engines.commercial_knowledge.retrieval_service import RetrievalService

from .conftest import strong_chart_with_useful_god


def test_wave_1_1_allow_list_contents() -> None:
    """Allow-list contains exactly the five Golden Baseline ids."""
    assert WAVE_1_1_ALLOW_LIST == frozenset(
        {
            "KU-ID-001",
            "KU-ST-001",
            "KU-WK-001",
            "KU-UG-001",
            "KU-RC-001",
        }
    )


def test_retrieval_ignores_non_allow_listed_ids() -> None:
    """Units outside Wave 1.1 allow-list are never selected."""
    service = RetrievalService()
    selected, dropped, _signals = service.retrieve(
        analysis=strong_chart_with_useful_god(),
        scenario_id="default",
    )
    selected_ids = {row["knowledge_unit_id"] for row in selected}
    assert selected_ids.issubset(WAVE_1_1_ALLOW_LIST)
    assert all(
        unit_id in WAVE_1_1_ALLOW_LIST or reason == "not_in_wave_1_1_allow_list"
        for unit_id, reason in dropped
        if reason == "not_in_wave_1_1_allow_list" or unit_id in WAVE_1_1_ALLOW_LIST
    )


def test_adapter_selected_units_respect_allow_list() -> None:
    """Adapter bundle selected_units stay within allow-list."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(analysis=strong_chart_with_useful_god())
    for item in bundle.selected_units:
        assert item.knowledge_unit_id in WAVE_1_1_ALLOW_LIST
