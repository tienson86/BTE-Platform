"""IE-2 reasoning selector tests."""

from __future__ import annotations

from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.knowledge.composition_context import build_composition_context
from engines.interpretation_engine.knowledge.knowledge_selector import KnowledgeSelector
from engines.interpretation_engine.knowledge.reasoning_selector import ReasoningSelector
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def test_reasoning_ids_are_copied_unmodified() -> None:
    """Chains, graphs, and traces are selected by identity only."""
    interpretation = build_interpretation_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    context = build_composition_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
        interpretation_context=interpretation,
    )
    knowledge = KnowledgeSelector().select(context)
    reasoning = ReasoningSelector().select(knowledge)
    useful = next(item for item in reasoning if item.knowledge_id == "KN-IE2-AN-USEFUL_GOD")
    assert useful.reasoning_id == "RC-IE2-AN-USEFUL_GOD"
    assert useful.chain_id == "RC-IE2-AN-USEFUL_GOD"
    assert useful.graph_id == "RG-IE2-AN-USEFUL_GOD"
    assert useful.trace_id == "RT-IE2-AN-USEFUL_GOD"
    assert useful.trace_nodes == ("RT-IE2-AN-USEFUL_GOD",)
    assert [item.reasoning_id for item in reasoning] == sorted(item.reasoning_id for item in reasoning)
