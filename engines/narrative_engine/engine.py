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
from .runtime import NarrativeRuntime, NarrativeTree, RuntimeInput
from .composer import NarrativeResult, NarrativeResultComposer
from .service import NarrativeService


class NarrativeEngine(BaseEngine):
    """Narrative Engine — WP7 prose path + Pack 05 D1 tree + D2 result composer."""

    name = "NarrativeEngine"
    version = "1.2.0"
    stage = "narrative"
    description = "Compose NarrativeTree (D1) and NarrativeResult (D2)."

    def __init__(
        self,
        sentence_library_root: str | Path | None = None,
    ) -> None:
        super().__init__()
        self.service = NarrativeService(sentence_library_root)
        self.runtime = NarrativeRuntime()
        self.result_composer = NarrativeResultComposer()

    def compose_tree(
        self,
        runtime_input: RuntimeInput | None = None,
        *,
        analysis: Any = None,
        interpretation: Any = None,
        run_id: str = "",
    ) -> NarrativeTree:
        """
        Sprint D1 public API: compose NarrativeTree only.

        Does not generate paragraphs or prose.
        """
        if runtime_input is not None:
            return self.runtime.compose_tree(runtime_input)
        return self.runtime.compose_tree_from_sources(
            analysis=analysis,
            interpretation=interpretation,
            run_id=run_id,
        )

    def compose_narrative_result(
        self,
        *,
        analysis: Any = None,
        interpretation: Any = None,
        run_id: str = "",
        tree: NarrativeTree | None = None,
    ) -> NarrativeResult:
        """
        Sprint D2 public API: NarrativeTree → NarrativeResult.

        Sentences are sourced from Interpretation/Evidence only.
        """
        narrative_tree = tree or self.compose_tree(
            analysis=analysis,
            interpretation=interpretation,
            run_id=run_id,
        )
        return self.result_composer.compose(
            narrative_tree,
            analysis=analysis,
            interpretation=interpretation,
        )

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
