"""B02 request and Canonical-contract validation. No evidence or decision rules."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from consulting.marriage.adapters.contract import CanonicalAnalysis
from consulting.marriage.dto.request import (
    MarriageConsultationOptions,
    MarriageConsultationRequest,
    MarriagePersonInput,
)
from consulting.marriage.exceptions import MarriageCanonicalContractError, MarriageValidationError
from consulting.marriage.models.evidence import MarriageEvidence
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.validation.contract import MarriageValidationContract

_REQUIRED_BAZI_FIELDS = (
    "year_pillar",
    "month_pillar",
    "day_pillar",
    "day_master",
    "day_master_element",
    "day_master_yin_yang",
)


class MarriageRuntimeValidation(MarriageValidationContract):
    """Runtime validation for TV1-B02. Evidence and decision remain unimplemented."""

    def validate_request(self, request: MarriageConsultationRequest) -> None:
        """Validate person A/B identity, gender, and birth formats. No gender default."""
        if request.person_a is None or request.person_b is None:
            raise MarriageValidationError("person_required")
        _validate_person(request.person_a, "person_a")
        _validate_person(request.person_b, "person_b")
        _validate_options(request.options)

    def validate_canonical_contract(
        self,
        analysis_a: CanonicalAnalysis,
        analysis_b: CanonicalAnalysis,
    ) -> None:
        """Confirm Canonical payloads expose required Truth fields before snapshot."""
        _validate_analysis(analysis_a, "A")
        _validate_analysis(analysis_b, "B")

    def validate_evidence(self, evidence: list[MarriageEvidence]) -> None:
        """Refuse evidence validation. Evidence belongs to a later phase."""
        raise NotImplementedError("TV1-B02: evidence validation is not implemented")

    def validate_decision(self, result: MarriageDecisionResult) -> None:
        """Refuse decision validation. Decision belongs to a later phase."""
        raise NotImplementedError("TV1-B02: decision validation is not implemented")


def _validate_person(person: MarriagePersonInput, label: str) -> None:
    """Validate one person input."""
    if person.gender is None:
        raise MarriageValidationError(f"{label}_gender_required")
    if not person.birth_date:
        raise MarriageValidationError(f"{label}_birth_date_required")
    try:
        datetime.strptime(person.birth_date, "%Y-%m-%d")
    except ValueError as exc:
        raise MarriageValidationError(f"{label}_birth_date_invalid") from exc
    if person.birth_time is not None:
        _validate_time(person.birth_time, label)
    if person.birth_place is not None:
        place = person.birth_place
        if place.latitude is not None and not (-90.0 <= place.latitude <= 90.0):
            raise MarriageValidationError(f"{label}_birth_place_invalid")
        if place.longitude is not None and not (-180.0 <= place.longitude <= 180.0):
            raise MarriageValidationError(f"{label}_birth_place_invalid")


def _validate_time(value: str, label: str) -> None:
    """Validate HH:mm or HH:mm:ss."""
    for pattern in ("%H:%M", "%H:%M:%S"):
        try:
            datetime.strptime(value, pattern)
            return
        except ValueError:
            continue
    raise MarriageValidationError(f"{label}_birth_time_invalid")


def _validate_options(options: MarriageConsultationOptions | None) -> None:
    """Validate optional luck window bounds."""
    if options is None or options.luck_window is None:
        return
    window = options.luck_window
    if window.start_year > window.end_year:
        raise MarriageValidationError("luck_window_invalid")


def _validate_analysis(analysis: CanonicalAnalysis, side: str) -> None:
    """Require Canonical Truth fields used by the snapshot builder."""
    payload: Mapping[str, Any]
    nested = analysis.get("canonical")
    if isinstance(nested, Mapping):
        payload = nested
    elif "bazi" in analysis:
        payload = analysis
    else:
        raise MarriageCanonicalContractError(f"canonical_payload_missing:{side}")
    bazi = payload.get("bazi")
    if not isinstance(bazi, Mapping):
        raise MarriageCanonicalContractError(f"canonical_bazi_missing:{side}")
    for field_name in _REQUIRED_BAZI_FIELDS:
        if not bazi.get(field_name):
            raise MarriageCanonicalContractError(f"canonical_{field_name}_missing:{side}")
    if not payload.get("strength"):
        raise MarriageCanonicalContractError(f"canonical_strength_missing:{side}")
    if not payload.get("useful_god"):
        raise MarriageCanonicalContractError(f"canonical_useful_god_missing:{side}")
