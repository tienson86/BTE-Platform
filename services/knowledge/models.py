"""Knowledge infrastructure models."""

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
    knowledge_id: str = ""


@dataclass(slots=True)
class ValidationResult:
    """Aggregated validation outcome."""

    ok: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    records_checked: int = 0
    schemas_checked: int = 0

    @property
    def errors(self) -> list[ValidationIssue]:
        """Return error-severity issues."""
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        """Return warning-severity issues."""
        return [issue for issue in self.issues if issue.severity == "warning"]


@dataclass(slots=True)
class KnowledgeRecord:
    """Loaded Knowledge Record with source metadata."""

    knowledge_id: str
    domain: str
    domain_dir: str
    path: str
    schema_name: str
    data: dict[str, Any]


@dataclass(slots=True)
class SchemaDocument:
    """Loaded JSON Schema document."""

    name: str
    path: str
    schema_id: str
    raw: dict[str, Any]


@dataclass(slots=True)
class SearchHit:
    """Search match against a knowledge record."""

    knowledge_id: str
    domain: str
    canonical_name: str
    status: str
    score: float = 1.0
    path: str = ""


@dataclass(slots=True)
class KnowledgeStats:
    """Aggregate knowledge statistics."""

    total_records: int
    by_domain: dict[str, int]
    by_status: dict[str, int]
    schema_count: int
    generated_at: str = ""
