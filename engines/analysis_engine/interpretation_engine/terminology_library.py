"""Terminology Library access for placeholder display resolution."""

from __future__ import annotations

from typing import Mapping

from engines.analysis_engine.interpretation_engine.knowledge_access import (
    ASSET_TERMINOLOGY,
    KnowledgeSession,
)


class TerminologyLibrary:
    """Resolve analytical term codes to display labels."""

    def resolve_map(self, session: KnowledgeSession) -> dict[str, str]:
        """Return term_id → display_name map from Terminology Library."""
        rows = list(session.get_asset(ASSET_TERMINOLOGY).data.get("rows") or [])
        resolved: dict[str, str] = {}
        for row in sorted(rows, key=lambda item: str(item.get("term_id") or "")):
            term_id = str(row.get("term_id") or "").strip()
            display = str(row.get("display_name") or "").strip()
            if term_id and display:
                resolved[term_id] = display
        return resolved

    def apply_to_values(
        self,
        values: Mapping[str, str],
        *,
        session: KnowledgeSession,
    ) -> tuple[dict[str, str], tuple[str, ...]]:
        """Replace known term codes in placeholder values.

        Returns updated values and the terminology ids that were applied.
        """
        terms = self.resolve_map(session)
        if not terms:
            return dict(values), ()
        updated = dict(values)
        used: list[str] = []
        for key, raw in values.items():
            if raw in terms:
                updated[key] = terms[raw]
                used.append(raw)
                continue
            # Comma-separated lists of term ids.
            parts = [part.strip() for part in raw.split(",")]
            if len(parts) > 1 and all(part in terms for part in parts if part):
                updated[key] = ", ".join(terms[part] for part in parts if part)
                used.extend(part for part in parts if part)
        return updated, tuple(dict.fromkeys(used))
