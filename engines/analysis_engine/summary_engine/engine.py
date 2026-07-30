"""Summary Engine — Analysis Runtime stage module."""

from __future__ import annotations

import logging
from typing import Sequence

from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from engines.analysis_engine.runtime.models import AnalysisContext, StageResult
from engines.analysis_engine.summary_engine.aggregator import SummaryAggregator
from engines.analysis_engine.summary_engine.models import SummaryResult
from engines.analysis_engine.summary_engine.validators import (
    validate_context,
    validate_result,
    validate_upstream,
    validate_upstream_schema,
)

logger = logging.getLogger(__name__)

MODULE_VERSION = "1.0.0"
STAGE_ID = "summary"
DEPENDENCIES: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "ten_gods",
    "combination",
    "shensha",
    "luck",
)


class SummaryEngine(BaseAnalysisModule):
    """Cross-stage consolidation stage for the Analysis Runtime.

    Aggregation only — no domain recomputation and no Knowledge SDK access.

    Public contract:
        evaluate(context: AnalysisContext) -> StageResult

    Typed domain output ``SummaryResult`` is embedded in
    ``StageResult.payload`` and recoverable via
    ``SummaryResult.from_stage_result``.
    """

    stage_id: str = STAGE_ID
    version: str = MODULE_VERSION
    dependencies: Sequence[str] = DEPENDENCIES

    def __init__(
        self,
        *,
        aggregator: SummaryAggregator | None = None,
        version: str | None = None,
    ) -> None:
        super().__init__(
            stage_id=STAGE_ID,
            version=version or MODULE_VERSION,
            dependencies=DEPENDENCIES,
        )
        self._aggregator = aggregator or SummaryAggregator()

    def evaluate(self, context: AnalysisContext) -> StageResult:
        """Aggregate upstream results and return a Runtime StageResult."""
        summary_result = self.evaluate_summary(context)
        stage_result = StageResult(
            stage_id=self.stage_id,
            status="success",
            module_version=self.version,
            payload=summary_result.to_dict(),
            confidence=summary_result.confidence,
            evidence=list(summary_result.evidence),
            diagnostics=list(summary_result.diagnostics),
        )
        logger.info(
            "summary_evaluated",
            extra={
                "request_id": context.request_id,
                "consistency_status": summary_result.consistency.status,
                "confidence_score": summary_result.confidence.score,
                "evidence_index_count": summary_result.summary.get(
                    "evidence_index_count"
                ),
            },
        )
        return stage_result

    def evaluate_summary(self, context: AnalysisContext) -> SummaryResult:
        """Typed evaluation returning SummaryResult."""
        validate_context(context)
        upstream = validate_upstream(context)
        validate_upstream_schema(upstream)
        result = self._aggregator.aggregate(context, upstream=upstream)
        validate_result(result)
        return result
