"""Luck Engine — Analysis Runtime stage module."""

from __future__ import annotations

import logging
from typing import Sequence

from engines.analysis_engine.luck_engine.calculator import LuckCalculator
from engines.analysis_engine.luck_engine.models import LuckResult
from engines.analysis_engine.luck_engine.validators import (
    validate_context,
    validate_knowledge_session,
    validate_result,
    validate_upstream,
)
from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from engines.analysis_engine.runtime.models import AnalysisContext, StageResult

logger = logging.getLogger(__name__)

MODULE_VERSION = "1.0.0"
STAGE_ID = "luck"
DEPENDENCIES: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "ten_gods",
    "combination",
    "shensha",
)


class LuckEngine(BaseAnalysisModule):
    """Luck-layer analysis stage for the Analysis Runtime.

    Supports Da Yun, Liu Nian, Liu Yue, Liu Ri, and Liu Shi.

    Public contract:
        evaluate(context: AnalysisContext) -> StageResult

    Typed domain output ``LuckResult`` is embedded in
    ``StageResult.payload`` and recoverable via
    ``LuckResult.from_stage_result``.
    """

    stage_id: str = STAGE_ID
    version: str = MODULE_VERSION
    dependencies: Sequence[str] = DEPENDENCIES

    def __init__(
        self,
        *,
        calculator: LuckCalculator | None = None,
        version: str | None = None,
    ) -> None:
        super().__init__(
            stage_id=STAGE_ID,
            version=version or MODULE_VERSION,
            dependencies=DEPENDENCIES,
        )
        self._calculator = calculator or LuckCalculator()

    def evaluate(self, context: AnalysisContext) -> StageResult:
        """Evaluate Luck layers and return a Runtime StageResult."""
        luck_result = self.evaluate_luck(context)
        stage_result = StageResult(
            stage_id=self.stage_id,
            status="success",
            module_version=self.version,
            payload=luck_result.to_dict(),
            confidence=luck_result.confidence,
            evidence=list(luck_result.evidence),
            diagnostics=list(luck_result.diagnostics),
        )
        logger.info(
            "luck_evaluated",
            extra={
                "request_id": context.request_id,
                "active_count": luck_result.summary.get("active_count"),
                "confidence_score": luck_result.confidence.score,
                "knowledge_version": luck_result.knowledge_version,
            },
        )
        return stage_result

    def evaluate_luck(self, context: AnalysisContext) -> LuckResult:
        """Typed evaluation returning LuckResult."""
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
