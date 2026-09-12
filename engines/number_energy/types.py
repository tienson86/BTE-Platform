"""Result models for Number Energy Engine V1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class DigitType(str, Enum):
    """Internal digit classification from NUMBER_ENERGY_MASTER_KNOWLEDGE_V1."""

    GUA = "gua"
    MODIFIER = "modifier"


class EnergyState(str, Enum):
    """Canonical energy states plus the V1 undefined sentinel."""

    NORMAL = "NORMAL"
    HIDDEN = "HIDDEN"
    AMPLIFIED = "AMPLIFIED"
    REPEATED = "REPEATED"
    CONTROLLED = "CONTROLLED"
    NEUTRALIZED = "NEUTRALIZED"
    UNKNOWN_OR_NOT_DEFINED = "UNKNOWN_OR_NOT_DEFINED"


class PurposeContext(str, Enum):
    """Supported V1 purpose contexts."""

    PHONE_NUMBER = "phone_number"
    CAR_PLATE = "car_plate"
    MOTORBIKE_PLATE = "motorbike_plate"
    ID_NUMBER = "id_number"
    BANK_ACCOUNT = "bank_account"
    HOUSE_NUMBER = "house_number"
    GENERIC_NUMBER = "generic_number"


class Classification(str, Enum):
    """Frozen energy classes."""

    SUPPORTIVE = "supportive"
    SUPPORTIVE_STABILIZING = "supportive_stabilizing"
    CHALLENGING = "challenging"


@dataclass(slots=True)
class ClassifiedDigit:
    """One digit after Layer 2 classification."""

    index: int
    digit: int
    internal_type: str
    gua_or_field: str
    direction: str
    element: str | None
    group: str
    pair_role: str


@dataclass(slots=True)
class ParsedNumber:
    """Layer 1–2 parse result. ``raw_digits`` keeps the original digit order."""

    input_raw: str
    raw_digits: tuple[int, ...]
    classified_digits: tuple[ClassifiedDigit, ...]


@dataclass(slots=True)
class EnergyOccurrence:
    """One detected Du Niên occurrence."""

    occurrence_id: str
    source_span: tuple[int, int]
    source_digits: str
    pair_digits: str
    energy_id: str
    display_name: str
    strength_rank: int | None
    classification: str
    state: str
    via_modifier: int | None
    notes: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one occurrence."""
        return asdict(self)


@dataclass(slots=True)
class UndefinedSegment:
    """A span whose interaction is not frozen in V1."""

    source_span: tuple[int, int]
    source_digits: str
    state: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one undefined segment."""
        return asdict(self)


@dataclass(slots=True)
class SequenceSummary:
    """Aggregation without numeric scoring."""

    dominant_energy_ids: tuple[str, ...]
    strongest_rank: int | None
    repeated_energy_ids: tuple[str, ...]
    controlled_energy_ids: tuple[str, ...]
    challenging_without_control: tuple[str, ...]
    fu_wei_supported: bool
    approved_supportive_chain: bool

    def to_dict(self) -> dict[str, Any]:
        """Serialize sequence summary."""
        return asdict(self)


@dataclass(slots=True)
class CustomerNarrative:
    """Customer-facing Vietnamese copy with V1 safety bounds."""

    language: str
    system_name: str
    system_short_name: str
    summary: str
    paragraphs: tuple[str, ...]
    strengths: tuple[str, ...]
    watchouts: tuple[str, ...]
    purpose_focus: str
    health_disclaimer: str | None
    compatibility_note: str
    unknown_notice: str | None

    def to_dict(self) -> dict[str, Any]:
        """Serialize customer narrative."""
        return asdict(self)


@dataclass(slots=True)
class CustomerPairOccurrence:
    """Customer-safe overlapping pair for adapter input (RB05-A)."""

    index: int
    pair_digits: str
    display_name: str
    category: str
    category_label: str
    strength_label: str
    strength_slots: int
    strength_visual: tuple[bool, bool, bool, bool]

    def to_dict(self) -> dict[str, Any]:
        """Serialize without technical rank, state, or energy_id."""
        return {
            "index": self.index,
            "pair_digits": self.pair_digits,
            "display_name": self.display_name,
            "category": self.category,
            "category_label": self.category_label,
            "strength_label": self.strength_label,
            "strength_slots": self.strength_slots,
            "strength_visual": list(self.strength_visual),
        }


@dataclass(slots=True)
class PairSummaryView:
    """Pair-count summary. Counts are pairs, not unique energy groups."""

    pair_count: int
    supportive_pair_count: int
    challenging_pair_count: int
    primary_energy_label: str | None
    terminal_energy_label: str | None
    terminal_pair_digits: str | None

    def to_dict(self) -> dict[str, Any]:
        """Serialize pair_summary for the public API."""
        return {
            "pair_count": self.pair_count,
            "supportive_pair_count": self.supportive_pair_count,
            "challenging_pair_count": self.challenging_pair_count,
            "primary_energy_label": self.primary_energy_label,
            "terminal_energy_label": self.terminal_energy_label,
            "terminal_pair_digits": self.terminal_pair_digits,
        }


@dataclass(slots=True)
class EnergyDistributionRow:
    """One of eight catalog energies, including zero counts."""

    energy_label: str
    count: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize one distribution row without energy_id."""
        return {
            "energy_label": self.energy_label,
            "count": self.count,
        }


