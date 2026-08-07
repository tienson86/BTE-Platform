"""
Pack 04 Interpretation Pipeline

AnalysisResult
    ↓
Narrative Context
    ↓
Evidence
    ↓
Rule Matching (narrative)
    ↓
Sentence Selection
    ↓
Placeholder Binding
    ↓
Interpretation Builder
    ↓
Result<NarrativeInterpretationResult>
"""

from __future__ import annotations

import time
from typing import Any

from .evidence import EvidenceCollector
from .interpretation_builder import InterpretationBuilder
from .library_loader import NarrativeLibrary
from .models import EngineResult, NarrativeInterpretationResult
from .narrative_context import NarrativeContextBuilder
from .placeholder_binding import PlaceholderBinder
from .rule_matching import NarrativeRuleMatcher
from .sentence_selection import SentenceSelector


class Pack04Pipeline:
    """Official Pack 04 narrative pipeline orchestrator."""

    def __init__(self, library: NarrativeLibrary | None = None) -> None:
        self.library = library or NarrativeLibrary()
        self.context_builder = NarrativeContextBuilder()
        self.evidence_collector = EvidenceCollector()
        self.rule_matcher = NarrativeRuleMatcher(self.library)
        self.sentence_selector = SentenceSelector(self.library)
        self.placeholder_binder = PlaceholderBinder()
        self.builder = InterpretationBuilder()

    def run(
        self,
        analysis: Any,
    ) -> EngineResult[NarrativeInterpretationResult]:
        """
        Execute Pack 04 pipeline for one AnalysisResult.

        Parameters
        ----------
        analysis:
            Canonical Score Engine AnalysisResult (read-only).
        """
        started = time.perf_counter()
        trace: list[str] = []
        warnings: list[str] = []

        try:
            from engines.score_engine.analysis import AnalysisResult

            if analysis is None or not isinstance(analysis, AnalysisResult):
                return EngineResult(
                    success=False,
                    error="AnalysisResult is required.",
                    trace=["validate_input"],
                )
            if not getattr(analysis, "success", True):
                warnings.append("analysis_success_false")

            context = self.context_builder.build(analysis)
            trace.append("narrative_context")

            evidence_ids = self.evidence_collector.collect(context)
            trace.append(f"evidence:{len(evidence_ids)}")

            matched_rules = self.rule_matcher.match(context)
            trace.append(f"rule_matching:{len(matched_rules)}")
            if not matched_rules:
                return EngineResult(
                    success=False,
                    error="No narrative rules matched.",
                    warnings=warnings,
                    trace=trace,
                )

            selected = self.sentence_selector.select(matched_rules)
            trace.append(f"sentence_selection:{len(selected)}")
            if not selected:
                return EngineResult(
                    success=False,
                    error="No sentences selected from library.",
                    warnings=warnings,
                    trace=trace,
                    metadata={"matched_rules": [r.get("rule_id") for r in matched_rules]},
                )

            rendered = self.placeholder_binder.bind(selected, context)
            trace.append(f"placeholder_binding:{len(rendered)}")

            duration_ms = round((time.perf_counter() - started) * 1000.0, 3)
            result = self.builder.build(
                rendered,
                context,
                matched_rules=matched_rules,
                duration_ms=duration_ms,
            )
            trace.append("interpretation_builder")

            return EngineResult(
                success=True,
                value=result,
                warnings=warnings,
                metadata={
                    "pack": "04",
                    "pipeline": "pack04",
                    "section_count": len([s for s in result.sections() if s.sentences]),
                    "sentence_count": sum(len(s.sentences) for s in result.sections()),
                },
                trace=trace,
            )
        except Exception as exc:
            return EngineResult(
                success=False,
                error=str(exc),
                warnings=warnings,
                trace=trace + ["error"],
                metadata={"exception_type": type(exc).__name__},
            )

    def run_stages(self, analysis: Any) -> dict[str, Any]:
        """
        Debug helper — return intermediate stage payloads.

        Not part of production public API.
        """
        context = self.context_builder.build(analysis)
        evidence = self.evidence_collector.collect(context)
        matched = self.rule_matcher.match(context)
        selected = self.sentence_selector.select(matched)
        rendered = self.placeholder_binder.bind(selected, context)
        return {
            "placeholders": dict(context.placeholders),
            "evidence_ids": evidence,
            "matched_rules": matched,
            "selected": selected,
            "rendered": [s.text for s in rendered],
        }
