"""RE-1 Report Foundation exceptions."""

from __future__ import annotations


class ReportFoundationError(Exception):
    """Base error for Report Foundation failures."""


class ReportContractError(ReportFoundationError):
    """Raised when a report foundation contract is invalid."""


class ReportDuplicateIdError(ReportFoundationError):
    """Raised when a foundation identifier is published twice."""


class ReportVersionError(ReportFoundationError):
    """Raised when upstream or foundation versions are incompatible."""


class ReportContextIntegrityError(ReportFoundationError):
    """Raised when Report Context integrity checks fail."""


class ReportPackageNotReleasedError(ReportFoundationError):
    """Raised when a future Report Package is requested before release."""
