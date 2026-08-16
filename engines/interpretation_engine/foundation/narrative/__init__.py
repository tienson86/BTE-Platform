"""Narrative Composer V2 — composition layer over already-validated bundles."""

from engines.interpretation_engine.foundation.narrative.case_thesis import (
    CaseThesisResult,
    compare_case_theses,
    generate_case_thesis,
)
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
from engines.interpretation_engine.foundation.narrative.result_v2 import (
    narrative_result_v2_to_dict,
)
from engines.interpretation_engine.foundation.narrative.production import (
    build_composer_input_from_production,
)

__all__ = [
    "CANONICAL_BUNDLE_KINDS",
    "CUSTOMER_DOMAINS",
    "CaseThesisResult",
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
    "compare_case_theses",
    "generate_case_thesis",
    "narrative_result_v2_to_dict",
]
