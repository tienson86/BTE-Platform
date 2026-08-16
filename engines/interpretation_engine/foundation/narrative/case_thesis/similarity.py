"""Cross-case similarity guard for Case Thesis.

Compares structural source axes, not wording polish.
"""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.case_thesis.functions import (
    CROSS_CASE_SIMILARITY_MAX,
)
from engines.interpretation_engine.foundation.narrative.case_thesis.models import (
    CaseThesisResult,
    ThesisComparison,
)
from engines.interpretation_engine.foundation.narrative.text import fingerprint

_DIAGNOSTIC = "case_thesis_overgeneralized"


def structural_signature(thesis: CaseThesisResult) -> frozenset[str]:
    """Axes that must differ when analytical truth differs."""
    key_parts = [part for part in thesis.thesis_key.split("|") if part]
    return frozenset(
        item
        for item in (
            *key_parts,
            thesis.pattern_function,
            thesis.strength_function,
            thesis.useful_function,
            thesis.ky_function,
            thesis.tension_id,
            thesis.corrective_id,
            thesis.core_pattern,
        )
        if item
    )


def compare_case_theses(
    left: CaseThesisResult,
    right: CaseThesisResult,
    *,
    similarity_max: float = CROSS_CASE_SIMILARITY_MAX,
) -> ThesisComparison:
    """Compare two theses. Overgeneralization is a diagnostic, not a rewrite."""
    left_sig = structural_signature(left)
    right_sig = structural_signature(right)
    structural = _jaccard(left_sig, right_sig)
    narrative = _narrative_similarity(left, right)
    differing = tuple(sorted((left_sig | right_sig) - (left_sig & right_sig)))
    collapsed = (
        left.status == "complete"
        and right.status == "complete"
        and structural < similarity_max
        and _outputs_collapsed(left, right)
    )
    diagnostics = (_DIAGNOSTIC,) if collapsed else ()
    return ThesisComparison(
        structural_similarity=structural,
        narrative_similarity=narrative,
        overgeneralized=collapsed,
        diagnostics=diagnostics,
        differing_axes=differing,
    )


def _outputs_collapsed(left: CaseThesisResult, right: CaseThesisResult) -> bool:
    """True when customer-visible spine is the same despite different sources."""
    return (
        left.title == right.title
        and left.tension_id == right.tension_id
        and left.corrective_id == right.corrective_id
        and fingerprint(left.short_thesis) == fingerprint(right.short_thesis)
    )


def _narrative_similarity(left: CaseThesisResult, right: CaseThesisResult) -> float:
    """Token overlap of title, tension, and corrective — secondary to structure."""
    left_tokens = _tokens(left)
    right_tokens = _tokens(right)
    return _jaccard(left_tokens, right_tokens)


def _tokens(thesis: CaseThesisResult) -> frozenset[str]:
    """Visible spine tokens used only for narrative similarity."""
    blob = " ".join(
        (
            thesis.title,
            thesis.core_tension,
            thesis.corrective_direction,
            thesis.career_implication,
        )
    )
    return frozenset(item for item in fingerprint(blob).split() if len(item) > 2)


def _jaccard(left: frozenset[str], right: frozenset[str]) -> float:
    """Set overlap in [0, 1]. Empty vs empty is identical."""
    if not left and not right:
        return 1.0
    union = left | right
    if not union:
        return 1.0
    return len(left & right) / len(union)
