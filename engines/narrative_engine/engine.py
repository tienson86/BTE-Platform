"""
BTE Narrative Engine (WP7)

InterpretationResult + ReportModel
      ↓
Paragraph Builder
Transition Generator
Redundancy Reducer
Contradiction Checker
Tone Controller
      ↓
NarrativeReport → HTML / Markdown / PDF

No LLM. Knowledge = Sentence Library + Report templates (via ReportModel) + Rules (via Interpretation).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from engines.base.base_engine import BaseEngine
from engines.base.context import EngineContext
from engines.base.result import EngineResult

from .models import NarrativeReport
from .service import NarrativeService


class NarrativeEngine(BaseEngine):
    """Narrative Engine — polish Interpretation + Report into cohesive prose."""

    name = "NarrativeEngine"
    version = "1.0.0"
    stage = "narrative"
    description = "Compose narrative from InterpretationResult and ReportModel."

    def __init__(
        self,
        sentence_library_root: str | Path | None = None,
    ) -> None:
        super().__init__()
        self.service = NarrativeService(sentence_library_root)

    def compose(
        self,
        interpretation: Any,
        report: Any,
        *,
        pdf_output: str | Path | None = None,
        target_tone: str | None = None,
    ) -> NarrativeReport:
        """Public WP7 entry: build NarrativeReport with HTML/MD/PDF."""
        return self.service.compose(
            interpretation,
            report,
            pdf_output=pdf_output,
            target_tone=target_tone,
        )

    def validate(self, context: EngineContext) -> None:
        """Require interpretation and report payloads."""
        if context.get("interpretation") is None:
            raise ValueError("InterpretationResult not found.")
        if context.get("report") is None:
            raise ValueError("ReportModel not found.")

    def run(self, context: EngineContext) -> EngineResult:
        """Pipeline-compatible run."""
        interpretation = context.get("interpretation")
        report = context.get("report")
        pdf_output = context.get("narrative_pdf_output") or context.get("pdf_output")
        target_tone = context.get("narrative_tone")
        narrative = self.compose(
            interpretation,
            report,
            pdf_output=pdf_output,
            target_tone=target_tone,
        )
        context.set("narrative", narrative)
        context.set("narrative_html", narrative.html)
        context.set("narrative_markdown", narrative.markdown)
        context.set("narrative_pdf", narrative.pdf_path)
        return EngineResult(
            success=True,
            data=narrative,
            message="Narrative composed successfully.",
        )
