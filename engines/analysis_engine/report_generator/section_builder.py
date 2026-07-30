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
        section_order: tuple[str, ...] | None = None,
    ) -> tuple[ReportSection, ...]:
        """Bind interpretation sections in published or template order."""
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

        by_id = {section.section_id: section for section in interpretation.sections}
        ordered_ids: list[str]
        if section_order:
            ordered_ids = [section_id for section_id in section_order if section_id in by_id]
            for section_id in by_id:
                if section_id not in ordered_ids:
                    ordered_ids.append(section_id)
        else:
            ordered_ids = [section.section_id for section in interpretation.sections]

        sections: list[ReportSection] = []
        for order, section_id in enumerate(ordered_ids):
            section = by_id[section_id]
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
