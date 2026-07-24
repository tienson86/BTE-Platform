"""License application service."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from applications.edition.editions import Edition
from applications.features.flags import Feature, features_for_edition
from applications.license.activation import ActivationError, LicenseActivation
from applications.license.generator import generate_license
from applications.license.machine_id import get_machine_id
from applications.license.models import LicenseModel
from applications.license.repository import LicenseRepository
from applications.license.validator import LicenseValidator, ValidationResult


class LicenseService:
    """High-level license operations for Applications Layer."""

    def __init__(
        self,
        repository: LicenseRepository,
        *,
        validator: LicenseValidator | None = None,
    ) -> None:
        self.repository = repository
        self.validator = validator or LicenseValidator()
        self.activation = LicenseActivation(repository, validator=self.validator)

    @classmethod
    def from_data_dir(cls, data_dir: Path | str) -> LicenseService:
        """Create service with JSON store under ``data_dir/licenses.json``."""
        root = Path(data_dir)
        root.mkdir(parents=True, exist_ok=True)
        return cls(LicenseRepository(root / "licenses.json"))

    def issue(
        self,
        *,
        edition: Edition | str,
        customer: str,
        organization: str = "",
        days_valid: int | None = 365,
        max_users: int | None = None,
        max_cases: int | None = None,
        enabled_features: list[str] | None = None,
    ) -> LicenseModel:
        """Generate and persist a license (offline)."""
        license_obj = generate_license(
            edition=edition,
            customer=customer,
            organization=organization,
            days_valid=days_valid,
            max_users=max_users,
            max_cases=max_cases,
            enabled_features=enabled_features,
        )
        return self.repository.save(license_obj)

    def activate(self, license_key: str) -> LicenseModel:
        """Activate a license on this machine."""
        license_obj, _ = self.activation.activate(license_key)
        return license_obj

    def status(self) -> dict[str, Any]:
        """Return active license status snapshot."""
        active = self.repository.get_active()
        validation = self.validator.validate(active)
        return {
            "machine_id": get_machine_id(),
            "has_license": active is not None,
            "license": active.to_dict() if active else None,
            "validation": validation.to_dict(),
        }

    def validate(
        self,
        *,
        license_key: str | None = None,
        feature: str | None = None,
        current_users: int | None = None,
        current_cases: int | None = None,
    ) -> ValidationResult:
        """Validate active license or a specific key."""
        if license_key:
            license_obj = self.repository.get(license_key)
        else:
            license_obj = self.repository.get_active()
        feature_enum: Feature | None = None
        if feature:
            feature_enum = Feature(feature)
        return self.validator.validate(
            license_obj,
            feature=feature_enum,
            current_users=current_users,
            current_cases=current_cases,
        )

    def features(self) -> dict[str, Any]:
        """List features for the active license (or community defaults)."""
        active = self.repository.get_active()
        if active is None:
            edition = Edition.COMMUNITY
            enabled = sorted(f.value for f in features_for_edition(edition))
            return {
                "edition": edition.value,
                "features": enabled,
                "licensed": False,
            }
        enabled = list(active.enabled_features) or sorted(
            f.value for f in features_for_edition(active.edition)
        )
        return {
            "edition": active.edition,
            "features": enabled,
            "licensed": True,
            "license_key": active.license_key,
        }
