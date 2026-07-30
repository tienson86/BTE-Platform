"""Validate Knowledge Record relationships and dependency integrity."""

from __future__ import annotations

import re
from collections import defaultdict

from services.knowledge.constants import KNOWLEDGE_ID_PATTERN
from services.knowledge.dependency_loader import DependencyLoader
from services.knowledge.models import KnowledgeRecord, ValidationIssue


class RelationshipValidator:
    """Validate relationship structure and dependency references."""

    def __init__(self) -> None:
        """Initialize relationship validator."""
        self._id_re = re.compile(KNOWLEDGE_ID_PATTERN)
        self._deps = DependencyLoader()

    def validate(
        self,
        records: list[KnowledgeRecord],
    ) -> list[ValidationIssue]:
        """Validate relationships across the record set."""
        issues: list[ValidationIssue] = []
        known = {record.knowledge_id for record in records if record.knowledge_id}
        edges = self._deps.load_edges(records)

        for record in records:
            relationships = record.data.get("relationships", {})
            if relationships is None:
                continue
            if not isinstance(relationships, dict):
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="invalid_relationships",
                        message="relationships must be an object",
                        path=record.path,
                        knowledge_id=record.knowledge_id,
                    )
                )
                continue
            for key, value in relationships.items():
                issues.extend(
                    self._validate_relationship_value(
                        record,
                        key,
                        value,
                        known,
                    )
                )

        # Pairwise circular detection
        for src, deps in edges.items():
            for dep in deps:
                if src in edges.get(dep, []):
                    issues.append(
                        ValidationIssue(
                            severity="error",
                            code="circular_relationship",
                            message=f"Circular relationship between {src} and {dep}",
                            knowledge_id=src,
                        )
                    )
        return issues

    def _validate_relationship_value(
        self,
        record: KnowledgeRecord,
        key: str,
        value: object,
        known: set[str],
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        links: list[dict[str, object]] = []
        if isinstance(value, dict):
            links = [value]
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    links.append(item)
                else:
                    issues.append(
                        ValidationIssue(
                            severity="error",
                            code="invalid_relationship_item",
                            message=f"relationships.{key} items must be objects",
                            path=record.path,
                            knowledge_id=record.knowledge_id,
                        )
                    )
        else:
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="invalid_relationship_value",
                    message=f"relationships.{key} must be object or array",
                    path=record.path,
                    knowledge_id=record.knowledge_id,
                )
            )
            return issues

        for link in links:
            kid = str(link.get("knowledge_id", "")).strip()
            rel_type = str(link.get("relationship_type", "")).strip()
            if kid and not self._id_re.match(kid):
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="invalid_relationship_id",
                        message=f"Invalid relationship knowledge_id: {kid}",
                        path=record.path,
                        knowledge_id=record.knowledge_id,
                    )
                )
            if kid and known and kid not in known:
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="broken_relationship",
                        message=f"Relationship target not found: {kid}",
                        path=record.path,
                        knowledge_id=record.knowledge_id,
                    )
                )
            if key in {"depends_on", "related_to", "see_also"} and kid and not rel_type:
                issues.append(
                    ValidationIssue(
                        severity="warning",
                        code="missing_relationship_type",
                        message=f"relationships.{key} missing relationship_type",
                        path=record.path,
                        knowledge_id=record.knowledge_id,
                    )
                )
        return issues
