"""CK-01 Consulting Knowledge — match published signals to frozen catalog."""

from engines.consulting_knowledge.catalog import CONSULTING_KNOWLEDGE_CATALOG
from engines.consulting_knowledge.contracts import (
    CATALOG_ID,
    CATALOG_VERSION,
    CK01_FROZEN,
    COMMERCIAL_KNOWLEDGE_ID,
    COMMERCIAL_KNOWLEDGE_VERSION,
    CONSULTING_DOMAINS,
    CONTRACT_ID,
    DOMAIN_TITLES_VI,
    FORBIDDEN_OPERATIONS,
    FRAMEWORK_VERSION,
    INSUFFICIENT_COPY,
    KNOWLEDGE_UNIT_FIELDS,
    MATCHING_RUNTIME_ID,
    MATCHING_RUNTIME_VERSION,
    MATCHING_STAGES,
    SIGNAL_SOURCES,
    consulting_knowledge_contract,
    consulting_matching_contract,
)
from engines.consulting_knowledge.exceptions import ConsultingKnowledgeError
from engines.consulting_knowledge.freeze import (
    CANONICAL_COMPOSER,
    FROZEN_CATALOG_UNIT_IDS,
    INT03_EDITORIAL_COMPOSER,
    RUNTIME_PATH,
    SECTION_OUTPUT_FIELDS,
    commercial_knowledge_freeze,
)
from engines.consulting_knowledge.loader import (
    catalog_by_domain,
    get_catalog_unit,
    load_consulting_knowledge_catalog,
)
from engines.consulting_knowledge.matching import (
    match_consulting_knowledge,
    project_signals,
)
from engines.consulting_knowledge.models import (
    ConsultingKnowledgePack,
    ConsultingKnowledgeUnit,
    empty_knowledge_pack,
    empty_knowledge_unit,
)
from engines.consulting_knowledge.runtime import match_published_knowledge

__all__ = [
    "CANONICAL_COMPOSER",
    "CATALOG_ID",
    "CATALOG_VERSION",
    "CK01_FROZEN",
    "COMMERCIAL_KNOWLEDGE_ID",
    "COMMERCIAL_KNOWLEDGE_VERSION",
    "CONSULTING_DOMAINS",
    "CONSULTING_KNOWLEDGE_CATALOG",
    "CONTRACT_ID",
    "DOMAIN_TITLES_VI",
    "FORBIDDEN_OPERATIONS",
    "FRAMEWORK_VERSION",
    "FROZEN_CATALOG_UNIT_IDS",
    "INSUFFICIENT_COPY",
    "INT03_EDITORIAL_COMPOSER",
    "KNOWLEDGE_UNIT_FIELDS",
    "MATCHING_RUNTIME_ID",
    "MATCHING_RUNTIME_VERSION",
    "MATCHING_STAGES",
    "RUNTIME_PATH",
    "SECTION_OUTPUT_FIELDS",
    "SIGNAL_SOURCES",
    "ConsultingKnowledgeError",
    "ConsultingKnowledgePack",
    "ConsultingKnowledgeUnit",
    "catalog_by_domain",
    "commercial_knowledge_freeze",
    "consulting_knowledge_contract",
    "consulting_matching_contract",
    "empty_knowledge_pack",
    "empty_knowledge_unit",
    "get_catalog_unit",
    "load_consulting_knowledge_catalog",
    "match_consulting_knowledge",
    "match_published_knowledge",
    "project_signals",
]
