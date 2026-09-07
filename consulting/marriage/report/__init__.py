"""Report package."""

from __future__ import annotations

from consulting.marriage.report.contract import (
    MarriageReportProfile,
    MarriageReportProfileDescriptor,
)
from consulting.marriage.report.placeholder import PlaceholderMarriageReportProfile
from consulting.marriage.report.profile import MarriageReportProfileV1

__all__ = [
    "MarriageReportProfile",
    "MarriageReportProfileDescriptor",
    "MarriageReportProfileV1",
    "PlaceholderMarriageReportProfile",
]
