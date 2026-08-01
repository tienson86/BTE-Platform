"""Combination analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CombinationInputContextContract:
    """Input context contract for the Combination analyzer."""

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
class CombinationOutputResultContract:
    """Output result contract for the Combination analyzer."""

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
class CombinationDependenciesContract:
    """Dependency contract for the Combination analyzer."""

    analyzer_id: str = "combination"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class CombinationProducedMetadataContract:
    """Metadata produced by the Combination analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class CombinationConsumedMetadataContract:
    """Metadata consumed by the Combination analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class CombinationSupportedRulesContract:
    """Supported rule identifiers for the Combination analyzer."""

    rule_namespaces: tuple[str, ...] = ("combination",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CombinationSupportedResultTypesContract:
    """Supported result types for the Combination analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class CombinationAnalyzerContracts:
    """Aggregate contract surface for the Combination analyzer."""

    analyzer_id: str = "combination"
    input_context: CombinationInputContextContract = field(
        default_factory=CombinationInputContextContract
    )
    output_result: CombinationOutputResultContract = field(
        default_factory=CombinationOutputResultContract
    )
    dependencies: CombinationDependenciesContract = field(
        default_factory=CombinationDependenciesContract
    )
    produced_metadata: CombinationProducedMetadataContract = field(
        default_factory=CombinationProducedMetadataContract
    )
    consumed_metadata: CombinationConsumedMetadataContract = field(
        default_factory=CombinationConsumedMetadataContract
    )
    supported_rules: CombinationSupportedRulesContract = field(
        default_factory=CombinationSupportedRulesContract
    )
    supported_result_types: CombinationSupportedResultTypesContract = field(
        default_factory=CombinationSupportedResultTypesContract
    )
