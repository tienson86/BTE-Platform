"""Relationship Reasoning Framework — reusable interaction contracts."""

from engines.interpretation_engine.foundation.relationship.explainer import (
    GenericRelationshipExplainer,
)
from engines.interpretation_engine.foundation.relationship.metrics import (
    compute_relationship_metrics,
)
from engines.interpretation_engine.foundation.relationship.models import (
    RelationshipApplication,
    RelationshipAssessment,
    RelationshipEdge,
    RelationshipEvidence,
    RelationshipGraph,
    RelationshipInput,
    RelationshipMeaning,
    RelationshipMetrics,
    RelationshipNode,
    RelationshipRecord,
    RelationshipWarning,
)
from engines.interpretation_engine.foundation.relationship.protocol import (
    RelationshipExplainer,
)
from engines.interpretation_engine.foundation.relationship.types import (
    CANONICAL_RELATIONSHIP_TYPES,
)
from engines.interpretation_engine.foundation.relationship.validation import (
    BROKEN_EVIDENCE,
    DUPLICATE_EDGE,
    INVALID_CONFIDENCE,
    MISSING_PARTICIPANT,
    SELF_LOOP,
    UNKNOWN_RELATIONSHIP_TYPE,
    RelationshipValidationIssue,
    validate_relationship_assessment,
)

__all__ = [
    "BROKEN_EVIDENCE",
    "CANONICAL_RELATIONSHIP_TYPES",
    "DUPLICATE_EDGE",
    "INVALID_CONFIDENCE",
    "MISSING_PARTICIPANT",
    "SELF_LOOP",
    "UNKNOWN_RELATIONSHIP_TYPE",
    "GenericRelationshipExplainer",
    "RelationshipApplication",
    "RelationshipAssessment",
    "RelationshipEdge",
    "RelationshipEvidence",
    "RelationshipExplainer",
    "RelationshipGraph",
    "RelationshipInput",
    "RelationshipMeaning",
    "RelationshipMetrics",
    "RelationshipNode",
    "RelationshipRecord",
    "RelationshipValidationIssue",
    "RelationshipWarning",
    "compute_relationship_metrics",
    "validate_relationship_assessment",
]
