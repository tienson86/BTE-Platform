"""Validation for Relationship Reasoning Framework."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.relationship.models import (
    RelationshipAssessment,
)
from engines.interpretation_engine.foundation.relationship.types import (
    CANONICAL_RELATIONSHIP_TYPES,
)
from engines.interpretation_engine.foundation.status import DataAvailability

MISSING_PARTICIPANT = "missing_participant"
SELF_LOOP = "self_loop"
UNKNOWN_RELATIONSHIP_TYPE = "unknown_relationship_type"
BROKEN_EVIDENCE = "broken_evidence"
DUPLICATE_EDGE = "duplicate_edge"
INVALID_CONFIDENCE = "invalid_confidence"


@dataclass(frozen=True, slots=True)
class RelationshipValidationIssue:
    """One relationship-framework validation issue."""

    code: str
    message: str
    severity: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize validation issue."""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
        }


@dataclass(frozen=True, slots=True)
class RelationshipValidationResult:
    """Outcome of relationship assessment validation."""

    passed: bool
    issues: tuple[RelationshipValidationIssue, ...]
    status: DataAvailability

    def to_dict(self) -> dict[str, Any]:
        """Serialize validation result."""
        return {
            "passed": self.passed,
            "issues": [item.to_dict() for item in self.issues],
            "status": self.status.value,
        }


def validate_relationship_assessment(
    assessment: RelationshipAssessment,
) -> RelationshipValidationResult:
    """Validate graph structure, types, evidence, and confidence."""
    issues: list[RelationshipValidationIssue] = []
    node_ids = {node.node_id for node in assessment.graph.nodes}
    evidence_ids = {item.evidence_id for item in assessment.evidence}
    seen_edges: set[tuple[str, str, str]] = set()

    _check_confidence(assessment.confidence, "assessment", issues)
    for item in assessment.evidence:
        _check_confidence(item.confidence, item.evidence_id, issues)

    for edge in assessment.graph.edges:
        _check_edge(edge, node_ids, evidence_ids, seen_edges, issues)

    for item in assessment.meaning:
        _check_refs(item.evidence_ids, evidence_ids, issues)
    for item in assessment.applications:
        _check_refs(item.evidence_ids, evidence_ids, issues)
        _check_confidence(item.confidence, item.area or "application", issues)
    for item in assessment.warnings:
        _check_refs(item.evidence_ids, evidence_ids, issues)

    has_error = any(issue.severity == "error" for issue in issues)
    if not assessment.graph.edges and assessment.status == DataAvailability.AVAILABLE:
        status = DataAvailability.MISSING
    elif has_error:
        status = DataAvailability.INVALID
    elif issues:
        status = DataAvailability.PARTIAL
    else:
        status = assessment.status
    return RelationshipValidationResult(
        passed=not has_error,
        issues=tuple(issues),
        status=status,
    )


def _check_edge(
    edge: Any,
    node_ids: set[str],
    evidence_ids: set[str],
    seen_edges: set[tuple[str, str, str]],
    issues: list[RelationshipValidationIssue],
) -> None:
    """Validate one edge against graph, type, evidence, and uniqueness."""
    if not edge.source or edge.source not in node_ids:
        issues.append(
            _issue(
                MISSING_PARTICIPANT,
                f"edge {edge.edge_id} missing source participant {edge.source!r}",
            )
        )
    if not edge.target or edge.target not in node_ids:
        issues.append(
            _issue(
                MISSING_PARTICIPANT,
                f"edge {edge.edge_id} missing target participant {edge.target!r}",
            )
        )
    if edge.source and edge.target and edge.source == edge.target:
        issues.append(
            _issue(SELF_LOOP, f"edge {edge.edge_id} is a self-loop on {edge.source!r}")
        )
    if edge.relationship_type not in CANONICAL_RELATIONSHIP_TYPES:
        issues.append(
            _issue(
                UNKNOWN_RELATIONSHIP_TYPE,
                f"edge {edge.edge_id} has unknown type {edge.relationship_type!r}",
            )
        )
    key = (edge.source, edge.target, edge.relationship_type)
    if key in seen_edges:
        issues.append(
            _issue(
                DUPLICATE_EDGE,
                f"duplicate edge {edge.source}->{edge.target}:{edge.relationship_type}",
            )
        )
    else:
        seen_edges.add(key)
    _check_confidence(edge.confidence, edge.edge_id, issues)
    _check_refs(edge.evidence_ids, evidence_ids, issues)


def _check_refs(
    refs: tuple[str, ...],
    evidence_ids: set[str],
    issues: list[RelationshipValidationIssue],
) -> None:
    """Flag evidence ids that do not resolve."""
    for ref in refs:
        if ref and ref not in evidence_ids:
            issues.append(
                _issue(BROKEN_EVIDENCE, f"missing evidence reference {ref!r}")
            )


def _check_confidence(
    value: float,
    owner: str,
    issues: list[RelationshipValidationIssue],
) -> None:
    """Flag confidence outside [0.0, 1.0]."""
    if value < 0.0 or value > 1.0:
        issues.append(
            _issue(INVALID_CONFIDENCE, f"confidence out of range on {owner}: {value}")
        )


def _issue(code: str, message: str) -> RelationshipValidationIssue:
    """Build one error-severity issue."""
    return RelationshipValidationIssue(code=code, message=message, severity="error")
