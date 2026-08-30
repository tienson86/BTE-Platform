"""Canonical consulting style profile. Language only. No UI."""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_PROFILE_ID = "consultant.customer.vi.v1"


@dataclass(frozen=True, slots=True)
class ConsultingStyleProfile:
    """Spoken-register profile. Not a visual theme."""

    profile_id: str
    locale: str
    audience: str
    address: str
    voice: str
    tone: str
    register: str
    certainty: str
    mysticism: str
    technical_density: str
    sales_pressure: str


def default_profile() -> ConsultingStyleProfile:
    """Return the canonical customer Vietnamese consulting profile."""
    return ConsultingStyleProfile(
        profile_id=DEFAULT_PROFILE_ID,
        locale="vi",
        audience="customer",
        address="Bạn",
        voice="professional",
        tone="calm",
        register="natural_consulting",
        certainty="evidence_bounded",
        mysticism="low",
        technical_density="low",
        sales_pressure="none",
    )
