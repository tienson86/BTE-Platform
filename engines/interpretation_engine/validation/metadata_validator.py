"""Metadata validator for Pack 03 output metadata.

Infrastructure only. No BaZi logic.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.models.metadata import Metadata
from engines.interpretation_engine.validation.models import (
    ValidationDomain,
    ValidationIssue,
    ValidationReport,
)


class MetadataValidator:
    """Validate Pack 03 Metadata structural integrity."""

    def validate(self, metadata: Any) -> ValidationReport:
        """Validate a Metadata instance."""
        domain = ValidationDomain.METADATA.value
        if metadata is None:
            issue = ValidationIssue(
                code="metadata_required",
                domain=domain,
                message="metadata is required",
            )
            return ValidationReport(
                success=False,
                messages=("metadata_required",),
                issues=(issue,),
                domain=domain,
            )
        if not isinstance(metadata, Metadata):
            issue = ValidationIssue(
                code="metadata_type_invalid",
                domain=domain,
                message="Metadata type required",
                attributes={"type": type(metadata).__name__},
            )
            return ValidationReport(
                success=False,
                messages=("metadata_type_invalid",),
                issues=(issue,),
                domain=domain,
            )
        if not metadata.validate():
            issue = ValidationIssue(
                code="metadata_integrity_failed",
                domain=domain,
                message="metadata structural validation failed",
                attributes={"id": metadata.id},
            )
            return ValidationReport(
                success=False,
                messages=("metadata_integrity_failed",),
                issues=(issue,),
                domain=domain,
            )
        return ValidationReport(
            success=True,
            messages=("metadata_ok",),
            details={
                "id": metadata.id,
                "created_at": metadata.created_at,
                "schema_version": metadata.version_info.schema_version,
            },
            domain=domain,
        )
