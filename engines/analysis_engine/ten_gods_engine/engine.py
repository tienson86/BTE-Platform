"""Ten Gods Engine — Analysis Runtime stage module."""

from __future__ import annotations

import logging
from typing import Sequence

from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    StageResult,
)
from engines.analysis_engine.ten_gods_engine.calculator import TenGodsCalculator
from engines.analysis_engine.ten_gods_engine.models import TenGodsResult
from engines.analysis_engine.ten_gods_engine.validators import (
    validate_context,
    validate_knowledge_session,
    validate_result,
    validate_upstream,
)

logger = logging.getLogger(__name__)

MODULE_VERSION = "1.0.0"
STAGE_ID = "ten_gods"
DEPENDENCIES: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
)


class TenGodsEngine(BaseAnalysisModule):
    """Natal Ten Gods analysis stage for the Analysis Runtime.

    Public contract:
        evaluate(context: AnalysisContext) -> StageResult

    The typed domain output ``TenGodsResult`` is embedded in
    ``StageResult.payload`` and recoverable via
    ``TenGodsResult.from_stage_result``.
    """

    stage_id: str = STAGE_ID
    version: str = MODULE_VERSION
    dependencies: Sequence[str] = DEPENDENCIES

    def __init__(
        self,
        *,
        calculator: TenGodsCalculator | None = None,
        version: str | None = None,
    ) -> None:
        super().__init__(
            stage_id=STAGE_ID,
            version=version or MODULE_VERSION,
            dependencies=DEPENDENCIES,
        )
        self._calculator = calculator or TenGodsCalculator()

    def evaluate(self, context: AnalysisContext) -> StageResult:
        """Evaluate Ten Gods and return a Runtime StageResult."""
        ten_gods_result = self.evaluate_ten_gods(context)
        stage_result = StageResult(
            stage_id=self.stage_id,
            status="success",
            module_version=self.version,
            payload=ten_gods_result.to_dict(),
            confidence=ten_gods_result.confidence,
            evidence=list(ten_gods_result.evidence),
            diagnostics=list(ten_gods_result.diagnostics),
        )
        logger.info(
            "ten_gods_evaluated",
            extra={
                "request_id": context.request_id,
                "presence_count": len(ten_gods_result.presence),
                "confidence_score": ten_gods_result.confidence.score,
                "knowledge_version": ten_gods_result.knowledge_version,
            },
        )
        return stage_result

    def evaluate_ten_gods(self, context: AnalysisContext) -> TenGodsResult:
        """Typed evaluation returning TenGodsResult (domain public output)."""
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
