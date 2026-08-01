"""Test builders package for Analysis Engine."""

from __future__ import annotations

from engines.analysis_engine.context.runtime_context import RuntimeContext
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class ContextBuilder:
    """Public builder interface for test contexts.

    Framework skeleton only. No builder logic.
    """

    def build_runtime_context(self, context_id: str) -> RuntimeContext:
        """Build a runtime context stub for tests."""
        raise NotImplementedError

    def build_pipeline_context(self, context_id: str, pipeline_id: str) -> PipelineContext:
        """Build a pipeline context stub for tests."""
        raise NotImplementedError


class ResultBuilder:
    """Public builder interface for test results.

    Framework skeleton only. No builder logic.
    """

    def build_empty_result(self, pipeline_id: str) -> object:
        """Build an empty result stub for tests."""
        raise NotImplementedError
