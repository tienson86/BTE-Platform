"""License validation rules (offline)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from applications.edition.editions import Edition
from applications.features.flags import Feature, is_feature_enabled
from applications.license.models import LicenseModel


@dataclass(slots=True)
class ValidationResult:
    """Outcome of a license validation."""

    valid: bool
    reason: str = "ok"
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize result."""
        return {
            "valid": self.valid,
            "reason": self.reason,
            "details": self.details,
        }


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


class LicenseValidator:
    """Validate expiration, edition, features, and usage limits."""

    def validate(
        self,
        license_obj: LicenseModel | None,
        *,
        feature: Feature | str | None = None,
        current_users: int | None = None,
        current_cases: int | None = None,
        now: datetime | None = None,
    ) -> ValidationResult:
        """Run validation checks against a license."""
        if license_obj is None:
            return ValidationResult(False, "no_license")

        if license_obj.status == "revoked":
            return ValidationResult(False, "revoked")

        if license_obj.status not in {"issued", "active", "expired"}:
            return ValidationResult(False, "invalid_status")

        try:
            Edition(license_obj.edition)
        except ValueError:
            return ValidationResult(False, "invalid_edition")

        moment = now or datetime.now(timezone.utc)
        expires = _parse_dt(license_obj.expires_at)
        if expires is not None and moment > expires:
            return ValidationResult(
                False,
                "expired",
                {"expires_at": license_obj.expires_at},
            )

        if feature is not None:
            allowed = is_feature_enabled(
                license_obj.edition,
                feature,
                enabled_features=license_obj.enabled_features,
            )
            if not allowed:
                return ValidationResult(
                    False,
                    "feature_disabled",
                    {"feature": str(feature)},
                )

        if current_users is not None and current_users > license_obj.max_users:
            return ValidationResult(
                False,
                "max_users_exceeded",
                {
                    "current_users": current_users,
                    "max_users": license_obj.max_users,
                },
            )

        if current_cases is not None and current_cases > license_obj.max_cases:
            return ValidationResult(
                False,
                "max_cases_exceeded",
                {
                    "current_cases": current_cases,
                    "max_cases": license_obj.max_cases,
                },
            )

        return ValidationResult(
            True,
            "ok",
            {
                "edition": license_obj.edition,
                "status": license_obj.status,
                "expires_at": license_obj.expires_at,
            },
        )
