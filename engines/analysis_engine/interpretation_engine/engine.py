"""Interpretation Engine — narrative generation from AnalysisResult."""

from __future__ import annotations

import logging

from engines.analysis_engine.interpretation_engine.default_knowledge import (
    KNOWLEDGE_VERSION,
)
from engines.analysis_engine.interpretation_engine.models import (
    InterpretationContext,
    InterpretationResult,
)
from engines.analysis_engine.interpretation_engine.pipeline import (
    InterpretationPipeline,
)
from engines.analysis_engine.interpretation_engine.validators import (
    validate_analysis_result,
    validate_context,
    validate_knowledge_session,
    validate_result,
)

logger = logging.getLogger(__name__)

MODULE_VERSION = "1.0.0"


class InterpretationEngine:
    """Produce InterpretationResult from published AnalysisResult.

    Public contract:
        interpret(context: InterpretationContext) -> InterpretationResult

    Pipeline:
        Sentence Selection → Template Binding → Placeholder Binding
        → Paragraph Builder → Interpretation Builder

    Does not recompute analytical stages and does not render reports.
    """

    version: str = MODULE_VERSION

    def __init__(
        self,
        *,
        pipeline: InterpretationPipeline | None = None,
        version: str | None = None,
    ) -> None:
        self.version = version or MODULE_VERSION
        self._pipeline = pipeline or InterpretationPipeline(
            module_version=self.version,
        )

    def interpret(self, context: InterpretationContext) -> InterpretationResult:
        """Run interpretation pipeline and return InterpretationResult."""
        validate_context(context)
        validate_analysis_result(context.analysis_result)
        session = validate_knowledge_session(context)
        knowledge_version = (
            context.knowledge_version
            or getattr(session.get_module("interpretation_knowledge"), "version", None)
            or KNOWLEDGE_VERSION
        )
        result = self._pipeline.run(
            context,
            session=session,
            knowledge_version=str(knowledge_version),
        )
        validate_result(result)
        logger.info(
            "interpretation_completed",
            extra={
                "request_id": result.request_id,
                "section_count": result.summary.get("section_count"),
                "sentence_count": result.summary.get("sentence_count"),
                "confidence_score": result.confidence.score,
                "knowledge_version": result.knowledge_version,
            },
        )
        return result

    def run(self, context: InterpretationContext) -> InterpretationResult:
        """Alias of :meth:`interpret` for pipeline-style callers."""
        return self.interpret(context)
