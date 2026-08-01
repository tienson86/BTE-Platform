"""Conflict analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ConflictInputContextContract:
    """Input context contract for the Conflict analyzer."""

    context_type: str = "AnalysisContext"
    required_fields: tuple[str, ...] = (
        "id",
        "version",
        "metadata",
        "trace",
        "timestamps",
        "pipeline_id",
    )
    optional_fields: tuple[str, ...] = ("chart_id", "attributes")


@dataclass(frozen=True, slots=True)
class ConflictOutputResultContract:
    """Output result contract for the Conflict analyzer."""

    result_type: str = "ModuleResult"
    required_fields: tuple[str, ...] = (
        "id",
        "version",
        "metadata",
        "trace",
        "timestamps",
        "module_id",
        "success",
    )
    optional_fields: tuple[str, ...] = (
        "stage_results",
        "scores",
        "decisions",
        "payload",
    )


@dataclass(frozen=True, slots=True)
class ConflictDependenciesContract:
    """Dependency contract for the Conflict analyzer."""

    analyzer_id: str = "conflict"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class ConflictProducedMetadataContract:
    """Metadata produced by the Conflict analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class ConflictConsumedMetadataContract:
    """Metadata consumed by the Conflict analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class ConflictSupportedRulesContract:
    """Supported rule identifiers for the Conflict analyzer."""

    rule_namespaces: tuple[str, ...] = ("conflict",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ConflictSupportedResultTypesContract:
    """Supported result types for the Conflict analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class ConflictAnalyzerContracts:
    """Aggregate contract surface for the Conflict analyzer."""

    analyzer_id: str = "conflict"
    input_context: ConflictInputContextContract = field(
        default_factory=ConflictInputContextContract
    )
    output_result: ConflictOutputResultContract = field(
        default_factory=ConflictOutputResultContract
    )
    dependencies: ConflictDependenciesContract = field(
        default_factory=ConflictDependenciesContract
    )
    produced_metadata: ConflictProducedMetadataContract = field(
        default_factory=ConflictProducedMetadataContract
    )
    consumed_metadata: ConflictConsumedMetadataContract = field(
        default_factory=ConflictConsumedMetadataContract
    )
    supported_rules: ConflictSupportedRulesContract = field(
        default_factory=ConflictSupportedRulesContract
    )
    supported_result_types: ConflictSupportedResultTypesContract = field(
        default_factory=ConflictSupportedResultTypesContract
    )
