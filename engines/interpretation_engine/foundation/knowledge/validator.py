"""Knowledge validation for interpretation knowledge system."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.knowledge.domains import CANONICAL_KNOWLEDGE_DOMAINS
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    CANONICAL_KNOWLEDGE_ENTITY_TYPES,
    KNOWLEDGE_ENTITY_TYPE_STATE,
    STRENGTH_STATE_KEYS,
    USEFUL_GOD_ROLE_KEYS,
    USEFUL_GOD_STEM_KEYS,
)


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
        role_keys_seen: dict[str, str] = {}
        state_keys_seen: dict[str, str] = {}
        stem_keys = set(USEFUL_GOD_STEM_KEYS)
        role_keys = set(USEFUL_GOD_ROLE_KEYS)
        state_keys = set(STRENGTH_STATE_KEYS)

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

            if entity.domain == "UsefulGod":
                issues.extend(
                    _useful_god_type_issues(
                        entity,
                        stem_keys=stem_keys,
                        role_keys=role_keys,
                        role_keys_seen=role_keys_seen,
                    )
                )
            if entity.domain == "Strength":
                issues.extend(
                    _strength_state_issues(
                        entity,
                        state_keys=state_keys,
                        state_keys_seen=state_keys_seen,
                    )
                )

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


def _useful_god_type_issues(
    entity: KnowledgeEntity,
    *,
    stem_keys: set[str],
    role_keys: set[str],
    role_keys_seen: dict[str, str],
) -> list[KnowledgeValidationIssue]:
    """Validate explicit entity_type for Useful God entities."""
    issues: list[KnowledgeValidationIssue] = []
    entity_type = entity.entity_type.strip()
    if not entity_type:
        issues.append(
            KnowledgeValidationIssue(
                code="unknown_entity_type",
                message="Useful God entity missing entity_type",
                entity_id=entity.id,
            )
        )
        return issues

    if entity_type not in CANONICAL_KNOWLEDGE_ENTITY_TYPES:
        issues.append(
            KnowledgeValidationIssue(
                code="unknown_entity_type",
                message=f"unknown entity_type: {entity_type}",
                entity_id=entity.id,
            )
        )
        return issues

    if entity_type == "stem" and entity.key in role_keys:
        issues.append(
            KnowledgeValidationIssue(
                code="entity_type_mismatch",
                message=f"role key {entity.key} declared as stem",
                entity_id=entity.id,
            )
        )
    if entity_type == "role" and entity.key in stem_keys:
        issues.append(
            KnowledgeValidationIssue(
                code="entity_type_mismatch",
                message=f"stem key {entity.key} declared as role",
                entity_id=entity.id,
            )
        )
    if entity_type == "element" and (
        entity.key in stem_keys or entity.key in role_keys
    ):
        issues.append(
            KnowledgeValidationIssue(
                code="entity_type_mismatch",
                message=f"non-element key {entity.key} declared as element",
                entity_id=entity.id,
            )
        )

    if entity_type == "stem" and not entity.concept_ids:
        issues.append(
            KnowledgeValidationIssue(
                code="stem_missing_concept",
                message="stem entity missing concept_ids",
                entity_id=entity.id,
            )
        )
    if entity_type == "role" and not entity.concept_ids:
        issues.append(
            KnowledgeValidationIssue(
                code="role_missing_concept",
                message="role entity missing concept_ids",
                entity_id=entity.id,
            )
        )

    if entity_type == "role":
        previous = role_keys_seen.get(entity.key)
        if previous:
            issues.append(
                KnowledgeValidationIssue(
                    code="duplicate_role_entity",
                    message=f"duplicate role entity for key {entity.key}",
                    entity_id=entity.id,
                )
            )
        else:
            role_keys_seen[entity.key] = entity.id

    return issues


def _strength_state_issues(
    entity: KnowledgeEntity,
    *,
    state_keys: set[str],
    state_keys_seen: dict[str, str],
) -> list[KnowledgeValidationIssue]:
    """Validate Strength state entities against engine inventory."""
    issues: list[KnowledgeValidationIssue] = []
    entity_type = entity.entity_type.strip()
    if not entity_type:
        issues.append(
            KnowledgeValidationIssue(
                code="unknown_entity_type",
                message="Strength entity missing entity_type",
                entity_id=entity.id,
            )
        )
    elif entity_type != KNOWLEDGE_ENTITY_TYPE_STATE:
        code = (
            "unknown_entity_type"
            if entity_type not in CANONICAL_KNOWLEDGE_ENTITY_TYPES
            else "entity_type_mismatch"
        )
        issues.append(
            KnowledgeValidationIssue(
                code=code,
                message=f"Strength entity_type must be state, got {entity_type}",
                entity_id=entity.id,
            )
        )

    if entity.key and entity.key not in state_keys:
        issues.append(
            KnowledgeValidationIssue(
                code="invalid_state",
                message=f"invalid Strength state key: {entity.key}",
                entity_id=entity.id,
            )
        )

    if not entity.concept_ids:
        issues.append(
            KnowledgeValidationIssue(
                code="strength_missing_concept",
                message="Strength entity missing concept_ids",
                entity_id=entity.id,
            )
        )

    previous = state_keys_seen.get(entity.key)
    if previous:
        issues.append(
            KnowledgeValidationIssue(
                code="duplicate_state",
                message=f"duplicate Strength state entity for key {entity.key}",
                entity_id=entity.id,
            )
        )
    elif entity.key:
        state_keys_seen[entity.key] = entity.id

    return issues
