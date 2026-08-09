"""RE-1 foundation validation tests."""

from __future__ import annotations

from engines.report_engine.context.canonical_report_context import build_report_context
from engines.report_engine.contracts.report_contracts import ReportSection
from engines.report_engine.exceptions.foundation_error import ReportDuplicateIdError
from engines.report_engine.validation.foundation_validation import (
    CODE_CONTEXT_OK,
    CODE_CONTRACT_OK,
    CODE_DUP_ID,
    CODE_REGISTRY_OK,
    CODE_VERSION_INCOMPATIBLE,
    validate_duplicate_ids,
    validate_foundation,
    validate_structural_ids,
)
from tests.report_engine.re1_snapshots import (
    ax2_snapshot,
    ax3_snapshot,
    ax4_snapshot,
    ix1_snapshot,
)


def test_validate_foundation_passes_for_canonical_snapshots() -> None:
    """Contracts, registry, versions, and context integrity succeed together."""
    context = build_report_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
        interpretation_result=ix1_snapshot(),
    )
    report = validate_foundation(context=context)
    assert report.success is True
    assert CODE_CONTRACT_OK in report.codes
    assert CODE_REGISTRY_OK in report.codes
    assert CODE_CONTEXT_OK in report.codes


def test_incompatible_interpretation_version_fails() -> None:
    """Non-IX-1 interpretation pipeline version is rejected."""
    interpretation = ix1_snapshot()
    interpretation["interpretation_pipeline_version"] = "9.0.0"
    context = build_report_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
        interpretation_result=interpretation,
    )
    report = validate_foundation(context=context)
    assert report.success is False
    assert CODE_VERSION_INCOMPATIBLE in report.codes


def test_duplicate_ids_rejected() -> None:
    """Duplicate structural identifiers fail closed."""
    try:
        validate_duplicate_ids(("sec-1", "sec-1"))
        raised = False
    except ReportDuplicateIdError:
        raised = True
    assert raised is True
    try:
        validate_structural_ids(
            sections=(
                ReportSection(section_id="sec-1", module_id="cover"),
                ReportSection(section_id="sec-1", module_id="overview"),
            )
        )
        structural_ok = True
    except ReportDuplicateIdError:
        structural_ok = False
    assert structural_ok is False
    assert CODE_DUP_ID == "DUP-ID"
