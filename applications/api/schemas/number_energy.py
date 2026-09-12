"""Request and public-data schemas for Number Energy API V1."""

from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from engines.number_energy.constants import (
    MAX_INPUT_DIGITS,
    is_ascii_digit_string,
)

ALPHANUMERIC_CONTEXTS = {"car_plate", "motorbike_plate", "id_number"}
PLATE_SEPARATORS_RE = re.compile(r"[.\s-]+")
PLATE_BODY_RE = re.compile(r"^[0-9A-Za-z]+$")

NumberEnergyPurposeContext = Literal[
    "phone_number",
    "car_plate",
    "motorbike_plate",
    "id_number",
    "bank_account",
    "house_number",
    "generic_number",
]


class NumberEnergyRequest(BaseModel):
    """Analyze a number or vehicle plate with a frozen V1 purpose context."""

    number: str = Field(
        ...,
        min_length=1,
        max_length=MAX_INPUT_DIGITS,
        examples=["141319"],
    )
    purpose_context: NumberEnergyPurposeContext = Field(
        default="generic_number",
        examples=["phone_number"],
    )

    @field_validator("number")
    @classmethod
    def normalize_raw(cls, value: str) -> str:
        """Trim raw input before purpose-specific validation."""
        raw = value.strip()
        if not raw:
            raise ValueError("number input must not be empty")
        if len(raw) > MAX_INPUT_DIGITS:
            raise ValueError(
                f"number input must not exceed {MAX_INPUT_DIGITS} digits"
            )
        return raw

    @model_validator(mode="after")
    def validate_number_for_purpose(self) -> "NumberEnergyRequest":
        """Allow A-Z vehicle plates/passports; keep other contexts digit-only."""
        if self.purpose_context in ALPHANUMERIC_CONTEXTS:
            compact = PLATE_SEPARATORS_RE.sub("", self.number)
            if (
                not compact
                or not compact.isascii()
                or PLATE_BODY_RE.fullmatch(compact) is None
            ):
                raise ValueError(
                    "input must contain ASCII letters A-Z, digits 0-9, and separators only"
                )
            return self
        if not is_ascii_digit_string(self.number):
            raise ValueError("number input must contain digits 0-9 only")
        return self


class NumberEnergyDataOut(BaseModel):
    """Stable public payload the Customer Portal is allowed to render."""

    model_config = ConfigDict(extra="allow")

    occurrences: list[dict[str, Any]]
    sequence_state: str
    patterns: list[str]
    narrative: dict[str, Any]
    warnings: list[dict[str, Any]]
    metadata: dict[str, Any]
    reading: dict[str, Any] = Field(default_factory=dict)
    pair_occurrences: list[dict[str, Any]] = Field(default_factory=list)
    pair_summary: dict[str, Any] | None = None
    energy_distribution: list[dict[str, Any]] = Field(default_factory=list)
    triple_occurrences: list[dict[str, Any]] = Field(default_factory=list)
    chain: dict[str, Any] | None = None
    wealth_nodes: list[dict[str, Any]] = Field(default_factory=list)
    wealth_flow: dict[str, Any] | None = None
    later_outcome: dict[str, Any] | None = None
    wealth_story: dict[str, Any] | None = None
    domain_insights: list[dict[str, Any]] = Field(default_factory=list)
    strengths: list[dict[str, Any]] = Field(default_factory=list)
    cautions: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    assessment: dict[str, Any] | None = None
    recommendation: dict[str, Any] | None = None
    score: dict[str, Any] | None = None
    grade: str | None = None
    verified_by_runtime: bool = False
