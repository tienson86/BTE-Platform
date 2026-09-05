"""Shared Pack 07 value objects: version, confidence, trace, identity, metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import (
    as_enum,
    as_float,
    as_str,
    as_str_dict,
    as_str_tuple,
)
from engines.detailed_interpretation_engine.constants import (
    DEFAULT_LOCALE,
    SCHEMA_MINGJU_DECISION,
    SCHEMA_RESULT,
    SCHEMA_RUNTIME_CONTRACT,
    SCHEMA_RULES,
    SCHEMA_COMPOSER,
)
from engines.detailed_interpretation_engine.enums import EvaluationStatus, HourCompleteness


@dataclass(frozen=True, slots=True)
class VersionBundle:
    """Frozen schema / ruleset / composer / contract versions."""

    contract_version: str = SCHEMA_RUNTIME_CONTRACT
    schema_version: str = SCHEMA_RESULT
    ruleset_version: str = SCHEMA_RULES
    composer_version: str = SCHEMA_COMPOSER

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> VersionBundle:
        """Rebuild versions from a mapping."""
        payload = data or {}
        return cls(
            contract_version=as_str(payload.get("contract_version"), SCHEMA_RUNTIME_CONTRACT),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_RESULT),
            ruleset_version=as_str(payload.get("ruleset_version"), SCHEMA_RULES),
            composer_version=as_str(payload.get("composer_version"), SCHEMA_COMPOSER),
        )


@dataclass(frozen=True, slots=True)
class ConfidenceValue:
    """Confidence in range 0.0..1.0, or None when not evaluated."""

    value: float | None = None
    summary: str = ""

    @classmethod
    def from_dict(cls, data: Any) -> ConfidenceValue:
        """Rebuild confidence from a mapping or scalar."""
        if data is None:
            return cls()
        if isinstance(data, (int, float)):
            return cls(value=float(data))
        if isinstance(data, Mapping):
            return cls(
                value=as_float(data.get("value")),
                summary=as_str(data.get("summary")),
            )
        return cls()


@dataclass(frozen=True, slots=True)
class TraceRef:
    """Evidence and engine trace identifiers."""

    trace_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TraceRef:
        """Rebuild trace pointers from a mapping."""
        payload = data or {}
        return cls(
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
        )


@dataclass(frozen=True, slots=True)
class ChartIdentity:
    """Immutable chart identity. No interpretation."""

    analysis_id: str = ""
    chart_id: str = ""
    person_label_ref: str = ""
    birth_civil: str = ""
    calendar_system_ref: str = ""
    gender_or_party_ref: str = ""
    hour_completeness: HourCompleteness = HourCompleteness.UNKNOWN
    timezone_ref: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ChartIdentity:
        """Rebuild identity from a mapping."""
        payload = data or {}
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            chart_id=as_str(payload.get("chart_id")),
            person_label_ref=as_str(payload.get("person_label_ref")),
            birth_civil=as_str(payload.get("birth_civil")),
            calendar_system_ref=as_str(payload.get("calendar_system_ref")),
            gender_or_party_ref=as_str(payload.get("gender_or_party_ref")),
            hour_completeness=as_enum(
                HourCompleteness,
                payload.get("hour_completeness"),
                HourCompleteness.UNKNOWN,
            ),
            timezone_ref=as_str(payload.get("timezone_ref")),
        )


@dataclass(frozen=True, slots=True)
class Mc01Reference:
    """MC-01 reference only. Never a second structural engine."""

    mingju_result_id: str = ""
    schema_version: str = SCHEMA_MINGJU_DECISION
    ruleset_version: str = ""
    content_hash: str = ""
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> Mc01Reference:
        """Rebuild the MC-01 pointer from a mapping."""
        payload = data or {}
        return cls(
            mingju_result_id=as_str(payload.get("mingju_result_id")),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_MINGJU_DECISION),
            ruleset_version=as_str(payload.get("ruleset_version")),
            content_hash=as_str(payload.get("content_hash")),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
        )


@dataclass(frozen=True, slots=True)
class RuntimeMetadata:
    """Publication metadata. created_at must not feed natal calculation."""

    contract_version: str = SCHEMA_RUNTIME_CONTRACT
    schema_version: str = SCHEMA_RESULT
    ruleset_version: str = SCHEMA_RULES
    composer_version: str = SCHEMA_COMPOSER
    analysis_id: str = ""
    created_at: str = ""
    locale: str = DEFAULT_LOCALE
    requested_layers: tuple[str, ...] = ()
    confidence_summary: str = ""
    source_versions: dict[str, str] = field(default_factory=dict)
    content_hash: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> RuntimeMetadata:
        """Rebuild metadata from a mapping."""
        payload = data or {}
        return cls(
            contract_version=as_str(payload.get("contract_version"), SCHEMA_RUNTIME_CONTRACT),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_RESULT),
            ruleset_version=as_str(payload.get("ruleset_version"), SCHEMA_RULES),
            composer_version=as_str(payload.get("composer_version"), SCHEMA_COMPOSER),
            analysis_id=as_str(payload.get("analysis_id")),
            created_at=as_str(payload.get("created_at")),
            locale=as_str(payload.get("locale"), DEFAULT_LOCALE),
            requested_layers=as_str_tuple(payload.get("requested_layers")),
            confidence_summary=as_str(payload.get("confidence_summary")),
            source_versions=as_str_dict(payload.get("source_versions")),
            content_hash=as_str(payload.get("content_hash")),
        )
