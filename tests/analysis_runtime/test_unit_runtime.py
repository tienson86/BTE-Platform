"""Unit tests for Analysis Runtime models and components."""

from __future__ import annotations

import pytest

from engines.analysis_engine.runtime import (
    AdmissionError,
    AnalysisContext,
    AnalysisRuntime,
    CacheError,
    CacheManager,
    DependencyResolver,
    ErrorHandler,
    PrerequisiteError,
    RegistrationError,
    StageExecutionError,
    StageResult,
    StateError,
    ValidationError,
    ValidationManager,
)
from engines.analysis_engine.runtime.constants import CANONICAL_STAGES
from tests.analysis_runtime.conftest import (
    FailingModule,
    make_stub,
    register_all_stubs,
)


class TestAnalysisContext:
    def test_chart_is_immutable_mapping(self, context: AnalysisContext) -> None:
        with pytest.raises(TypeError):
            context.chart["day_master"] = "Yi"  # type: ignore[index]

    def test_publish_is_append_only(self, context: AnalysisContext) -> None:
        result = StageResult(stage_id="strength", payload={"ok": True})
        context.publish_stage_result(result)
        assert context.strength_result is result
        with pytest.raises(StateError):
            context.publish_stage_result(
                StageResult(stage_id="strength", payload={"again": True})
            )

    def test_stage_accessors(self, context: AnalysisContext) -> None:
        context.publish_stage_result(StageResult(stage_id="temperature"))
        assert context.temperature_result is not None
        assert context.pattern_result is None


class TestDependencyResolver:
    def test_canonical_order(self) -> None:
        resolver = DependencyResolver()
        order = resolver.resolve_order(CANONICAL_STAGES)
        assert order == CANONICAL_STAGES

    def test_rejects_forward_dependency(self) -> None:
        resolver = DependencyResolver()
        with pytest.raises(RegistrationError):
            resolver.register("strength", dependencies=("temperature",))


class TestCacheManager:
    def test_request_scope_get_set(self) -> None:
        cache = CacheManager()
        cache.set("a", 1, scope="request")
        assert cache.get("a", scope="request") == 1
        assert cache.hits == 1
        assert cache.misses == 0

    def test_cross_request_disabled_by_default(self) -> None:
        cache = CacheManager()
        with pytest.raises(CacheError):
            cache.set("a", 1, scope="cross_request")

    def test_begin_request_clears_request_cache(self) -> None:
        cache = CacheManager()
        cache.set("a", 1, scope="request")
        cache.begin_request()
        assert cache.get("a", scope="request") is None


class TestValidationManager:
    def test_admission_requires_request_id(self) -> None:
        manager = ValidationManager()
        ctx = AnalysisContext(request_id="")
        with pytest.raises(AdmissionError):
            manager.validate_admission(ctx)

    def test_precondition_missing(self, context: AnalysisContext) -> None:
        manager = ValidationManager()
        with pytest.raises(PrerequisiteError):
            manager.validate_preconditions(
                context,
                stage_id="temperature",
                dependencies=("strength",),
            )

    def test_stage_result_mismatch(self) -> None:
        manager = ValidationManager()
        with pytest.raises(ValidationError):
            manager.validate_stage_result(
                StageResult(stage_id="luck"),
                expected_stage_id="strength",
            )


class TestErrorHandler:
    def test_classifies_generic_exception(self) -> None:
        handler = ErrorHandler()
        error = handler.classify(RuntimeError("x"), stage_id="pattern")
        assert isinstance(error, StageExecutionError)
        assert error.stage_id == "pattern"
        assert error.retryable is True


class TestAnalysisRuntimeUnit:
    def test_register_and_duplicate(self, partial_runtime: AnalysisRuntime) -> None:
        partial_runtime.register(make_stub("strength"))
        with pytest.raises(RegistrationError):
            partial_runtime.register(make_stub("strength"))

    def test_validate_context(self, runtime: AnalysisRuntime, context: AnalysisContext) -> None:
        report = runtime.validate(context)
        assert report.is_valid is True

    def test_execute_single_module(
        self,
        partial_runtime: AnalysisRuntime,
        context: AnalysisContext,
    ) -> None:
        partial_runtime.register(make_stub("strength"))
        result = partial_runtime.execute("strength", context)
        assert result.stage_id == "strength"
        assert context.strength_result is result

    def test_execute_requires_prerequisites(
        self,
        partial_runtime: AnalysisRuntime,
        context: AnalysisContext,
    ) -> None:
        partial_runtime.register(make_stub("temperature"))
        with pytest.raises(PrerequisiteError):
            partial_runtime.execute("temperature", context)

    def test_run_requires_all_canonical_by_default(
        self,
        runtime: AnalysisRuntime,
        context: AnalysisContext,
    ) -> None:
        runtime.register(make_stub("strength"))
        with pytest.raises(StateError):
            runtime.run(context)

    def test_stage_failure_is_classified(
        self,
        partial_runtime: AnalysisRuntime,
        context: AnalysisContext,
    ) -> None:
        partial_runtime.register(
            FailingModule(stage_id="strength", dependencies=())
        )
        with pytest.raises(StageExecutionError):
            partial_runtime.execute("strength", context)

    def test_run_full_pipeline(
        self,
        runtime: AnalysisRuntime,
        context: AnalysisContext,
    ) -> None:
        register_all_stubs(runtime)
        result = runtime.run(context)
        assert result.request_id == context.request_id
        assert result.summary_result is not None
        assert len(result.stage_results) == len(CANONICAL_STAGES)
        assert result.execution_metadata.status == "completed"
        assert result.performance_metrics.total_duration_ms >= 0
        assert len(result.execution_trace.spans) == len(CANONICAL_STAGES)

    def test_evaluate_alias(
        self,
        runtime: AnalysisRuntime,
        context: AnalysisContext,
    ) -> None:
        register_all_stubs(runtime)
        result = runtime.evaluate(context)
        assert result.strength_result is not None
