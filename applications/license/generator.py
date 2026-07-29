"""Offline license key generator (no external server)."""

from __future__ import annotations

from applications.edition.editions import Edition
from applications.license.models import LicenseModel


def generate_license(
    *,
    edition: Edition | str,
    customer: str,
    organization: str = "",
    days_valid: int | None = 365,
    max_users: int | None = None,
    max_cases: int | None = None,
    enabled_features: list[str] | None = None,
) -> LicenseModel:
    """Generate a new offline license record."""
    return LicenseModel.create(
        edition=edition,
        customer=customer,
        organization=organization,
        days_valid=days_valid,
        max_users=max_users,
        max_cases=max_cases,
        enabled_features=enabled_features,
    )
