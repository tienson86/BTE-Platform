"""IE-1 Interpretation Foundation contract tests."""

from __future__ import annotations

from engines.interpretation_engine.contracts.interpretation_contracts import (
    CanonicalInterpretationResult,
    InterpretationChapter,
    InterpretationContext,
    InterpretationMetadata,
    InterpretationParagraph,
    InterpretationReference,
    InterpretationSection,
    empty_interpretation_result,
    interpretation_foundation_contract,
)
from engines.interpretation_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    INTERPRETATION_VERSION,
    PUBLISHED_CONTRACTS,
)


def test_foundation_contract_surface() -> None:
    """Published contract lists structure only and forbids text generation."""
    contract = interpretation_foundation_contract()
    assert contract["interpretation_version"] == INTERPRETATION_VERSION
    assert contract["contracts"] == list(PUBLISHED_CONTRACTS)
    assert contract["modules"] == list(CANONICAL_MODULE_ORDER)
    assert contract["text_generation"] is False
    assert contract["reports"] is False
    assert contract["ai"] is False
    assert contract["packages_loaded"] is False


def test_structural_contracts_have_no_text_fields() -> None:
    """Section / chapter / paragraph / reference hold ids only."""
    section = InterpretationSection(section_id="sec-overview", module_id="overview")
    chapter = InterpretationChapter(chapter_id="ch-1", section_id="sec-overview")
    paragraph = InterpretationParagraph(paragraph_id="p-1", chapter_id="ch-1")
    reference = InterpretationReference(
        reference_id="ref-1",
        source="analysis",
        field_path="useful_god.useful_god",
        value_ref="Giáp",
    )
    metadata = InterpretationMetadata(
        interpretation_version="1.0.0",
        schema_version="2.0.0",
        module_ids=CANONICAL_MODULE_ORDER,
    )
    for payload in (
        section.to_dict(),
        chapter.to_dict(),
        paragraph.to_dict(),
        reference.to_dict(),
        metadata.to_dict(),
    ):
        assert "narrative" not in payload
        assert "sentence" not in payload
        assert "report_text" not in payload


def test_canonical_result_is_empty_shell() -> None:
    """IE-1 result shell contains no generated sections."""
    result = empty_interpretation_result()
    assert isinstance(result, CanonicalInterpretationResult)
    payload = result.to_dict()
    assert payload["status"] == "empty"
    assert payload["sections"] == []
    assert payload["chapters"] == []
    assert payload["paragraphs"] == []
    assert payload["success"] is True
    assert "IE1-EMPTY-SHELL" in payload["diagnostics"]


def test_context_contract_serializes_snapshots() -> None:
    """InterpretationContext contract carries sealed snapshots."""
    context = InterpretationContext(
        interpretation_version="1.0.0",
        analysis_snapshot={"pipeline_version": "2.0.0"},
        decision_snapshot={"decision_pipeline_version": "1.0.0"},
        luck_snapshot={"luck_pipeline_version": "1.0.0"},
    )
    payload = context.to_dict()
    assert payload["analysis_snapshot"]["pipeline_version"] == "2.0.0"
    assert payload["status"] == "ready"
