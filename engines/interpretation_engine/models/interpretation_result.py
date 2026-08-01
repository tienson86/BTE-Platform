"""Interpretation result output model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.metadata import Metadata
from engines.interpretation_engine.models.section_result import SectionResult
from engines.interpretation_engine.models.trace_information import TraceInformation


@dataclass(frozen=True, slots=True)
class InterpretationResult:
    """Immutable top-level Pack 03 interpretation output model.

    Aggregates section results with metadata and trace.
    Does not render reports or narrative prose.
    """

    id: str
    metadata: Metadata
    trace: TraceInformation
    source_final_result_id: str
    pipeline_id: str
    success: bool
    sections: tuple[SectionResult, ...] = ()
    explanation_refs: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate interpretation result structural integrity."""
        if not self.id or not self.source_final_result_id or not self.pipeline_id:
            return False
        if not self.metadata.validate():
            return False
        if not self.trace.validate():
            return False
        if (
            self.trace.source_final_result_id
            and self.trace.source_final_result_id != self.source_final_result_id
        ):
            return False
        if self.trace.pipeline_id and self.trace.pipeline_id != self.pipeline_id:
            return False
        for section in self.sections:
            if not section.validate():
                return False
        return True

    def section_ids(self) -> tuple[str, ...]:
        """Return ordered section identifiers."""
        return tuple(section.id for section in self.sections)

    def section_for(self, section_id: str) -> SectionResult | None:
        """Return a section result by identifier."""
        for section in self.sections:
            if section.id == section_id:
                return section
        return None

    def sentence_ref_ids(self) -> tuple[str, ...]:
        """Return ordered sentence reference identifiers across all sections."""
        refs: list[str] = []
        for section in self.sections:
            refs.extend(section.sentence_ref_ids())
        return tuple(refs)
