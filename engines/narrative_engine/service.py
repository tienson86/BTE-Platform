"""Public service API for Narrative Engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import NarrativeReport
from .pipeline import NarrativePipeline


class NarrativeService:
    """Facade: InterpretationResult + ReportModel → NarrativeReport."""

    def __init__(
        self,
        sentence_library_root: str | Path | None = None,
    ) -> None:
        self.pipeline = NarrativePipeline(sentence_library_root)

    def compose(
        self,
        interpretation: Any,
        report: Any,
        *,
        pdf_output: str | Path | None = None,
        target_tone: str | None = None,
    ) -> NarrativeReport:
        """Compose polished narrative report."""
        return self.pipeline.run(
            interpretation,
            report,
            pdf_output=pdf_output,
            target_tone=target_tone,
        )

    def to_html(self, narrative: NarrativeReport) -> str:
        """HTML export."""
        return narrative.html or self.pipeline.formatter.to_html(narrative)

    def to_markdown(self, narrative: NarrativeReport) -> str:
        """Markdown export."""
        return narrative.markdown or self.pipeline.formatter.to_markdown(narrative)

    def to_pdf(self, narrative: NarrativeReport, output: str | Path) -> Path:
        """PDF export."""
        return self.pipeline.formatter.to_pdf(narrative, output)
