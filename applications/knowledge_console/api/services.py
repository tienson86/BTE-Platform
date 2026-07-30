"""Editor + approval workflow services for Knowledge Console."""

from __future__ import annotations

import uuid
from typing import Any

from applications.knowledge_console.api.diff import build_diff
from applications.knowledge_console.api.models import (
    ASSET_TYPES,
    AssetStatus,
    AssetType,
    DiffResult,
    HistoryEntry,
    KnowledgeAsset,
    ValidationIssue,
    VersionSnapshot,
    utc_now,
)
from applications.knowledge_console.api.store import AssetStore, get_store
from applications.knowledge_console.api.validators import (
    validate_asset,
    validate_asset_payload,
)


class KnowledgeEditorError(Exception):
    """Base editor error."""

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class NotFoundError(KnowledgeEditorError):
    """Asset not found."""


class ValidationError(KnowledgeEditorError):
    """Payload failed validation."""

    def __init__(
        self,
        message: str,
        *,
        issues: list[ValidationIssue],
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, details=details)
        self.issues = issues


class WorkflowError(KnowledgeEditorError):
    """Illegal lifecycle transition."""


_TRANSITIONS: dict[str, set[AssetStatus]] = {
    "submit": {"draft", "rejected"},
    "approve": {"review"},
    "reject": {"review"},
    "release": {"approved"},
}

_NEXT_STATUS: dict[str, AssetStatus] = {
    "submit": "review",
    "approve": "approved",
    "reject": "rejected",
    "release": "released",
}


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def _bump_patch(version: str) -> str:
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        return "0.1.1"
    major, minor, patch = (int(part) for part in parts)
    return f"{major}.{minor}.{patch + 1}"


