"""WP7 Narrative pipeline orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .contradiction_checker import ContradictionChecker
from .formatter import NarrativeFormatter
from .models import NarrativeReport, utc_now
from .paragraph_builder import ParagraphBuilder
from .redundancy_reducer import RedundancyReducer, normalize_text
from .sentence_library_loader import SentenceLibraryLoader
from .source_collector import NarrativeSourceCollector
from .tone_controller import ToneController
from .transition_generator import TransitionGenerator


class NarrativePipeline:
    """
    InterpretationResult + ReportModel
          ↓
    collect → reduce → contradict → tone → paragraph → transition
          ↓
    NarrativeReport (+ HTML / Markdown / PDF)
    """

    def __init__(
        self,
        sentence_library_root: str | Path | None = None,
    ) -> None:
        self.loader = SentenceLibraryLoader(sentence_library_root)
        self.collector = NarrativeSourceCollector(self.loader)
        self.reducer = RedundancyReducer()
        self.contradictions = ContradictionChecker()
        self.tone = ToneController(self.loader)
        self.paragraphs = ParagraphBuilder()
        self.transitions = TransitionGenerator(self.loader)
        self.formatter = NarrativeFormatter()

    def run(
        self,
        interpretation: Any,
        report: Any,
        *,
        pdf_output: str | Path | None = None,
        target_tone: str | None = None,
    ) -> NarrativeReport:
        """Execute full WP7 narrative pipeline."""
        units = self.collector.collect(interpretation, report)
        input_count = len(units)

        units = self.reducer.reduce(units)
        units = self.contradictions.check(units)
        units = self.tone.apply(units, target_tone=target_tone)
        document_tone = self.tone.resolve_document_tone(units)

        paragraphs = self.paragraphs.build(units)
        paragraphs = self.transitions.apply(paragraphs)

        schema = self.loader.load_schema()
        title = str(schema.get("schema_name") or "BTE Narrative")
        # Prefer report metadata title when present
        if report is not None:
            metadata = getattr(report, "metadata", None)
            report_title = getattr(metadata, "title", None) if metadata is not None else None
            if not report_title and isinstance(report, dict):
                report_title = (report.get("metadata") or {}).get("title")
            if report_title:
                title = str(report_title)

        issues = [
            *self.reducer.issues,
            *self.contradictions.issues,
            *self.tone.issues,
            *self.transitions.issues,
        ]

        sections = [
            {
                "section_id": paragraph.section_id,
                "title": paragraph.section_title,
                "text": paragraph.text,
                "is_transition": paragraph.is_transition,
                "tone": paragraph.tone,
            }
            for paragraph in paragraphs
        ]

        narrative = NarrativeReport(
            title=title,
            paragraphs=paragraphs,
            sections=sections,
            tone=document_tone,
            issues_fixed=issues,
            metrics={
                "input_units": input_count,
                "output_paragraphs": len(paragraphs),
                "transitions": sum(1 for item in paragraphs if item.is_transition),
                "issues_fixed": len(issues),
                "duplicate_sentences": self._count_duplicate_paragraphs(paragraphs),
                "hard_same_section_transitions": self._count_hard_transitions(paragraphs),
                "success_no_duplicate_sentences": self._count_duplicate_paragraphs(paragraphs) == 0,
                "success_no_hard_transitions": self._count_hard_transitions(paragraphs) == 0,
            },
            generated_at=utc_now(),
        )

        narrative.markdown = self.formatter.to_markdown(narrative)
        narrative.html = self.formatter.to_html(narrative)
        target = Path(pdf_output) if pdf_output else Path("reports") / "wp7_narrative.pdf"
        narrative.pdf_path = str(self.formatter.to_pdf(narrative, target))
        return narrative

    @staticmethod
    def _count_duplicate_paragraphs(paragraphs: list[Any]) -> int:
        seen: set[str] = set()
        dups = 0
        for paragraph in paragraphs:
            if getattr(paragraph, "is_transition", False):
                continue
            key = normalize_text(str(getattr(paragraph, "text", "")))
            if not key:
                continue
            if key in seen:
                dups += 1
            else:
                seen.add(key)
        return dups

    @staticmethod
    def _count_hard_transitions(paragraphs: list[Any]) -> int:
        """Count transitions that bridge a section to itself."""
        hard = 0
        for paragraph in paragraphs:
            if not getattr(paragraph, "is_transition", False):
                continue
            section_id = str(getattr(paragraph, "section_id", ""))
            if "->" not in section_id:
                continue
            left, right = section_id.split("->", 1)
            left = left.replace("transition:", "")
            if left == right:
                hard += 1
        return hard
