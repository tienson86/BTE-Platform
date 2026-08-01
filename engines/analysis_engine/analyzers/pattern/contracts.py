"""Pattern analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class PatternInputContextContract:
    """Input context contract for the Pattern analyzer."""

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
class PatternOutputResultContract:
    """Output result contract for the Pattern analyzer."""

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
class PatternDependenciesContract:
    """Dependency contract for the Pattern analyzer."""

    analyzer_id: str = "pattern"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class PatternProducedMetadataContract:
    """Metadata produced by the Pattern analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class PatternConsumedMetadataContract:
    """Metadata consumed by the Pattern analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class PatternSupportedRulesContract:
    """Supported rule identifiers for the Pattern analyzer."""

    rule_namespaces: tuple[str, ...] = ("pattern",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PatternSupportedResultTypesContract:
    """Supported result types for the Pattern analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class PatternAnalyzerContracts:
    """Aggregate contract surface for the Pattern analyzer."""

    analyzer_id: str = "pattern"
    input_context: PatternInputContextContract = field(
        default_factory=PatternInputContextContract
    )
    output_result: PatternOutputResultContract = field(
        default_factory=PatternOutputResultContract
    )
    dependencies: PatternDependenciesContract = field(
        default_factory=PatternDependenciesContract
    )
    produced_metadata: PatternProducedMetadataContract = field(
        default_factory=PatternProducedMetadataContract
    )
    consumed_metadata: PatternConsumedMetadataContract = field(
        default_factory=PatternConsumedMetadataContract
    )
    supported_rules: PatternSupportedRulesContract = field(
        default_factory=PatternSupportedRulesContract
    )
    supported_result_types: PatternSupportedResultTypesContract = field(
        default_factory=PatternSupportedResultTypesContract
    )
