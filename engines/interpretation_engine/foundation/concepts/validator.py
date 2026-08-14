"""Concept validation for interpretation concept layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.concepts.categories import (
    CANONICAL_CONCEPT_CATEGORIES,
)
from engines.interpretation_engine.foundation.concepts.entity import ConceptEntity
from engines.interpretation_engine.foundation.concepts.relationships import (
    CANONICAL_RELATIONSHIP_TYPES,
)


@dataclass(frozen=True, slots=True)
class ConceptValidationIssue:
    """One concept validation issue."""

    code: str
    message: str
    concept_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize issue."""
        return {
            "code": self.code,
            "message": self.message,
            "concept_id": self.concept_id,
        }


@dataclass(frozen=True, slots=True)
class ConceptValidationResult:
    """Outcome of concept validation."""

    passed: bool
    issues: tuple[ConceptValidationIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize validation result."""
        return {
            "passed": self.passed,
            "issues": [item.to_dict() for item in self.issues],
        }


class ConceptValidator:
    """Validate loaded concept entities and graph links."""

    def validate(self, concepts: list[ConceptEntity]) -> ConceptValidationResult:
        """Run all validation checks."""
        issues: list[ConceptValidationIssue] = []
        seen_ids: set[str] = set()
        index: dict[str, ConceptEntity] = {}

        for concept in concepts:
            if not concept.id:
                issues.append(
                    ConceptValidationIssue(
                        code="missing_id",
                        message="concept missing id",
                    )
                )
            elif concept.id in seen_ids:
                issues.append(
                    ConceptValidationIssue(
                        code="duplicate_id",
                        message=f"duplicate id: {concept.id}",
                        concept_id=concept.id,
                    )
                )
            seen_ids.add(concept.id)

            if concept.category not in CANONICAL_CONCEPT_CATEGORIES:
                issues.append(
                    ConceptValidationIssue(
                        code="unknown_category",
                        message=f"unknown category: {concept.category}",
                        concept_id=concept.id,
                    )
                )

            if not concept.metadata.author or not concept.metadata.version:
                issues.append(
                    ConceptValidationIssue(
                        code="invalid_metadata",
                        message="metadata missing author or version",
                        concept_id=concept.id,
                    )
                )

            index[concept.id] = concept

        for concept in concepts:
            for rel in concept.related_concepts:
                if rel.relationship.value not in CANONICAL_RELATIONSHIP_TYPES:
                    issues.append(
                        ConceptValidationIssue(
                            code="unknown_relationship",
                            message=f"unknown relationship: {rel.relationship.value}",
                            concept_id=concept.id,
                        )
                    )

                if not rel.target_id:
                    issues.append(
                        ConceptValidationIssue(
                            code="broken_reference",
                            message=f"empty concept reference on {concept.id}",
                            concept_id=concept.id,
                        )
                    )
                    continue

                if rel.target_id == concept.id:
                    issues.append(
                        ConceptValidationIssue(
                            code="circular_self_reference",
                            message=f"self-reference on {concept.id}",
                            concept_id=concept.id,
                        )
                    )
                    continue

                if rel.target_id not in index:
                    issues.append(
                        ConceptValidationIssue(
                            code="broken_reference",
                            message=(
                                f"unresolved concept reference {rel.target_id} "
                                f"from {concept.id}"
                            ),
                            concept_id=concept.id,
                        )
                    )

        return ConceptValidationResult(
            passed=not issues,
            issues=tuple(issues),
        )
