"""Knowledge validation for interpretation knowledge system."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.knowledge.domains import CANONICAL_KNOWLEDGE_DOMAINS
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity


@dataclass(frozen=True, slots=True)
class KnowledgeValidationIssue:
    """One validation issue."""

    code: str
    message: str
    entity_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize issue."""
        return {
            "code": self.code,
            "message": self.message,
            "entity_id": self.entity_id,
        }


@dataclass(frozen=True, slots=True)
class KnowledgeValidationResult:
    """Outcome of knowledge validation."""

    passed: bool
    issues: tuple[KnowledgeValidationIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize validation result."""
        return {
            "passed": self.passed,
            "issues": [item.to_dict() for item in self.issues],
        }


class KnowledgeValidator:
    """Validate loaded knowledge entities."""

    def validate(
        self,
        entities: list[KnowledgeEntity],
        *,
        known_concept_ids: frozenset[str] | None = None,
    ) -> KnowledgeValidationResult:
        """Run all validation checks."""
        issues: list[KnowledgeValidationIssue] = []
        seen_ids: set[str] = set()
        index: dict[tuple[str, str], KnowledgeEntity] = {}

        for entity in entities:
            if not entity.id:
                issues.append(
                    KnowledgeValidationIssue(
                        code="missing_id",
                        message="entity missing id",
                    )
                )
            elif entity.id in seen_ids:
                issues.append(
                    KnowledgeValidationIssue(
                        code="duplicate_id",
                        message=f"duplicate id: {entity.id}",
                        entity_id=entity.id,
                    )
                )
            seen_ids.add(entity.id)

            if not entity.key:
                issues.append(
                    KnowledgeValidationIssue(
                        code="missing_key",
                        message="entity missing key",
                        entity_id=entity.id,
                    )
                )

            if entity.domain not in CANONICAL_KNOWLEDGE_DOMAINS:
                issues.append(
                    KnowledgeValidationIssue(
                        code="unknown_domain",
                        message=f"unknown domain: {entity.domain}",
                        entity_id=entity.id,
                    )
                )

            if not entity.metadata.author or not entity.metadata.version:
                issues.append(
                    KnowledgeValidationIssue(
                        code="invalid_metadata",
                        message="metadata missing author or version",
                        entity_id=entity.id,
                    )
                )

            pair = (entity.domain, entity.key)
            if pair in index:
                issues.append(
                    KnowledgeValidationIssue(
                        code="duplicate_domain_key",
                        message=f"duplicate domain/key: {entity.domain}/{entity.key}",
                        entity_id=entity.id,
                    )
                )
            index[pair] = entity

        for entity in entities:
            for ref in entity.related_entities:
                if not ref.domain or not ref.key:
                    issues.append(
                        KnowledgeValidationIssue(
                            code="broken_reference",
                            message=f"empty reference on {entity.id}",
                            entity_id=entity.id,
                        )
                    )
                    continue
                if (ref.domain, ref.key) not in index:
                    issues.append(
                        KnowledgeValidationIssue(
                            code="broken_reference",
                            message=(
                                f"unresolved reference {ref.domain}/{ref.key} "
                                f"from {entity.id}"
                            ),
                            entity_id=entity.id,
                        )
                    )

            if known_concept_ids is not None:
                for concept_id in entity.concept_ids:
                    if concept_id not in known_concept_ids:
                        issues.append(
                            KnowledgeValidationIssue(
                                code="broken_concept_reference",
                                message=(
                                    f"unresolved concept reference {concept_id} "
                                    f"from {entity.id}"
                                ),
                                entity_id=entity.id,
                            )
                        )

        return KnowledgeValidationResult(
            passed=not issues,
            issues=tuple(issues),
        )
