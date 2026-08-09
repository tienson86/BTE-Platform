"""IE-1 foundation validation tests."""

from __future__ import annotations

from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.contracts.interpretation_contracts import InterpretationSection
from engines.interpretation_engine.exceptions.foundation_error import InterpretationDuplicateIdError
from engines.interpretation_engine.validation.foundation_validation import (
    CODE_CONTEXT_OK,
    CODE_CONTRACT_OK,
    CODE_DUP_ID,
    CODE_REGISTRY_OK,
    CODE_VERSION_INCOMPATIBLE,
    validate_duplicate_ids,
    validate_foundation,
    validate_structural_ids,
)
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def test_validate_foundation_passes_for_canonical_snapshots() -> None:
    """Contracts, registry, versions, and context integrity succeed together."""
    context = build_interpretation_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    report = validate_foundation(context=context)
    assert report.success is True
    assert CODE_CONTRACT_OK in report.codes
    assert CODE_REGISTRY_OK in report.codes
    assert CODE_CONTEXT_OK in report.codes


def test_incompatible_analysis_version_fails() -> None:
    """AX-1 shaped analysis version is rejected."""
    analysis = ax2_snapshot()
    analysis["pipeline_version"] = "1.0.0"
    context = build_interpretation_context(
        analysis_result=analysis,
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    report = validate_foundation(context=context)
    assert report.success is False
    assert CODE_VERSION_INCOMPATIBLE in report.codes


def test_duplicate_ids_rejected() -> None:
    """Duplicate structural identifiers fail closed."""
    try:
        validate_duplicate_ids(("sec-1", "sec-1"))
        raised = False
    except InterpretationDuplicateIdError:
        raised = True
    assert raised is True
    try:
        validate_structural_ids(
            sections=(
                InterpretationSection(section_id="sec-1", module_id="overview"),
                InterpretationSection(section_id="sec-1", module_id="career"),
            )
        )
        structural_ok = True
    except InterpretationDuplicateIdError:
        structural_ok = False
    assert structural_ok is False
    assert CODE_DUP_ID == "DUP-ID"
