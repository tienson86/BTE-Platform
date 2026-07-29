"""Style Layer (WP7C) — ParagraphContext → StyledParagraphContext."""

from __future__ import annotations

from .emphasis_controller import EmphasisController
from .redundancy_reducer import RedundancyReducer
from .style_builder import StyleBuilder
from .style_models import (
    StyledParagraph,
    StyledParagraphContext,
    StyledSentence,
    StyleKnowledge,
)
from .synonym_rewriter import SynonymRewriter
from .tone_controller import ToneController

__all__ = [
    "EmphasisController",
    "RedundancyReducer",
    "StyleBuilder",
    "StyledParagraph",
    "StyledParagraphContext",
    "StyledSentence",
    "StyleKnowledge",
    "SynonymRewriter",
    "ToneController",
]
