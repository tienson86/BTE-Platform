"""Ten Gods analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class TenGodsInputContextContract:
    """Input context contract for the Ten Gods analyzer."""

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
class TenGodsOutputResultContract:
    """Output result contract for the Ten Gods analyzer."""

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
class TenGodsDependenciesContract:
    """Dependency contract for the Ten Gods analyzer."""

    analyzer_id: str = "ten_gods"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class TenGodsProducedMetadataContract:
    """Metadata produced by the Ten Gods analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class TenGodsConsumedMetadataContract:
    """Metadata consumed by the Ten Gods analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class TenGodsSupportedRulesContract:
    """Supported rule identifiers for the Ten Gods analyzer."""

    rule_namespaces: tuple[str, ...] = ("ten_gods",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TenGodsSupportedResultTypesContract:
    """Supported result types for the Ten Gods analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class TenGodsAnalyzerContracts:
    """Aggregate contract surface for the Ten Gods analyzer."""

    analyzer_id: str = "ten_gods"
    input_context: TenGodsInputContextContract = field(
        default_factory=TenGodsInputContextContract
    )
    output_result: TenGodsOutputResultContract = field(
        default_factory=TenGodsOutputResultContract
    )
    dependencies: TenGodsDependenciesContract = field(
        default_factory=TenGodsDependenciesContract
    )
    produced_metadata: TenGodsProducedMetadataContract = field(
        default_factory=TenGodsProducedMetadataContract
    )
    consumed_metadata: TenGodsConsumedMetadataContract = field(
        default_factory=TenGodsConsumedMetadataContract
    )
    supported_rules: TenGodsSupportedRulesContract = field(
        default_factory=TenGodsSupportedRulesContract
    )
    supported_result_types: TenGodsSupportedResultTypesContract = field(
        default_factory=TenGodsSupportedResultTypesContract
    )
