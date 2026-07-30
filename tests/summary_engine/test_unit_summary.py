"""Unit tests for Summary Engine."""

from __future__ import annotations

import pytest

from engines.analysis_engine.runtime.models import AnalysisContext, StageResult
from engines.analysis_engine.summary_engine import (
    SummaryConsistencyError,
    SummaryEngine,
    SummaryPrerequisiteError,
    SummaryResult,
    SummaryValidationError,
)
from engines.analysis_engine.summary_engine.models import UPSTREAM_STAGES
from tests.summary_engine.conftest import make_upstream_result, publish_all_upstream


class TestSummaryValidation:
    def test_missing_upstream_fails(self, engine: SummaryEngine) -> None:
        ctx = AnalysisContext(request_id="x", chart={"day_master": "Giáp"})
        with pytest.raises(SummaryPrerequisiteError) as exc_info:
            engine.evaluate(ctx)
        missing = exc_info.value.details.get("missing")
        assert set(missing) == set(UPSTREAM_STAGES)

    def test_partial_upstream_fails(self, engine: SummaryEngine) -> None:
        ctx = AnalysisContext(request_id="x", chart={"day_master": "Giáp"})
        ctx.publish_stage_result(make_upstream_result("strength"))
        with pytest.raises(SummaryPrerequisiteError):
            engine.evaluate(ctx)

    def test_request_id_required(self, engine: SummaryEngine) -> None:
        ctx = AnalysisContext(request_id="", chart={"day_master": "Giáp"})
        with pytest.raises(SummaryValidationError):
            engine.evaluate(ctx)


class TestSummaryAggregation:
    def test_aggregates_all_domains(
        self,
        engine: SummaryEngine,
        context: AnalysisContext,
    ) -> None:
        result = engine.evaluate_summary(context)
        assert result.strength_summary.stage_id == "strength"
        assert result.luck_summary.stage_id == "luck"
        assert result.strength_summary.payload_digest["classification"] == "strong"
        assert result.pattern_summary.payload_digest["pattern_id"] == "zheng_guan_ge"
        assert result.consistency.status in {"pass", "warn"}
        assert result.consolidated_confidence.score is not None
        assert len(result.evidence_index) == len(UPSTREAM_STAGES)
        assert result.summary["upstream_stage_count"] == 8

    def test_does_not_mutate_upstream(
        self,
        engine: SummaryEngine,
        context: AnalysisContext,
    ) -> None:
        before = {
            stage_id: dict(context.get_stage_result(stage_id).payload)  # type: ignore[union-attr]
            for stage_id in UPSTREAM_STAGES
        }
        engine.evaluate_summary(context)
        after = {
            stage_id: dict(context.get_stage_result(stage_id).payload)  # type: ignore[union-attr]
            for stage_id in UPSTREAM_STAGES
        }
        assert before == after

    def test_stage_result_roundtrip(
        self,
        engine: SummaryEngine,
        context: AnalysisContext,
    ) -> None:
        stage = engine.evaluate(context)
        assert stage.stage_id == "summary"
        rebuilt = SummaryResult.from_stage_result(stage)
        assert rebuilt.to_dict() == stage.payload

    def test_blocking_request_id_mismatch(
        self,
        engine: SummaryEngine,
    ) -> None:
        ctx = AnalysisContext(request_id="sum-req-002", chart={"day_master": "Giáp"})
        publish_all_upstream(ctx)
        # Replace luck with mismatched request_id in payload.
        ctx._stage_results["luck"] = StageResult(  # noqa: SLF001 - test-only replace
            stage_id="luck",
            status="success",
            payload={"request_id": "other", "summary": {"active_count": 1}},
            evidence=make_upstream_result("luck").evidence,
        )
        with pytest.raises(SummaryConsistencyError):
            engine.evaluate_summary(ctx)


class TestSummaryDeterminism:
    def test_identical_inputs_identical_outputs(
        self,
        engine: SummaryEngine,
        context: AnalysisContext,
    ) -> None:
        assert (
            engine.evaluate_summary(context).to_dict()
            == engine.evaluate_summary(context).to_dict()
        )
