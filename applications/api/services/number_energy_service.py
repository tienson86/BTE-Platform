"""Applications-layer adapter for Number Energy Engine V1."""

from __future__ import annotations

from typing import Any

from applications.api.schemas.number_energy import NumberEnergyDataOut
from engines.number_energy.constants import (
    CLASSIFICATION_CUSTOMER_LABELS,
    FORBIDDEN_CUSTOMER_PHRASES,
    PATTERN_CUSTOMER_LABELS,
    UNDEFINED_REASON_CUSTOMER_VI,
)
from engines.number_energy.engine import NumberEnergyEngine
from engines.number_energy.exceptions import (
    NumberEnergyEngineError,
    NumberEnergyValidationError,
)
from engines.number_energy.types import NumberEnergyResult


class NumberEnergyAPIService:
    """Shape engine output for the Applications API without adding V2 rules."""

    def __init__(self, engine: NumberEnergyEngine | None = None) -> None:
        self._engine = engine or NumberEnergyEngine()

    def analyze(self, number: str, *, purpose_context: str) -> dict[str, Any]:
        """Run V1 analysis and return the public API payload."""
        try:
            result = self._engine.analyze(number, purpose_context=purpose_context)
        except NumberEnergyValidationError:
            raise
        except NumberEnergyEngineError:
            raise
        payload = to_api_payload(result)
        _assert_safe_api_payload(payload)
        return NumberEnergyDataOut.model_validate(payload).model_dump()


def to_api_payload(result: NumberEnergyResult) -> dict[str, Any]:
    """Map engine result to occurrences / state / patterns / narrative / warnings."""
    occurrences = [_occurrence_payload(item.to_dict()) for item in result.occurrences]
    warnings = [
        {
            "code": item.state,
            "reason": item.reason,
            "customer_reason": UNDEFINED_REASON_CUSTOMER_VI.get(
                item.reason, item.reason
            ),
            "source_digits": item.source_digits,
            "source_span": [item.source_span[0], item.source_span[1]],
        }
        for item in result.undefined_segments
    ]
    narrative = result.narrative.to_dict()
    for key in ("paragraphs", "strengths", "watchouts"):
        narrative[key] = list(narrative[key])
    summary = result.summary.to_dict()
    for key in (
        "dominant_energy_ids",
        "repeated_energy_ids",
        "controlled_energy_ids",
        "challenging_without_control",
    ):
        summary[key] = list(summary[key])
    return {
        "occurrences": occurrences,
        "sequence_state": result.sequence_state,
        "patterns": list(result.approved_patterns),
        "narrative": narrative,
        "warnings": warnings,
        "metadata": {
            "engine": "number_energy",
            "engine_version": "1.0.0",
            "knowledge_version": result.knowledge_version,
            "system_name": "Bát Cực Linh Số",
            "system_short_name": "Năng lượng số",
            "purpose_context": result.purpose_context,
            "input_raw": result.input_raw,
            "raw_digits": list(result.raw_digits),
            "sequence_states": list(result.sequence_states),
            "summary": summary,
            "pattern_labels": [
                PATTERN_CUSTOMER_LABELS.get(item, item)
                for item in result.approved_patterns
            ],
            "analyzed_input": result.analyzed_input or result.input_raw,
            "leading_phone_zero": result.leading_phone_zero,
        },
        "reading": result.reading or {},
    }


def _occurrence_payload(item: dict[str, Any]) -> dict[str, Any]:
    """JSON-native occurrence (span as a two-item list)."""
    payload = dict(item)
    span = payload.get("source_span")
    if isinstance(span, tuple):
        payload["source_span"] = [span[0], span[1]]
    classification = str(payload.get("classification") or "")
    payload["classification_label"] = CLASSIFICATION_CUSTOMER_LABELS.get(
        classification, classification
    )
    return payload


def _assert_safe_api_payload(payload: dict[str, Any]) -> None:
    """Refuse forbidden fatalistic or diagnostic-certainty wording."""
    blob = str(payload).lower()
    for phrase in FORBIDDEN_CUSTOMER_PHRASES:
        if phrase.lower() in blob:
            raise NumberEnergyEngineError(f"forbidden customer phrase: {phrase}")
    if "chẩn đoán bệnh" in blob or "chan doan benh" in blob:
        raise NumberEnergyEngineError("forbidden medical diagnosis wording")
