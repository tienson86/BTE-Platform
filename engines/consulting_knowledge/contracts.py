"""CK-01A frozen Consulting Knowledge constants.

Architecture only. Matches published signals. Does not calculate.
"""

from __future__ import annotations

from typing import Any, Final, Mapping

CONTRACT_ID: Final[str] = "bte.consulting.knowledge.v1"
CATALOG_ID: Final[str] = "bte.consulting.knowledge.catalog.v1"
MATCHING_RUNTIME_ID: Final[str] = "bte.consulting.knowledge.matching.v1"
FRAMEWORK_VERSION: Final[str] = "1.0.0"
CATALOG_VERSION: Final[str] = "1.0.0"
MATCHING_RUNTIME_VERSION: Final[str] = "1.0.0"
COMMERCIAL_KNOWLEDGE_ID: Final[str] = "bte.commercial.knowledge.v1"
COMMERCIAL_KNOWLEDGE_VERSION: Final[str] = "1.0.0"
CK01_FROZEN: Final[bool] = True
INSUFFICIENT_COPY: Final[str] = "Chưa có dữ liệu"
SOURCE_PATH: Final[str] = "consulting_knowledge"
UNIT_SCHEMA: Final[str] = "1.0.0"

CONSULTING_DOMAINS: Final[tuple[str, ...]] = (
    "career",
    "finance",
    "relationship",
    "health",
    "leadership",
    "management",
    "communication",
    "business",
    "personality",
    "action_library",
)

DOMAIN_TITLES_VI: Final[Mapping[str, str]] = {
    "career": "Sự nghiệp",
    "finance": "Tài chính",
    "relationship": "Quan hệ",
    "health": "Sức khỏe",
    "leadership": "Lãnh đạo",
    "management": "Quản lý",
    "communication": "Giao tiếp",
    "business": "Kinh doanh",
    "personality": "Tính cách",
    "action_library": "Thư viện hành động",
}

SIGNAL_SOURCES: Final[tuple[str, ...]] = (
    "integrated_narrative",
    "identity",
    "analysis_result",
)

KNOWLEDGE_UNIT_FIELDS: Final[tuple[str, ...]] = (
    "condition",
    "applicable_scope",
    "consulting_meaning",
    "customer_wording",
    "recommended_actions",
    "references",
)

MATCHING_STAGES: Final[tuple[str, ...]] = (
    "published_truth",
    "signal_projection",
    "condition_match",
    "scope_filter",
    "consulting_knowledge_pack",
)

FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "calculate",
    "predict",
    "infer",
    "invent",
    "llm",
)

FORBIDDEN_EMPTY_TOKENS: Final[tuple[str, ...]] = (
    "N/A",
    "null",
    "undefined",
    "Không",
    "Chờ dữ liệu",
)


def consulting_knowledge_contract() -> dict[str, Any]:
    """Return the frozen CK-01A public contract surface."""
    return {
        "contract_id": CONTRACT_ID,
        "framework_version": FRAMEWORK_VERSION,
        "runtime": False,
        "recalculates": False,
        "llm": False,
        "engine": False,
        "frontend": False,
        "input": list(SIGNAL_SOURCES),
        "output": "ConsultingKnowledgePack",
        "domains": list(CONSULTING_DOMAINS),
        "domain_titles_vi": dict(DOMAIN_TITLES_VI),
        "unit_fields": list(KNOWLEDGE_UNIT_FIELDS),
        "matching_stages": list(MATCHING_STAGES),
        "forbidden_operations": list(FORBIDDEN_OPERATIONS),
        "insufficient_copy": INSUFFICIENT_COPY,
        "source_path": SOURCE_PATH,
        "catalog_id": CATALOG_ID,
        "catalog_version": CATALOG_VERSION,
        "matching_runtime": False,
        "matching_runtime_id": MATCHING_RUNTIME_ID,
    }


def consulting_matching_contract() -> dict[str, Any]:
    """Return the CK-01C matching runtime contract. Match only. No calculation."""
    return {
        "contract_id": MATCHING_RUNTIME_ID,
        "framework_version": MATCHING_RUNTIME_VERSION,
        "catalog_id": CATALOG_ID,
        "matching_runtime": True,
        "recalculates": False,
        "llm": False,
        "engine": False,
        "frontend": False,
        "input": list(SIGNAL_SOURCES),
        "output": "ConsultingKnowledgePack",
        "stages": list(MATCHING_STAGES),
        "forbidden_operations": list(FORBIDDEN_OPERATIONS),
        "insufficient_copy": INSUFFICIENT_COPY,
    }
