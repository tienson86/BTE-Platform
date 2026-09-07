"""Report package."""

from __future__ import annotations

from consulting.marriage.report.contract import (
    MarriageReportProfile,
    MarriageReportProfileDescriptor,
)
from consulting.marriage.report.placeholder import PlaceholderMarriageReportProfile

__all__ = [
    "MarriageReportProfile",
    "MarriageReportProfileDescriptor",
    "PlaceholderMarriageReportProfile",
]
