"""ShenSha Engine — Analysis Runtime stage module."""

from __future__ import annotations

import logging
from typing import Sequence

from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from engines.analysis_engine.runtime.models import AnalysisContext, StageResult
from engines.analysis_engine.shensha_engine.calculator import ShenShaCalculator
from engines.analysis_engine.shensha_engine.models import ShenShaResult
from engines.analysis_engine.shensha_engine.validators import (
    validate_context,
    validate_knowledge_session,
    validate_result,
    validate_upstream,
)

logger = logging.getLogger(__name__)

MODULE_VERSION = "1.0.0"
STAGE_ID = "shensha"
DEPENDENCIES: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "ten_gods",
    "combination",
)


class ShenShaEngine(BaseAnalysisModule):
    """Natal ShenSha analysis stage for the Analysis Runtime.

    Public contract:
        evaluate(context: AnalysisContext) -> StageResult

    Typed domain output ``ShenShaResult`` is embedded in
    ``StageResult.payload`` and recoverable via
    ``ShenShaResult.from_stage_result``.
    """

    stage_id: str = STAGE_ID
    version: str = MODULE_VERSION
    dependencies: Sequence[str] = DEPENDENCIES

    def __init__(
        self,
        *,
        calculator: ShenShaCalculator | None = None,
        version: str | None = None,
    ) -> None:
        super().__init__(
            stage_id=STAGE_ID,
            version=version or MODULE_VERSION,
            dependencies=DEPENDENCIES,
        )
        self._calculator = calculator or ShenShaCalculator()

    def evaluate(self, context: AnalysisContext) -> StageResult:
        """Evaluate ShenSha and return a Runtime StageResult."""
        shensha_result = self.evaluate_shensha(context)
        stage_result = StageResult(
            stage_id=self.stage_id,
            status="success",
            module_version=self.version,
            payload=shensha_result.to_dict(),
            confidence=shensha_result.confidence,
            evidence=list(shensha_result.evidence),
            diagnostics=list(shensha_result.diagnostics),
        )
        logger.info(
            "shensha_evaluated",
            extra={
                "request_id": context.request_id,
                "presence_count": shensha_result.summary.get("presence_count"),
                "confidence_score": shensha_result.confidence.score,
                "knowledge_version": shensha_result.knowledge_version,
            },
        )
        return stage_result

    def evaluate_shensha(self, context: AnalysisContext) -> ShenShaResult:
        """Typed evaluation returning ShenShaResult."""
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
