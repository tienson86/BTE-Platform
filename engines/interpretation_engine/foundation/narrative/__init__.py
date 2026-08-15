"""Narrative Composer V2 — composition layer over already-validated bundles."""

from engines.interpretation_engine.foundation.narrative.composer import (
    NarrativeComposerV2,
    compose_narrative_v2,
    compose_narrative_v2_from_production,
)
from engines.interpretation_engine.foundation.narrative.constants import (
    CANONICAL_BUNDLE_KINDS,
    CUSTOMER_DOMAINS,
    NARRATIVE_SECTIONS,
)
from engines.interpretation_engine.foundation.narrative.input import (
    DecisionBundle,
    KnowledgeBundle,
    NarrativeComposerInput,
    RelationshipBundle,
    StateBundle,
)
from engines.interpretation_engine.foundation.narrative.models import (
    ComposerMetrics,
    EvidenceGraph,
    NarrativeComposerResult,
    NarrativeSection,
)
from engines.interpretation_engine.foundation.narrative.production import (
    build_composer_input_from_production,
)

__all__ = [
    "CANONICAL_BUNDLE_KINDS",
    "CUSTOMER_DOMAINS",
    "ComposerMetrics",
    "DecisionBundle",
    "EvidenceGraph",
    "KnowledgeBundle",
    "NARRATIVE_SECTIONS",
    "NarrativeComposerInput",
    "NarrativeComposerResult",
    "NarrativeComposerV2",
    "NarrativeSection",
    "RelationshipBundle",
    "StateBundle",
    "build_composer_input_from_production",
    "compose_narrative_v2",
    "compose_narrative_v2_from_production",
]
