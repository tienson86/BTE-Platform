"""Case Thesis result — organizing spine, not a new analytical engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CaseThesisResult:
    """One central human operating pattern derived from current-chart truth."""

    case_id: str
    status: str
    thesis_key: str
    title: str
    short_thesis: str
    expanded_thesis: str
    core_pattern: str
    core_strength: str
    core_tension: str
    corrective_direction: str
    supporting_facts: tuple[str, ...]
    supporting_domains: tuple[str, ...]
    primary_risks: tuple[str, ...]
    primary_capacities: tuple[str, ...]
    career_implication: str
    finance_implication: str
    relationship_implication: str
    health_implication: str
    evidence_ids: tuple[str, ...]
    engine_truth_refs: tuple[str, ...]
    confidence: float
    alternatives: tuple[str, ...]
    diagnostics: tuple[str, ...]
    pattern_function: str = ""
    strength_function: str = ""
    useful_function: str = ""
    ky_function: str = ""
    tension_id: str = ""
    corrective_id: str = ""
    thesis_evidence_coverage: float = 1.0
    thesis_domain_coverage: float = 1.0
    thesis_specificity: float = 0.0
    unsupported_thesis_claims: int = 0
    core_tension_present: float = 0.0
    corrective_direction_present: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize the case thesis without adding architecture fields."""
        return {
            "case_id": self.case_id,
            "status": self.status,
            "thesis_key": self.thesis_key,
            "title": self.title,
            "short_thesis": self.short_thesis,
            "expanded_thesis": self.expanded_thesis,
            "core_pattern": self.core_pattern,
            "core_strength": self.core_strength,
            "core_tension": self.core_tension,
            "corrective_direction": self.corrective_direction,
            "supporting_facts": list(self.supporting_facts),
            "supporting_domains": list(self.supporting_domains),
            "primary_risks": list(self.primary_risks),
            "primary_capacities": list(self.primary_capacities),
            "career_implication": self.career_implication,
            "finance_implication": self.finance_implication,
            "relationship_implication": self.relationship_implication,
            "health_implication": self.health_implication,
            "evidence_ids": list(self.evidence_ids),
            "engine_truth_refs": list(self.engine_truth_refs),
            "confidence": self.confidence,
            "alternatives": list(self.alternatives),
            "diagnostics": list(self.diagnostics),
            "pattern_function": self.pattern_function,
            "strength_function": self.strength_function,
            "useful_function": self.useful_function,
            "ky_function": self.ky_function,
            "tension_id": self.tension_id,
            "corrective_id": self.corrective_id,
            "thesis_evidence_coverage": self.thesis_evidence_coverage,
            "thesis_domain_coverage": self.thesis_domain_coverage,
            "thesis_specificity": self.thesis_specificity,
            "unsupported_thesis_claims": self.unsupported_thesis_claims,
            "core_tension_present": self.core_tension_present,
            "corrective_direction_present": self.corrective_direction_present,
        }


@dataclass(frozen=True, slots=True)
class ThesisComparison:
    """Cross-case similarity of source structure, not wording polish."""

    structural_similarity: float
    narrative_similarity: float
    overgeneralized: bool
    diagnostics: tuple[str, ...]
    differing_axes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize one comparison."""
        return {
            "structural_similarity": self.structural_similarity,
            "narrative_similarity": self.narrative_similarity,
            "overgeneralized": self.overgeneralized,
            "diagnostics": list(self.diagnostics),
            "differing_axes": list(self.differing_axes),
        }


INCOMPLETE_THESIS = CaseThesisResult(
    case_id="",
    status="incomplete",
    thesis_key="",
    title="",
    short_thesis="",
    expanded_thesis="",
    core_pattern="",
    core_strength="",
    core_tension="",
    corrective_direction="",
    supporting_facts=(),
    supporting_domains=(),
    primary_risks=(),
    primary_capacities=(),
    career_implication="",
    finance_implication="",
    relationship_implication="",
    health_implication="",
    evidence_ids=(),
    engine_truth_refs=(),
    confidence=0.0,
    alternatives=(),
    diagnostics=("case_thesis_incomplete",),
)
