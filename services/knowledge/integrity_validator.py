"""Integrity checks for Knowledge Records (IDs, duplicates, domain consistency)."""

from __future__ import annotations

import re

from services.knowledge.constants import DOMAIN_CONST_MAP, KNOWLEDGE_ID_PATTERN
from services.knowledge.models import KnowledgeRecord, ValidationIssue


class IntegrityValidator:
    """Validate identity integrity and cross-record uniqueness."""

    def __init__(self) -> None:
        """Initialize integrity validator."""
        self._id_re = re.compile(KNOWLEDGE_ID_PATTERN)

    def validate(self, records: list[KnowledgeRecord]) -> list[ValidationIssue]:
        """Run integrity checks."""
        issues: list[ValidationIssue] = []
        seen_ids: dict[str, str] = {}

        for record in records:
            identity = record.data.get("identity", {})
            classification = record.data.get("classification", {})
            if not isinstance(identity, dict):
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="missing_identity",
                        message="identity object is required",
                        path=record.path,
                    )
                )
                continue

            knowledge_id = str(identity.get("knowledge_id", "")).strip()
            if not knowledge_id:
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="missing_knowledge_id",
                        message="identity.knowledge_id is required",
                        path=record.path,
                    )
                )
            elif not self._id_re.match(knowledge_id):
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="invalid_knowledge_id",
                        message=f"Invalid knowledge_id: {knowledge_id}",
                        path=record.path,
                        knowledge_id=knowledge_id,
                    )
                )
            else:
                prior = seen_ids.get(knowledge_id)
                if prior:
                    issues.append(
                        ValidationIssue(
                            severity="error",
                            code="duplicate_knowledge_id",
                            message=(
                                f"Duplicate knowledge_id {knowledge_id} "
                                f"(also {prior})"
                            ),
                            path=record.path,
                            knowledge_id=knowledge_id,
                        )
                    )
                else:
                    seen_ids[knowledge_id] = record.path

            expected_domain = DOMAIN_CONST_MAP.get(record.domain_dir)
            if (
                expected_domain
                and isinstance(classification, dict)
                and classification.get("domain")
                and str(classification.get("domain")) != expected_domain
            ):
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="domain_mismatch",
                        message=(
                            f"classification.domain "
                            f"'{classification.get('domain')}' does not match "
                            f"directory '{record.domain_dir}'"
                        ),
                        path=record.path,
                        knowledge_id=knowledge_id,
                    )
                )
        return issues
