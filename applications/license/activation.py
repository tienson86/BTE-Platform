"""Offline license activation."""

from __future__ import annotations

from datetime import datetime, timezone

from applications.license.machine_id import get_machine_id
from applications.license.models import LicenseModel
from applications.license.repository import LicenseRepository
from applications.license.validator import LicenseValidator, ValidationResult


class ActivationError(ValueError):
    """License activation failed."""


class LicenseActivation:
    """Activate a license key on this machine (offline)."""

    def __init__(
        self,
        repository: LicenseRepository,
        *,
        validator: LicenseValidator | None = None,
    ) -> None:
        self.repository = repository
        self.validator = validator or LicenseValidator()

    def activate(
        self,
        license_key: str,
        *,
        machine_id: str | None = None,
    ) -> tuple[LicenseModel, ValidationResult]:
        """
        Activate ``license_key`` locally.

        Deactivates other active licenses (single active license model).
        """
        license_obj = self.repository.get(license_key)
        if license_obj is None:
            raise ActivationError(f"Unknown license key: {license_key}")

        result = self.validator.validate(license_obj)
        if not result.valid and result.reason == "expired":
            license_obj.status = "expired"
            self.repository.save(license_obj)
            raise ActivationError("License expired")
        if not result.valid and result.reason == "revoked":
            raise ActivationError("License revoked")

        mid = machine_id or get_machine_id()
        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

        # Single active license: demote previous actives.
        for existing in self.repository.list():
            if existing.status == "active" and existing.license_key != license_key:
                existing.status = "issued"
                self.repository.save(existing)

        license_obj.status = "active"
        license_obj.machine_id = mid
        license_obj.activated_at = now
        self.repository.save(license_obj)
        return license_obj, self.validator.validate(license_obj)
