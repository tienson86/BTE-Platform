"""Report profile placeholder. No report rendering in TV1-B01."""

from __future__ import annotations

from consulting.marriage.report.contract import (
    MarriageReportProfile,
    MarriageReportProfileDescriptor,
)


class PlaceholderMarriageReportProfile(MarriageReportProfile):
    """Skeleton placeholder. Does not implement Report Profile content."""

    def descriptor(self) -> MarriageReportProfileDescriptor:
        """Refuse report profile resolution."""
        raise NotImplementedError("TV1-B01: report profile is not implemented")
