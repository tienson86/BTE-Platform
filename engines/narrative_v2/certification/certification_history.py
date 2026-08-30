"""Append-only certification history. Never edits prior rows."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from engines.narrative_v2.certification.certification_errors import CertificationError
from engines.narrative_v2.certification.certification_result import (
    STATUS_DRAFT,
    CertificationResult,
)

DEFAULT_STORE = (
    Path(__file__).resolve().parents[3]
    / "implementation"
    / "narrative_v2"
    / "certification"
    / "history.json"
)


class CertificationHistory:
    """JSON append-only log isolated from Narrative and Knowledge."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or DEFAULT_STORE

    def list_for(self, case_id: str) -> list[dict[str, Any]]:
        """Return rows for one case, oldest first."""
        return [row for row in self._load() if str(row.get("case_id")) == case_id]

    def current_status(self, case_id: str) -> str:
        """Latest status or DRAFT when no history exists."""
        rows = self.list_for(case_id)
        if not rows:
            return STATUS_DRAFT
        status = str(rows[-1].get("status") or STATUS_DRAFT)
        return status

    def latest(self, case_id: str) -> dict[str, Any] | None:
        """Newest row for the case."""
        rows = self.list_for(case_id)
        return rows[-1] if rows else None

    def append(self, result: CertificationResult) -> None:
        """Append a new row. Existing rows are never rewritten."""
        rows = self._load()
        existing_ids = {str(row.get("review_id")) for row in rows}
        if result.review_id in existing_ids:
            raise CertificationError("review_id already recorded")
        snapshot = [dict(row) for row in rows]
        snapshot.append(result.to_record())
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _load(self) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return []
        return [item for item in raw if isinstance(item, dict)]
