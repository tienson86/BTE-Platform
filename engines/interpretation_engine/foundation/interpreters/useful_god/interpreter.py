"""Useful God interpreter — framework-backed with B1 backward compatibility."""

from __future__ import annotations

from engines.interpretation_engine.foundation.explanation.models import DecisionExplanationResult
from engines.interpretation_engine.foundation.facts.useful_god import UsefulGodInterpretationFacts
from engines.interpretation_engine.foundation.interpreters.useful_god.adapter import (
    to_useful_god_interpretation_result,
)
from engines.interpretation_engine.foundation.interpreters.useful_god.explainer import (
    UsefulGodExplainer,
)
from engines.interpretation_engine.foundation.interpreters.useful_god.result import (
    UsefulGodInterpretationResult,
)


class UsefulGodInterpreter:
    """Transform UsefulGodInterpretationFacts into structured interpretation."""

    def __init__(self) -> None:
        """Initialize explainer delegate."""
        self._explainer = UsefulGodExplainer()

    def explain(self, facts: UsefulGodInterpretationFacts) -> DecisionExplanationResult:
        """Return framework DecisionExplanationResult."""
        return self._explainer.explain(facts)

    def interpret(self, facts: UsefulGodInterpretationFacts) -> UsefulGodInterpretationResult:
        """Return backward-compatible B1 UsefulGodInterpretationResult."""
        return to_useful_god_interpretation_result(self.explain(facts))
