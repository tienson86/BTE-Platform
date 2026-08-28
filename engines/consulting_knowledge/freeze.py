"""CK-01E Commercial Knowledge V1 freeze surface.

Locks the approved runtime. Does not render HTML/PDF/DOCX.
Does not merge INT-03 compose_commercial_narrative with CK-01 compose_commercial_consulting.
"""

from __future__ import annotations

from typing import Any, Final

from engines.consulting_knowledge.contracts import (
    CATALOG_ID,
    CATALOG_VERSION,
    COMMERCIAL_KNOWLEDGE_ID,
    COMMERCIAL_KNOWLEDGE_VERSION,
    CONSULTING_DOMAINS,
    CK01_FROZEN,
    CONTRACT_ID,
    FRAMEWORK_VERSION,
    KNOWLEDGE_UNIT_FIELDS,
    MATCHING_RUNTIME_ID,
    SIGNAL_SOURCES,
)

CANONICAL_COMPOSER: Final[str] = "compose_commercial_consulting"
INT03_EDITORIAL_COMPOSER: Final[str] = "compose_commercial_narrative"
CANONICAL_MATCHER: Final[str] = "match_published_knowledge"
CANONICAL_PUBLISHER: Final[str] = "publish_commercial_consulting"

RUNTIME_PATH: Final[tuple[str, ...]] = (
    "orchestrator",
    "match_published_knowledge",
    "compose_commercial_consulting",
    "CommercialComposerResult",
    "ReportInputV1.commercial_consulting",
    "data.commercial_consulting",
)

SECTION_OUTPUT_FIELDS: Final[tuple[str, ...]] = (
    "domain",
    "title",
    "summary",
    "meaning",
    "recommendations",
    "references",
    "source_unit_ids",
)

FROZEN_CATALOG_UNIT_IDS: Final[tuple[str, ...]] = (
    "ck-career-001",
    "ck-career-002",
    "ck-finance-001",
    "ck-finance-002",
    "ck-relationship-001",
    "ck-relationship-002",
    "ck-health-001",
    "ck-health-002",
    "ck-leadership-001",
    "ck-leadership-002",
    "ck-management-001",
    "ck-management-002",
    "ck-communication-001",
    "ck-communication-002",
    "ck-business-001",
    "ck-business-002",
    "ck-personality-001",
    "ck-personality-002",
    "ck-action-001",
    "ck-action-002",
    "ck-action-003",
    "ck-action-004",
)


def commercial_knowledge_freeze() -> dict[str, Any]:
    """Return the frozen CK-01 Commercial Knowledge V1 contract."""
    return {
        "contract_id": COMMERCIAL_KNOWLEDGE_ID,
        "version": COMMERCIAL_KNOWLEDGE_VERSION,
        "frozen": CK01_FROZEN,
        "catalog_id": CATALOG_ID,
        "catalog_version": CATALOG_VERSION,
        "knowledge_contract_id": CONTRACT_ID,
        "framework_version": FRAMEWORK_VERSION,
        "matching_runtime_id": MATCHING_RUNTIME_ID,
        "canonical_matcher": CANONICAL_MATCHER,
        "canonical_composer": CANONICAL_COMPOSER,
        "int03_editorial_composer": INT03_EDITORIAL_COMPOSER,
        "publisher": CANONICAL_PUBLISHER,
        "runtime_path": list(RUNTIME_PATH),
        "domains": list(CONSULTING_DOMAINS),
        "unit_fields": list(KNOWLEDGE_UNIT_FIELDS),
        "section_output_fields": list(SECTION_OUTPUT_FIELDS),
        "catalog_unit_ids": list(FROZEN_CATALOG_UNIT_IDS),
        "signal_sources": list(SIGNAL_SOURCES),
        "rendering": {
            "html": False,
            "pdf": False,
            "docx": False,
            "ui": False,
        },
        "llm": False,
        "recalculates": False,
        "engine": False,
    }
