"""Case Thesis Generator — one organizing spine per chart."""

from engines.interpretation_engine.foundation.narrative.case_thesis.functions import (
    CROSS_CASE_SIMILARITY_MAX,
)
from engines.interpretation_engine.foundation.narrative.case_thesis.generator import (
    generate_case_thesis,
)
from engines.interpretation_engine.foundation.narrative.case_thesis.models import (
    CaseThesisResult,
    ThesisComparison,
)
from engines.interpretation_engine.foundation.narrative.case_thesis.relevance import (
    apply_thesis_relevance,
    filter_evidence_graph,
    recommendation_matches_thesis,
    warning_matches_thesis,
)
from engines.interpretation_engine.foundation.narrative.case_thesis.similarity import (
    compare_case_theses,
    structural_signature,
)

__all__ = [
    "CROSS_CASE_SIMILARITY_MAX",
    "CaseThesisResult",
    "ThesisComparison",
    "apply_thesis_relevance",
    "compare_case_theses",
    "filter_evidence_graph",
    "generate_case_thesis",
    "recommendation_matches_thesis",
    "structural_signature",
    "warning_matches_thesis",
]
