"""Conflict Resolution — enforce exclusive groups and section caps."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.interpretation_engine.knowledge_access import (
    ASSET_PRIORITY,
    ASSET_SECTIONS,
    KnowledgeSession,
)
from engines.analysis_engine.interpretation_engine.models import SelectedSentence


class ConflictResolver:
    """Resolve conflicts among ranked sentence candidates."""

    def resolve(
        self,
        ranked: tuple[SelectedSentence, ...],
        *,
        session: KnowledgeSession,
    ) -> tuple[SelectedSentence, ...]:
        """Keep highest-priority winners under conflict and section limits."""
        priority_cfg = session.get_asset(ASSET_PRIORITY).data
        section_cfg = session.get_asset(ASSET_SECTIONS).data
        max_per_section = int(section_cfg.get("max_sentences_per_section") or 3)
        exclusive_groups = list(priority_cfg.get("exclusive_groups") or [])

        suppressed = self._exclusive_losers(ranked, exclusive_groups)
        kept: list[SelectedSentence] = []
        counts: dict[str, int] = {}
        for item in ranked:
            if item.sentence_id in suppressed:
                continue
            count = counts.get(item.section_id, 0)
            if count >= max_per_section:
                continue
            kept.append(item)
            counts[item.section_id] = count + 1
        return tuple(kept)

    @staticmethod
    def _exclusive_losers(
        ranked: tuple[SelectedSentence, ...],
        exclusive_groups: list[Mapping[str, Any]],
    ) -> set[str]:
        """Return sentence_ids suppressed by exclusive-group winners."""
        by_id = {item.sentence_id: item for item in ranked}
        losers: set[str] = set()
        for group in exclusive_groups:
            members = [
                sentence_id
                for sentence_id in list(group.get("sentence_ids") or [])
                if sentence_id in by_id
            ]
            if len(members) <= 1:
                continue
            strategy = str(group.get("strategy") or "highest_priority")
            if strategy == "highest_priority":
                winner = max(
                    members,
                    key=lambda sid: (by_id[sid].priority, sid),
                )
            else:
                winner = sorted(members)[0]
            for sentence_id in members:
                if sentence_id != winner:
                    losers.add(sentence_id)
        return losers
