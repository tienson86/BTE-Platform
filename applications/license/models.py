"""License domain model."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from applications.edition.editions import EDITION_DEFAULTS, Edition
from applications.features.flags import features_for_edition


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _iso(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


@dataclass(slots=True)
class LicenseModel:
    """Product license record (WP14)."""

    license_key: str
    edition: str
    customer: str
    organization: str
    issued_at: str
    expires_at: str | None
    max_users: int
    max_cases: int
    enabled_features: list[str] = field(default_factory=list)
    status: str = "issued"  # issued | active | expired | revoked
    machine_id: str | None = None
    activated_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize for storage / API."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LicenseModel:
        """Deserialize from storage."""
        features = data.get("enabled_features") or []
        if not isinstance(features, list):
            features = list(features)
        return cls(
            license_key=str(data["license_key"]),
            edition=str(data.get("edition") or Edition.COMMUNITY.value),
            customer=str(data.get("customer") or ""),
            organization=str(data.get("organization") or ""),
            issued_at=str(data.get("issued_at") or _iso(_utcnow())),
            expires_at=data.get("expires_at"),
            max_users=int(data.get("max_users") or 1),
            max_cases=int(data.get("max_cases") or 50),
            enabled_features=[str(item) for item in features],
            status=str(data.get("status") or "issued"),
            machine_id=data.get("machine_id"),
            activated_at=data.get("activated_at"),
        )

    @classmethod
    def create(
        cls,
        *,
        edition: Edition | str,
        customer: str,
        organization: str = "",
        days_valid: int | None = 365,
        max_users: int | None = None,
        max_cases: int | None = None,
        enabled_features: list[str] | None = None,
        license_key: str | None = None,
    ) -> LicenseModel:
        """Factory for a new license."""
        ed = Edition(edition) if not isinstance(edition, Edition) else edition
        defaults = EDITION_DEFAULTS[ed]
        now = _utcnow()
        expires = None if days_valid is None else now + timedelta(days=days_valid)
        features = enabled_features
        if features is None:
            features = sorted(f.value for f in features_for_edition(ed))
        return cls(
            license_key=license_key or f"BTE-{ed.value}-{uuid4().hex[:12].upper()}",
            edition=ed.value,
            customer=customer,
            organization=organization,
            issued_at=_iso(now) or "",
            expires_at=_iso(expires),
            max_users=max_users if max_users is not None else defaults["max_users"],
            max_cases=max_cases if max_cases is not None else defaults["max_cases"],
            enabled_features=list(features),
            status="issued",
        )
