"""Canonical Runtime adapter. Invokes existing OrchestratorService. Read-only."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Protocol

from consulting.marriage.adapters.contract import CanonicalAnalysis, CanonicalRuntimeAdapter
from consulting.marriage.dto.request import CanonicalBirthInput, MarriagePersonInput
from consulting.marriage.exceptions import MarriageCanonicalAnalysisError
from consulting.marriage.models.enums import PersonSide
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot
from consulting.marriage.runtime.phase import CANONICAL_STOP_STAGE, DEFAULT_CANONICAL_TIMEZONE
from consulting.marriage.runtime.snapshot_builder import build_marriage_snapshot


class CanonicalRuntimeRunner(Protocol):
    """Port to Canonical Runtime. Implemented by OrchestratorService."""

    def run_person(
        self,
        *,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        gender: str,
        timezone: str,
    ) -> Mapping[str, Any]:
        """Run Canonical analysis for one person and return the payload."""


class OrchestratorServiceRunner:
    """Default runner. Delegates to Canonical OrchestratorService."""

    def __init__(self, service: Any | None = None) -> None:
        self._service = service

    def run_person(
        self,
        *,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        gender: str,
        timezone: str,
    ) -> Mapping[str, Any]:
        """Invoke Canonical runtime through luck. Does not run Marriage Decision."""
        service = self._service
        if service is None:
            from applications.api.services.orchestrator import OrchestratorService

            service = OrchestratorService()
            self._service = service
        try:
            payload = service.run_stage(
                CANONICAL_STOP_STAGE,
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                gender=gender,
                timezone=timezone,
            )
        except Exception as exc:
            raise MarriageCanonicalAnalysisError("canonical_analysis_failed") from exc
        if not isinstance(payload, Mapping):
            raise MarriageCanonicalAnalysisError("canonical_payload_invalid")
        return payload


class CanonicalOrchestratorAdapter(CanonicalRuntimeAdapter):
    """TV-01 adapter over Canonical Runtime. Does not write Canonical Truth."""

    def __init__(self, runner: CanonicalRuntimeRunner | None = None) -> None:
        self._runner = runner or OrchestratorServiceRunner()

    def analyze(self, birth_input: MarriagePersonInput) -> CanonicalAnalysis:
        """Run Canonical analysis for one person."""
        return self.analyze_normalized(_to_canonical_birth(birth_input))

    def analyze_normalized(self, birth_input: CanonicalBirthInput) -> CanonicalAnalysis:
        """Run Canonical analysis from a normalized birth input."""
        year, month, day = _parse_date(birth_input.birth_date)
        hour, minute, hour_known = _parse_time(birth_input.birth_time)
        timezone = birth_input.timezone or DEFAULT_CANONICAL_TIMEZONE
        payload = self._runner.run_person(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            gender=birth_input.gender.value,
            timezone=timezone,
        )
        return {
            "canonical": payload,
            "hour_known": hour_known,
            "timezone_resolved": birth_input.timezone is not None,
        }

    def to_snapshot(self, analysis: CanonicalAnalysis) -> MarriageCanonicalSnapshot:
        """Bind a snapshot. Prefer build_marriage_snapshot from the pipeline."""
        raise NotImplementedError(
            "TV1-B02: snapshots are built by MarriageSnapshotBuilder, not the adapter directly"
        )


def build_person_analysis(
    adapter: CanonicalOrchestratorAdapter,
    person: CanonicalBirthInput,
    *,
    analysis_id: str,
    side: PersonSide,
) -> CanonicalAnalysis:
    """Run Canonical analysis and stamp TV-01 envelope metadata."""
    envelope = dict(adapter.analyze_normalized(person))
    envelope["analysis_id"] = analysis_id
    envelope["person"] = side.value
    return envelope


def _to_canonical_birth(person: MarriagePersonInput) -> CanonicalBirthInput:
    """Copy person input into the normalized birth shape."""
    return CanonicalBirthInput(
        gender=person.gender,
        birth_date=person.birth_date,
        full_name=person.full_name,
        birth_time=person.birth_time,
        birth_place=person.birth_place,
        timezone=person.timezone,
    )


def _parse_date(value: str) -> tuple[int, int, int]:
    """Parse YYYY-MM-DD into year, month, day."""
    parsed = datetime.strptime(value, "%Y-%m-%d")
    return parsed.year, parsed.month, parsed.day


def _parse_time(value: str | None) -> tuple[int, int, bool]:
    """Parse HH:mm[:ss]. Unknown time is not treated as a known hour in snapshots."""
    if value is None:
        return 0, 0, False
    parts = value.split(":")
    hour = int(parts[0])
    minute = int(parts[1]) if len(parts) > 1 else 0
    return hour, minute, True
