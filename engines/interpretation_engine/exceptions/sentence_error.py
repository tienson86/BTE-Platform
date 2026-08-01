"""Sentence Engine exception."""

from __future__ import annotations

from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)


class SentenceEngineError(InterpretationArchitectureError):
    """Raised for sentence engine infrastructure failures.

    Does not indicate natural-language generation errors — Pack 03 sentence
    engine has no NLG surface.
    """
