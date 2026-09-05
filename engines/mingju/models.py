"""MC-01 result and context models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.mingju.enums import AnalysisState, IntegrityState, MingJuDecisionStatus, PatternGrade
from engines.mingju.versions import RULESET_VERSION, SCHEMA_COMPOSER, SCHEMA_CONTEXT, SCHEMA_DECISION


def _empty_dict() -> dict[str, Any]:
    return {}


@dataclass(slots=True)
class ScoreResult:
    """Generic 0..100 score object."""

    score: float | None = None
    minimum: float = 0.0
    maximum: float = 100.0
    normalized: float | None = None
    state: str = AnalysisState.UNRESOLVED.value
    confidence: float = 0.0
    evidence_ids: tuple[str, ...] = ()


@dataclass(slots=True)
class EvidenceItem:
    """Traceable evidence record."""

    evidence_id: str
    kind: str
    statement_key: str
    source: str = ""
    details: dict[str, Any] = field(default_factory=_empty_dict)


@dataclass(slots=True)
class TraceItem:
    """One reasoning step."""

    trace_id: str
    stage: str
    rule_id: str
    summary_key: str
    evidence_ids: tuple[str, ...] = ()


@dataclass(slots=True)
class WarningItem:
    """Non-fatal warning."""

    warning_id: str
    code: str
    message_key: str


@dataclass(slots=True)
class GodActivation:
    """Normalized Ten God presence consumed from upstream facts."""

    god_id: str
    label: str
    family: str
    pillar: str
    layer: str
    stem: str = ""
    element: str = ""
    activation: float = 0.0
    material: bool = False


@dataclass(slots=True)
class PatternDecision:
    """Normalized Pattern Engine identity. MC-01 does not reclassify."""

    state: str = AnalysisState.UNRESOLVED.value
    pattern_id: str = ""
    label: str = ""
    family: str = ""
    source: str = "canonical_pattern_engine"
    source_code: str = ""
    secondary_ids: tuple[str, ...] = ()
    month_branch: str = ""
    month_main_qi: str = ""
    month_main_qi_ten_god: str = ""
    day_master: str = ""
    evidence_ids: tuple[str, ...] = ()
    confidence: float = 0.0


@dataclass(slots=True)
class PurityFactor:
    """One purity increase/decrease factor."""

    factor_id: str
    factor_type: str
    effect: str
    severity: str
    description_key: str
    evidence_ids: tuple[str, ...] = ()
    rule_id: str = ""


@dataclass(slots=True)
class PatternPurityResult:
    """Pattern purity independent of Pattern Strength and Grade."""

    state: str = AnalysisState.UNRESOLVED.value
    classification: str = "unresolved"
    score: float | None = None
    factors: tuple[PurityFactor, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    confidence: float = 0.0


@dataclass(slots=True)
class PatternStrengthResult:
    """Pattern Strength, not Day Master Strength."""

    state: str = AnalysisState.UNRESOLVED.value
    classification: str = "unresolved"
    score: float | None = None
    season_power: float | None = None
    root_power: float | None = None
    exposure_power: float | None = None
    generation_power: float | None = None
    continuity_power: float | None = None
    position_power: float | None = None
    evidence_ids: tuple[str, ...] = ()
    confidence: float = 0.0


@dataclass(slots=True)
class SupportResult:
    """Support synthesis for the primary pattern."""

    state: str = AnalysisState.UNRESOLVED.value
    classification: str = "unresolved"
    score: float | None = None
    generating_support: float = 0.0
    controlling_support: float = 0.0
    evidence_ids: tuple[str, ...] = ()
    confidence: float = 0.0


@dataclass(slots=True)
class DamageFinding:
    """Confirmed structural Damage. Co-presence alone is not enough."""

    damage_id: str
    damage_type: str
    source: str
    target: str
    severity: str
    directness: str = "indirect"
    reversibility: str = "unknown"
    state: str = "confirmed"
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    rule_id: str = ""
    confidence: float = 0.0
    causal_group: str = ""


@dataclass(slots=True)
class DamageResult:
    """Damage collection."""

    state: str = AnalysisState.RESOLVED.value
    findings: tuple[DamageFinding, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    confidence: float = 0.0


@dataclass(slots=True)
class RescueFinding:
    """Rescue that targets a registered Damage."""

    rescue_id: str
    rescue_type: str
    source: str
    target_damage_ids: tuple[str, ...]
    strength: str
    reliability: str = "conditional"
    coverage: str = "partial"
    damage_offset: float | None = None
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    rule_id: str = ""
    confidence: float = 0.0


@dataclass(slots=True)
class RescueResult:
    """Rescue collection. Empty is valid when no Damage exists."""

    state: str = AnalysisState.RESOLVED.value
    findings: tuple[RescueFinding, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    confidence: float = 0.0


@dataclass(slots=True)
class CompatibilityResult:
    """Useful God or climate compatibility with the pattern."""

    state: str = AnalysisState.UNRESOLVED.value
    classification: str = "unresolved"
    score: float | None = None
    evidence_ids: tuple[str, ...] = ()
    confidence: float = 0.0


@dataclass(slots=True)
class StructuralIntegrityResult:
    """Integrity synthesis. Grade must consume this, not duplicate it."""

    state: str = IntegrityState.UNRESOLVED.value
    score: float | None = None
    classification: str = IntegrityState.UNRESOLVED.value
    purity_component: float | None = None
    strength_component: float | None = None
    support_component: float | None = None
    damage_component: float | None = None
    rescue_component: float | None = None
    useful_god_component: float | None = None
    climate_component: float | None = None
    residual_damage: str = "none"
    critical_findings: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    confidence: float = 0.0


@dataclass(slots=True)
class PatternGradeResult:
    """MC-01 Pattern Grade. Distinct from ScoreEngine customer grade."""

    state: str = AnalysisState.UNRESOLVED.value
    grade: str = PatternGrade.UNRESOLVED.value
    score: float | None = None
    confidence: float = 0.0
    basis: str = "structural_integrity"
    integrity_state: str = IntegrityState.UNRESOLVED.value
    evidence_ids: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(slots=True)
class ProfileDimension:
    """One achievement / wealth / career dimension."""

    dimension: str
    state: str = AnalysisState.RESOLVED.value
    score: float | None = None
    classification: str = "unresolved"
    polarity: str = "higher_is_better"
    confidence: float = 0.0
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()


@dataclass(slots=True)
class AchievementProfile:
    """Capability potentials. Not biography or social-status prediction."""

    state: str = AnalysisState.UNRESOLVED.value
    dimensions: tuple[ProfileDimension, ...] = ()
    dominant_capabilities: tuple[str, ...] = ()
    secondary_capabilities: tuple[str, ...] = ()
    structural_risks: tuple[str, ...] = ()
    conditions_for_expression: tuple[str, ...] = ()
    confidence: float = 0.0
    evidence_ids: tuple[str, ...] = ()


@dataclass(slots=True)
class WealthProfile:
    """Wealth structural capacity. Not 'Tài nhiều = giàu'."""

    state: str = AnalysisState.UNRESOLVED.value
    dimensions: tuple[ProfileDimension, ...] = ()
    confidence: float = 0.0
    evidence_ids: tuple[str, ...] = ()


@dataclass(slots=True)
class CareerProfile:
    """Career fit potentials. Not exact professions."""

    state: str = AnalysisState.UNRESOLVED.value
    dimensions: tuple[ProfileDimension, ...] = ()
    dominant_work_styles: tuple[str, ...] = ()
    confidence: float = 0.0
    evidence_ids: tuple[str, ...] = ()


@dataclass(slots=True)
class MingJuComposedDecision:
    """Structural composer output. Not Pack 07 narrative."""

    composer_version: str = SCHEMA_COMPOSER
    locale: str = "vi"
    headline_key: str = ""
    headline: str = ""
    summary_key: str = ""
    summary: str = ""
    strength_keys: tuple[str, ...] = ()
    strengths: tuple[str, ...] = ()
    risk_keys: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    condition_keys: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()


@dataclass(slots=True)
class MingJuContext:
    """Normalized upstream facts. Contains no MC-01 conclusions."""

    schema_version: str = SCHEMA_CONTEXT
    analysis_id: str = ""
    chart_id: str = ""
    pattern_code: str = ""
    pattern_label: str = ""
    pattern_success: bool = False
    secondary_labels: tuple[str, ...] = ()
    month_branch: str = ""
    month_main_qi: str = ""
    month_main_qi_ten_god: str = ""
    day_master: str = ""
    day_master_strength_level: str = ""
    day_master_strength_score: float | None = None
    useful_god: str = ""
    useful_ten_god: str = ""
    useful_element: str = ""
    climate_state: str = ""
    five_elements: dict[str, Any] = field(default_factory=_empty_dict)
    activations: tuple[GodActivation, ...] = ()
    hour_present: bool = True
    source_versions: dict[str, str] = field(default_factory=_empty_dict)


@dataclass(slots=True)
class MingJuDecisionResult:
    """Canonical MC-01 root result."""

    analysis_id: str = ""
    chart_id: str = ""
    schema_version: str = SCHEMA_DECISION
    ruleset_version: str = RULESET_VERSION
    context_schema_version: str = SCHEMA_CONTEXT
    result_id: str = ""
    content_hash: str = ""
    status: str = MingJuDecisionStatus.UNRESOLVED.value
    confidence: float = 0.0
    trace_ids: tuple[str, ...] = ()
    pattern: PatternDecision = field(default_factory=PatternDecision)
    purity: PatternPurityResult = field(default_factory=PatternPurityResult)
    pattern_strength: PatternStrengthResult = field(default_factory=PatternStrengthResult)
    support: SupportResult = field(default_factory=SupportResult)
    damage: DamageResult = field(default_factory=DamageResult)
    rescue: RescueResult = field(default_factory=RescueResult)
    useful_god_compatibility: CompatibilityResult = field(default_factory=CompatibilityResult)
    climate_compatibility: CompatibilityResult = field(default_factory=CompatibilityResult)
    integrity: StructuralIntegrityResult = field(default_factory=StructuralIntegrityResult)
    grade: PatternGradeResult = field(default_factory=PatternGradeResult)
    achievement: AchievementProfile = field(default_factory=AchievementProfile)
    wealth: WealthProfile = field(default_factory=WealthProfile)
    career: CareerProfile = field(default_factory=CareerProfile)
    decision: MingJuComposedDecision = field(default_factory=MingJuComposedDecision)
    warnings: tuple[WarningItem, ...] = ()
    evidence: tuple[EvidenceItem, ...] = ()
    traces: tuple[TraceItem, ...] = ()
    source_versions: dict[str, str] = field(default_factory=_empty_dict)
