"""Redundancy Reducer — drop duplicate / near-duplicate narrative units."""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher

from .models import NarrativeIssue, NarrativeUnit

_WS = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Fold accents and whitespace for comparison."""
    decomposed = unicodedata.normalize("NFD", text.strip().lower())
    without = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return _WS.sub(" ", without).strip()


class RedundancyReducer:
    """Remove exact and near-duplicate sentences (no LLM)."""

    def __init__(self, *, similarity_threshold: float = 0.92) -> None:
        self.similarity_threshold = similarity_threshold
        self.issues: list[NarrativeIssue] = []

    def reduce(self, units: list[NarrativeUnit]) -> list[NarrativeUnit]:
        """Keep higher-priority unit when texts collide."""
        self.issues = []
        ordered = sorted(units, key=lambda u: (u.priority, len(u.text)), reverse=True)
        kept: list[NarrativeUnit] = []
        kept_norms: list[str] = []

        for unit in ordered:
            norm = normalize_text(unit.text)
            if not norm:
                self.issues.append(
                    NarrativeIssue(
                        kind="redundancy",
                        detail="Empty text dropped.",
                        section_id=unit.section_id,
                        action="drop",
                    )
                )
                continue
            duplicate_of = self._find_duplicate(norm, kept, kept_norms)
            if duplicate_of is not None:
                self.issues.append(
                    NarrativeIssue(
                        kind="redundancy",
                        detail=f"Duplicate of higher-priority unit ({duplicate_of.rule_id or duplicate_of.source}).",
                        section_id=unit.section_id,
                        action="drop",
                    )
                )
                continue
            # Prefer longer text when one subsumes the other
            covered = self._find_covered(norm, kept, kept_norms)
            if covered is not None:
                self.issues.append(
                    NarrativeIssue(
                        kind="redundancy",
                        detail="Subsumed by richer higher-priority unit.",
                        section_id=unit.section_id,
                        action="drop",
                    )
                )
                continue
            kept.append(unit)
            kept_norms.append(norm)

        # Restore section reading order: original relative order among survivors
        survivor_ids = {id(unit) for unit in kept}
        return [unit for unit in units if id(unit) in survivor_ids]

    def _find_duplicate(
        self,
        norm: str,
        kept: list[NarrativeUnit],
        kept_norms: list[str],
    ) -> NarrativeUnit | None:
        for index, other in enumerate(kept_norms):
            if norm == other:
                return kept[index]
            if SequenceMatcher(None, norm, other).ratio() >= self.similarity_threshold:
                return kept[index]
        return None

    @staticmethod
    def _find_covered(
        norm: str,
        kept: list[NarrativeUnit],
        kept_norms: list[str],
    ) -> NarrativeUnit | None:
        if len(norm) < 16:
            return None
        for index, other in enumerate(kept_norms):
            if len(other) < 16:
                continue
            if norm in other or other in norm:
                return kept[index]
        return None