@dataclass(slots=True)
class CustomerTripleOccurrence:
    """Customer-safe overlapping triple for adapter input (RB05-B)."""

    index: int
    digits: str
    left_pair_digits: str
    right_pair_digits: str
    left_energy_label: str
    right_energy_label: str
    interaction_label: str
    canonical_meaning_key: str | None
    customer_summary_key: str | None
    customer_title: str | None
    customer_summary: str | None
    priority: str | None
    domains: tuple[str, ...]
    interpretation_status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize without energy_id, rank, state, or source_span."""
        return {
            "index": self.index,
            "digits": self.digits,
            "left_pair_digits": self.left_pair_digits,
            "right_pair_digits": self.right_pair_digits,
            "left_energy_label": self.left_energy_label,
            "right_energy_label": self.right_energy_label,
            "interaction_label": self.interaction_label,
            "canonical_meaning_key": self.canonical_meaning_key,
            "customer_summary_key": self.customer_summary_key,
            "customer_title": self.customer_title,
            "customer_summary": self.customer_summary,
            "priority": self.priority,
            "domains": list(self.domains),
            "interpretation_status": self.interpretation_status,
        }


@dataclass(slots=True)
class NumberEnergyChainView:
    """Customer-safe chain snapshot. Not a wealth-flow resolver."""

    primary_energy_label: str | None
    primary_energy_pairs: tuple[str, ...]
    secondary_energy_labels: tuple[str, ...]
    terminal_pair_digits: str | None
    terminal_energy_label: str | None
    terminal_triple_digits: str | None
    terminal_interaction_label: str | None
    dominant_flow_summary: str | None

    def to_dict(self) -> dict[str, Any]:
        """Serialize chain labels only — no energy_id."""
        return {
            "primary_energy_label": self.primary_energy_label,
            "primary_energy_pairs": list(self.primary_energy_pairs),
            "secondary_energy_labels": list(self.secondary_energy_labels),
            "terminal_pair_digits": self.terminal_pair_digits,
            "terminal_energy_label": self.terminal_energy_label,
            "terminal_triple_digits": self.terminal_triple_digits,
            "terminal_interaction_label": self.terminal_interaction_label,
            "dominant_flow_summary": self.dominant_flow_summary,
        }


@dataclass(slots=True)
class CustomerWealthNode:
    """Customer-safe wealth node. Roles are presentation labels, not engine enums."""

    role: str
    reference_kind: str
    reference_digits: str
    evidence_digits: str
    source_energy_label: str | None
    target_energy_label: str | None
    interaction_label: str | None
    customer_headline: str | None
    customer_summary: str | None
    customer_summary_key: str | None
    interpretation_status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize without rank, state, energy_id, or source_span."""
        return {
            "role": self.role,
            "reference_kind": self.reference_kind,
            "reference_digits": self.reference_digits,
            "evidence_digits": self.evidence_digits,
            "source_energy_label": self.source_energy_label,
            "target_energy_label": self.target_energy_label,
            "interaction_label": self.interaction_label,
            "customer_headline": self.customer_headline,
            "customer_summary": self.customer_summary,
            "customer_summary_key": self.customer_summary_key,
            "interpretation_status": self.interpretation_status,
        }


@dataclass(slots=True)
class WealthStageView:
    """One of four Phone Wealth Flow customer stages."""

    id: str
    label: str
    headline: str
    evidence: str
    interaction: str
    narrative: str
    interpretation_status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one customer stage."""
        return {
            "id": self.id,
            "label": self.label,
            "headline": self.headline,
            "evidence": self.evidence,
            "interaction": self.interaction,
            "narrative": self.narrative,
            "interpretation_status": self.interpretation_status,
        }


@dataclass(slots=True)
class WealthFlowView:
    """Four-stage phone wealth flow. Not a score and not a recommendation."""

    stages: tuple[WealthStageView, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize wealth_flow.stages only."""
        return {"stages": [item.to_dict() for item in self.stages]}


