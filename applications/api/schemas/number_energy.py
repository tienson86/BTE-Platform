"""Request and public-data schemas for Number Energy API V1."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from engines.number_energy.constants import (
    MAX_INPUT_DIGITS,
    is_ascii_digit_string,
)

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
    """Analyze a digit string with a frozen V1 purpose context."""

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
    def digits_only(cls, value: str) -> str:
        """Reject non-ASCII-digit input at the API boundary (repo 422 convention)."""
        raw = value.strip()
        if not is_ascii_digit_string(raw):
            raise ValueError("number input must contain digits 0-9 only")
        if len(raw) > MAX_INPUT_DIGITS:
            raise ValueError(
                f"number input must not exceed {MAX_INPUT_DIGITS} digits"
            )
        return raw


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
