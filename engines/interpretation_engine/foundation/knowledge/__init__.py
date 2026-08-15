"""BaZi Interpretation Knowledge System (K1 + K2 Useful God population)."""

from engines.interpretation_engine.foundation.knowledge.entity import (
    KnowledgeEntity,
    KnowledgeEntityReference,
    KnowledgeMetadata,
)
from engines.interpretation_engine.foundation.knowledge.diagnostics import (
    BROKEN_RELATIONSHIP,
    INVALID_PATTERN,
    INVALID_POSITION,
    INVALID_SHENSHA,
    INVALID_STRENGTH_STATE,
    INVALID_TEN_GOD,
    MISSING_ACTIVATION,
    MISSING_MECHANISM,
    MISSING_NARRATIVE_MAPPING,
    PATTERN_CONCEPTS_MISSING,
    PATTERN_KNOWLEDGE_MISSING,
    STRENGTH_CONCEPTS_MISSING,
    STRENGTH_KNOWLEDGE_MISSING,
    TEN_GOD_CONCEPTS_MISSING,
    TEN_GOD_KNOWLEDGE_MISSING,
    SHENSHA_CONCEPTS_MISSING,
    SHENSHA_KNOWLEDGE_MISSING,
    DUPLICATE_ROLE,
    USEFUL_GOD_KNOWLEDGE_MISSING,
    USEFUL_GOD_ROLE_CONFLICT,
)
from engines.interpretation_engine.foundation.knowledge.domains import CANONICAL_KNOWLEDGE_DOMAINS
from engines.interpretation_engine.foundation.knowledge.loader import (
    JsonKnowledgeLoader,
    KnowledgeLoadError,
)
from engines.interpretation_engine.foundation.knowledge.quality import (
    DuplicateContentDetector,
    KnowledgeQualityGate,
)
from engines.interpretation_engine.foundation.knowledge.registry import KnowledgeRegistry
from engines.interpretation_engine.foundation.knowledge.service import (
    get_knowledge_registry,
    retrieve_knowledge,
)
from engines.interpretation_engine.foundation.knowledge.status import KnowledgeStatus
from engines.interpretation_engine.foundation.knowledge.validator import (
    KnowledgeValidationResult,
    KnowledgeValidator,
)

__all__ = [
    "CANONICAL_KNOWLEDGE_DOMAINS",
    "DuplicateContentDetector",
    "JsonKnowledgeLoader",
    "KnowledgeEntity",
    "KnowledgeEntityReference",
    "KnowledgeLoadError",
    "KnowledgeMetadata",
    "KnowledgeQualityGate",
    "KnowledgeRegistry",
    "KnowledgeStatus",
    "KnowledgeValidationResult",
    "KnowledgeValidator",
    "INVALID_STRENGTH_STATE",
    "PATTERN_CONCEPTS_MISSING",
    "PATTERN_KNOWLEDGE_MISSING",
    "INVALID_PATTERN",
    "INVALID_TEN_GOD",
    "INVALID_POSITION",
    "TEN_GOD_CONCEPTS_MISSING",
    "TEN_GOD_KNOWLEDGE_MISSING",
    "SHENSHA_CONCEPTS_MISSING",
    "SHENSHA_KNOWLEDGE_MISSING",
    "INVALID_SHENSHA",
    "MISSING_MECHANISM",
    "MISSING_ACTIVATION",
    "DUPLICATE_ROLE",
    "BROKEN_RELATIONSHIP",
    "MISSING_NARRATIVE_MAPPING",
    "STRENGTH_CONCEPTS_MISSING",
    "STRENGTH_KNOWLEDGE_MISSING",
    "USEFUL_GOD_KNOWLEDGE_MISSING",
    "USEFUL_GOD_ROLE_CONFLICT",
    "UsefulGodKnowledgeBundle",
    "UsefulGodKnowledgeCoverage",
    "UsefulGodQualityReport",
    "StrengthAssessment",
    "StrengthKnowledgeBundle",
    "StrengthKnowledgeCoverage",
    "StrengthQualityReport",
    "PatternKnowledgeBundle",
    "PatternKnowledgeCoverage",
    "PatternQualityReport",
    "TenGodKnowledgeBundle",
    "TenGodKnowledgeCoverage",
    "TenGodQualityReport",
    "ShenShaKnowledgeBundle",
    "ShenShaKnowledgeCoverage",
    "ShenShaQualityReport",
    "build_useful_god_knowledge_bundle",
    "build_useful_god_quality_report",
    "build_strength_assessment",
    "build_strength_knowledge_bundle",
    "build_strength_quality_report",
    "build_pattern_knowledge_bundle",
    "build_pattern_quality_report",
    "build_ten_god_knowledge_bundle",
    "build_ten_god_quality_report",
    "build_shensha_knowledge_bundle",
    "build_shensha_quality_report",
    "get_knowledge_registry",
    "retrieve_knowledge",
    "write_useful_god_reports",
    "write_strength_reports",
    "write_pattern_reports",
    "write_ten_god_reports",
    "write_shensha_reports",
]


