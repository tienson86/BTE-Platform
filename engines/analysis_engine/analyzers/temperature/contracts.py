"""Temperature analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class TemperatureInputContextContract:
    """Input context contract for the Temperature analyzer."""

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
class TemperatureOutputResultContract:
    """Output result contract for the Temperature analyzer."""

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
class TemperatureDependenciesContract:
    """Dependency contract for the Temperature analyzer."""

    analyzer_id: str = "temperature"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class TemperatureProducedMetadataContract:
    """Metadata produced by the Temperature analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class TemperatureConsumedMetadataContract:
    """Metadata consumed by the Temperature analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class TemperatureSupportedRulesContract:
    """Supported rule identifiers for the Temperature analyzer."""

    rule_namespaces: tuple[str, ...] = ("temperature",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TemperatureSupportedResultTypesContract:
    """Supported result types for the Temperature analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class TemperatureAnalyzerContracts:
    """Aggregate contract surface for the Temperature analyzer."""

    analyzer_id: str = "temperature"
    input_context: TemperatureInputContextContract = field(
        default_factory=TemperatureInputContextContract
    )
    output_result: TemperatureOutputResultContract = field(
        default_factory=TemperatureOutputResultContract
    )
    dependencies: TemperatureDependenciesContract = field(
        default_factory=TemperatureDependenciesContract
    )
    produced_metadata: TemperatureProducedMetadataContract = field(
        default_factory=TemperatureProducedMetadataContract
    )
    consumed_metadata: TemperatureConsumedMetadataContract = field(
        default_factory=TemperatureConsumedMetadataContract
    )
    supported_rules: TemperatureSupportedRulesContract = field(
        default_factory=TemperatureSupportedRulesContract
    )
    supported_result_types: TemperatureSupportedResultTypesContract = field(
        default_factory=TemperatureSupportedResultTypesContract
    )
