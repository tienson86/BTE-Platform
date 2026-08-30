"""Append-only Golden Case freeze files and registry. Never overwrite."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from engines.narrative_v2.golden.golden_case import GoldenCase
from engines.narrative_v2.golden.golden_errors import GoldenImmutabilityError
from engines.narrative_v2.golden.golden_registry import GoldenRegistryEntry, latest_version

DEFAULT_ROOT = (
    Path(__file__).resolve().parents[3] / "implementation" / "narrative_v2" / "golden"
)


class GoldenHistory:
    """JSON freeze store. Versions are append-only."""

    def __init__(self, root: Path | None = None) -> None:
        self._root = root or DEFAULT_ROOT

    def case_path(self, case_id: str, version: int) -> Path:
        """Return the freeze file path for one version."""
        return self._root / "cases" / case_id / f"v{version}.json"

    def registry_path(self) -> Path:
        """Return the append-only registry path."""
        return self._root / "registry.json"

    def load_case(self, case_id: str, version: int) -> GoldenCase | None:
        """Load one frozen version, or None when absent."""
        path = self.case_path(case_id, version)
        if not path.exists():
            return None
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            return None
        return GoldenCase.from_record(raw)

    def list_registry(self) -> list[GoldenRegistryEntry]:
        """Return all registry rows, oldest first."""
        path = self.registry_path()
        if not path.exists():
            return []
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return []
        return [
            GoldenRegistryEntry.from_record(item)
            for item in raw
            if isinstance(item, dict)
        ]

    def next_version(self, case_id: str) -> int:
        """Next append-only version number for a case."""
        return latest_version(self.list_registry(), case_id) + 1

    def latest(self, case_id: str) -> GoldenCase | None:
        """Return the highest frozen version for a case."""
        version = latest_version(self.list_registry(), case_id)
        if version <= 0:
            return None
        return self.load_case(case_id, version)

    def append(self, case: GoldenCase, entry: GoldenRegistryEntry) -> None:
        """Write a new version. Existing freeze files are never rewritten."""
        path = self.case_path(case.case_id, case.version)
        if path.exists():
            raise GoldenImmutabilityError(f"version_exists:{case.case_id}:v{case.version}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(case.to_record(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        rows = [item.to_record() for item in self.list_registry()]
        rows.append(entry.to_record())
        registry = self.registry_path()
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def registry_records(self) -> list[dict[str, Any]]:
        """Plain registry rows for artifacts and tests."""
        return [row.to_record() for row in self.list_registry()]
