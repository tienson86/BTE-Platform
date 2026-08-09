"""IE-1 Interpretation Context creation tests."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.exceptions.foundation_error import (
    InterpretationDuplicateIdError,
    InterpretationFoundationError,
)
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def test_context_creation_seals_upstream_snapshots() -> None:
    """Context copies AX-2 / AX-3 / AX-4 payloads and leaves originals intact."""
    analysis = ax2_snapshot()
    decision = ax3_snapshot()
    luck = ax4_snapshot()
    original_analysis = dict(analysis)
    context = build_interpretation_context(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
    )
    copied = context.analysis_snapshot()
    copied["pipeline_version"] = "mutated"
    assert analysis == original_analysis
    assert context.analysis_snapshot()["pipeline_version"] == "2.0.0"
    assert context.decision_snapshot()["decision_pipeline_version"] == "1.0.0"
    assert context.luck_snapshot()["luck_pipeline_version"] == "1.0.0"
    payload = context.to_dict()
    assert payload["interpretation_version"] == "1.0.0"
    assert payload["metadata"]["module_ids"][-1] == "summary"


def test_context_publish_is_append_only() -> None:
    """Foundation outputs publish once and cannot overwrite upstream snapshots."""
    context = build_interpretation_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    context.publish("overview_binding", {"module_id": "overview"})
    with pytest.raises(InterpretationDuplicateIdError, match="duplicate_output"):
        context.publish("overview_binding", {"module_id": "other"})
    assert context.published_outputs() == ("overview_binding",)
    shell = context.empty_result()
    assert shell["status"] == "empty"
    assert shell["sections"] == []


def test_missing_upstream_fails() -> None:
    """All three canonical upstream results are required."""
    with pytest.raises(InterpretationFoundationError, match="missing_canonical_luck_result"):
        build_interpretation_context(
            analysis_result=ax2_snapshot(),
            decision_result=ax3_snapshot(),
            luck_result=None,
        )
