"""Luck Analysis validation. No fortune checks."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from engines.luck_engine.analysis_constants import (
    ANALYSIS_VERSION,
    FORBIDDEN_FORTUNE_FIELDS,
    PUBLISHED_OUTPUTS,
    REQUIRED_ANALYSIS_PIPELINE_VERSION,
    REQUIRED_DECISION_PIPELINE_VERSION,
    REQUIRED_TIMELINE_VERSION,
)
from engines.luck_engine.exceptions import LuckAnalysisValidationError


def _contains_forbidden(payload: Any, path: str = "") -> str | None:
    """Return the first forbidden fortune field path when present."""
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            lowered = str(key).lower()
            next_path = f"{path}.{key}" if path else str(key)
            if lowered in FORBIDDEN_FORTUNE_FIELDS:
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
        raise LuckAnalysisValidationError(f"missing_published_outputs:{','.join(missing)}")


def validate_contract_integrity(payload: Mapping[str, Any]) -> None:
    """Ensure contract keys exist and fortune fields are absent."""
    validate_schema(payload)
    forbidden = _contains_forbidden(payload)
    if forbidden:
        raise LuckAnalysisValidationError(f"forbidden_field:{forbidden}")


def validate_dependency_order(
    executed: Sequence[str],
    expected: Sequence[str],
) -> None:
    """Require executed stages to follow registry order."""
    filtered = [item for item in expected if item in executed]
    if list(executed) != filtered:
        raise LuckAnalysisValidationError(
            f"dependency_order:{','.join(executed)}!={','.join(expected)}"
        )


def validate_duplicate_outputs(names: Sequence[str]) -> None:
    """Reject duplicate published names."""
    if len(names) != len(set(names)):
        raise LuckAnalysisValidationError("duplicate_outputs")


def validate_timeline_compatibility(timeline_version: str | None) -> None:
    """Admit only LE-1 timeline version."""
    if timeline_version != REQUIRED_TIMELINE_VERSION:
        raise LuckAnalysisValidationError(
            f"incompatible_timeline_version:{timeline_version}"
        )


def validate_analysis_compatibility(pipeline_version: str | None) -> None:
    """Admit only AX-2 analysis pipeline version."""
    if pipeline_version != REQUIRED_ANALYSIS_PIPELINE_VERSION:
        raise LuckAnalysisValidationError(
            f"incompatible_analysis_version:{pipeline_version}"
        )


def validate_decision_compatibility(pipeline_version: str | None) -> None:
    """Admit only AX-3 decision pipeline version."""
    if pipeline_version != REQUIRED_DECISION_PIPELINE_VERSION:
        raise LuckAnalysisValidationError(
            f"incompatible_decision_version:{pipeline_version}"
        )


def validate_version_compatibility(*, analysis_version: str) -> None:
    """Admit only this Luck Analysis generation."""
    if analysis_version != ANALYSIS_VERSION:
        raise LuckAnalysisValidationError(
            f"incompatible_luck_analysis_version:{analysis_version}"
        )


def validate_result_payload(
    payload: Mapping[str, Any],
    *,
    executed: Sequence[str],
    expected_order: Sequence[str],
    published_names: Sequence[str],
    timeline_version: str | None,
    analysis_pipeline_version: str | None,
    decision_pipeline_version: str | None,
) -> None:
    """Run the full LE-2 validation suite on a published payload."""
    validate_contract_integrity(payload)
    validate_dependency_order(executed, expected_order)
    validate_duplicate_outputs(published_names)
    validate_timeline_compatibility(timeline_version)
    validate_analysis_compatibility(analysis_pipeline_version)
    validate_decision_compatibility(decision_pipeline_version)
    validate_version_compatibility(
        analysis_version=str(payload.get("analysis_version") or ""),
    )
