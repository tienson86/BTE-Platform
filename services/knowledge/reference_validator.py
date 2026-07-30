"""Validate Knowledge Record references section."""

from __future__ import annotations

from services.knowledge.models import KnowledgeRecord, ValidationIssue


class ReferenceValidator:
    """Validate bibliographic / evidence references on records."""

    def validate(
        self,
        records: list[KnowledgeRecord],
        *,
        require_references_for_official: bool = True,
    ) -> list[ValidationIssue]:
        """Validate references arrays."""
        issues: list[ValidationIssue] = []
        for record in records:
            refs = record.data.get("references", [])
            metadata = record.data.get("metadata", {})
            status = (
                str(metadata.get("status", ""))
                if isinstance(metadata, dict)
                else ""
            )
            if not isinstance(refs, list):
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="invalid_references",
                        message="references must be an array",
                        path=record.path,
                        knowledge_id=record.knowledge_id,
                    )
                )
                continue

            if (
                require_references_for_official
                and status in {"official", "approved"}
                and not refs
            ):
                issues.append(
                    ValidationIssue(
                        severity="error",
                        code="missing_references",
                        message="Official/approved records require at least one reference",
                        path=record.path,
                        knowledge_id=record.knowledge_id,
                    )
                )

            seen: set[str] = set()
            for index, item in enumerate(refs):
                if not isinstance(item, dict):
                    issues.append(
                        ValidationIssue(
                            severity="error",
                            code="invalid_reference_item",
                            message=f"references[{index}] must be an object",
                            path=record.path,
                            knowledge_id=record.knowledge_id,
                        )
                    )
                    continue
                ref_id = str(item.get("reference_id", "")).strip()
                title = str(item.get("title", "")).strip()
                if not ref_id:
                    issues.append(
                        ValidationIssue(
                            severity="error",
                            code="missing_reference_id",
                            message=f"references[{index}] missing reference_id",
                            path=record.path,
                            knowledge_id=record.knowledge_id,
                        )
                    )
                if not title:
                    issues.append(
                        ValidationIssue(
                            severity="error",
                            code="missing_reference_title",
                            message=f"references[{index}] missing title",
                            path=record.path,
                            knowledge_id=record.knowledge_id,
                        )
                    )
                if ref_id:
                    if ref_id in seen:
                        issues.append(
                            ValidationIssue(
                                severity="warning",
                                code="duplicate_reference_id",
                                message=f"Duplicate reference_id within record: {ref_id}",
                                path=record.path,
                                knowledge_id=record.knowledge_id,
                            )
                        )
                    seen.add(ref_id)
        return issues