def __getattr__(name: str) -> object:
    """Lazy-load K2 retrieval/report types to avoid a concepts circular import."""
    if name in {"UsefulGodKnowledgeBundle", "UsefulGodKnowledgeCoverage"}:
        from engines.interpretation_engine.foundation.knowledge.bundle import (
            UsefulGodKnowledgeBundle,
            UsefulGodKnowledgeCoverage,
        )

        mapping = {
            "UsefulGodKnowledgeBundle": UsefulGodKnowledgeBundle,
            "UsefulGodKnowledgeCoverage": UsefulGodKnowledgeCoverage,
        }
        return mapping[name]
    if name in {
        "UsefulGodQualityReport",
        "build_useful_god_quality_report",
        "write_useful_god_reports",
    }:
        from engines.interpretation_engine.foundation.knowledge.coverage import (
            UsefulGodQualityReport,
            build_useful_god_quality_report,
            write_useful_god_reports,
        )

        mapping = {
            "UsefulGodQualityReport": UsefulGodQualityReport,
            "build_useful_god_quality_report": build_useful_god_quality_report,
            "write_useful_god_reports": write_useful_god_reports,
        }
        return mapping[name]
    if name == "build_useful_god_knowledge_bundle":
        from engines.interpretation_engine.foundation.knowledge.retrieval import (
            build_useful_god_knowledge_bundle,
        )

        return build_useful_god_knowledge_bundle
    if name in {"StrengthKnowledgeBundle", "StrengthKnowledgeCoverage"}:
        from engines.interpretation_engine.foundation.knowledge.strength_bundle import (
            StrengthKnowledgeBundle,
            StrengthKnowledgeCoverage,
        )

        mapping = {
            "StrengthKnowledgeBundle": StrengthKnowledgeBundle,
            "StrengthKnowledgeCoverage": StrengthKnowledgeCoverage,
        }
        return mapping[name]
    if name == "build_strength_knowledge_bundle":
        from engines.interpretation_engine.foundation.knowledge.strength_retrieval import (
            build_strength_knowledge_bundle,
        )

        return build_strength_knowledge_bundle
    if name in {
        "StrengthQualityReport",
        "build_strength_quality_report",
        "write_strength_reports",
    }:
        from engines.interpretation_engine.foundation.knowledge.strength_coverage import (
            StrengthQualityReport,
            build_strength_quality_report,
            write_strength_reports,
        )

        mapping = {
            "StrengthQualityReport": StrengthQualityReport,
            "build_strength_quality_report": build_strength_quality_report,
            "write_strength_reports": write_strength_reports,
        }
        return mapping[name]
    if name in {"StrengthAssessment", "build_strength_assessment"}:
        from engines.interpretation_engine.foundation.assessment.strength import (
            StrengthAssessment,
            build_strength_assessment,
        )

        mapping = {
            "StrengthAssessment": StrengthAssessment,
            "build_strength_assessment": build_strength_assessment,
        }
        return mapping[name]
    if name in {"PatternKnowledgeBundle", "PatternKnowledgeCoverage"}:
        from engines.interpretation_engine.foundation.knowledge.pattern_bundle import (
            PatternKnowledgeBundle,
            PatternKnowledgeCoverage,
        )

        mapping = {
            "PatternKnowledgeBundle": PatternKnowledgeBundle,
            "PatternKnowledgeCoverage": PatternKnowledgeCoverage,
        }
        return mapping[name]
    if name == "build_pattern_knowledge_bundle":
        from engines.interpretation_engine.foundation.knowledge.pattern_retrieval import (
            build_pattern_knowledge_bundle,
        )

        return build_pattern_knowledge_bundle
    if name in {
        "PatternQualityReport",
        "build_pattern_quality_report",
        "write_pattern_reports",
    }:
        from engines.interpretation_engine.foundation.knowledge.pattern_coverage import (
            PatternQualityReport,
            build_pattern_quality_report,
            write_pattern_reports,
        )

        mapping = {
            "PatternQualityReport": PatternQualityReport,
            "build_pattern_quality_report": build_pattern_quality_report,
            "write_pattern_reports": write_pattern_reports,
        }
        return mapping[name]
    if name in {"TenGodKnowledgeBundle", "TenGodKnowledgeCoverage"}:
        from engines.interpretation_engine.foundation.knowledge.ten_god_bundle import (
            TenGodKnowledgeBundle,
            TenGodKnowledgeCoverage,
        )

        mapping = {
            "TenGodKnowledgeBundle": TenGodKnowledgeBundle,
            "TenGodKnowledgeCoverage": TenGodKnowledgeCoverage,
        }
        return mapping[name]
    if name == "build_ten_god_knowledge_bundle":
        from engines.interpretation_engine.foundation.knowledge.ten_god_retrieval import (
            build_ten_god_knowledge_bundle,
        )

        return build_ten_god_knowledge_bundle
    if name in {
        "TenGodQualityReport",
        "build_ten_god_quality_report",
        "write_ten_god_reports",
    }:
        from engines.interpretation_engine.foundation.knowledge.ten_god_coverage import (
            TenGodQualityReport,
            build_ten_god_quality_report,
            write_ten_god_reports,
        )

        mapping = {
            "TenGodQualityReport": TenGodQualityReport,
            "build_ten_god_quality_report": build_ten_god_quality_report,
            "write_ten_god_reports": write_ten_god_reports,
        }
        return mapping[name]
    if name in {"ShenShaKnowledgeBundle", "ShenShaKnowledgeCoverage"}:
        from engines.interpretation_engine.foundation.knowledge.shensha_bundle import (
            ShenShaKnowledgeBundle,
            ShenShaKnowledgeCoverage,
        )

        mapping = {
            "ShenShaKnowledgeBundle": ShenShaKnowledgeBundle,
            "ShenShaKnowledgeCoverage": ShenShaKnowledgeCoverage,
        }
        return mapping[name]
    if name == "build_shensha_knowledge_bundle":
        from engines.interpretation_engine.foundation.knowledge.shensha_retrieval import (
            build_shensha_knowledge_bundle,
        )

        return build_shensha_knowledge_bundle
    if name in {
        "ShenShaQualityReport",
        "build_shensha_quality_report",
        "write_shensha_reports",
    }:
        from engines.interpretation_engine.foundation.knowledge.shensha_coverage import (
            ShenShaQualityReport,
            build_shensha_quality_report,
            write_shensha_reports,
        )

        mapping = {
            "ShenShaQualityReport": ShenShaQualityReport,
            "build_shensha_quality_report": build_shensha_quality_report,
            "write_shensha_reports": write_shensha_reports,
        }
        return mapping[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
