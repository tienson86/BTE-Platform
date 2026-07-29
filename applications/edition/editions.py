"""Product edition definitions."""

from __future__ import annotations

from enum import Enum


class Edition(str, Enum):
    """BTE product editions (WP14)."""

    COMMUNITY = "COMMUNITY"
    STANDARD = "STANDARD"
    PROFESSIONAL = "PROFESSIONAL"
    ENTERPRISE = "ENTERPRISE"


# Soft limits used for validation when license omits explicit caps.
EDITION_DEFAULTS: dict[Edition, dict[str, int]] = {
    Edition.COMMUNITY: {"max_users": 1, "max_cases": 50},
    Edition.STANDARD: {"max_users": 5, "max_cases": 500},
    Edition.PROFESSIONAL: {"max_users": 25, "max_cases": 5_000},
    Edition.ENTERPRISE: {"max_users": 1_000, "max_cases": 1_000_000},
}
