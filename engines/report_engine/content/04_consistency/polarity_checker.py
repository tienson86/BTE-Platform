"""Detect polarity conflicts within the same section."""

from __future__ import annotations

from typing import Any

from ._text_utils import polarity_conflict
from .consistency_models import ConsistencyIssue


class PolarityChecker:
    """
    Within one section, opposing polarities are inconsistent.

    Keep the higher-score paragraph; drop the lower one (content of keeper unchanged).
    """

    def check(
        self,
        paragraphs: list[Any],
    ) -> tuple[list[Any], list[ConsistencyIssue]]:
        """Return polarity-consistent paragraphs and issues."""
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
        dropped_ids: set[str] = set()

        for section in order:
            group = by_section[section]
            ranked = sorted(
                group,
                key=lambda item: float(getattr(item, "score", 0) or 0),
                reverse=True,
            )
            accepted: list[Any] = []
            for candidate in ranked:
                cand_id = str(getattr(candidate, "paragraph_id", ""))
                cand_pol = str(getattr(candidate, "polarity", "neutral"))
                conflict = None
                for kept in accepted:
                    if polarity_conflict(
                        cand_pol,
                        str(getattr(kept, "polarity", "neutral")),
                    ):
                        conflict = kept
                        break
                if conflict is not None:
                    dropped_ids.add(cand_id)
                    issues.append(
                        ConsistencyIssue(
                            kind="polarity",
                            detail=(
                                "Polarity conflicts with higher-priority "
                                f"paragraph in section '{section}'."
                            ),
                            paragraph_id=cand_id,
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

        # Preserve input order of survivors
        survivor_ids = {id(item) for item in survivors}
        return [p for p in paragraphs if id(p) in survivor_ids], issues
