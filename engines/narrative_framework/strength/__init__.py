"""INT-02B Strength Narrative public API."""

from .classify import classify_strength_evidence
from .compose import compose_strength_narrative
from .constants import STRENGTH_BLOCKS, STRENGTH_BLOCK_TITLES, TOPIC_ID
from .evidence import bind_strength_evidence
from .impact import build_impact
from .models import (
    StrengthEvidence,
    StrengthNarrativeBlock,
    StrengthNarrativeEvidencePack,
    StrengthNarrativeUnit,
)
from .observation import build_observation
from .reasoning import build_reasoning
from .recommendation import build_recommendation
from .summary import build_summary

__all__ = [
    "STRENGTH_BLOCKS",
    "STRENGTH_BLOCK_TITLES",
    "TOPIC_ID",
    "StrengthEvidence",
    "StrengthNarrativeBlock",
    "StrengthNarrativeEvidencePack",
    "StrengthNarrativeUnit",
    "bind_strength_evidence",
    "build_impact",
    "build_observation",
    "build_reasoning",
    "build_recommendation",
    "build_summary",
    "classify_strength_evidence",
    "compose_strength_narrative",
]
