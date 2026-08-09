"""Luck Decision validation. No interpretation checks beyond forbidden prose fields."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from engines.luck_engine.decision_constants import (
    DECISION_VERSION,
    FORBIDDEN_INTERPRETATION_FIELDS,
    PRIORITY_BALANCED,
    PRIORITY_OPPORTUNITY_FIRST,
    PRIORITY_RISK_FIRST,
    PRIORITY_WITHHELD,
    PUBLISHED_OUTPUTS,
    REQUIRED_ANALYSIS_PIPELINE_VERSION,
    REQUIRED_DECISION_PIPELINE_VERSION,
    REQUIRED_LUCK_ANALYSIS_VERSION,
    REQUIRED_TIMELINE_VERSION,
)
from engines.luck_engine.exceptions import LuckDecisionValidationError

LEGAL_PRIORITIES = {
    PRIORITY_OPPORTUNITY_FIRST,
    PRIORITY_RISK_FIRST,
    PRIORITY_BALANCED,
    PRIORITY_WITHHELD,
}
LEGAL_CONFIDENCE = {"high", "medium", "low", "none"}


def _contains_forbidden(payload: Any, path: str = "") -> str | None:
    """Return the first forbidden interpretation field path when present."""
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            lowered = str(key).lower()
            next_path = f"{path}.{key}" if path else str(key)
            if lowered in FORBIDDEN_INTERPRETATION_FIELDS:
                return next_path
            nested = _contains_forbidden(value, next_path)
            if nested:
                return nested
    elif isinstance(payload, (list, tuple)):
        for index, item in enumerate(payload):
            nested = _contains_forbidden(item, f"{path}[{index}]")
            if nested:
                return nested
    return None


def validate_schema(payload: Mapping[str, Any]) -> None:
    """Require published contract keys on a serialized result."""
    missing = [name for name in PUBLISHED_OUTPUTS if name not in payload]
    if missing:
        raise LuckDecisionValidationError(f"missing_published_outputs:{','.join(missing)}")


def validate_contract_integrity(payload: Mapping[str, Any]) -> None:
    """Ensure contract keys exist and interpretation fields are absent."""
    validate_schema(payload)
    forbidden = _contains_forbidden(payload)
    if forbidden:
        raise LuckDecisionValidationError(f"forbidden_field:{forbidden}")


def validate_dependency_order(executed: Sequence[str], expected: Sequence[str]) -> None:
    """Require executed stages to follow registry order."""
    filtered = [item for item in expected if item in executed]
    if list(executed) != filtered:
        raise LuckDecisionValidationError(
            f"dependency_order:{','.join(executed)}!={','.join(expected)}"
        )


def validate_duplicate_outputs(names: Sequence[str]) -> None:
    """Reject duplicate published names."""
    if len(names) != len(set(names)):
        raise LuckDecisionValidationError("duplicate_outputs")


def validate_timeline_compatibility(timeline_version: str | None) -> None:
    """Admit only LE-1 timeline version."""
    if timeline_version != REQUIRED_TIMELINE_VERSION:
        raise LuckDecisionValidationError(f"incompatible_timeline_version:{timeline_version}")


def validate_analysis_compatibility(
    *,
    luck_analysis_version: str | None,
    pipeline_version: str | None,
) -> None:
    """Admit LE-2 analysis version and AX-2 pipeline version."""
    if luck_analysis_version != REQUIRED_LUCK_ANALYSIS_VERSION:
        raise LuckDecisionValidationError(
            f"incompatible_luck_analysis_version:{luck_analysis_version}"
        )
    if pipeline_version != REQUIRED_ANALYSIS_PIPELINE_VERSION:
        raise LuckDecisionValidationError(f"incompatible_analysis_version:{pipeline_version}")


def validate_decision_compatibility(pipeline_version: str | None) -> None:
    """Admit only AX-3 decision pipeline version."""
    if pipeline_version != REQUIRED_DECISION_PIPELINE_VERSION:
        raise LuckDecisionValidationError(f"incompatible_ax3_version:{pipeline_version}")


def validate_version_compatibility(*, decision_version: str) -> None:
    """Admit only this Luck Decision generation."""
    if decision_version != DECISION_VERSION:
        raise LuckDecisionValidationError(f"incompatible_luck_decision_version:{decision_version}")


def validate_priority_legality(priority: Mapping[str, Any] | None) -> None:
    """Admit only registered priority classes."""
    value = None if priority is None else priority.get("value")
    if value not in LEGAL_PRIORITIES:
        raise LuckDecisionValidationError(f"illegal_priority:{value}")


def validate_confidence_value(confidence: Mapping[str, Any] | None) -> None:
    """Admit only registered confidence labels."""
    value = None if confidence is None else confidence.get("value")
    if value not in LEGAL_CONFIDENCE:
        raise LuckDecisionValidationError(f"illegal_confidence:{value}")


def validate_result_payload(
    payload: Mapping[str, Any],
    *,
    executed: Sequence[str],
    expected_order: Sequence[str],
    published_names: Sequence[str],
    timeline_version: str | None,
    luck_analysis_version: str | None,
    analysis_pipeline_version: str | None,
    decision_pipeline_version: str | None,
) -> None:
    """Run the full LE-3 validation suite on a published payload."""
    validate_contract_integrity(payload)
    validate_dependency_order(executed, expected_order)
    validate_duplicate_outputs(published_names)
    validate_timeline_compatibility(timeline_version)
    validate_analysis_compatibility(
        luck_analysis_version=luck_analysis_version,
        pipeline_version=analysis_pipeline_version,
    )
    validate_decision_compatibility(decision_pipeline_version)
    validate_version_compatibility(decision_version=str(payload.get("decision_version") or ""))
    if payload.get("luck_priority") is not None:
        validate_priority_legality(payload.get("luck_priority"))
    if payload.get("decision_confidence") is not None:
        validate_confidence_value(payload.get("decision_confidence"))
