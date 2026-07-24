"""Detect lexical / semantic contradictions within a section."""

from __future__ import annotations

from typing import Any

from ._text_utils import has_antonym_clash, polarity_conflict
from .consistency_models import ConsistencyIssue


class ContradictionChecker:
    """
    Drop lower-priority paragraph when it contradicts a kept one in-section.

    Does not rewrite text of retained paragraphs.
    """

    def check(
        self,
        paragraphs: list[Any],
    ) -> tuple[list[Any], list[ConsistencyIssue]]:
        """Return non-contradictory paragraphs and contradiction issues."""
        by_section: dict[str, list[Any]] = {}
        order: list[str] = []
        for paragraph in paragraphs:
            section = str(getattr(paragraph, "section", "") or "")
            if section not in by_section:
                order.append(section)
                by_section[section] = []
            by_section[section].append(paragraph)

        survivors: list[Any] = []
        issues: list[ConsistencyIssue] = []

        for section in order:
            group = by_section[section]
            ranked = sorted(
                group,
                key=lambda item: float(getattr(item, "score", 0) or 0),
                reverse=True,
            )
            accepted: list[Any] = []
            for candidate in ranked:
                conflict = self._conflicts_with(candidate, accepted)
                if conflict is not None:
                    issues.append(
                        ConsistencyIssue(
                            kind="contradiction",
                            detail=(
                                "Contradicts higher-priority paragraph "
                                f"in section '{section}'."
                            ),
                            paragraph_id=str(
                                getattr(candidate, "paragraph_id", "")
                            ),
                            section=section,
                            action="drop",
                            related_paragraph_id=str(
                                getattr(conflict, "paragraph_id", "")
                            ),
                        )
                    )
                    continue
                accepted.append(candidate)
            survivors.extend(accepted)

        survivor_ids = {id(item) for item in survivors}
        return [p for p in paragraphs if id(p) in survivor_ids], issues

    def _conflicts_with(self, candidate: Any, accepted: list[Any]) -> Any | None:
        cand_text = str(getattr(candidate, "text", "") or "")
        cand_pol = str(getattr(candidate, "polarity", "neutral"))
        for kept in accepted:
            kept_text = str(getattr(kept, "text", "") or "")
            kept_pol = str(getattr(kept, "polarity", "neutral"))
            if polarity_conflict(cand_pol, kept_pol):
                return kept
            if has_antonym_clash(cand_text, kept_text):
                return kept
        return None
