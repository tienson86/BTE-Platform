"""Shen Sha analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ShenshaInputContextContract:
    """Input context contract for the Shen Sha analyzer."""

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
class ShenshaOutputResultContract:
    """Output result contract for the Shen Sha analyzer."""

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
class ShenshaDependenciesContract:
    """Dependency contract for the Shen Sha analyzer."""

    analyzer_id: str = "shensha"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class ShenshaProducedMetadataContract:
    """Metadata produced by the Shen Sha analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class ShenshaConsumedMetadataContract:
    """Metadata consumed by the Shen Sha analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class ShenshaSupportedRulesContract:
    """Supported rule identifiers for the Shen Sha analyzer."""

    rule_namespaces: tuple[str, ...] = ("shensha",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ShenshaSupportedResultTypesContract:
    """Supported result types for the Shen Sha analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class ShenshaAnalyzerContracts:
    """Aggregate contract surface for the Shen Sha analyzer."""

    analyzer_id: str = "shensha"
    input_context: ShenshaInputContextContract = field(
        default_factory=ShenshaInputContextContract
    )
    output_result: ShenshaOutputResultContract = field(
        default_factory=ShenshaOutputResultContract
    )
    dependencies: ShenshaDependenciesContract = field(
        default_factory=ShenshaDependenciesContract
    )
    produced_metadata: ShenshaProducedMetadataContract = field(
        default_factory=ShenshaProducedMetadataContract
    )
    consumed_metadata: ShenshaConsumedMetadataContract = field(
        default_factory=ShenshaConsumedMetadataContract
    )
    supported_rules: ShenshaSupportedRulesContract = field(
        default_factory=ShenshaSupportedRulesContract
    )
    supported_result_types: ShenshaSupportedResultTypesContract = field(
        default_factory=ShenshaSupportedResultTypesContract
    )
