"""Sentence Engine architecture and runtime package.

Infrastructure for sentence *reference* selection, ranking, resolution,
and composition. No sentence library. No natural language generation.
"""

from __future__ import annotations

from engines.interpretation_engine.sentence_engine.composer import Composer
from engines.interpretation_engine.sentence_engine.interface import (
    SentenceEngine,
    SentenceEngineInterface,
)
from engines.interpretation_engine.sentence_engine.metadata import (
    Metadata,
    SentenceCandidate,
    SentenceComposition,
    SentenceRef,
)
from engines.interpretation_engine.sentence_engine.ranking import Ranking
from engines.interpretation_engine.sentence_engine.resolver import Resolver
from engines.interpretation_engine.sentence_engine.selector import Selector

__all__ = [
    "Composer",
    "Metadata",
    "Ranking",
    "Resolver",
    "Selector",
    "SentenceCandidate",
    "SentenceComposition",
    "SentenceEngine",
    "SentenceEngineInterface",
    "SentenceRef",
]
