"""Case (luận giải hồ sơ) domain models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class CaseModel:
    """Stored analysis case linked to a customer."""

    case_id: str
    customer_id: str
    created_at: str
    engine_version: str
    input_snapshot: dict[str, Any] = field(default_factory=dict)
    calendar_result: dict[str, Any] = field(default_factory=dict)
    bazi_result: dict[str, Any] = field(default_factory=dict)
    pattern_result: dict[str, Any] = field(default_factory=dict)
    score_result: dict[str, Any] = field(default_factory=dict)
    interpretation_result: dict[str, Any] = field(default_factory=dict)
    report_result: dict[str, Any] = field(default_factory=dict)
    narrative_result: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        customer_id: str,
        engine_version: str,
        input_snapshot: dict[str, Any] | None = None,
        calendar_result: dict[str, Any] | None = None,
        bazi_result: dict[str, Any] | None = None,
        pattern_result: dict[str, Any] | None = None,
        score_result: dict[str, Any] | None = None,
        interpretation_result: dict[str, Any] | None = None,
        report_result: dict[str, Any] | None = None,
        narrative_result: dict[str, Any] | None = None,
        case_id: str | None = None,
    ) -> CaseModel:
        """Factory for a new case."""
        return cls(
            case_id=case_id or str(uuid4()),
            customer_id=customer_id,
            created_at=_utcnow_iso(),
            engine_version=engine_version,
            input_snapshot=dict(input_snapshot or {}),
            calendar_result=dict(calendar_result or {}),
            bazi_result=dict(bazi_result or {}),
            pattern_result=dict(pattern_result or {}),
            score_result=dict(score_result or {}),
            interpretation_result=dict(interpretation_result or {}),
            report_result=dict(report_result or {}),
            narrative_result=dict(narrative_result or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize for JSON storage."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CaseModel:
        """Deserialize from storage."""
        return cls(
            case_id=str(data["case_id"]),
            customer_id=str(data["customer_id"]),
            created_at=str(data.get("created_at") or _utcnow_iso()),
            engine_version=str(data.get("engine_version") or ""),
            input_snapshot=dict(data.get("input_snapshot") or {}),
            calendar_result=dict(data.get("calendar_result") or {}),
            bazi_result=dict(data.get("bazi_result") or {}),
            pattern_result=dict(data.get("pattern_result") or {}),
            score_result=dict(data.get("score_result") or {}),
            interpretation_result=dict(data.get("interpretation_result") or {}),
            report_result=dict(data.get("report_result") or {}),
            narrative_result=dict(data.get("narrative_result") or {}),
        )
