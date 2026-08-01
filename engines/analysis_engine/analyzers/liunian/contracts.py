"""Liunian analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class LiunianInputContextContract:
    """Input context contract for the Liunian analyzer."""

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
class LiunianOutputResultContract:
    """Output result contract for the Liunian analyzer."""

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
class LiunianDependenciesContract:
    """Dependency contract for the Liunian analyzer."""

    analyzer_id: str = "liunian"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class LiunianProducedMetadataContract:
    """Metadata produced by the Liunian analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class LiunianConsumedMetadataContract:
    """Metadata consumed by the Liunian analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class LiunianSupportedRulesContract:
    """Supported rule identifiers for the Liunian analyzer."""

    rule_namespaces: tuple[str, ...] = ("liunian",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class LiunianSupportedResultTypesContract:
    """Supported result types for the Liunian analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class LiunianAnalyzerContracts:
    """Aggregate contract surface for the Liunian analyzer."""

    analyzer_id: str = "liunian"
    input_context: LiunianInputContextContract = field(
        default_factory=LiunianInputContextContract
    )
    output_result: LiunianOutputResultContract = field(
        default_factory=LiunianOutputResultContract
    )
    dependencies: LiunianDependenciesContract = field(
        default_factory=LiunianDependenciesContract
    )
    produced_metadata: LiunianProducedMetadataContract = field(
        default_factory=LiunianProducedMetadataContract
    )
    consumed_metadata: LiunianConsumedMetadataContract = field(
        default_factory=LiunianConsumedMetadataContract
    )
    supported_rules: LiunianSupportedRulesContract = field(
        default_factory=LiunianSupportedRulesContract
    )
    supported_result_types: LiunianSupportedResultTypesContract = field(
        default_factory=LiunianSupportedResultTypesContract
    )
