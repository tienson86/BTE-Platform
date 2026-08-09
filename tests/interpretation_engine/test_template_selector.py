"""IE-2 template selector tests."""

from __future__ import annotations

from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.knowledge.composition_context import build_composition_context
from engines.interpretation_engine.knowledge.knowledge_selector import KnowledgeSelector
from engines.interpretation_engine.knowledge.template_selector import TemplateSelector
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def test_template_selection_is_identifier_only() -> None:
    """Templates are ids. No body, formatting, or prose keys."""
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
    templates = TemplateSelector().select(knowledge)
    payload = [item.to_dict() for item in templates]
    assert [item["template_id"] for item in payload] == sorted(item["template_id"] for item in payload)
    for item in payload:
        assert set(item) == {"template_id", "knowledge_id", "module_id"}
        assert "template_body" not in item
        assert "html" not in item
