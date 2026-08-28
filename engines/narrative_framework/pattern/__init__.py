"""INT-02D Pattern Narrative public API."""

from .classify import classify_pattern_evidence
from .compose import compose_pattern_narrative
from .constants import PATTERN_BLOCKS, PATTERN_BLOCK_TITLES, TOPIC_ID
from .evidence import bind_pattern_evidence
from .impact import build_impact
from .models import (
    PatternEvidence,
    PatternNarrativeBlock,
    PatternNarrativeEvidencePack,
    PatternNarrativeUnit,
)
from .observation import build_observation
from .reasoning import build_reasoning
from .recommendation import build_recommendation
from .summary import build_summary

__all__ = [
    "PATTERN_BLOCKS",
    "PATTERN_BLOCK_TITLES",
    "TOPIC_ID",
    "PatternEvidence",
    "PatternNarrativeBlock",
    "PatternNarrativeEvidencePack",
    "PatternNarrativeUnit",
    "bind_pattern_evidence",
    "build_impact",
    "build_observation",
    "build_reasoning",
    "build_recommendation",
    "build_summary",
    "classify_pattern_evidence",
    "compose_pattern_narrative",
]
