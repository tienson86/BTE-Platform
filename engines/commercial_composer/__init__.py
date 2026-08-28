"""INT-03A Commercial Composer — Integrated Narrative → Commercial Narrative."""

from engines.commercial_composer.compose import compose_commercial_narrative
from engines.commercial_composer.consulting_compose import (
    compose_commercial_consulting,
    stable_unique,
)
from engines.commercial_composer.consulting_models import (
    CommercialComposerInput,
    CommercialComposerResult,
    CommercialConsultingSection,
    empty_commercial_composer_result,
)
from engines.commercial_composer.contracts import (
    ALLOWED_OPERATIONS,
    COMMERCIAL_SECTIONS,
    COMPOSITION_STAGES,
    CONTRACT_ID,
    FORBIDDEN_OPERATIONS,
    FRAMEWORK_VERSION,
    INSUFFICIENT_COPY,
    SECTION_IDS,
    SECTION_SOURCES,
    SECTION_TITLES_VI,
    commercial_composer_contract,
)
from engines.commercial_composer.exceptions import CommercialComposerError
from engines.commercial_composer.models import (
    CommercialNarrativeBlock,
    CommercialNarrativeUnit,
    CommercialSentence,
    empty_commercial_unit,
)
from engines.commercial_composer.rules import (
    ALLOWED_EDITORIAL_OPERATIONS,
    COMPOSITION_RULES,
    CUSTOMER_SECTION_ORDER,
    FORBIDDEN_EDITORIAL_OPERATIONS,
    commercial_composition_rules,
)

__all__ = [
    "ALLOWED_EDITORIAL_OPERATIONS",
    "ALLOWED_OPERATIONS",
    "COMMERCIAL_SECTIONS",
    "COMPOSITION_RULES",
    "COMPOSITION_STAGES",
    "CONTRACT_ID",
    "CUSTOMER_SECTION_ORDER",
    "FORBIDDEN_EDITORIAL_OPERATIONS",
    "FORBIDDEN_OPERATIONS",
    "FRAMEWORK_VERSION",
    "INSUFFICIENT_COPY",
    "SECTION_IDS",
    "SECTION_SOURCES",
    "SECTION_TITLES_VI",
    "CommercialComposerError",
    "CommercialComposerInput",
    "CommercialComposerResult",
    "CommercialConsultingSection",
    "CommercialNarrativeBlock",
    "CommercialNarrativeUnit",
    "CommercialSentence",
    "commercial_composer_contract",
    "commercial_composition_rules",
    "compose_commercial_consulting",
    "compose_commercial_narrative",
    "empty_commercial_composer_result",
    "empty_commercial_unit",
    "stable_unique",
]
