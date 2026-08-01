"""Useful God analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class UsefulGodInputContextContract:
    """Input context contract for the Useful God analyzer."""

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
class UsefulGodOutputResultContract:
    """Output result contract for the Useful God analyzer."""

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
class UsefulGodDependenciesContract:
    """Dependency contract for the Useful God analyzer."""

    analyzer_id: str = "useful_god"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class UsefulGodProducedMetadataContract:
    """Metadata produced by the Useful God analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class UsefulGodConsumedMetadataContract:
    """Metadata consumed by the Useful God analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class UsefulGodSupportedRulesContract:
    """Supported rule identifiers for the Useful God analyzer."""

    rule_namespaces: tuple[str, ...] = ("useful_god",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class UsefulGodSupportedResultTypesContract:
    """Supported result types for the Useful God analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class UsefulGodAnalyzerContracts:
    """Aggregate contract surface for the Useful God analyzer."""

    analyzer_id: str = "useful_god"
    input_context: UsefulGodInputContextContract = field(
        default_factory=UsefulGodInputContextContract
    )
    output_result: UsefulGodOutputResultContract = field(
        default_factory=UsefulGodOutputResultContract
    )
    dependencies: UsefulGodDependenciesContract = field(
        default_factory=UsefulGodDependenciesContract
    )
    produced_metadata: UsefulGodProducedMetadataContract = field(
        default_factory=UsefulGodProducedMetadataContract
    )
    consumed_metadata: UsefulGodConsumedMetadataContract = field(
        default_factory=UsefulGodConsumedMetadataContract
    )
    supported_rules: UsefulGodSupportedRulesContract = field(
        default_factory=UsefulGodSupportedRulesContract
    )
    supported_result_types: UsefulGodSupportedResultTypesContract = field(
        default_factory=UsefulGodSupportedResultTypesContract
    )
