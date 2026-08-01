"""Liuyue analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class LiuyueInputContextContract:
    """Input context contract for the Liuyue analyzer."""

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
class LiuyueOutputResultContract:
    """Output result contract for the Liuyue analyzer."""

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
class LiuyueDependenciesContract:
    """Dependency contract for the Liuyue analyzer."""

    analyzer_id: str = "liuyue"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class LiuyueProducedMetadataContract:
    """Metadata produced by the Liuyue analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class LiuyueConsumedMetadataContract:
    """Metadata consumed by the Liuyue analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class LiuyueSupportedRulesContract:
    """Supported rule identifiers for the Liuyue analyzer."""

    rule_namespaces: tuple[str, ...] = ("liuyue",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class LiuyueSupportedResultTypesContract:
    """Supported result types for the Liuyue analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class LiuyueAnalyzerContracts:
    """Aggregate contract surface for the Liuyue analyzer."""

    analyzer_id: str = "liuyue"
    input_context: LiuyueInputContextContract = field(
        default_factory=LiuyueInputContextContract
    )
    output_result: LiuyueOutputResultContract = field(
        default_factory=LiuyueOutputResultContract
    )
    dependencies: LiuyueDependenciesContract = field(
        default_factory=LiuyueDependenciesContract
    )
    produced_metadata: LiuyueProducedMetadataContract = field(
        default_factory=LiuyueProducedMetadataContract
    )
    consumed_metadata: LiuyueConsumedMetadataContract = field(
        default_factory=LiuyueConsumedMetadataContract
    )
    supported_rules: LiuyueSupportedRulesContract = field(
        default_factory=LiuyueSupportedRulesContract
    )
    supported_result_types: LiuyueSupportedResultTypesContract = field(
        default_factory=LiuyueSupportedResultTypesContract
    )
