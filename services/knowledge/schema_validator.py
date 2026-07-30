"""Validate Knowledge Records against foundation JSON Schemas."""

from __future__ import annotations

import logging
from typing import Any

from services.knowledge.exceptions import KnowledgeSchemaError
from services.knowledge.knowledge_loader import KnowledgeLoader
from services.knowledge.models import KnowledgeRecord, ValidationIssue, ValidationResult

logger = logging.getLogger(__name__)


class SchemaValidator:
    """JSON Schema validation using knowledge/schema contracts."""

    def __init__(self, loader: KnowledgeLoader) -> None:
        """Initialize with a knowledge loader."""
        self.loader = loader

    def validate_record(self, record: KnowledgeRecord) -> list[ValidationIssue]:
        """Validate one record against its domain schema."""
        issues: list[ValidationIssue] = []
        try:
            schema_doc = self.loader.schema_loader.schema_for_domain(record.domain_dir)
        except KnowledgeSchemaError as exc:
            return [
                ValidationIssue(
                    severity="error",
                    code="missing_schema_mapping",
                    message=str(exc),
                    path=record.path,
                    knowledge_id=record.knowledge_id,
                )
            ]

        validator = self._build_validator(schema_doc.raw)
        for error in validator.iter_errors(record.data):
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="schema_validation",
                    message=error.message,
                    path=record.path,
                    knowledge_id=record.knowledge_id,
                )
            )
        return issues

    def validate_all(
        self,
        records: list[KnowledgeRecord] | None = None,
    ) -> ValidationResult:
        """Validate all records."""
        payload = records if records is not None else self.loader.load_records()
        result = ValidationResult(ok=True, schemas_checked=len(self.loader.load_schemas()))
        for record in payload:
            result.records_checked += 1
            result.issues.extend(self.validate_record(record))
        result.ok = not result.errors
        return result

    def validate_foundation_schemas(self) -> ValidationResult:
        """Validate that foundation schemas themselves are Draft 2020-12 compliant."""
        from jsonschema import Draft202012Validator
        from jsonschema.exceptions import SchemaError

        result = ValidationResult(ok=True)
        for doc in self.loader.load_schemas():
            result.schemas_checked += 1
            try:
                Draft202012Validator.check_schema(doc.raw)
            except SchemaError as exc:
                result.issues.append(
                    ValidationIssue(
                        severity="error",
                        code="invalid_foundation_schema",
                        message=str(exc),
                        path=doc.path,
                    )
                )
        result.ok = not result.errors
        return result

    def _build_validator(self, schema: dict[str, Any]) -> Any:
        try:
            from jsonschema import Draft202012Validator
        except ImportError as exc:
            raise KnowledgeSchemaError(
                "jsonschema is required for schema validation"
            ) from exc
        registry = self.loader.schema_loader.build_registry()
        return Draft202012Validator(schema, registry=registry)
