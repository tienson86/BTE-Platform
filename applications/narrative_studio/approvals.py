"""Internal approval records. Does not write Narrative or Knowledge."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_VERDICTS = frozenset({"PASS", "REVIEW", "REJECT"})

DEFAULT_STORE = (
    Path(__file__).resolve().parents[2]
    / "implementation"
    / "narrative_v2"
    / "studio_reviews"
    / "approvals.json"
)


@dataclass(frozen=True, slots=True)
class StudioApproval:
    """One internal Product Owner review row."""

    case_id: str
    verdict: str
    comment: str
    reviewer: str
    timestamp: str


class ApprovalStore:
    """JSON file of studio approvals. Isolated from engines and knowledge CSVs."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or DEFAULT_STORE

    def list_for(self, case_id: str) -> list[StudioApproval]:
        """Return approvals for one case, oldest first."""
        return [row for row in self._load() if row.case_id == case_id]

    def latest(self, case_id: str) -> StudioApproval | None:
        """Return the newest approval for a case, if any."""
        rows = self.list_for(case_id)
        return rows[-1] if rows else None

    def record(
        self,
        *,
        case_id: str,
        verdict: str,
        comment: str,
        reviewer: str,
    ) -> StudioApproval:
        """Append an internal review. Does not change Presentation or Knowledge."""
        token = verdict.strip().upper()
        if token not in ALLOWED_VERDICTS:
            raise ValueError("verdict must be PASS, REVIEW, or REJECT")
        entry = StudioApproval(
            case_id=case_id,
            verdict=token,
            comment=comment.strip(),
            reviewer=reviewer.strip() or "internal",
            timestamp=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        )
        rows = self._load()
        rows.append(entry)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = [self._to_dict(row) for row in rows]
        self._path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return entry

    def _load(self) -> list[StudioApproval]:
        if not self._path.exists():
            return []
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return []
        rows: list[StudioApproval] = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            rows.append(
                StudioApproval(
                    case_id=str(item.get("case_id") or ""),
                    verdict=str(item.get("verdict") or ""),
                    comment=str(item.get("comment") or ""),
                    reviewer=str(item.get("reviewer") or ""),
                    timestamp=str(item.get("timestamp") or ""),
                )
            )
        return rows

    @staticmethod
    def _to_dict(row: StudioApproval) -> dict[str, Any]:
        return {
            "case_id": row.case_id,
            "verdict": row.verdict,
            "comment": row.comment,
            "reviewer": row.reviewer,
            "timestamp": row.timestamp,
        }
