"""IE-2 placeholder binding tests."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.knowledge.composition_context import (
    PlaceholderIntegrityError,
    build_composition_context,
)
from engines.interpretation_engine.knowledge.knowledge_selector import (
    KnowledgeSelector,
    ReleasedKnowledgeSpec,
)
from engines.interpretation_engine.knowledge.placeholder_binder import PlaceholderBinder
from engines.interpretation_engine.knowledge.template_selector import TemplateSelector
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def test_placeholders_bind_published_contract_values() -> None:
    """Bindings copy AX-2 / AX-3 / AX-4 field values only."""
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
    bindings = PlaceholderBinder().bind(context, knowledge, templates)
    values = {item.binding_path: item.value for item in bindings}
    assert values["analysis.useful_god.useful_god"] == "Giáp"
    assert values["decision.final_useful_god"] == "Giáp"
    assert values["luck.overall_luck_result.luck_priority.value"] == "balanced"
    assert all(item.status == "bound" for item in bindings)


def test_unpublished_path_fails_closed() -> None:
    """Computed fields outside published roots are rejected."""
    spec = ReleasedKnowledgeSpec(
        knowledge_id="KN-BAD",
        source="analysis",
        field_path="useful_god.useful_god",
        evidence_id="EV-BAD",
        reasoning_id="RC-BAD",
        reasoning_chain_id="RC-BAD",
        reasoning_graph_id="RG-BAD",
        reasoning_trace_id="RT-BAD",
        template_id="TPL-BAD",
        placeholders=("computed.score_delta",),
        default_confidence="low",
    )
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
    knowledge = KnowledgeSelector((spec,)).select(context)
    with pytest.raises(PlaceholderIntegrityError, match="unpublished_root:computed"):
        PlaceholderBinder().bind(context, knowledge)
