"""Consistency Layer builder — StyledParagraphContext → ConsistentParagraphContext."""

from __future__ import annotations

import importlib
from typing import Any, Mapping

from .coherence_checker import CoherenceChecker
from .consistency_models import ConsistentParagraphContext
from .contradiction_checker import ContradictionChecker
from .duplicate_checker import DuplicateChecker
from .polarity_checker import PolarityChecker

_style = importlib.import_module("engines.report_engine.content.03_style.style_models")
StyledParagraph = _style.StyledParagraph
StyledParagraphContext = _style.StyledParagraphContext
StyledSentence = _style.StyledSentence


class ConsistencyBuilder:
    """
    Independent Consistency Layer entry point.

    Pipeline
    --------
    StyledParagraphContext
      → duplicate check (drop, keep higher score)
      → polarity check (drop, keep higher score)
      → contradiction check (drop, keep higher score)
      → coherence check (warn only)
      → ConsistentParagraphContext

    Never invents sentences; never rewrites retained paragraph text.
    """

    def __init__(self) -> None:
        self.duplicates = DuplicateChecker()
        self.polarity = PolarityChecker()
        self.contradictions = ContradictionChecker()
        self.coherence = CoherenceChecker()

    def apply(
        self,
        styled: StyledParagraphContext | Mapping[str, Any],
    ) -> ConsistentParagraphContext:
        """Run consistency pass."""
        ctx = self._as_styled(styled)
        paragraphs = list(ctx.styled_paragraphs)

        paragraphs, removed, dup_issues = self.duplicates.check(paragraphs)
        paragraphs, pol_issues = self.polarity.check(paragraphs)
        paragraphs, contra_issues = self.contradictions.check(paragraphs)
        coherence_issues = self.coherence.check(paragraphs)

        contradiction_report = [
            issue.to_dict()
            for issue in [*pol_issues, *contra_issues]
        ]
        coherence_report = [issue.to_dict() for issue in coherence_issues]
        warnings = [
            f"[{issue.kind}] {issue.detail}"
            for issue in [*dup_issues, *pol_issues, *contra_issues, *coherence_issues]
            if issue.action in {"warn", "info", "drop"}
        ]

        # Preserve emphasis for surviving paragraphs only
        surviving_ids = {
            str(getattr(paragraph, "paragraph_id", "")) for paragraph in paragraphs
        }
        emphasis = {
            key: value
            for key, value in (ctx.emphasis_levels or {}).items()
            if key in surviving_ids
        }

        return ConsistentParagraphContext(
            checked_paragraphs=paragraphs,
            removed_duplicates=list(ctx.removed_duplicates or []) + list(removed),
            contradiction_report=contradiction_report,
            coherence_report=coherence_report,
            warnings=warnings,
            tone=ctx.tone,
            emphasis_levels=emphasis,
            metadata={
                "input_count": len(ctx.styled_paragraphs),
                "output_count": len(paragraphs),
                "duplicate_drops": len(dup_issues),
                "contradiction_drops": len(contradiction_report),
                "coherence_notes": len(coherence_report),
            },
        )

    def _as_styled(
        self,
        value: StyledParagraphContext | Mapping[str, Any],
    ) -> StyledParagraphContext:
        if isinstance(value, StyledParagraphContext):
            return value
        paragraphs: list[Any] = []
        for row in value.get("styled_paragraphs") or []:
            if not isinstance(row, Mapping):
                continue
            sentences = [
                StyledSentence(
                    original=str(item.get("original") or ""),
                    rewritten=str(item.get("rewritten") or item.get("original") or ""),
                    section=str(item.get("section") or row.get("section") or ""),
                    paragraph_id=str(
                        item.get("paragraph_id") or row.get("paragraph_id") or ""
                    ),
                    polarity=str(item.get("polarity") or "neutral"),
                    emphasis=str(item.get("emphasis") or "normal"),
                    rule_id=str(item.get("rule_id") or ""),
                )
                for item in (row.get("sentences") or [])
                if isinstance(item, Mapping)
            ]
            paragraphs.append(
                StyledParagraph(
                    paragraph_id=str(row.get("paragraph_id") or ""),
                    section=str(row.get("section") or ""),
                    polarity=str(row.get("polarity") or "neutral"),
                    text=str(row.get("text") or ""),
                    original_text=str(row.get("original_text") or row.get("text") or ""),
                    emphasis=str(row.get("emphasis") or "normal"),
                    score=float(row.get("score") or 0),
                    sentences=sentences,
                )
            )
        return StyledParagraphContext(
            styled_paragraphs=paragraphs,
            rewritten_sentences=[],
            emphasis_levels=dict(value.get("emphasis_levels") or {}),
            tone=str(value.get("tone") or "neutral"),
            removed_duplicates=list(value.get("removed_duplicates") or []),
            metadata=dict(value.get("metadata") or {}),
        )
