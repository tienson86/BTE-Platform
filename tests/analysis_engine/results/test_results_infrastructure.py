"""Results infrastructure integration tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.exceptions.result_error import ResultError
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.analysis_score import AnalysisScore
from engines.analysis_engine.results.result_aggregator import ResultAggregator
from engines.analysis_engine.results.result_builder import ResultBuilder
from engines.analysis_engine.results.result_merger import ResultMerger
from engines.analysis_engine.results.result_repository import ResultRepository
from engines.analysis_engine.results.result_serializer import ResultSerializer
from engines.analysis_engine.results.summary_builder import SummaryBuilder


def _timestamps() -> ModelTimestamps:
    return ModelTimestamps(created_at="2026-08-01T00:00:00Z")


def _metadata() -> AnalysisMetadata:
    return AnalysisMetadata(id="meta_test", version="1.0.0", timestamps=_timestamps())


class TestResultsInfrastructureIntegration:
    """Integration coverage for result runtime infrastructure."""

    def test_builder_aggregator_summary_repository_serializer(self) -> None:
        """Result stack should compose without interpretation."""
        score = AnalysisScore(
            id="score_1",
            version="1.0.0",
            metadata=_metadata(),
            trace=(),
            timestamps=_timestamps(),
            dimension="mock_dim",
            value=1.0,
        )
        stage = (
            ResultBuilder()
            .with_id("stage_1")
            .with_pipeline_id("pipe_1")
            .with_stage_id("mock_stage")
            .with_scores(score)
            .with_created_at(_timestamps().created_at)
            .build_stage_result()
        )
        module = (
            ResultBuilder()
            .with_id("module_1")
            .with_pipeline_id("pipe_1")
            .with_module_id("mock_module")
            .with_stage_results(stage)
            .with_scores(score)
            .with_created_at(_timestamps().created_at)
            .build_module_result()
        )
        aggregator = ResultAggregator()
        analysis = aggregator.aggregate_modules_to_analysis(
            pipeline_id="pipe_1",
            module_results=(module,),
            result_id="analysis_1",
        )
        assert analysis.validate() is True
        final = aggregator.aggregate_to_final(analysis, result_id="final_1")
        assert final.validate() is True
        assert any(code.startswith("module:mock_module:ok") for code in final.summary_codes)

        summary = SummaryBuilder().build_from_final_result(final)
        assert summary.success is True
        assert "mock_module" in summary.module_ids

        repo = ResultRepository()
        repo.put_final_result(final)
        assert repo.get_final_result("final_1").id == "final_1"
        assert repo.get_analysis_result("analysis_1").id == "analysis_1"

        serializer = ResultSerializer()
        restored = serializer.final_from_json(serializer.to_json(final))
        assert restored.id == "final_1"
        assert restored.analysis_result is not None

    def test_merger_dedupes_by_id(self) -> None:
        """Merger should keep one entry per result id."""
        module = (
            ResultBuilder()
            .with_id("mod")
            .with_pipeline_id("p")
            .with_module_id("m")
            .build_module_result()
        )
        left = (
            ResultBuilder()
            .with_id("a1")
            .with_pipeline_id("p")
            .with_module_results(module)
            .build_analysis_result()
        )
        right = (
            ResultBuilder()
            .with_id("a2")
            .with_pipeline_id("p")
            .with_module_results(module)
            .build_analysis_result()
        )
        merged = ResultMerger().merge_analysis_results(left, right, result_id="merged")
        assert len(merged.module_results) == 1

    def test_repository_rejects_duplicate(self) -> None:
        """Repository should reject overwrite of stored finals."""
        analysis = (
            ResultBuilder()
            .with_id("ar")
            .with_pipeline_id("p")
            .build_analysis_result()
        )
        final = (
            ResultBuilder()
            .with_id("fr")
            .with_pipeline_id("p")
            .build_final_result(analysis_result=analysis)
        )
        repo = ResultRepository()
        repo.put_final_result(final)
        with pytest.raises(ResultError):
            repo.put_final_result(final)
