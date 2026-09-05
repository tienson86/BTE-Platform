"""Ten God combination engine. Deterministic; no LLM."""

from __future__ import annotations

from engines.detailed_interpretation_engine.enums import CombinationState, EvaluationStatus
from engines.detailed_interpretation_engine.ten_gods.combinations.constants import V1_SPECS
from engines.detailed_interpretation_engine.ten_gods.combinations.evaluate import (
    apply_chain_dedupe,
    evaluate_spec,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.models import (
    TenGodCombinationCollection,
)
from engines.detailed_interpretation_engine.ten_gods.models import TenGodInterpretationCollection
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


def interpret_ten_god_combinations(
    natal: TenGodInterpretationCollection,
    *,
    mc01_bound: bool = False,
    damage_ids: tuple[str, ...] = (),
    rescue_ids: tuple[str, ...] = (),
    purity_ref: str = "",
) -> TenGodCombinationCollection:
    """Evaluate all V1 combinations from DI-01 natal results."""
    if natal.state is EvaluationStatus.NOT_EVALUATED and not natal.items:
        return TenGodCombinationCollection(analysis_id=natal.analysis_id)
    if natal.state is EvaluationStatus.UNRESOLVED:
        return TenGodCombinationCollection(
            analysis_id=natal.analysis_id,
            state=EvaluationStatus.UNRESOLVED,
            confidence=ConfidenceValue(summary="unresolved"),
        )
    raw = tuple(
        evaluate_spec(
            spec,
            natal,
            mc01_bound=mc01_bound,
            damage_ids=damage_ids,
            rescue_ids=rescue_ids,
            purity_ref=purity_ref,
        )
        for spec in V1_SPECS
    )
    items = apply_chain_dedupe(raw)
    evidence_ids = tuple(eid for item in items for eid in item.evidence_ids)
    trace_ids = tuple(tid for item in items for tid in item.trace_ids)
    if not mc01_bound:
        state = EvaluationStatus.PARTIALLY_RESOLVED
        confidence = ConfidenceValue(summary="low")
    elif any(item.state is CombinationState.UNRESOLVED for item in items):
        state = EvaluationStatus.PARTIALLY_RESOLVED
        confidence = ConfidenceValue(summary="moderate")
    else:
        state = EvaluationStatus.RESOLVED
        confidence = ConfidenceValue(summary="moderate")
    return TenGodCombinationCollection(
        analysis_id=natal.analysis_id,
        state=state,
        items=items,
        evidence_ids=evidence_ids,
        trace_ids=trace_ids,
        confidence=confidence,
    )
