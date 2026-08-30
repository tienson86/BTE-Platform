"""Release Freeze. Records V1.0 baseline. Does not change Runtime or Presentation."""

from __future__ import annotations

import json
from pathlib import Path

from engines.narrative_v2.release.release_errors import ReleaseError
from engines.narrative_v2.release.release_manifest import (
    FREEZE_STATUS_FROZEN,
    ReleaseManifest,
    build_v1_manifest,
)

DEFAULT_MANIFEST = (
    Path(__file__).resolve().parents[3]
    / "implementation"
    / "narrative_release"
    / "release_manifest_v1.json"
)


class ReleaseFreezeError(ReleaseError):
    """Freeze already recorded or freeze file is invalid."""


class ReleaseFreeze:
    """Write-once V1.0 freeze. Existing freeze files are never rewritten."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or DEFAULT_MANIFEST

    @property
    def path(self) -> Path:
        """Freeze file path."""
        return self._path

    def is_frozen(self) -> bool:
        """True when a V1.0 freeze record exists."""
        if not self._path.exists():
            return False
        return self.load().freeze_status == FREEZE_STATUS_FROZEN

    def load(self) -> ReleaseManifest:
        """Load the freeze record."""
        if not self._path.exists():
            raise ReleaseFreezeError("freeze_not_recorded")
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ReleaseFreezeError("invalid_freeze_record")
        return ReleaseManifest.from_record(raw)

    def write(self, manifest: ReleaseManifest | None = None) -> ReleaseManifest:
        """Record Freeze once. Refuses overwrite of an existing freeze."""
        if self._path.exists():
            raise ReleaseFreezeError("freeze_already_recorded")
        record = manifest or build_v1_manifest()
        if record.freeze_status != FREEZE_STATUS_FROZEN:
            raise ReleaseFreezeError("freeze_status_required")
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(record.to_record(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return record
