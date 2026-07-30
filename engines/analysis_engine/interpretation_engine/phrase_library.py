"""Phrase Library access for interpretive paragraph composition."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.interpretation_engine.knowledge_access import (
    ASSET_PHRASES,
    KnowledgeSession,
)


class PhraseLibrary:
    """Resolve deterministic opening phrases from Knowledge Phrase Library."""

    def opening_for_section(
        self,
        section_id: str,
        *,
        session: KnowledgeSession,
    ) -> tuple[str | None, str]:
        """Return ``(phrase_id, phrase_text)`` for a section, or ``(None, "")``.

        Prefer enabled opening phrases that explicitly tag ``section_id``.
        Fall back to ``general`` only when no section-specific phrase exists.
        Ordering: priority ascending, then phrase id ascending.
        """
        rows = list(session.get_asset(ASSET_PHRASES).data.get("rows") or [])
        specific: list[Mapping[str, Any]] = []
        general: list[Mapping[str, Any]] = []
        for row in rows:
            if not bool(row.get("enabled", True)):
                continue
            if str(row.get("type") or "") != "opening":
                continue
            tags = {str(tag) for tag in list(row.get("tags") or [])}
            if section_id in tags:
                specific.append(row)
            elif "general" in tags:
                general.append(row)

        candidates = specific or general
        if not candidates:
            return None, ""
        candidates.sort(
            key=lambda row: (int(row.get("priority") or 0), str(row.get("id") or ""))
        )
        chosen = candidates[0]
        return str(chosen.get("id") or "") or None, str(chosen.get("text") or "").strip()
