"""Pack 03 Validation Framework facade.

Validates:
- Contracts
- Registries
- Context
- Metadata
- Dependencies
- Versions

Dependency Injection only. No singleton. No BaZi logic.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping

from engines.interpretation_engine.runtime.contracts import RuntimeContract
from engines.interpretation_engine.runtime.registry_base import BaseRegistry
from engines.interpretation_engine.validation.context_validator import ContextValidator
from engines.interpretation_engine.validation.contract_validator import ContractValidator
from engines.interpretation_engine.validation.dependency_validator import (
    DependencyValidator,
)
from engines.interpretation_engine.validation.metadata_validator import MetadataValidator
from engines.interpretation_engine.validation.models import ValidationReport
from engines.interpretation_engine.validation.registry_validator import RegistryValidator
from engines.interpretation_engine.validation.version_validator import VersionValidator

logger = logging.getLogger(__name__)


class ValidationFramework:
    """Aggregate validator for Pack 03 infrastructure domains."""

    def __init__(
        self,
        *,
        contract_validator: ContractValidator | None = None,
        registry_validator: RegistryValidator | None = None,
        context_validator: ContextValidator | None = None,
        metadata_validator: MetadataValidator | None = None,
        dependency_validator: DependencyValidator | None = None,
        version_validator: VersionValidator | None = None,
    ) -> None:
        """Initialize with optional injected domain validators."""
        self._contracts = contract_validator or ContractValidator()
        self._registries = registry_validator or RegistryValidator()
        self._context = context_validator or ContextValidator()
        self._metadata = metadata_validator or MetadataValidator()
        self._dependencies = dependency_validator or DependencyValidator()
        self._versions = version_validator or VersionValidator()

    @property
    def contracts(self) -> ContractValidator:
        """Return contract validator."""
        return self._contracts

    @property
    def registries(self) -> RegistryValidator:
        """Return registry validator."""
        return self._registries

    @property
    def context(self) -> ContextValidator:
        """Return context validator."""
        return self._context

    @property
    def metadata(self) -> MetadataValidator:
        """Return metadata validator."""
        return self._metadata

    @property
    def dependencies(self) -> DependencyValidator:
        """Return dependency validator."""
        return self._dependencies

    @property
    def versions(self) -> VersionValidator:
        """Return version validator."""
        return self._versions

    def validate_all(
        self,
        *,
        runtime: RuntimeContract | None = None,
        registry: BaseRegistry[Any] | None = None,
        context: Any | None = None,
        metadata: Any | None = None,
        required_dependencies: tuple[str, ...] = (),
        available_dependencies: tuple[str, ...] = (),
        dependency_map: Mapping[str, tuple[str, ...]] | None = None,
        execution_graph: Any | None = None,
        version_info: Any | None = None,
    ) -> ValidationReport:
        """Run all provided domain validations and merge reports."""
        reports: list[ValidationReport] = []
        if runtime is not None:
            reports.append(self._contracts.validate(runtime))
        if registry is not None:
            if hasattr(registry, "validate_registry"):
                reports.append(self._registries.validate_interpreter_registry(registry))
            else:
                reports.append(self._registries.validate(registry))
        if context is not None:
            reports.append(self._context.validate(context))
        if metadata is not None:
            reports.append(self._metadata.validate(metadata))
        if (
            required_dependencies
            or available_dependencies
            or dependency_map is not None
            or execution_graph is not None
        ):
            reports.append(
                self._dependencies.validate(
                    required=required_dependencies,
                    available=available_dependencies,
                    dependency_map=dependency_map,
                    execution_graph=execution_graph,
                )
            )
        if version_info is not None:
            reports.append(self._versions.validate_version_info(version_info))

        if not reports:
            return ValidationReport(
                success=True,
                messages=("validation_framework_noop",),
                domain="framework",
            )

        merged = ValidationReport.merge(*reports, domain="framework")
        logger.info(
            "validation_framework_complete",
            extra={
                "success": merged.success,
                "issue_count": len(merged.issues),
                "domains": list(merged.details.keys()),
            },
        )
        return merged
