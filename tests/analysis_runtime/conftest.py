"""Shared fixtures for Analysis Runtime tests."""

from __future__ import annotations

from typing import Sequence

import pytest

from engines.analysis_engine.runtime import (
    AnalysisContext,
    AnalysisRuntime,
    BaseAnalysisModule,
    StageResult,
)
from engines.analysis_engine.runtime.constants import (
    CANONICAL_STAGES,
    DEFAULT_DEPENDENCIES,
)


class StubModule(BaseAnalysisModule):
    """Deterministic stub module with no business rules."""

    def evaluate(self, context: AnalysisContext) -> StageResult:
        upstream = {
            dep: context.get_stage_result(dep).payload if context.get_stage_result(dep) else None
            for dep in self.dependencies
        }
        return StageResult(
            stage_id=self.stage_id,
            module_version=self.version,
            payload={
                "stage": self.stage_id,
                "request_id": context.request_id,
                "upstream": upstream,
                "day_master": context.chart.get("day_master"),
            },
        )


class FailingModule(BaseAnalysisModule):
    """Stub that always raises."""

    def evaluate(self, context: AnalysisContext) -> StageResult:
        raise RuntimeError(f"boom:{self.stage_id}")


def make_stub(
    stage_id: str,
    *,
    dependencies: Sequence[str] | None = None,
) -> StubModule:
    deps = (
        tuple(dependencies)
        if dependencies is not None
        else DEFAULT_DEPENDENCIES.get(stage_id, ())
    )
    return StubModule(stage_id=stage_id, dependencies=deps)


def register_all_stubs(runtime: AnalysisRuntime) -> None:
    for stage_id in CANONICAL_STAGES:
        runtime.register(make_stub(stage_id))


@pytest.fixture
def context() -> AnalysisContext:
    return AnalysisContext(
        request_id="req-test-001",
        chart={"day_master": "Jia", "year": 1990},
        calendar={"solar_term": "立春"},
        metadata={"source": "unit-test"},
        knowledge_version="knowledge-1.0.0",
    )


@pytest.fixture
def runtime() -> AnalysisRuntime:
    return AnalysisRuntime(require_all_canonical_stages=True)


@pytest.fixture
def partial_runtime() -> AnalysisRuntime:
    return AnalysisRuntime(require_all_canonical_stages=False)
