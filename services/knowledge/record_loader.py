"""Load Knowledge Record JSON files from Knowledge Canon domains."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from services.knowledge.cache import MtimeCache
from services.knowledge.constants import (
    DEFAULT_CANON_ROOT_RELATIVE,
    DOMAIN_SCHEMA_MAP,
    SCHEMA_FILENAME_SUFFIX,
)
from services.knowledge.exceptions import KnowledgeLoadError
from services.knowledge.models import KnowledgeRecord

logger = logging.getLogger(__name__)


class RecordLoader:
    """Discover and load Knowledge Record JSON payloads."""

    def __init__(self, canon_root: str | Path) -> None:
        """Initialize record loader."""
        self.canon_root = Path(canon_root).resolve()
        self._cache: MtimeCache[KnowledgeRecord] = MtimeCache()

    @classmethod
    def from_project_root(cls, project_root: str | Path) -> RecordLoader:
        """Build loader from repository root."""
        root = Path(project_root).resolve() / DEFAULT_CANON_ROOT_RELATIVE
        return cls(root)

    def clear_cache(self) -> None:
        """Clear record cache."""
        self._cache.clear()

    def list_domain_dirs(self) -> list[str]:
        """Return mapped Canon domain directory names that exist."""
        domains: list[str] = []
        for domain_dir in DOMAIN_SCHEMA_MAP:
            if (self.canon_root / domain_dir).is_dir():
                domains.append(domain_dir)
        return domains

    def list_record_paths(self, domain_dir: str | None = None) -> list[Path]:
        """List JSON record paths, excluding schema pointer files."""
        domains = [domain_dir] if domain_dir else self.list_domain_dirs()
        paths: list[Path] = []
        for name in domains:
            folder = self.canon_root / name
            if not folder.is_dir():
                continue
            for path in sorted(folder.rglob("*.json")):
                if path.name.endswith(SCHEMA_FILENAME_SUFFIX):
                    continue
                # Skip non-record JSON helpers if any appear later.
                if path.name in {"package.json", "package-lock.json"}:
                    continue
                paths.append(path.resolve())
        return paths

    def load_record(self, path: str | Path, *, domain_dir: str | None = None) -> KnowledgeRecord:
        """Load one Knowledge Record JSON file."""
        record_path = Path(path).resolve()
        cached = self._cache.get(record_path)
        if cached is not None:
            return cached
        if not record_path.exists():
            raise KnowledgeLoadError(f"Record not found: {record_path}")

        raw = self._read_json(record_path)
        resolved_domain = domain_dir or self._infer_domain_dir(record_path)
        schema_name = DOMAIN_SCHEMA_MAP.get(resolved_domain, "")
        identity = raw.get("identity", {}) if isinstance(raw, dict) else {}
        knowledge_id = (
            str(identity.get("knowledge_id", ""))
            if isinstance(identity, dict)
            else ""
        )
        classification = raw.get("classification", {}) if isinstance(raw, dict) else {}
        domain_const = (
            str(classification.get("domain", ""))
            if isinstance(classification, dict)
            else ""
        )
        record = KnowledgeRecord(
            knowledge_id=knowledge_id,
            domain=domain_const or resolved_domain,
            domain_dir=resolved_domain,
            path=str(record_path),
            schema_name=schema_name,
            data=raw if isinstance(raw, dict) else {},
        )
        return self._cache.set(record_path, record)

    def load_domain(self, domain_dir: str) -> list[KnowledgeRecord]:
        """Load all records for one domain directory."""
        return [
            self.load_record(path, domain_dir=domain_dir)
            for path in self.list_record_paths(domain_dir)
        ]

    def load_all(self) -> list[KnowledgeRecord]:
        """Load all discoverable Knowledge Records."""
        records: list[KnowledgeRecord] = []
        for domain_dir in self.list_domain_dirs():
            records.extend(self.load_domain(domain_dir))
        logger.debug("Loaded %s knowledge records", len(records))
        return records

    def _infer_domain_dir(self, path: Path) -> str:
        try:
            relative = path.relative_to(self.canon_root)
        except ValueError as exc:
            raise KnowledgeLoadError(
                f"Record path is outside canon root: {path}"
            ) from exc
        parts = relative.parts
        if not parts:
            raise KnowledgeLoadError(f"Unable to infer domain for {path}")
        return parts[0]

    def _read_json(self, path: Path) -> dict[str, Any]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise KnowledgeLoadError(f"Invalid record JSON {path}: {exc}") from exc
        except OSError as exc:
            raise KnowledgeLoadError(f"Unable to read record {path}: {exc}") from exc
        if not isinstance(payload, dict):
            raise KnowledgeLoadError(f"Record root must be object: {path}")
        return payload
