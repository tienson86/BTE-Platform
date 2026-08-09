"""IE-3 composition registry and validation tests."""

from __future__ import annotations

from engines.interpretation_engine.composition.composition_registry import (
    CANONICAL_STAGE_ORDER,
    CompositionRegistry,
)
from engines.interpretation_engine.composition.composition_result import (
    DIAG_CHAPTER_DUPLICATE,
    DIAG_FLOW_VIOLATION,
    DIAG_REFERENCE_BROKEN,
    DIAG_SECTION_DUPLICATE,
)
from engines.interpretation_engine.composition.chapter_builder import AssembledChapter
from engines.interpretation_engine.composition.cross_reference_builder import CrossReference
from engines.interpretation_engine.composition.flow_optimizer import FlowPlan
from engines.interpretation_engine.composition.section_builder import AssembledSection
from engines.interpretation_engine.composition.validation import (
    validate_chapter_order,
    validate_cross_references,
    validate_registry,
    validate_section_integrity,
)
import pytest


def test_registry_is_complete_and_deterministic() -> None:
    """Five assembly stages are registered, enabled, and ordered."""
    registry = CompositionRegistry.default()
    assert registry.registered_ids() == CANONICAL_STAGE_ORDER
    assert registry.resolve_order() == CANONICAL_STAGE_ORDER
    validate_registry(registry)
    for stage_id in CANONICAL_STAGE_ORDER:
        record = registry.get(stage_id)
        assert record.enabled is True
        assert record.deterministic is True


def test_validation_detects_duplicates_and_broken_references() -> None:
    """Section/chapter duplicates and missing xref targets fail closed."""
    section = AssembledSection(
        section_id="SEC-overview",
        module_id="overview",
        candidate_ids=("SC-1",),
        knowledge_ids=("KN-1",),
        evidence_ids=("EV-1",),
        reasoning_ids=("RC-1",),
        template_ids=("TPL-1",),
        status="assembled",
    )
    with pytest.raises(ValueError, match=DIAG_SECTION_DUPLICATE):
        validate_section_integrity((section, section))
    chapter = AssembledChapter(
        chapter_id="CH-overview",
        module_id="overview",
        section_ids=("SEC-overview",),
        sequence=0,
        status="assembled",
    )
    with pytest.raises(ValueError, match=DIAG_CHAPTER_DUPLICATE):
        validate_chapter_order((chapter, chapter))
    broken = CrossReference(
        reference_id="XREF-bad",
        source_type="section",
        source_id="SEC-overview",
        target_type="knowledge",
        target_id="KN-MISSING",
    )
    with pytest.raises(ValueError, match=DIAG_REFERENCE_BROKEN):
        validate_cross_references((broken,), (section,), (chapter,))
    assert FlowPlan(
        section_order=("SEC-overview",),
        chapter_order=("CH-overview",),
        groups=(("SEC-overview",),),
        dependencies=(),
        operations=("order_by_module",),
    )
    assert DIAG_FLOW_VIOLATION == "FLOW-VIOLATION"
