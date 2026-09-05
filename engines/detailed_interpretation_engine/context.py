"""Pack 07 interpretation context (input contract only)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import DEFAULT_LOCALE, SCHEMA_CONTEXT
from engines.detailed_interpretation_engine.value_objects import (
    ChartIdentity,
    Mc01Reference,
    VersionBundle,
)


@dataclass(frozen=True, slots=True)
class InterpretationContext:
    """Frozen input identity for a Pack 07 analysis. No interpretation."""

    analysis_id: str = ""
    chart_id: str = ""
    mingju_result_id: str = ""
    mingju_content_hash: str = ""
    locale: str = DEFAULT_LOCALE
    requested_layers: tuple[str, ...] = ()
    time_windows: dict[str, str] = field(default_factory=dict)
    versions: VersionBundle = field(default_factory=VersionBundle)
    schema_version: str = SCHEMA_CONTEXT
    mc01: Mc01Reference = field(default_factory=Mc01Reference)
    pattern_ref: str = ""
    grade_ref: str = ""
    integrity_ref: str = ""
    strength_ref: str = ""
    useful_god_ref: str = ""
    temperature_ref: str = ""
    five_elements_ref: str = ""
    chart_identity: ChartIdentity = field(default_factory=ChartIdentity)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> InterpretationContext:
        """Rebuild context from a mapping."""
        payload = data or {}
        windows_raw = payload.get("time_windows")
        windows: dict[str, str] = {}
        if isinstance(windows_raw, Mapping):
            windows = {str(key): str(item) for key, item in windows_raw.items()}
        versions_raw = payload.get("versions")
        versions = (
            VersionBundle.from_dict(versions_raw)
            if isinstance(versions_raw, Mapping)
            else VersionBundle.from_dict(payload)
        )
        mc01_raw = payload.get("mc01")
        identity_raw = payload.get("chart_identity")
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            chart_id=as_str(payload.get("chart_id")),
            mingju_result_id=as_str(payload.get("mingju_result_id")),
            mingju_content_hash=as_str(payload.get("mingju_content_hash")),
            locale=as_str(payload.get("locale"), DEFAULT_LOCALE),
            requested_layers=as_str_tuple(payload.get("requested_layers")),
            time_windows=windows,
            versions=versions,
            schema_version=as_str(payload.get("schema_version"), SCHEMA_CONTEXT),
            mc01=Mc01Reference.from_dict(mc01_raw if isinstance(mc01_raw, Mapping) else None),
            pattern_ref=as_str(payload.get("pattern_ref")),
            grade_ref=as_str(payload.get("grade_ref")),
            integrity_ref=as_str(payload.get("integrity_ref")),
            strength_ref=as_str(payload.get("strength_ref")),
            useful_god_ref=as_str(payload.get("useful_god_ref")),
            temperature_ref=as_str(payload.get("temperature_ref")),
            five_elements_ref=as_str(payload.get("five_elements_ref")),
            chart_identity=ChartIdentity.from_dict(
                identity_raw if isinstance(identity_raw, Mapping) else None
            ),
        )


DetailedInterpretationContext = InterpretationContext
