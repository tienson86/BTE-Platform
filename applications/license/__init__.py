"""Licensing layer package."""

from applications.license.activation import ActivationError, LicenseActivation
from applications.license.generator import generate_license
from applications.license.machine_id import get_machine_id
from applications.license.models import LicenseModel
from applications.license.repository import LicenseRepository
from applications.license.service import LicenseService
from applications.license.validator import LicenseValidator, ValidationResult

__all__ = [
    "ActivationError",
    "LicenseActivation",
    "LicenseModel",
    "LicenseRepository",
    "LicenseService",
    "LicenseValidator",
    "ValidationResult",
    "generate_license",
    "get_machine_id",
]