@dataclass(slots=True)
class LaterOutcomeView:
    """Terminal / hậu vận snapshot from chain structure."""

    terminal_pair_digits: str | None
    terminal_energy_label: str | None
    terminal_triple_digits: str | None
    terminal_interaction_label: str | None
    customer_summary: str | None

    def to_dict(self) -> dict[str, Any]:
        """Serialize later_outcome without energy_id or rank."""
        return {
            "terminal_pair_digits": self.terminal_pair_digits,
            "terminal_energy_label": self.terminal_energy_label,
            "terminal_triple_digits": self.terminal_triple_digits,
            "terminal_interaction_label": self.terminal_interaction_label,
            "customer_summary": self.customer_summary,
        }


@dataclass(slots=True)
class WealthStoryView:
    """Customer-safe structural wealth story. No financial guarantee."""

    nodes: tuple[str, ...]
    display: str
    synthesis: str | None

    def to_dict(self) -> dict[str, Any]:
        """Serialize wealth_story as labels plus synthesis."""
        return {
            "nodes": list(self.nodes),
            "display": self.display,
            "synthesis": self.synthesis,
        }


@dataclass(slots=True)
class EvidenceRefView:
    """Pointer to an already-emitted RB05-A/B/C object. No score refs."""

    source: str
    ref: str
    label: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize source + customer label only."""
        return {
            "source": self.source,
            "ref": self.ref,
            "label": self.label,
        }


@dataclass(slots=True)
class EvidenceGroupView:
    """Customer-safe evidence group for basis presentation."""

    title: str
    source: str
    items: tuple[EvidenceRefView, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize grouped refs without technical ids."""
        return {
            "title": self.title,
            "source": self.source,
            "items": [item.to_dict() for item in self.items],
        }


