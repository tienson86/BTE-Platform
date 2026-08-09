"""RE-1 Report Foundation contract tests."""

from __future__ import annotations

from engines.report_engine.contracts.report_contracts import (
    CanonicalReportResult,
    ReportAsset,
    ReportBlock,
    ReportContext,
    ReportDocument,
    ReportMetadata,
    ReportSection,
    empty_report_result,
    report_foundation_contract,
)
from engines.report_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    PUBLISHED_CONTRACTS,
    REPORT_VERSION,
)


def test_foundation_contract_surface() -> None:
    """Published contract lists structure only and forbids rendering."""
    contract = report_foundation_contract()
    assert contract["report_version"] == REPORT_VERSION
    assert contract["contracts"] == list(PUBLISHED_CONTRACTS)
    assert contract["modules"] == list(CANONICAL_MODULE_ORDER)
    assert contract["rendering"] is False
    assert contract["export"] is False
    assert contract["formatting"] is False
    assert contract["pdf"] is False
    assert contract["docx"] is False
    assert contract["html"] is False
    assert contract["markdown"] is False
    assert contract["packages_loaded"] is False


def test_structural_contracts_have_no_render_fields() -> None:
    """Document / section / block / asset hold ids only."""
    document = ReportDocument(document_id="doc-1")
    section = ReportSection(section_id="sec-cover", module_id="cover")
    block = ReportBlock(block_id="blk-1", section_id="sec-cover")
    asset = ReportAsset(asset_id="ast-1", asset_type="chart_ref", source_ref="ax2.seasonal")
    metadata = ReportMetadata(
        report_version="1.0.0",
        schema_version="2.0.0",
        module_ids=CANONICAL_MODULE_ORDER,
    )
    for payload in (
        document.to_dict(),
        section.to_dict(),
        block.to_dict(),
        asset.to_dict(),
        metadata.to_dict(),
    ):
        assert "html" not in payload
        assert "markdown" not in payload
        assert "pdf" not in payload
        assert "report_text" not in payload


def test_canonical_result_is_empty_shell() -> None:
    """RE-1 result shell contains no rendered sections."""
    result = empty_report_result()
    assert isinstance(result, CanonicalReportResult)
    payload = result.to_dict()
    assert payload["status"] == "empty"
    assert payload["sections"] == []
    assert payload["blocks"] == []
    assert payload["assets"] == []
    assert payload["success"] is True
    assert "RE1-EMPTY-SHELL" in payload["diagnostics"]


def test_context_contract_serializes_snapshots() -> None:
    """ReportContext contract carries sealed snapshots."""
    context = ReportContext(
        report_version="1.0.0",
        analysis_snapshot={"pipeline_version": "2.0.0"},
        decision_snapshot={"decision_pipeline_version": "1.0.0"},
        luck_snapshot={"luck_pipeline_version": "1.0.0"},
        interpretation_snapshot={"interpretation_pipeline_version": "1.0.0"},
    )
    payload = context.to_dict()
    assert payload["analysis_snapshot"]["pipeline_version"] == "2.0.0"
    assert payload["interpretation_snapshot"]["interpretation_pipeline_version"] == "1.0.0"
    assert payload["status"] == "ready"
