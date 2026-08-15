"""BaZi Interpretation Knowledge System (K1 + K2 Useful God population)."""

from engines.interpretation_engine.foundation.knowledge.entity import (
    KnowledgeEntity,
    KnowledgeEntityReference,
    KnowledgeMetadata,
)
from engines.interpretation_engine.foundation.knowledge.diagnostics import (
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
    "USEFUL_GOD_KNOWLEDGE_MISSING",
    "USEFUL_GOD_ROLE_CONFLICT",
    "UsefulGodKnowledgeBundle",
    "UsefulGodKnowledgeCoverage",
    "UsefulGodQualityReport",
    "build_useful_god_knowledge_bundle",
    "build_useful_god_quality_report",
    "get_knowledge_registry",
    "retrieve_knowledge",
    "write_useful_god_reports",
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
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
