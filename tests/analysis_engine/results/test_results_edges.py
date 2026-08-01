"""Additional results infrastructure edge-case tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.exceptions.result_error import ResultError
from engines.analysis_engine.models.analysis_decision import AnalysisDecision
from engines.analysis_engine.models.analysis_evidence import AnalysisEvidence
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.results.result_aggregator import ResultAggregator
from engines.analysis_engine.results.result_builder import ResultBuilder
from engines.analysis_engine.results.result_repository import ResultRepository
from engines.analysis_engine.results.result_serializer import ResultSerializer


def _ts() -> ModelTimestamps:
    return ModelTimestamps(created_at="2026-08-01T00:00:00Z")


def _meta() -> AnalysisMetadata:
    return AnalysisMetadata(id="m", version="1.0.0", timestamps=_ts())


class TestResultsInfrastructureEdges:
    """Extra coverage for serializer/repository/aggregator edges."""

    def test_stage_module_repository_and_decision_roundtrip(self) -> None:
        """Repository and serializer should handle nested decision/evidence."""
        evidence = AnalysisEvidence(
            id="ev1",
            version="1.0.0",
            metadata=_meta(),
            trace=(),
            timestamps=_ts(),
            source="mock",
            reference_ids=("ref1",),
            payload={"k": 1},
        )
        decision = AnalysisDecision(
            id="d1",
            version="1.0.0",
            metadata=_meta(),
            trace=(),
            timestamps=_ts(),
            decision_type="mock",
            outcome="pass",
            confidence=0.5,
            evidence=(evidence,),
        )
        stage = (
            ResultBuilder()
            .with_id("st")
            .with_pipeline_id("p")
            .with_stage_id("stage_mock")
            .with_decisions(decision)
            .with_created_at(_ts().created_at)
            .build_stage_result()
        )
        module = ResultAggregator().aggregate_stages_to_module(
            module_id="mod_mock",
            stage_results=(stage,),
            pipeline_id="p",
            result_id="mod_result",
        )
        repo = ResultRepository()
        repo.put_stage_result(stage)
        repo.put_module_result(module)
        assert repo.get_stage_result("st").stage_id == "stage_mock"
        assert repo.get_module_result("mod_result").module_id == "mod_mock"
        with pytest.raises(ResultError):
            repo.put_stage_result(stage)

        serializer = ResultSerializer()
        analysis = ResultAggregator().aggregate_modules_to_analysis(
            pipeline_id="p",
            module_results=(module,),
            result_id="ar",
        )
        restored = serializer.analysis_from_json(serializer.to_json(analysis))
        assert restored.decisions or restored.module_results
        assert restored.module_results[0].stage_results[0].decisions[0].id == "d1"
        repo.clear()
        assert repo.list_analysis_result_ids() == ()

    def test_builder_requires_ids(self) -> None:
        """Builder should require stage/module/pipeline identifiers."""
        with pytest.raises(ResultError):
            ResultBuilder().build_stage_result()
        with pytest.raises(ResultError):
            ResultBuilder().build_module_result()
        with pytest.raises(ResultError):
            ResultBuilder().build_analysis_result()