class KnowledgeEditorService:
    """CRUD, validation, preview, diff, history, version, approval."""

    def __init__(self, store: AssetStore | None = None) -> None:
        self._store = store or get_store()

    def list_assets(
        self,
        *,
        asset_type: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        """List workspace assets."""
        if asset_type and asset_type not in ASSET_TYPES:
            raise ValidationError(
                "Invalid asset_type filter",
                issues=[],
                details={"asset_type": asset_type},
            )
        return [
            asset.to_dict()
            for asset in self._store.list_assets(
                asset_type=asset_type,
                status=status,
            )
        ]

    def get_asset(self, asset_id: str) -> dict[str, Any]:
        """Return one asset."""
        asset = self._require(asset_id)
        return asset.to_dict()

    def create_asset(
        self,
        *,
        asset_type: AssetType,
        title: str,
        content: dict[str, Any],
        actor: str = "editor",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a draft asset and snapshot version 0.1.0."""
        issues = validate_asset_payload(
            asset_type=asset_type,
            title=title,
            content=content,
        )
        errors = [issue for issue in issues if issue.severity == "error"]
        if errors:
            raise ValidationError(
                "Asset validation failed",
                issues=issues,
            )

        now = utc_now()
        asset_id = _new_id(asset_type[:3])
        snapshot = VersionSnapshot(
            version="0.1.0",
            created_at=now,
            created_by=actor,
            status="draft",
            content=dict(content),
            title=title,
            note="Initial draft",
        )
        history = [
            HistoryEntry(
                event_id=_new_id("evt"),
                action="created",
                actor=actor,
                at=now,
                message="Asset created as draft",
            )
        ]
        asset = KnowledgeAsset(
            asset_id=asset_id,
            asset_type=asset_type,
            title=title.strip(),
            content=dict(content),
            status="draft",
            version="0.1.0",
            created_at=now,
            updated_at=now,
            created_by=actor,
            updated_by=actor,
            history=history,
            versions=[snapshot],
            metadata=dict(metadata or {}),
        )
        return self._store.upsert(asset).to_dict()

    def update_asset(
        self,
        asset_id: str,
        *,
        title: str | None = None,
        content: dict[str, Any] | None = None,
        actor: str = "editor",
        bump_version: bool = True,
        note: str = "Edited",
    ) -> dict[str, Any]:
        """Update draft/rejected assets; snapshots a new version."""
        asset = self._require(asset_id)
        if asset.status not in {"draft", "rejected"}:
            raise WorkflowError(
                "Only draft or rejected assets can be edited",
                details={"status": asset.status},
            )
        next_title = title.strip() if title is not None else asset.title
        next_content = dict(content) if content is not None else dict(asset.content)
        issues = validate_asset_payload(
            asset_type=asset.asset_type,
            title=next_title,
            content=next_content,
        )
        errors = [issue for issue in issues if issue.severity == "error"]
        if errors:
            raise ValidationError("Asset validation failed", issues=issues)

        now = utc_now()
        if asset.status == "rejected":
            asset.status = "draft"
        if bump_version:
            asset.version = _bump_patch(asset.version)
            asset.versions.append(
                VersionSnapshot(
                    version=asset.version,
                    created_at=now,
                    created_by=actor,
                    status=asset.status,
                    content=dict(next_content),
                    title=next_title,
                    note=note,
                )
            )
        asset.title = next_title
        asset.content = next_content
        asset.updated_at = now
        asset.updated_by = actor
        asset.history.insert(
            0,
            HistoryEntry(
                event_id=_new_id("evt"),
                action="updated",
                actor=actor,
                at=now,
                message=note,
                details={"version": asset.version},
            ),
        )
        return self._store.upsert(asset).to_dict()

    def validate(self, asset_id: str) -> dict[str, Any]:
        """Run validation against current content."""
        asset = self._require(asset_id)
        issues = validate_asset(asset)
        return {
            "asset_id": asset.asset_id,
            "valid": not any(issue.severity == "error" for issue in issues),
            "issues": [issue.to_dict() for issue in issues],
        }

    def preview(self, asset_id: str) -> dict[str, Any]:
        """Render a deterministic preview payload."""
        asset = self._require(asset_id)
        content = asset.content
        if asset.asset_type == "rule":
            body = (
                f"IF {content.get('condition', '')} "
                f"THEN {content.get('action', '')} "
                f"(priority={content.get('priority', 0)})"
            )
        elif asset.asset_type == "sentence":
            body = str(content.get("template") or "")
        elif asset.asset_type == "phrase":
            body = str(content.get("text") or "")
        else:
            body = (
                f"{content.get('display_name', '')} "
                f"[{content.get('term_id', '')}] "
                f"— {content.get('domain', '')}"
            )
        return {
            "asset_id": asset.asset_id,
            "asset_type": asset.asset_type,
            "title": asset.title,
            "version": asset.version,
            "status": asset.status,
            "preview_text": body.strip(),
            "content": dict(content),
        }

    def history(self, asset_id: str) -> list[dict[str, Any]]:
        """Return history newest-first."""
        asset = self._require(asset_id)
        return [item.to_dict() for item in asset.history]

    def versions(self, asset_id: str) -> list[dict[str, Any]]:
        """Return version snapshots oldest-first."""
        asset = self._require(asset_id)
        return [item.to_dict() for item in asset.versions]

    def diff(
        self,
        asset_id: str,
        *,
        from_version: str,
        to_version: str | None = None,
    ) -> dict[str, Any]:
        """Diff two versions; omit to_version to compare against current."""
        asset = self._require(asset_id)
        left = self._version_content(asset, from_version)
        if to_version is None:
            right_content = dict(asset.content)
            right_label = f"current:{asset.version}"
        else:
            right_content = self._version_content(asset, to_version)
            right_label = to_version
        result: DiffResult = build_diff(
            asset_id=asset.asset_id,
            from_version=from_version,
            to_version=right_label,
            from_content=left,
            to_content=right_content,
        )
        return result.to_dict()

    def transition(
        self,
        asset_id: str,
        *,
        action: str,
        actor: str = "reviewer",
        message: str = "",
    ) -> dict[str, Any]:
        """Apply approval workflow transition."""
        if action not in _TRANSITIONS:
            raise WorkflowError(
                f"Unknown workflow action: {action}",
                details={"action": action},
            )
        asset = self._require(asset_id)
        allowed = _TRANSITIONS[action]
        if asset.status not in allowed:
            raise WorkflowError(
                f"Cannot {action} from status '{asset.status}'",
                details={
                    "status": asset.status,
                    "allowed_from": sorted(allowed),
                },
            )
        issues = validate_asset(asset)
        if action in {"submit", "approve", "release"} and any(
            issue.severity == "error" for issue in issues
        ):
            raise ValidationError(
                f"Cannot {action}: asset has validation errors",
                issues=issues,
            )

        now = utc_now()
        asset.status = _NEXT_STATUS[action]
        asset.updated_at = now
        asset.updated_by = actor
        if action in {"approve", "release"}:
            asset.version = _bump_patch(asset.version)
            asset.versions.append(
                VersionSnapshot(
                    version=asset.version,
                    created_at=now,
                    created_by=actor,
                    status=asset.status,
                    content=dict(asset.content),
                    title=asset.title,
                    note=message or action,
                )
            )
        asset.history.insert(
            0,
            HistoryEntry(
                event_id=_new_id("evt"),
                action=action,
                actor=actor,
                at=now,
                message=message or f"Workflow action: {action}",
                details={"status": asset.status, "version": asset.version},
            ),
        )
        return self._store.upsert(asset).to_dict()

    def approval_queue(self) -> list[dict[str, Any]]:
        """Assets awaiting review."""
        return self.list_assets(status="review")

    def _require(self, asset_id: str) -> KnowledgeAsset:
        asset = self._store.get(asset_id)
        if asset is None:
            raise NotFoundError(
                f"Asset not found: {asset_id}",
                details={"asset_id": asset_id},
            )
        return asset

    @staticmethod
    def _version_content(asset: KnowledgeAsset, version: str) -> dict[str, Any]:
        for snapshot in asset.versions:
            if snapshot.version == version:
                return dict(snapshot.content)
        raise NotFoundError(
            f"Version not found: {version}",
            details={"asset_id": asset.asset_id, "version": version},
        )


def seed_demo_assets(service: KnowledgeEditorService | None = None) -> None:
    """Seed sample assets when workspace is empty."""
    svc = service or KnowledgeEditorService()
    if svc.list_assets():
        return
    samples: list[tuple[AssetType, str, dict[str, Any]]] = [
        (
            "rule",
            "Strength strong classification",
            {
                "rule_id": "STR-001",
                "condition": "strength.classification == strong",
                "action": "select_sentence strength_strong",
                "priority": 90,
            },
        ),
        (
            "sentence",
            "Overview intro template",
            {
                "sentence_id": "overview_intro",
                "template": "Bản luận giải cho Nhật Chủ {day_master}.",
                "section_id": "overview",
                "placeholders": ["day_master"],
            },
        ),
        (
            "phrase",
            "Formal opening phrase",
            {
                "phrase_id": "OPEN_001",
                "text": "Xét tổng thể mệnh cục,",
                "type": "opening",
                "tags": ["general", "formal"],
            },
        ),
        (
            "terminology",
            "Zheng Guan Ge",
            {
                "term_id": "zheng_guan_ge",
                "display_name": "Chính Quan Cách",
                "domain": "pattern",
                "status": "active",
            },
        ),
    ]
    for asset_type, title, content in samples:
        svc.create_asset(
            asset_type=asset_type,
            title=title,
            content=content,
            actor="system",
        )
