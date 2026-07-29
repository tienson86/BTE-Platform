"""Detect and drop duplicate styled paragraphs (keep higher score)."""

from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

from ._text_utils import normalize
from .consistency_models import ConsistencyIssue


class DuplicateChecker:
    """
    Remove near-duplicate paragraphs without altering kept content.

    Priority: higher ``score`` wins; ties keep the earlier paragraph.
    """

    def __init__(self, *, similarity_threshold: float = 0.92) -> None:
        self.similarity_threshold = similarity_threshold

    def check(
        self,
        paragraphs: list[Any],
    ) -> tuple[list[Any], list[str], list[ConsistencyIssue]]:
        """Return kept paragraphs, removed texts, and issues."""
        ordered = sorted(
            enumerate(paragraphs),
            key=lambda item: (-float(getattr(item[1], "score", 0) or 0), item[0]),
        )
        kept: list[Any] = []
        kept_norms: list[str] = []
        removed: list[str] = []
        issues: list[ConsistencyIssue] = []

        accepted_ids: set[int] = set()
        for _index, paragraph in ordered:
            text = str(getattr(paragraph, "text", "") or "")
            norm = normalize(text)
            if not norm:
                removed.append(text)
                issues.append(
                    ConsistencyIssue(
                        kind="duplicate",
                        detail="Empty paragraph dropped.",
                        paragraph_id=str(getattr(paragraph, "paragraph_id", "")),
                        section=str(getattr(paragraph, "section", "")),
                        action="drop",
                    )
                )
                continue
            match = self._find_duplicate(norm, kept, kept_norms)
            if match is not None:
                removed.append(text)
                issues.append(
                    ConsistencyIssue(
                        kind="duplicate",
                        detail="Duplicate of higher-priority paragraph.",
                        paragraph_id=str(getattr(paragraph, "paragraph_id", "")),
                        section=str(getattr(paragraph, "section", "")),
                        action="drop",
                        related_paragraph_id=str(
                            getattr(match, "paragraph_id", "")
                        ),
                    )
                )
                continue
            kept.append(paragraph)
            kept_norms.append(norm)
            accepted_ids.add(id(paragraph))

        # Restore original relative order among survivors
        survivors = [p for p in paragraphs if id(p) in accepted_ids]
        return survivors, removed, issues

    def _find_duplicate(
        self,
        norm: str,
        kept: list[Any],
        kept_norms: list[str],
    ) -> Any | None:
        for index, other in enumerate(kept_norms):
            if norm == other:
                return kept[index]
            if len(norm) >= 12 and len(other) >= 12:
                if norm in other or other in norm:
                    return kept[index]
            if SequenceMatcher(None, norm, other).ratio() >= self.similarity_threshold:
                return kept[index]
        return None
