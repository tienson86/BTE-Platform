"""Final coverage push for infrastructure runtime modules."""

from __future__ import annotations

import pytest

from engines.analysis_engine.context.context_manager import ContextManager
from engines.analysis_engine.exceptions.context_error import ContextError
from engines.analysis_engine.exceptions.result_error import ResultError
from engines.analysis_engine.pipeline.execution_policy import ExecutionPolicy
from engines.analysis_engine.pipeline.executor import Executor
from engines.analysis_engine.pipeline.pipeline import Pipeline
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.registry.query_engine import QueryEngine
from engines.analysis_engine.registry.registry_builder import RegistryBuilder
from engines.analysis_engine.registry.registry_cache import RegistryCache
from engines.analysis_engine.registry.registry_models import (
    RegistryEntry,
    RegistryQuerySpec,
    RegistrySnapshot,
)
from engines.analysis_engine.registry.registry_service import RegistryService
from engines.analysis_engine.results.result_builder import ResultBuilder
from engines.analysis_engine.results.result_repository import ResultRepository
from engines.analysis_engine.results.summary_builder import SummaryBuilder
from tests.analysis_engine.mocks import MockSuccessStage


class TestInfrastructureCoveragePush:
    """Fill remaining high-value infrastructure branches."""

    def test_registry_cache_facade_and_query_resolve(self) -> None:
        """Registry cache facade and query resolve helpers."""
        cache = RegistryCache()
        entry = RegistryEntry(
            entry_id="e1",
            object_type="rule",
            name="n",
            metadata={"object_id": "obj1"},
            references=("ref1",),
        )
        cache.put_entry(entry)
        snap = RegistrySnapshot(snapshot_id="s1", schema_version="1.0.0", entries=(entry,))
        cache.put_snapshot(snap)
        assert cache.get_entry("e1") is not None
        assert cache.get_snapshot("s1") is not None
        cache.invalidate("e1")
        assert cache.get_entry("e1") is None
        cache.clear()

        service = RegistryService()
        service.register(entry)
        engine = QueryEngine(
            entry_provider=service.list_entries,
            resolver=service.resolve,
        )
        assert engine.resolve("e1") is not None
        assert engine.resolve("obj1") is not None
        assert engine.query(RegistryQuerySpec(name="missing")) == ()

        builder = RegistryBuilder()
        registry = builder.create()
        builder.add_entry(registry, entry)
        assert registry.list_entries()[0].entry_id == "e1"
        assert registry.snapshot().entries

    def test_result_repository_and_summary_without_analysis(self) -> None:
        """Repository miss paths and summary without nested analysis."""
        repo = ResultRepository()
        with pytest.raises(ResultError):
            repo.get_analysis_result("missing")
        with pytest.raises(ResultError):
            repo.get_final_result("missing")
        analysis = (
            ResultBuilder()
            .with_id("ar1")
            .with_pipeline_id("p")
            .build_analysis_result()
        )
        repo.put_analysis_result(analysis)
        with pytest.raises(ResultError):
            repo.put_analysis_result(analysis)
        assert "ar1" in repo.list_analysis_result_ids()

        final = (
            ResultBuilder()
            .with_id("fr1")
            .with_pipeline_id("p")
            .with_module_results(
                ResultBuilder()
                .with_id("m1")
                .with_pipeline_id("p")
                .with_module_id("mod")
                .build_module_result()
            )
            .build_final_result()
        )
        summary = SummaryBuilder().build_from_final_result(final)
        assert summary.result_id == "fr1"
        assert "mod" in summary.module_ids

    def test_pipeline_validate_mismatch_and_nondeterministic(self) -> None:
        """Pipeline validate mismatch and non-deterministic ordering path."""
        pipeline = Pipeline("pipe-a", stages=(MockSuccessStage(stage_id="z", order=1),))
        ctx = PipelineContext(context_id="c", pipeline_id="other")
        assert pipeline.validate(ctx) is False
        ctx2 = PipelineContext(context_id="", pipeline_id="pipe-a")
        assert pipeline.validate(ctx2) is False

        policy = ExecutionPolicy(deterministic=False)
        result = Executor(policy=policy).run(
            stages=(MockSuccessStage(stage_id="only"),),
            pipeline_context=PipelineContext(context_id="c", pipeline_id="p"),
            policy=policy,
        )
        assert result.success is True

    def test_context_manager_guard_paths(self) -> None:
        """Context manager should reject invalid transitions."""
        manager = ContextManager()
        with pytest.raises(ContextError):
            manager.initialize()
        manager.create(pipeline_id="p")
        with pytest.raises(ContextError):
            manager.create(pipeline_id="p2")
        with pytest.raises(ContextError):
            manager.expand({"a": 1})
        manager.initialize()
        with pytest.raises(ContextError):
            manager.expand({})
