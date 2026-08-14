"""Interpretation readiness matrix — data readiness only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.builders.interpretation_facts_builder import (
    InterpretationFactsBundle,
)
from engines.interpretation_engine.foundation.status import DataAvailability, ReadinessLevel


@dataclass(frozen=True, slots=True)
class InterpretationReadiness:
    """Runtime completeness matrix for domain interpretation."""

    strength: ReadinessLevel
    pattern: ReadinessLevel
    useful_god: ReadinessLevel
    ten_gods: ReadinessLevel
    shensha: ReadinessLevel
    luck: ReadinessLevel
    temperature: ReadinessLevel
    five_elements: ReadinessLevel
    reasons: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        """Serialize readiness matrix."""
        return {
            "interpretation_readiness": {
                "strength": self.strength.value,
                "pattern": self.pattern.value,
                "useful_god": self.useful_god.value,
                "ten_gods": self.ten_gods.value,
                "shensha": self.shensha.value,
                "luck": self.luck.value,
                "temperature": self.temperature.value,
                "five_elements": self.five_elements.value,
            },
            "reasons": dict(self.reasons),
        }


def evaluate_interpretation_readiness(facts: InterpretationFactsBundle) -> InterpretationReadiness:
    """Map domain fact status onto readiness levels."""
    reasons: dict[str, str] = {}
    return InterpretationReadiness(
        strength=_to_readiness(facts.strength.status, "strength", reasons),
        pattern=_to_readiness(facts.pattern.status, "pattern", reasons),
        useful_god=_to_readiness(facts.useful_god.status, "useful_god", reasons),
        ten_gods=_to_readiness(facts.ten_gods.status, "ten_gods", reasons),
        shensha=_to_readiness(facts.shensha.status, "shensha", reasons),
        luck=_to_readiness(facts.luck.status, "luck", reasons),
        temperature=_to_readiness(facts.temperature.status, "temperature", reasons),
        five_elements=_to_readiness(facts.five_elements.status, "five_elements", reasons),
        reasons=reasons,
    )


def _to_readiness(
    status: DataAvailability,
    domain: str,
    reasons: dict[str, str],
) -> ReadinessLevel:
    """Convert DataAvailability to ReadinessLevel."""
    if status == DataAvailability.AVAILABLE:
        return ReadinessLevel.READY
    if status == DataAvailability.PARTIAL:
        reasons[domain] = status.value
        return ReadinessLevel.PARTIAL
    if status in {DataAvailability.MISSING, DataAvailability.INVALID}:
        reasons[domain] = status.value
        return ReadinessLevel.MISSING
    if status == DataAvailability.NOT_IMPLEMENTED:
        reasons[domain] = status.value
        return ReadinessLevel.NOT_READY
    reasons[domain] = status.value
    return ReadinessLevel.PARTIAL
