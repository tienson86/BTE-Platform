"""TV-01 Marriage Report Profile v1. Semantic document only. No renderer."""

from __future__ import annotations

from consulting.marriage.models.narrative import MarriageNarrativeResult
from consulting.marriage.models.report import MarriageReportModel
from consulting.marriage.narrative.input import NarrativeInput
from consulting.marriage.report.composer import compose_report
from consulting.marriage.report.contract import MarriageReportProfile, MarriageReportProfileDescriptor
from consulting.marriage.report.versions import REPORT_PROFILE_ID, REPORT_PROFILE_VERSION


class MarriageReportProfileV1(MarriageReportProfile):
    """Customer-story profile for TV-01. Does not render PDF, DOCX, or HTML."""

    def descriptor(self) -> MarriageReportProfileDescriptor:
        """Return the bound report profile identity."""
        return MarriageReportProfileDescriptor(
            profile_id=REPORT_PROFILE_ID,
            version=REPORT_PROFILE_VERSION,
        )

    def compose(
        self,
        payload: NarrativeInput,
        narrative: MarriageNarrativeResult,
    ) -> MarriageReportModel:
        """Build the semantic report model from Narrative and Decision facts."""
        return compose_report(payload, narrative)
