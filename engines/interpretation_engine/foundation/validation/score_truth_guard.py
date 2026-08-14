"""Prevent score components from replacing analytical truth."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.interpretation_engine.foundation import diagnostics as diag
from engines.interpretation_engine.foundation.builders.interpretation_facts_builder import (
    InterpretationFactsBundle,
)
from engines.interpretation_engine.foundation.canonical_context import CanonicalAnalysisContext


@dataclass(frozen=True, slots=True)
class ScoreTruthGuardResult:
    """Outcome of score-as-truth validation."""

    passed: bool
    violations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize guard result."""
        return {
            "passed": self.passed,
            "violations": list(self.violations),
        }


def validate_score_not_used_as_truth(
    context: CanonicalAnalysisContext,
    facts: InterpretationFactsBundle,
    *,
    score_payload: Mapping[str, Any] | None = None,
) -> ScoreTruthGuardResult:
    """
    Enforce analytical truth != score component mapping.

    Checks that domain facts were built from engine slices, not score fields.
    """
    violations: list[str] = []
    score = dict(score_payload or {})
    fe = facts.five_elements

    # Analytical strength must exist independently of ScoreEngine component.
    if not context.strength.level and score.get("strength_score") is not None:
        violations.append(diag.SCORE_USED_AS_STRENGTH_TRUTH)

    # Five-elements counts must not be absent while wuxing_score is present.
    if score.get("wuxing_score") is not None and all(
        value is None for value in (fe.wood, fe.fire, fe.earth, fe.metal, fe.water)
    ):
        violations.append(diag.SCORE_USED_AS_WUXING_TRUTH)

    if score.get("ten_god_score") is not None and not facts.ten_gods.visible:
        violations.append(diag.SCORE_USED_AS_TEN_GOD_TRUTH)

    if score.get("useful_god_score") is not None and not facts.useful_god.selected:
        violations.append(diag.SCORE_USED_AS_USEFUL_GOD_TRUTH)

    if score.get("luck_score") is not None and not facts.luck.cycles:
        violations.append(diag.SCORE_USED_AS_LUCK_TRUTH)

    return ScoreTruthGuardResult(
        passed=not violations,
        violations=tuple(dict.fromkeys(violations)),
    )
