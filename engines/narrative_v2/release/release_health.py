"""ReleaseHealth model and per-surface assessment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.narrative_v2.certification.certification_result import STATUS_CERTIFIED
from engines.narrative_v2.export.export_errors import IncompatiblePresentationVersion
from engines.narrative_v2.export.export_serializer import presentation_from_mapping
from engines.narrative_v2.presentation.presentation_errors import PresentationValidationError
from engines.narrative_v2.presentation.presentation_model import NarrativeV2Presentation
from engines.narrative_v2.presentation.presentation_status import PRESENTATION_VERSION
from engines.narrative_v2.presentation.presentation_validator import PresentationValidator
from engines.narrative_v2.release.release_events import utc_now

HEALTH_PASS = "PASS"
HEALTH_WARNING = "WARNING"
HEALTH_FAIL = "FAIL"
HEALTH_UNKNOWN = "UNKNOWN"

ALLOWED_HEALTH: frozenset[str] = frozenset(
    {HEALTH_PASS, HEALTH_WARNING, HEALTH_FAIL, HEALTH_UNKNOWN}
)

CERTIFIED_PASS = STATUS_CERTIFIED


@dataclass(frozen=True, slots=True)
class ReleaseHealth:
    """Dual-run health snapshot. No personal data."""

    runtime_status: str
    presentation_status: str
    portal_status: str
    export_status: str
    provider: str
    fallback_count: int
    parity_status: str
    golden_status: str
    certification_status: str
    timestamp: str

    def overall(self) -> str:
        """Aggregate health. FAIL wins, then WARNING, then PASS."""
        surfaces = (
            self.runtime_status,
            self.presentation_status,
            self.portal_status,
            self.export_status,
            self.parity_status,
            self.golden_status,
            self.certification_status,
        )
        if HEALTH_FAIL in surfaces:
            return HEALTH_FAIL
        if self.fallback_count > 0 or HEALTH_WARNING in surfaces:
            return HEALTH_WARNING
        if all(item == HEALTH_PASS for item in surfaces):
            return HEALTH_PASS
        return HEALTH_UNKNOWN

    def to_record(self) -> dict[str, Any]:
        """JSON-safe snapshot including overall."""
        return {
            "runtime_status": self.runtime_status,
            "presentation_status": self.presentation_status,
            "portal_status": self.portal_status,
            "export_status": self.export_status,
            "provider": self.provider,
            "fallback_count": self.fallback_count,
            "parity_status": self.parity_status,
            "golden_status": self.golden_status,
            "certification_status": self.certification_status,
            "timestamp": self.timestamp,
            "overall": self.overall(),
        }


def assess_runtime(runtime_ok: bool | None) -> str:
    """Runtime generation health."""
    if runtime_ok is None:
        return HEALTH_UNKNOWN
    return HEALTH_PASS if runtime_ok else HEALTH_FAIL


def assess_presentation(presentation: NarrativeV2Presentation | Mapping[str, Any] | None) -> str:
    """Presentation version and public-contract health."""
    if presentation is None:
        return HEALTH_FAIL
    try:
        model = _as_presentation(presentation)
    except (IncompatiblePresentationVersion, PresentationValidationError, TypeError, ValueError):
        return HEALTH_FAIL
    if model.metadata.version != PRESENTATION_VERSION:
        return HEALTH_FAIL
    try:
        PresentationValidator().validate(model)
    except PresentationValidationError:
        return HEALTH_FAIL
    return HEALTH_PASS


def assess_portal(*, provider: str, selected: str, fallback: bool) -> str:
    """Portal render health. Fallback is WARNING, not a customer interrupt."""
    if selected not in {"pack05", "v2"}:
        return HEALTH_FAIL
    if fallback:
        return HEALTH_WARNING
    if provider in {"v2", "auto"} and selected == "v2":
        return HEALTH_PASS
    if provider == "pack05" and selected == "pack05":
        return HEALTH_PASS
    return HEALTH_WARNING


def assess_export(parity_matched: bool | None) -> str:
    """Export consumer health follows content-hash parity."""
    if parity_matched is None:
        return HEALTH_UNKNOWN
    return HEALTH_PASS if parity_matched else HEALTH_FAIL


def assess_golden(matched: bool | None) -> str:
    """Golden regression health."""
    if matched is None:
        return HEALTH_UNKNOWN
    return HEALTH_PASS if matched else HEALTH_FAIL


def assess_certification(status: str | None) -> str:
    """Certification gate health for the observed case."""
    if not status:
        return HEALTH_UNKNOWN
    if status == CERTIFIED_PASS:
        return HEALTH_PASS
    if status in {"REJECTED", "REVOKED"}:
        return HEALTH_FAIL
    if status in {"REVIEW", "DRAFT"}:
        return HEALTH_WARNING
    return HEALTH_UNKNOWN


def build_health(
    *,
    runtime_status: str,
    presentation_status: str,
    portal_status: str,
    export_status: str,
    provider: str,
    fallback_count: int,
    parity_status: str,
    golden_status: str,
    certification_status: str,
    timestamp: str | None = None,
) -> ReleaseHealth:
    """Assemble a health snapshot."""
    return ReleaseHealth(
        runtime_status=_clamp(runtime_status),
        presentation_status=_clamp(presentation_status),
        portal_status=_clamp(portal_status),
        export_status=_clamp(export_status),
        provider=provider,
        fallback_count=max(0, fallback_count),
        parity_status=_clamp(parity_status),
        golden_status=_clamp(golden_status),
        certification_status=_clamp(certification_status),
        timestamp=timestamp or utc_now(),
    )


def _as_presentation(
    presentation: NarrativeV2Presentation | Mapping[str, Any],
) -> NarrativeV2Presentation:
    if isinstance(presentation, NarrativeV2Presentation):
        return presentation
    return presentation_from_mapping(presentation)


def _clamp(value: str) -> str:
    return value if value in ALLOWED_HEALTH else HEALTH_UNKNOWN
