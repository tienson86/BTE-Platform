"""Decision Explanation Framework — reusable expert-system explanation contracts."""

from engines.interpretation_engine.foundation.explanation.models import (
    AdviceItem,
    AnalysisFact,
    Decision,
    DecisionAlternative,
    DecisionExplanationResult,
    DecisionPathStep,
    DomainApplication,
    DomainMeaningItem,
    EvidenceItem,
    ExplainabilityMetrics,
    WarningItem,
)
from engines.interpretation_engine.foundation.explanation.metrics import compute_explainability_metrics
from engines.interpretation_engine.foundation.explanation.protocol import DecisionExplainer
from engines.interpretation_engine.foundation.explanation.validation import (
    ValidationIssue,
    validate_decision_explanation,
)

__all__ = [
    "AdviceItem",
    "AnalysisFact",
    "Decision",
    "DecisionAlternative",
    "DecisionExplanationResult",
    "DecisionExplainer",
    "DecisionPathStep",
    "DomainApplication",
    "DomainMeaningItem",
    "EvidenceItem",
    "ExplainabilityMetrics",
    "ValidationIssue",
    "WarningItem",
    "validate_decision_explanation",
]
