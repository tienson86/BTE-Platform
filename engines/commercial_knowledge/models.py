"""Commercial Knowledge models (Retrieval Contract v1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

CONTRACT_ID = "bte.commercial_knowledge.retrieval.v1"
CONTRACT_VERSION = "1.0.0"

WAVE_1_1_ALLOW_LIST: frozenset[str] = frozenset(
    {
        "KU-ID-001",
        "KU-ST-001",
        "KU-WK-001",
        "KU-UG-001",
        "KU-RC-001",
    }
)

# Domain 01 — Career Selection Assessment (Production Capability V1 · Frozen).
CAREER_SELECTION_ALLOW_LIST: frozenset[str] = frozenset(
    {
        "KU-CN-CA-000001",
        "KU-CN-CA-000010",
        "KU-CN-CA-000011",
        "KU-CN-CA-000012",
        "KU-CN-CA-000013",
        "KU-CN-CA-000014",
        "KU-RK-CA-000010",
        "KU-MT-CA-000010",
        "KU-CN-CA-000015",
        "KU-CN-CA-000016",
        "KU-AC-CA-000001",
    }
)

# Domain 01 — Promotion Readiness Assessment (Production Capability V1).
PROMOTION_READINESS_ALLOW_LIST: frozenset[str] = frozenset(
    {
        "KU-CN-CA-000020",
        "KU-CN-CA-000021",
        "KU-CN-CA-000022",
        "KU-CN-CA-000023",
        "KU-CN-CA-000024",
        "KU-CN-CA-000025",
        "KU-OP-CA-000001",
        "KU-RK-CA-000020",
        "KU-MT-CA-000020",
        "KU-AC-CA-000020",
    }
)

PRODUCTION_ALLOW_LIST: frozenset[str] = (
    WAVE_1_1_ALLOW_LIST
    | CAREER_SELECTION_ALLOW_LIST
    | PROMOTION_READINESS_ALLOW_LIST
)

CAPABILITY_CAREER_SELECTION = "CAP-D1-CA-SEL"
CAPABILITY_PROMOTION_READINESS = "CAP-D1-CA-PRO"

DEFAULT_TARGET_COMPONENTS: tuple[str, ...] = (
    "executive_summary",
    "recommendation",
    "observation",
    "reasoning",
    "warning",
    "conclusion",
    "impact",
)

# evidence_kind → Career Selection Assessment field
CAREER_SELECTION_FIELD_BY_KIND: dict[str, str] = {
    "career_direction": "career_direction",
    "career_environment": "working_environment",
    "career_org_role": "preferred_role",
    "career_lead_vs_spec": "leadership_posture",
    "career_path_mode": "employment_posture",
    "career_advantage": "career_strengths",
    "career_risk": "career_risks",
    "career_mitigation": "career_mitigation",
    "career_development": "development_focus",
    "career_timing": "timing_guidance",
}

# evidence_kind → Promotion Readiness Assessment field
PROMOTION_READINESS_FIELD_BY_KIND: dict[str, str] = {
    "promotion_readiness": "promotion_readiness",
    "promotion_mgmt_role": "management_role_posture",
    "promotion_competency_gaps": "competency_gaps",
    "promotion_strengths": "promotion_strengths",
    "promotion_posture": "advancement_posture",
    "promotion_timing": "timing_guidance",
    "promotion_window": "advancement_window",
    "promotion_risk": "promotion_risks",
    "promotion_mitigation": "promotion_mitigation",
    "promotion_action_90d": "action_plan_90d",
}


@dataclass(slots=True)
class RetrievalRequest:
    """Inputs for commercial knowledge retrieval."""

    analysis_signals: dict[str, Any]
    scenario_id: str = "default"
    allow_list_ids: frozenset[str] = WAVE_1_1_ALLOW_LIST
    target_components: tuple[str, ...] = DEFAULT_TARGET_COMPONENTS
    locale: str = "vi"
    run_id: str = ""


@dataclass(slots=True)
class SelectedUnitSummary:
    """Allow-listed unit summary for traces — not a raw Knowledge Unit dump."""

    knowledge_unit_id: str
    version: str
    evidence_kind: str
    priority: int
    confidence: float
    narrative_targets: tuple[str, ...] = ()


@dataclass(slots=True)
class DroppedUnit:
    """Record of a unit that was considered but not selected."""

    knowledge_unit_id: str
    reason: str


@dataclass(slots=True)
class BundleItem:
    """One customer-facing commercial statement with provenance."""

    text: str
    evidence_kind: str
    knowledge_unit_id: str
    version: str
    component_targets: tuple[str, ...]
    signal_refs: tuple[str, ...]
    confidence: float
    role: str = ""


@dataclass(slots=True)
class CareerSelectionAssessment:
    """
    Career Selection Assessment capability projection.

    Narrative / Portal consume this object — never raw Knowledge Units.
    """

    capability_id: str = CAPABILITY_CAREER_SELECTION
    status: str = "empty"
    career_direction: BundleItem | None = None
    working_environment: BundleItem | None = None
    preferred_role: BundleItem | None = None
    leadership_posture: BundleItem | None = None
    employment_posture: BundleItem | None = None
    career_strengths: BundleItem | None = None
    career_risks: BundleItem | None = None
    career_mitigation: BundleItem | None = None
    development_focus: BundleItem | None = None
    timing_guidance: BundleItem | None = None
    action_plan_90d: BundleItem | None = None
    knowledge_unit_ids: tuple[str, ...] = ()


@dataclass(slots=True)
class PromotionReadinessAssessment:
    """
    Promotion Readiness Assessment capability projection.

    Narrative / Portal consume this object — never raw Knowledge Units.
    """

    capability_id: str = CAPABILITY_PROMOTION_READINESS
    status: str = "empty"
    promotion_readiness: BundleItem | None = None
    management_role_posture: BundleItem | None = None
    competency_gaps: BundleItem | None = None
    promotion_strengths: BundleItem | None = None
    advancement_posture: BundleItem | None = None
    timing_guidance: BundleItem | None = None
    advancement_window: BundleItem | None = None
    promotion_risks: BundleItem | None = None
    promotion_mitigation: BundleItem | None = None
    action_plan_90d: BundleItem | None = None
    knowledge_unit_ids: tuple[str, ...] = ()


@dataclass(slots=True)
class CommercialKnowledgeBundle:
    """
    Narrative-facing commercial bundle.

    Must not expose raw Knowledge Unit records.
    """

    contract_id: str = CONTRACT_ID
    contract_version: str = CONTRACT_VERSION
    bundle_id: str = ""
    scenario_id: str = "default"
    bundle_status: str = "empty"
    identity: tuple[BundleItem, ...] = ()
    strengths: tuple[BundleItem, ...] = ()
    weaknesses: tuple[BundleItem, ...] = ()
    useful_god: tuple[BundleItem, ...] = ()
    recommendations: tuple[BundleItem, ...] = ()
    warnings: tuple[BundleItem, ...] = ()
    opportunities: tuple[BundleItem, ...] = ()
    career_selection: CareerSelectionAssessment | None = None
    promotion_readiness: PromotionReadinessAssessment | None = None
    confidence: float = 0.0
    selected_units: tuple[SelectedUnitSummary, ...] = ()
    dropped_units: tuple[DroppedUnit, ...] = ()
    traceability: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class NarrativeEvidenceUnit:
    """Narrative-ready evidence unit derived from the bundle."""

    evidence_kind: str
    text: str
    knowledge_unit_id: str
    version: str
    component_targets: tuple[str, ...]
    signal_refs: tuple[str, ...]
    confidence: float


@dataclass(slots=True)
class NarrativeKnowledgePayload:
    """Payload Narrative consumes (via merge helper) — never raw KUs."""

    evidence_units: tuple[NarrativeEvidenceUnit, ...] = ()
    bundle_id: str = ""
    bundle_status: str = "empty"
