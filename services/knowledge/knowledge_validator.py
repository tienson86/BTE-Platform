"""Composite Knowledge Validator orchestrating all validation stages."""

from __future__ import annotations

from services.knowledge.integrity_validator import IntegrityValidator
from services.knowledge.knowledge_loader import KnowledgeLoader
from services.knowledge.models import KnowledgeRecord, ValidationResult
from services.knowledge.reference_validator import ReferenceValidator
from services.knowledge.relationship_validator import RelationshipValidator
from services.knowledge.schema_validator import SchemaValidator


class KnowledgeValidator:
    """Run schema, relationship, reference, and integrity validation."""

    def __init__(self, loader: KnowledgeLoader) -> None:
        """Initialize composite validator."""
        self.loader = loader
        self.schema_validator = SchemaValidator(loader)
        self.relationship_validator = RelationshipValidator()
        self.reference_validator = ReferenceValidator()
        self.integrity_validator = IntegrityValidator()

    def validate_all(
        self,
        records: list[KnowledgeRecord] | None = None,
        *,
        check_foundation_schemas: bool = True,
        check_schema: bool = True,
        check_relationships: bool = True,
        check_references: bool = True,
        check_integrity: bool = True,
    ) -> ValidationResult:
        """Validate foundation schemas and/or knowledge records."""
        result = ValidationResult(ok=True)
        if check_foundation_schemas:
            foundation = self.schema_validator.validate_foundation_schemas()
            result.schemas_checked = foundation.schemas_checked
            result.issues.extend(foundation.issues)

        payload = records if records is not None else self.loader.load_records()
        result.records_checked = len(payload)

        if check_integrity:
            result.issues.extend(self.integrity_validator.validate(payload))
        if check_schema and payload:
            schema_result = self.schema_validator.validate_all(payload)
            result.issues.extend(schema_result.issues)
        if check_relationships:
            result.issues.extend(self.relationship_validator.validate(payload))
        if check_references:
            result.issues.extend(self.reference_validator.validate(payload))

        result.ok = not result.errors
        return result
