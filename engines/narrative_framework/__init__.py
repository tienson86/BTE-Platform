"""INT-02A Narrative Framework — frozen contracts, no runtime engine."""

from .contracts import (
    ANALYTICAL_TOPICS,
    BLOCK_IDS,
    BLOCK_TITLES_VI,
    COMPOSITION_STAGES,
    CONTRACT_ID,
    FRAMEWORK_VERSION,
    INSUFFICIENT_COPY,
    NARRATIVE_BLOCKS,
    SENTENCE_OWNERS,
    TEMPLATE_HIERARCHY,
    WORKSPACE_BLOCK_ALIASES,
    narrative_framework_contract,
)
from .exceptions import NarrativeFrameworkError
from .models import (
    NarrativeBlock,
    NarrativeSentence,
    TopicEvidencePack,
    TopicNarrativeUnit,
)

__all__ = [
    "ANALYTICAL_TOPICS",
    "BLOCK_IDS",
    "BLOCK_TITLES_VI",
    "COMPOSITION_STAGES",
    "CONTRACT_ID",
    "FRAMEWORK_VERSION",
    "INSUFFICIENT_COPY",
    "NARRATIVE_BLOCKS",
    "SENTENCE_OWNERS",
    "TEMPLATE_HIERARCHY",
    "WORKSPACE_BLOCK_ALIASES",
    "NarrativeBlock",
    "NarrativeFrameworkError",
    "NarrativeSentence",
    "TopicEvidencePack",
    "TopicNarrativeUnit",
    "narrative_framework_contract",
]
