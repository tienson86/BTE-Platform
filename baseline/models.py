"""Typed models for baseline infrastructure."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ValidationFinding:
    """Single validation finding."""

    code: str
    severity: str
    message: str
    path: str = ""
    object_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize finding to a plain dictionary."""
        return asdict(self)


@dataclass(slots=True)
class ValidationReport:
    """Aggregated validation report for one domain."""

    report_id: str
    domain: str
    status: str
    schema_version: str
    findings: list[ValidationFinding] = field(default_factory=list)
    statistics: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def error_count(self) -> int:
        """Count ERROR and CRITICAL findings."""
        return sum(
            1 for f in self.findings if f.severity in {"ERROR", "CRITICAL"}
        )

    @property
    def warning_count(self) -> int:
        """Count WARNING findings."""
        return sum(1 for f in self.findings if f.severity == "WARNING")

    def to_dict(self) -> dict[str, Any]:
        """Serialize report to a plain dictionary."""
        return {
            "report_id": self.report_id,
            "domain": self.domain,
            "status": self.status,
            "schema_version": self.schema_version,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "findings": [f.to_dict() for f in self.findings],
            "statistics": self.statistics,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class GraphNode:
    """Knowledge graph node."""

    node_id: str
    node_type: str
    label: str
    status: str = "official"
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize node to a plain dictionary."""
        payload = {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "label": self.label,
            "status": self.status,
        }
        if self.properties:
            payload["properties"] = self.properties
        return payload


@dataclass(slots=True)
class GraphEdge:
    """Knowledge graph edge."""

    edge_id: str
    source: str
    target: str
    edge_type: str
    relationship: str = ""
    status: str = "official"
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize edge to a plain dictionary."""
        payload = {
            "edge_id": self.edge_id,
            "source": self.source,
            "target": self.target,
            "edge_type": self.edge_type,
            "relationship": self.relationship or self.edge_type,
            "status": self.status,
        }
        if self.properties:
            payload["properties"] = self.properties
        return payload


@dataclass(slots=True)
class BuildContext:
    """Shared context for a deterministic baseline build."""

    project_root: str
    version: str
    timestamp: str
    pack_id: str
    schema_version: str
    dry_run: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Serialize build context."""
        return asdict(self)
