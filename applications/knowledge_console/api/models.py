"""Domain models for Knowledge Console editor workspace."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

AssetType = Literal["rule", "sentence", "phrase", "terminology"]
AssetStatus = Literal["draft", "review", "approved", "released", "rejected"]
ApprovalAction = Literal["submit", "approve", "reject", "release"]

ASSET_TYPES: tuple[AssetType, ...] = (
    "rule",
    "sentence",
    "phrase",
    "terminology",
)


def utc_now() -> str:
    """Return ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class HistoryEntry:
    """One history event for an asset."""

    event_id: str
    action: str
    actor: str
    at: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize history entry."""
        return asdict(self)


@dataclass(slots=True)
class VersionSnapshot:
    """Immutable version snapshot of asset content."""

    version: str
    created_at: str
    created_by: str
    status: AssetStatus
    content: dict[str, Any]
    title: str
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize version snapshot."""
        return asdict(self)


@dataclass(slots=True)
class ValidationIssue:
    """Validation finding for an asset."""

    code: str
    severity: Literal["error", "warning", "info"]
    message: str
    path: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize validation issue."""
        return asdict(self)


@dataclass(slots=True)
class KnowledgeAsset:
    """Editable knowledge asset in the console workspace."""

    asset_id: str
    asset_type: AssetType
    title: str
    content: dict[str, Any]
    status: AssetStatus = "draft"
    version: str = "0.1.0"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    created_by: str = "editor"
    updated_by: str = "editor"
    history: list[HistoryEntry] = field(default_factory=list)
    versions: list[VersionSnapshot] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize asset for API responses."""
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type,
            "title": self.title,
            "content": dict(self.content),
            "status": self.status,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "history": [item.to_dict() for item in self.history],
            "versions": [item.to_dict() for item in self.versions],
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> KnowledgeAsset:
        """Rebuild asset from serialized payload."""
        return cls(
            asset_id=str(payload["asset_id"]),
            asset_type=payload["asset_type"],
            title=str(payload.get("title") or ""),
            content=dict(payload.get("content") or {}),
            status=payload.get("status") or "draft",
            version=str(payload.get("version") or "0.1.0"),
            created_at=str(payload.get("created_at") or utc_now()),
            updated_at=str(payload.get("updated_at") or utc_now()),
            created_by=str(payload.get("created_by") or "editor"),
            updated_by=str(payload.get("updated_by") or "editor"),
            history=[
                HistoryEntry(**item) for item in payload.get("history") or []
            ],
            versions=[
                VersionSnapshot(**item) for item in payload.get("versions") or []
            ],
            metadata=dict(payload.get("metadata") or {}),
        )


@dataclass(slots=True)
class DiffLine:
    """One unified-diff style line."""

    kind: Literal["equal", "add", "remove"]
    text: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize diff line."""
        return asdict(self)


@dataclass(slots=True)
class DiffResult:
    """Diff between two versions or drafts."""

    asset_id: str
    from_version: str
    to_version: str
    lines: list[DiffLine]

    def to_dict(self) -> dict[str, Any]:
        """Serialize diff result."""
        return {
            "asset_id": self.asset_id,
            "from_version": self.from_version,
            "to_version": self.to_version,
            "lines": [line.to_dict() for line in self.lines],
        }
