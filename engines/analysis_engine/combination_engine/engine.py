"""Combination Engine — Analysis Runtime stage module."""

from __future__ import annotations

import logging
from typing import Sequence

from engines.analysis_engine.combination_engine.calculator import CombinationCalculator
from engines.analysis_engine.combination_engine.models import CombinationResult
from engines.analysis_engine.combination_engine.validators import (
    validate_context,
    validate_knowledge_session,
    validate_result,
    validate_upstream,
)
from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from engines.analysis_engine.runtime.models import AnalysisContext, StageResult

logger = logging.getLogger(__name__)

MODULE_VERSION = "1.0.0"
STAGE_ID = "combination"
DEPENDENCIES: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "ten_gods",
)


class CombinationEngine(BaseAnalysisModule):
    """Natal Combination analysis stage for the Analysis Runtime.

    Public contract:
        evaluate(context: AnalysisContext) -> StageResult

    Typed domain output ``CombinationResult`` is embedded in
    ``StageResult.payload`` and recoverable via
    ``CombinationResult.from_stage_result``.
    """

    stage_id: str = STAGE_ID
    version: str = MODULE_VERSION
    dependencies: Sequence[str] = DEPENDENCIES

    def __init__(
        self,
        *,
        calculator: CombinationCalculator | None = None,
        version: str | None = None,
    ) -> None:
        super().__init__(
            stage_id=STAGE_ID,
            version=version or MODULE_VERSION,
            dependencies=DEPENDENCIES,
        )
        self._calculator = calculator or CombinationCalculator()

    def evaluate(self, context: AnalysisContext) -> StageResult:
        """Evaluate Combination relations and return a Runtime StageResult."""
        combination_result = self.evaluate_combination(context)
        stage_result = StageResult(
            stage_id=self.stage_id,
            status="success",
            module_version=self.version,
            payload=combination_result.to_dict(),
            confidence=combination_result.confidence,
            evidence=list(combination_result.evidence),
            diagnostics=list(combination_result.diagnostics),
        )
        logger.info(
            "combination_evaluated",
            extra={
                "request_id": context.request_id,
                "active_count": combination_result.summary.get("active_count"),
                "confidence_score": combination_result.confidence.score,
                "knowledge_version": combination_result.knowledge_version,
            },
        )
        return stage_result

    def evaluate_combination(self, context: AnalysisContext) -> CombinationResult:
        """Typed evaluation returning CombinationResult."""
        validate_context(context)
        upstream = validate_upstream(context)
        session = validate_knowledge_session(context)
        result = self._calculator.calculate(
            context,
            session=session,
            upstream=upstream,
        )
        validate_result(result)
        return result
