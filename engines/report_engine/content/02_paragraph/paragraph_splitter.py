"""Split sentence streams so opposing polarities never share a paragraph."""

from __future__ import annotations

from typing import Iterable

from .paragraph_models import SentenceUnit


class ParagraphSplitter:
    """
    Enforce polarity separation.

    If a merged candidate group still mixes polarities (defensive),
    split into polarity-homogeneous runs without creating new text.
    """

    def split(self, groups: Iterable[list[SentenceUnit]]) -> list[list[SentenceUnit]]:
        """Return polarity-pure groups (section/topic already constrained upstream)."""
        result: list[list[SentenceUnit]] = []
        for group in groups:
            if not group:
                continue
            # Defensive: never allow polarity mix inside one paragraph candidate
            by_polarity: dict[str, list[SentenceUnit]] = {}
            order: list[str] = []
            for unit in group:
                if unit.polarity not in by_polarity:
                    order.append(unit.polarity)
                    by_polarity[unit.polarity] = []
                by_polarity[unit.polarity].append(unit)
            for polarity in order:
                chunk = by_polarity[polarity]
                if chunk:
                    result.append(chunk)
        return result

    def split_units_by_polarity_runs(
        self,
        units: list[SentenceUnit],
    ) -> list[list[SentenceUnit]]:
        """
        Split a same-section sequence into contiguous polarity runs.

        Useful when callers pass a flat section list before merging.
        """
        if not units:
            return []
        runs: list[list[SentenceUnit]] = []
        current: list[SentenceUnit] = [units[0]]
        for unit in units[1:]:
            if unit.section != current[0].section:
                # Hard stop — different section must not continue the run
                runs.append(current)
                current = [unit]
                continue
            if unit.polarity != current[0].polarity:
                runs.append(current)
                current = [unit]
                continue
            current.append(unit)
        if current:
            runs.append(current)
        return runs
