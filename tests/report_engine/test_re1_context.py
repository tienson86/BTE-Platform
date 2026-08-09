"""RE-1 Report Context creation tests."""

from __future__ import annotations

import pytest

from engines.report_engine.context.canonical_report_context import build_report_context
from engines.report_engine.exceptions.foundation_error import (
    ReportDuplicateIdError,
    ReportFoundationError,
)
from tests.report_engine.re1_snapshots import (
    ax2_snapshot,
    ax3_snapshot,
    ax4_snapshot,
    ix1_snapshot,
)


def test_context_creation_seals_upstream_snapshots() -> None:
    """Context copies AX-2 / AX-3 / AX-4 / IX-1 payloads and leaves originals intact."""
    analysis = ax2_snapshot()
    decision = ax3_snapshot()
    luck = ax4_snapshot()
    interpretation = ix1_snapshot()
    original_analysis = dict(analysis)
    context = build_report_context(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
        interpretation_result=interpretation,
    )
    copied = context.analysis_snapshot()
    copied["pipeline_version"] = "mutated"
    assert analysis == original_analysis
    assert context.analysis_snapshot()["pipeline_version"] == "2.0.0"
    assert context.decision_snapshot()["decision_pipeline_version"] == "1.0.0"
    assert context.luck_snapshot()["luck_pipeline_version"] == "1.0.0"
    assert context.interpretation_snapshot()["interpretation_pipeline_version"] == "1.0.0"
    payload = context.to_dict()
    assert payload["report_version"] == "1.0.0"
    assert payload["metadata"]["module_ids"][-1] == "summary"


def test_context_publish_is_append_only() -> None:
    """Foundation outputs publish once and cannot overwrite upstream snapshots."""
    context = build_report_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
        interpretation_result=ix1_snapshot(),
    )
    context.publish("cover_binding", {"module_id": "cover"})
    with pytest.raises(ReportDuplicateIdError, match="duplicate_output"):
        context.publish("cover_binding", {"module_id": "other"})
    assert context.published_outputs() == ("cover_binding",)
    shell = context.empty_result()
    assert shell["status"] == "empty"
    assert shell["sections"] == []


def test_missing_upstream_fails() -> None:
    """All four canonical upstream results are required."""
    with pytest.raises(ReportFoundationError, match="missing_canonical_interpretation_result"):
        build_report_context(
            analysis_result=ax2_snapshot(),
            decision_result=ax3_snapshot(),
            luck_result=ax4_snapshot(),
            interpretation_result=None,
        )
