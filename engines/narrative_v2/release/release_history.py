"""Append-only release event history. Never edits prior rows."""

from __future__ import annotations

import json
from pathlib import Path

from engines.narrative_v2.release.release_errors import ReleaseHistoryError
from engines.narrative_v2.release.release_events import ReleaseEvent

DEFAULT_STORE = (
    Path(__file__).resolve().parents[3]
    / "implementation"
    / "narrative_release"
    / "n_rel_02"
    / "release_history.json"
)


class ReleaseHistory:
    """JSON append-only log. Isolated from Narrative content."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or DEFAULT_STORE

    @property
    def path(self) -> Path:
        """History file path."""
        return self._path

    def list(self) -> list[ReleaseEvent]:
        """Return all events, oldest first."""
        return [ReleaseEvent.from_record(row) for row in self._load()]

    def latest(self) -> ReleaseEvent | None:
        """Newest event, if any."""
        rows = self.list()
        return rows[-1] if rows else None

    def append(self, event: ReleaseEvent) -> None:
        """Append one event. Existing rows are never rewritten."""
        snapshot = [dict(row) for row in self._load()]
        snapshot.append(event.to_record())
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def replace_all(self, events: list[ReleaseEvent]) -> None:
        """Forbidden rewrite path. Raises so tests can prove immutability."""
        raise ReleaseHistoryError("history_is_append_only")

    def _load(self) -> list[dict]:
        if not self._path.exists():
            return []
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return []
        return [item for item in raw if isinstance(item, dict)]
