"""Customer domain models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class CustomerModel:
    """Customer profile for BTE Applications (WP11)."""

    customer_id: str
    full_name: str
    gender: str | None = None
    birth_datetime: str | None = None
    timezone: str = "Asia/Ho_Chi_Minh"
    language: str = "vi"
    phone: str | None = None
    email: str | None = None
    notes: str | None = None
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=_utcnow_iso)
    updated_at: str = field(default_factory=_utcnow_iso)

    @classmethod
    def create(
        cls,
        *,
        full_name: str,
        gender: str | None = None,
        birth_datetime: str | None = None,
        timezone: str = "Asia/Ho_Chi_Minh",
        language: str = "vi",
        phone: str | None = None,
        email: str | None = None,
        notes: str | None = None,
        tags: list[str] | None = None,
        customer_id: str | None = None,
    ) -> CustomerModel:
        """Factory for a new customer record."""
        now = _utcnow_iso()
        return cls(
            customer_id=customer_id or str(uuid4()),
            full_name=full_name,
            gender=gender,
            birth_datetime=birth_datetime,
            timezone=timezone,
            language=language,
            phone=phone,
            email=email,
            notes=notes,
            tags=list(tags or []),
            created_at=now,
            updated_at=now,
        )

    def touch(self) -> None:
        """Bump ``updated_at``."""
        self.updated_at = _utcnow_iso()

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict for JSON storage."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CustomerModel:
        """Deserialize from storage dict."""
        tags = data.get("tags") or []
        if not isinstance(tags, list):
            tags = list(tags)
        return cls(
            customer_id=str(data["customer_id"]),
            full_name=str(data.get("full_name") or ""),
            gender=data.get("gender"),
            birth_datetime=data.get("birth_datetime"),
            timezone=str(data.get("timezone") or "Asia/Ho_Chi_Minh"),
            language=str(data.get("language") or "vi"),
            phone=data.get("phone"),
            email=data.get("email"),
            notes=data.get("notes"),
            tags=[str(tag) for tag in tags],
            created_at=str(data.get("created_at") or _utcnow_iso()),
            updated_at=str(data.get("updated_at") or _utcnow_iso()),
        )
