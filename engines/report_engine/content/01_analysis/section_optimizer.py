"""Optimize suggested section order from scores and canonical narrative flow."""

from __future__ import annotations

from typing import Any


# Preferred narrative spine (Analysis Layer prior — not report template mutation).
_CANONICAL_ORDER: tuple[str, ...] = (
    "summary",
    "strength",
    "weakness",
    "pattern",
    "useful_god",
    "personality",
    "career",
    "wealth",
    "relationship",
    "health",
    "children",
    "luck",
    "luck_cycle",
    "yearly_fortune",
    "warning",
    "conclusion",
)


class SectionOptimizer:
    """Build suggested_order from importance + canonical narrative spine."""

    def optimize(
        self,
        *,
        section_scores: dict[str, float],
        important_sections: list[str],
        grouped_rules: dict[str, list[Any]] | None = None,
    ) -> list[str]:
        """
        Return suggested section order.

        Rules
        -----
        1. Keep canonical relative order for known sections.
        2. Prefer important / scored sections first among unknowns.
        3. Drop empty sections (no rules) when grouped_rules provided.
        """
        grouped = grouped_rules or {}
        present = set(section_scores) | set(grouped) | set(important_sections)

        def _has_content(name: str) -> bool:
            if name not in grouped:
                return name in section_scores and float(section_scores.get(name, 0)) > 0
            return len(grouped.get(name) or []) > 0 or float(section_scores.get(name, 0)) > 0

        ordered: list[str] = []
        for name in _CANONICAL_ORDER:
            if name not in present:
                continue
            if grouped and not _has_content(name):
                # Still keep summary/conclusion slots if scored
                if name not in {"summary", "conclusion"}:
                    continue
            ordered.append(name)

        leftovers = [
            name
            for name in sorted(
                present,
                key=lambda item: float(section_scores.get(item, 0.0)),
                reverse=True,
            )
            if name not in ordered and (not grouped or _has_content(name))
        ]
        # Important leftovers first
        important_set = set(important_sections)
        leftovers.sort(
            key=lambda item: (
                1 if item in important_set else 0,
                float(section_scores.get(item, 0.0)),
            ),
            reverse=True,
        )
        ordered.extend(leftovers)
        return ordered
