"""IE-2 selector registry and validation tests."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.knowledge.composition_context import build_composition_context
from engines.interpretation_engine.knowledge.composition_result import SentenceCandidate
from engines.interpretation_engine.knowledge.selector_registry import (
    CANONICAL_SELECTOR_ORDER,
    SelectorRegistry,
)
from engines.interpretation_engine.knowledge.sentence_candidate_builder import (
    SentenceCandidateBuilder,
)
from engines.interpretation_engine.knowledge.validation import (
    CODE_DUP_CANDIDATE,
    CODE_REGISTRY_OK,
    CODE_VALIDATION_OK,
    validate_composition,
    validate_duplicate_candidates,
    validate_registry,
)
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def test_registry_is_complete_and_deterministic() -> None:
    """All six selectors are registered, enabled, and ordered by dependency."""
    registry = SelectorRegistry.default()
    assert registry.registered_ids() == CANONICAL_SELECTOR_ORDER
    assert registry.resolve_order() == CANONICAL_SELECTOR_ORDER
    validate_registry(registry)
    for selector_id in CANONICAL_SELECTOR_ORDER:
        record = registry.get(selector_id)
        assert record.enabled is True
        assert record.deterministic is True


def test_validation_passes_for_full_pipeline() -> None:
    """End-to-end selection validates contracts, refs, and versions."""
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
    result = SentenceCandidateBuilder().run(context)
    assert result.success is True
    assert CODE_REGISTRY_OK in result.diagnostics
    assert CODE_VALIDATION_OK in result.diagnostics


def test_duplicate_candidates_fail_validation() -> None:
    """Duplicate sentence_id values are rejected."""
    candidate = SentenceCandidate(
        sentence_id="SC-DUP",
        template_id="TPL-X",
        placeholder_values={},
        evidence_ids=("EV-X",),
        reasoning_ids=("RC-X",),
        confidence="high",
        references=("analysis.useful_god.useful_god",),
    )
    with pytest.raises(ValueError, match="duplicate_sentence_id"):
        validate_duplicate_candidates((candidate, candidate))
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
    report = validate_composition(
        context=context,
        registry=SelectorRegistry.default(),
        knowledge=(),
        evidence=(),
        reasoning=(),
        templates=(),
        placeholders=(),
        candidates=(candidate, candidate),
    )
    assert report.success is False
    assert CODE_DUP_CANDIDATE in report.codes