@dataclass(slots=True)
class FindingView:
    """One customer strength or caution. Not a recommendation."""

    id: str
    title: str
    summary: str
    semantic_key: str
    evidence_refs: tuple[EvidenceRefView, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize finding copy plus customer-safe refs."""
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "semantic_key": self.semantic_key,
            "evidence_refs": [item.to_dict() for item in self.evidence_refs],
        }


@dataclass(slots=True)
class DomainInsightView:
    """One of five required customer domain cards."""

    id: str
    domain: str
    conclusion: str
    narrative: str
    caution: str
    conclusion_key: str
    narrative_key: str
    caution_key: str | None
    evidence_refs: tuple[EvidenceRefView, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize domain insight without rank, state, or energy_id."""
        return {
            "id": self.id,
            "domain": self.domain,
            "conclusion": self.conclusion,
            "narrative": self.narrative,
            "caution": self.caution,
            "conclusion_key": self.conclusion_key,
            "narrative_key": self.narrative_key,
            "caution_key": self.caution_key,
            "evidence_refs": [item.to_dict() for item in self.evidence_refs],
        }


@dataclass(slots=True)
class AssessmentView:
    """Customer-safe overall assessment. Not a score and not Expert Mode."""

    title: str
    summary: str
    story_line: str
    story_nodes: tuple[str, ...]
    story_key: str | None

    def to_dict(self) -> dict[str, Any]:
        """Serialize assessment labels only."""
        return {
            "title": self.title,
            "summary": self.summary,
            "story_line": self.story_line,
            "story_nodes": list(self.story_nodes),
            "story_key": self.story_key,
        }


@dataclass(slots=True)
class RecommendationView:
    """Phone recommendation from structure, never from score."""

    label: str | None
    summary: str
    copy_key: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize customer-safe recommendation; state is the customer label."""
        return {
            "state": self.label,
            "label": self.label,
            "summary": self.summary,
            "copy_key": self.copy_key,
        }


@dataclass(slots=True)
class ScoreBreakdownRow:
    """One of five Phone Score dimensions."""

    label: str
    earned: int
    max_points: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize earned/max without percent."""
        return {
            "label": self.label,
            "earned": self.earned,
            "max": self.max_points,
            "display": f"{self.earned} / {self.max_points}",
        }


@dataclass(slots=True)
class ScoreReasonView:
    """Customer-safe score reason. Summarizes findings; does not create them."""

    title: str
    summary: str
    reason_key: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize reason copy only."""
        return {
            "title": self.title,
            "summary": self.summary,
            "reason_key": self.reason_key,
        }


@dataclass(slots=True)
class PhoneScoreView:
    """Phone Score Result after interpretation. Not a recommendation driver."""

    total: int
    max_points: int
    grade: str
    breakdown: tuple[ScoreBreakdownRow, ...]
    reasons: tuple[ScoreReasonView, ...]
    verified_by_runtime: bool

    def to_dict(self) -> dict[str, Any]:
        """Serialize 0–100 score, five rows, and reasons."""
        return {
            "total": self.total,
            "max": self.max_points,
            "display": f"{self.total} / {self.max_points}",
            "grade": self.grade,
            "breakdown": [item.to_dict() for item in self.breakdown],
            "reasons": [item.to_dict() for item in self.reasons],
            "verified_by_runtime": self.verified_by_runtime,
        }


@dataclass(slots=True)
class NumberEnergyResult:
    """Canonical engine result for one number string."""

    input_raw: str
    raw_digits: tuple[int, ...]
    classified_digits: tuple[ClassifiedDigit, ...]
    occurrences: tuple[EnergyOccurrence, ...]
    undefined_segments: tuple[UndefinedSegment, ...]
    sequence_state: str
    sequence_states: tuple[str, ...]
    approved_patterns: tuple[str, ...]
    purpose_context: str
    summary: SequenceSummary
    narrative: CustomerNarrative
    expert_notes: tuple[str, ...]
    knowledge_version: str = "1.0"
    analyzed_input: str = ""
    leading_phone_zero: bool = False
    reading: dict[str, Any] | None = None
    pair_occurrences: tuple[CustomerPairOccurrence, ...] = ()
    pair_summary: PairSummaryView | None = None
    energy_distribution: tuple[EnergyDistributionRow, ...] = ()
    triple_occurrences: tuple[CustomerTripleOccurrence, ...] = ()
    chain: NumberEnergyChainView | None = None
    wealth_nodes: tuple[CustomerWealthNode, ...] = ()
    wealth_flow: WealthFlowView | None = None
    later_outcome: LaterOutcomeView | None = None
    wealth_story: WealthStoryView | None = None
    domain_insights: tuple[DomainInsightView, ...] = ()
    strengths: tuple[FindingView, ...] = ()
    cautions: tuple[FindingView, ...] = ()
    evidence: tuple[EvidenceGroupView, ...] = ()
    assessment: AssessmentView | None = None
    recommendation: RecommendationView | None = None
    score: PhoneScoreView | None = None
    verified_by_runtime: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation layers."""
        return {
            "input_raw": self.input_raw,
            "raw_digits": list(self.raw_digits),
            "classified_digits": [asdict(item) for item in self.classified_digits],
            "occurrences": [item.to_dict() for item in self.occurrences],
            "undefined_segments": [item.to_dict() for item in self.undefined_segments],
            "sequence_state": self.sequence_state,
            "sequence_states": list(self.sequence_states),
            "approved_patterns": list(self.approved_patterns),
            "purpose_context": self.purpose_context,
            "summary": self.summary.to_dict(),
            "narrative": self.narrative.to_dict(),
            "expert_notes": list(self.expert_notes),
            "knowledge_version": self.knowledge_version,
            "system_name": "Bát Cực Linh Số",
            "system_short_name": "Năng lượng số",
            "analyzed_input": self.analyzed_input or self.input_raw,
            "leading_phone_zero": self.leading_phone_zero,
            "reading": self.reading,
            "pair_occurrences": [item.to_dict() for item in self.pair_occurrences],
            "pair_summary": (
                self.pair_summary.to_dict() if self.pair_summary is not None else None
            ),
            "energy_distribution": [item.to_dict() for item in self.energy_distribution],
            "triple_occurrences": [item.to_dict() for item in self.triple_occurrences],
            "chain": self.chain.to_dict() if self.chain is not None else None,
            "wealth_nodes": [item.to_dict() for item in self.wealth_nodes],
            "wealth_flow": (
                self.wealth_flow.to_dict() if self.wealth_flow is not None else None
            ),
            "later_outcome": (
                self.later_outcome.to_dict()
                if self.later_outcome is not None
                else None
            ),
            "wealth_story": (
                self.wealth_story.to_dict() if self.wealth_story is not None else None
            ),
            "domain_insights": [item.to_dict() for item in self.domain_insights],
            "strengths": [item.to_dict() for item in self.strengths],
            "cautions": [item.to_dict() for item in self.cautions],
            "evidence": [item.to_dict() for item in self.evidence],
            "assessment": (
                self.assessment.to_dict() if self.assessment is not None else None
            ),
            "recommendation": (
                self.recommendation.to_dict()
                if self.recommendation is not None
                else None
            ),
            "score": self.score.to_dict() if self.score is not None else None,
            "grade": self.score.grade if self.score is not None else None,
            "verified_by_runtime": self.verified_by_runtime,
        }
