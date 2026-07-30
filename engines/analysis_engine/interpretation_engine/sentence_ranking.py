"""Sentence Ranking — order selected sentences deterministically."""

from __future__ import annotations

from engines.analysis_engine.interpretation_engine.knowledge_access import (
    ASSET_PRIORITY,
    KnowledgeSession,
)
from engines.analysis_engine.interpretation_engine.models import SelectedSentence


class SentenceRanker:
    """Rank selected sentences using Knowledge priority policy."""

    def rank(
        self,
        selected: tuple[SelectedSentence, ...],
        *,
        session: KnowledgeSession,
    ) -> tuple[SelectedSentence, ...]:
        """Return sentences ordered by priority policy then sentence_id."""
        policy = list(
            session.get_asset(ASSET_PRIORITY).data.get("tie_break")
            or ["priority_desc", "sentence_id_asc"]
        )
        items = list(selected)

        def sort_key(item: SelectedSentence) -> tuple[object, ...]:
            keys: list[object] = []
            for rule in policy:
                if rule == "priority_desc":
                    keys.append(-item.priority)
                elif rule == "priority_asc":
                    keys.append(item.priority)
                elif rule == "sentence_id_asc":
                    keys.append(item.sentence_id)
                elif rule == "sentence_id_desc":
                    # Invert lexicographic order via negated ordinals is awkward;
                    # use a descending secondary pass after primary key.
                    keys.append(item.sentence_id)
                elif rule == "section_id_asc":
                    keys.append(item.section_id)
                else:
                    keys.append(item.sentence_id)
            if "sentence_id_asc" not in policy and "sentence_id_desc" not in policy:
                keys.append(item.sentence_id)
            return tuple(keys)

        items.sort(key=sort_key)
        if "sentence_id_desc" in policy:
            # Re-apply priority order, then reverse sentence_id within ties.
            items.sort(key=lambda item: item.sentence_id, reverse=True)
            if "priority_desc" in policy:
                items.sort(key=lambda item: -item.priority)
            elif "priority_asc" in policy:
                items.sort(key=lambda item: item.priority)
        return tuple(items)
