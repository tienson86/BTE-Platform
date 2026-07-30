"""Registry infrastructure result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ValidationIssue:
    """A single validation finding."""

    severity: str
    code: str
    message: str
    path: str = ""
    registry_id: str = ""


@dataclass(slots=True)
class ValidationResult:
    """Aggregated validation outcome."""

    ok: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    catalogs_checked: int = 0
    records_checked: int = 0

    @property
    def errors(self) -> list[ValidationIssue]:
        """Return error-severity issues."""
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        """Return warning-severity issues."""
        return [issue for issue in self.issues if issue.severity == "warning"]


@dataclass(slots=True)
class RegistryCatalog:
    """Loaded registry catalog container."""

    name: str
    path: str
    version: str
    prefix: str
    description: str
    records: list[dict[str, Any]]
    raw: dict[str, Any]
    checksum: str


@dataclass(slots=True)
class IndexEntry:
    """A single derived index entry."""

    key: str
    registry_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RegistryIndex:
    """Derived in-memory index."""

    name: str
    entries: list[IndexEntry] = field(default_factory=list)


@dataclass(slots=True)
class SearchHit:
    """A search match against a registry record."""

    registry_name: str
    registry_id: str
    object_id: str
    canonical_name: str
    status: str
    score: float = 1.0


@dataclass(slots=True)
class StatisticsSnapshot:
    """Aggregate registry statistics."""

    total_records: int
    by_registry: dict[str, int]
    by_status: dict[str, int]
    by_namespace: dict[str, int]
    generated_at: str = ""
