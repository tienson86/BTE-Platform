"""Ten Gods ecosystem engine. Consumes DI-01 and DI-02. No new identity."""

from __future__ import annotations

from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.ten_gods.combinations.models import (
    TenGodCombinationCollection,
)
from engines.detailed_interpretation_engine.ten_gods.ecosystem.evaluate import evaluate_ecosystem
from engines.detailed_interpretation_engine.ten_gods.ecosystem.models import TenGodEcosystemResult
from engines.detailed_interpretation_engine.ten_gods.models import TenGodInterpretationCollection
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


def interpret_ten_gods_ecosystem(
    natal: TenGodInterpretationCollection,
    combinations: TenGodCombinationCollection,
    *,
    mc01_bound: bool = False,
) -> TenGodEcosystemResult:
    """Build the natal Ten Gods ecosystem from evaluated combinations."""
    if natal.state is EvaluationStatus.NOT_EVALUATED and not natal.items:
        return TenGodEcosystemResult(analysis_id=natal.analysis_id)
    if natal.state is EvaluationStatus.UNRESOLVED:
        return TenGodEcosystemResult(
            analysis_id=natal.analysis_id,
            state=EvaluationStatus.UNRESOLVED,
            confidence=ConfidenceValue(summary="unresolved"),
        )
    return evaluate_ecosystem(natal, combinations, mc01_bound=mc01_bound)
