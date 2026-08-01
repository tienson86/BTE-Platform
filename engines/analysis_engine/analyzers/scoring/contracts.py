"""Scoring analyzer contracts.

Contract declarations only. No analysis logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ScoringInputContextContract:
    """Input context contract for the Scoring analyzer."""

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
class ScoringOutputResultContract:
    """Output result contract for the Scoring analyzer."""

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
class ScoringDependenciesContract:
    """Dependency contract for the Scoring analyzer."""

    analyzer_id: str = "scoring"
    depends_on_analyzers: tuple[str, ...] = ()
    depends_on_packs: tuple[str, ...] = ("PACK_01",)
    depends_on_providers: tuple[str, ...] = (
        "ContextProviderInterface",
        "RegistryProviderInterface",
    )


@dataclass(frozen=True, slots=True)
class ScoringProducedMetadataContract:
    """Metadata produced by the Scoring analyzer."""

    metadata_keys: tuple[str, ...] = (
        "analyzer_id",
        "analyzer_version",
        "result_id",
        "decision_ids",
        "score_ids",
    )


@dataclass(frozen=True, slots=True)
class ScoringConsumedMetadataContract:
    """Metadata consumed by the Scoring analyzer."""

    metadata_keys: tuple[str, ...] = (
        "chart_id",
        "pipeline_id",
        "schema_version",
        "registry_snapshot_id",
    )


@dataclass(frozen=True, slots=True)
class ScoringSupportedRulesContract:
    """Supported rule identifiers for the Scoring analyzer."""

    rule_namespaces: tuple[str, ...] = ("scoring",)
    rule_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ScoringSupportedResultTypesContract:
    """Supported result types for the Scoring analyzer."""

    result_types: tuple[str, ...] = (
        "ModuleResult",
        "StageResult",
        "AnalysisScore",
        "AnalysisDecision",
    )


@dataclass(frozen=True, slots=True)
class ScoringAnalyzerContracts:
    """Aggregate contract surface for the Scoring analyzer."""

    analyzer_id: str = "scoring"
    input_context: ScoringInputContextContract = field(
        default_factory=ScoringInputContextContract
    )
    output_result: ScoringOutputResultContract = field(
        default_factory=ScoringOutputResultContract
    )
    dependencies: ScoringDependenciesContract = field(
        default_factory=ScoringDependenciesContract
    )
    produced_metadata: ScoringProducedMetadataContract = field(
        default_factory=ScoringProducedMetadataContract
    )
    consumed_metadata: ScoringConsumedMetadataContract = field(
        default_factory=ScoringConsumedMetadataContract
    )
    supported_rules: ScoringSupportedRulesContract = field(
        default_factory=ScoringSupportedRulesContract
    )
    supported_result_types: ScoringSupportedResultTypesContract = field(
        default_factory=ScoringSupportedResultTypesContract
    )
