"""Strength analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class StrengthInputContextContract:
    """Input context contract for the Strength analyzer."""

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
class StrengthOutputResultContract:
    """Output result contract for the Strength analyzer."""

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
class StrengthDependenciesContract:
    """Dependency contract for the Strength analyzer."""

    analyzer_id: str = "strength"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class StrengthProducedMetadataContract:
    """Metadata produced by the Strength analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class StrengthConsumedMetadataContract:
    """Metadata consumed by the Strength analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class StrengthSupportedRulesContract:
    """Supported rule identifiers for the Strength analyzer."""

    rule_namespaces: tuple[str, ...] = ("strength",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class StrengthSupportedResultTypesContract:
    """Supported result types for the Strength analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class StrengthAnalyzerContracts:
    """Aggregate contract surface for the Strength analyzer."""

    analyzer_id: str = "strength"
    input_context: StrengthInputContextContract = field(
        default_factory=StrengthInputContextContract
    )
    output_result: StrengthOutputResultContract = field(
        default_factory=StrengthOutputResultContract
    )
    dependencies: StrengthDependenciesContract = field(
        default_factory=StrengthDependenciesContract
    )
    produced_metadata: StrengthProducedMetadataContract = field(
        default_factory=StrengthProducedMetadataContract
    )
    consumed_metadata: StrengthConsumedMetadataContract = field(
        default_factory=StrengthConsumedMetadataContract
    )
    supported_rules: StrengthSupportedRulesContract = field(
        default_factory=StrengthSupportedRulesContract
    )
    supported_result_types: StrengthSupportedResultTypesContract = field(
        default_factory=StrengthSupportedResultTypesContract
    )
