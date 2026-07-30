"""Section Builder — bind InterpretationResult sections into ReportSection."""

from __future__ import annotations

from engines.analysis_engine.interpretation_engine.models import InterpretationResult
from engines.analysis_engine.report_generator.exceptions import ReportBindingError
from engines.analysis_engine.report_generator.models import FormatProfile, ReportSection


class SectionBuilder:
    """Map published interpretation sections into presentation sections.

    Does not rewrite or regenerate narrative text.
    """

    def build(
        self,
        interpretation: InterpretationResult,
        *,
        profile: FormatProfile,
    ) -> tuple[ReportSection, ...]:
        """Bind interpretation sections in published order."""
        if not interpretation.sections:
            raise ReportBindingError(
                "InterpretationResult has no sections to bind",
            )

        present = {section.section_id for section in interpretation.sections}
        missing = [
            section_id
            for section_id in profile.mandatory_sections
            if section_id not in present
        ]
        if missing:
            raise ReportBindingError(
                "Mandatory interpreted sections missing",
                details={"missing": missing},
            )

        sections: list[ReportSection] = []
        for order, section in enumerate(interpretation.sections):
            body = section.body.strip()
            if not body:
                raise ReportBindingError(
                    "Interpretation section body is empty",
                    details={"section_id": section.section_id},
                )
            sections.append(
                ReportSection(
                    section_id=section.section_id,
                    title=section.title or section.section_id,
                    body=body,
                    order=order,
                    source_sentence_ids=tuple(section.sentence_ids),
                    source_stages=tuple(section.source_stages),
                    trace={
                        "request_id": interpretation.request_id,
                        "knowledge_version": interpretation.knowledge_version,
                    },
                )
            )
        return tuple(sections)
