"""Dayun analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class DayunInputContextContract:
    """Input context contract for the Dayun analyzer."""

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
class DayunOutputResultContract:
    """Output result contract for the Dayun analyzer."""

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
class DayunDependenciesContract:
    """Dependency contract for the Dayun analyzer."""

    analyzer_id: str = "dayun"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class DayunProducedMetadataContract:
    """Metadata produced by the Dayun analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class DayunConsumedMetadataContract:
    """Metadata consumed by the Dayun analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class DayunSupportedRulesContract:
    """Supported rule identifiers for the Dayun analyzer."""

    rule_namespaces: tuple[str, ...] = ("dayun",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DayunSupportedResultTypesContract:
    """Supported result types for the Dayun analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class DayunAnalyzerContracts:
    """Aggregate contract surface for the Dayun analyzer."""

    analyzer_id: str = "dayun"
    input_context: DayunInputContextContract = field(
        default_factory=DayunInputContextContract
    )
    output_result: DayunOutputResultContract = field(
        default_factory=DayunOutputResultContract
    )
    dependencies: DayunDependenciesContract = field(
        default_factory=DayunDependenciesContract
    )
    produced_metadata: DayunProducedMetadataContract = field(
        default_factory=DayunProducedMetadataContract
    )
    consumed_metadata: DayunConsumedMetadataContract = field(
        default_factory=DayunConsumedMetadataContract
    )
    supported_rules: DayunSupportedRulesContract = field(
        default_factory=DayunSupportedRulesContract
    )
    supported_result_types: DayunSupportedResultTypesContract = field(
        default_factory=DayunSupportedResultTypesContract
    )
