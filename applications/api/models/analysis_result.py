"""Production AnalysisResult contract (Phase 2: Bazi slice authoritative)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.identity.models import CanonicalIdentity


@dataclass(slots=True)
class PillarView:
    """Single pillar — portal and downstream read the same fields."""

    stem: str
    branch: str
    hidden_stems: list[str] = field(default_factory=list)
    ten_god: str = ""
    nap_am: str = ""
    truong_sinh: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / Portal (unchanged JSON shape)."""
        return {
            "stem": self.stem,
            "branch": self.branch,
            "hidden_stems": list(self.hidden_stems),
            "ten_god": self.ten_god,
            "nap_am": self.nap_am,
            "truong_sinh": self.truong_sinh,
        }


@dataclass(slots=True)
class ShenShaMatchView:
    """One published ShenSha copied from the engine — no recalculation."""

    id: str
    canonical_name: str
    aliases: list[str] = field(default_factory=list)
    source_type: str = ""
    source_value: str = ""
    target_type: str = ""
    target_value: str = ""
    pillar: str = ""
    location: str = ""
    rule_source: str = ""
    presence_label: str = ""
    evidence_text: str = ""
    occurrences: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize one match for API / Portal / Report."""
        return {
            "id": self.id,
            "canonical_name": self.canonical_name,
            "aliases": list(self.aliases),
            "source_type": self.source_type,
            "source_value": self.source_value,
            "target_type": self.target_type,
            "target_value": self.target_value,
            "pillar": self.pillar,
            "location": self.location,
            "rule_source": self.rule_source,
            "presence_label": self.presence_label,
            "evidence_text": self.evidence_text,
            "occurrences": [dict(item) for item in self.occurrences],
        }

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "ShenShaMatchView":
        """Build a view from an engine match dict."""
        occurrences_raw = payload.get("occurrences") or []
        occurrences = [
            {
                "pillar": str(item.get("pillar") or ""),
                "location": str(item.get("location") or ""),
                "target_value": str(item.get("target_value") or ""),
            }
            for item in occurrences_raw
            if isinstance(item, dict)
        ]
        return cls(
            id=str(payload.get("id") or ""),
            canonical_name=str(payload.get("canonical_name") or payload.get("name") or ""),
            aliases=[str(item) for item in (payload.get("aliases") or []) if item],
            source_type=str(payload.get("source_type") or ""),
            source_value=str(payload.get("source_value") or ""),
            target_type=str(payload.get("target_type") or ""),
            target_value=str(payload.get("target_value") or ""),
            pillar=str(payload.get("pillar") or ""),
            location=str(payload.get("location") or ""),
            rule_source=str(payload.get("rule_source") or ""),
            presence_label=str(payload.get("presence_label") or ""),
            evidence_text=str(payload.get("evidence_text") or ""),
            occurrences=occurrences,
        )


@dataclass(slots=True)
class BaziView:
    """Authoritative Bazi slice for the production pipeline."""

    year_pillar: PillarView
    month_pillar: PillarView
    day_pillar: PillarView
    hour_pillar: PillarView
    day_master: str
    day_master_element: str
    day_master_yin_yang: str
    gender: str | None = None
    hidden_stems: list[str] = field(default_factory=list)
    ten_gods: list[str] = field(default_factory=list)
    shensha: list[str] = field(default_factory=list)
    shensha_matches: list[ShenShaMatchView] = field(default_factory=list)

    def published_shensha_names(self) -> list[str]:
        """Legacy name list projected from structured matches when present."""
        if self.shensha_matches:
            return [item.canonical_name for item in self.shensha_matches if item.canonical_name]
        return list(self.shensha)

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible `data.bazi` JSON."""
        names = self.published_shensha_names()
        return {
            "year_pillar": self.year_pillar.to_dict(),
            "month_pillar": self.month_pillar.to_dict(),
            "day_pillar": self.day_pillar.to_dict(),
            "hour_pillar": self.hour_pillar.to_dict(),
            "day_master": self.day_master,
            "day_master_element": self.day_master_element,
            "day_master_yin_yang": self.day_master_yin_yang,
            "gender": self.gender,
            "hidden_stems": list(self.hidden_stems),
            "ten_gods": list(self.ten_gods),
            "shensha": names,
            "shensha_matches": [item.to_dict() for item in self.shensha_matches],
        }

    def pillar_ten_gods(self) -> list[str]:
        """Per-pillar Thập thần in year → hour order."""
        return [
            self.year_pillar.ten_god,
            self.month_pillar.ten_god,
            self.day_pillar.ten_god,
            self.hour_pillar.ten_god,
        ]

    def can_chi(self, part: str) -> str:
        """Can Chi text for calendar enrichment."""
        pillar_map = {
            "year": self.year_pillar,
            "month": self.month_pillar,
            "day": self.day_pillar,
            "hour": self.hour_pillar,
        }
        pillar = pillar_map.get(part)
        if pillar is None:
            return ""
        return f"{pillar.stem} {pillar.branch}".strip()


@dataclass(slots=True)
class AnalysisMeta:
    """Pipeline metadata (expanded in later phases)."""

    contract_version: str = "1.0"
    pipeline: list[str] = field(default_factory=list)
    stage: str | None = None
    bazi_source: dict[str, str] = field(default_factory=dict)
    pattern_source: dict[str, str] = field(default_factory=dict)
    score_source: dict[str, str] = field(default_factory=dict)
    interpretation_source: dict[str, str] = field(default_factory=dict)
    report_source: dict[str, str] = field(default_factory=dict)
    rule_context_built_once: bool = False


@dataclass(slots=True)
class InterpretationSectionView:
    """One commercial interpretation section."""

    id: str
    title: str
    body: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one section for API / Portal."""
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
        }


@dataclass(slots=True)
class InterpretationView:
    """Authoritative interpretation slice for the production pipeline."""

    sections: list[InterpretationSectionView] = field(default_factory=list)
    section_count: int = 0
    sentence_count: int = 0
    confidence: float = 0.0
    summary: str = ""
    matched_rule_count: int = 0
    resolved_rule_count: int = 0
    coverage: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible ``data.interpretation`` JSON.

        Production responses omit internal engine fields
        (summary, matched_rule_count, resolved_rule_count, coverage,
        metadata, priority_resolution, discarded_rules, unused_rules).
        """
        return {
            "sections": [section.to_dict() for section in self.sections],
            "section_count": int(self.section_count),
            "sentence_count": int(self.sentence_count),
            "confidence": float(self.confidence),
        }


@dataclass(slots=True)
class ScoreView:
    """Authoritative score slice for the production pipeline."""

    success: bool
    total_score: float
    strength_score: float
    pattern_score: float
    ten_god_score: float
    wuxing_score: float
    grade: str = ""
    confidence: str = ""
    recommendation: str = ""
    useful_god_score: float | None = None
    shensha_score: float | None = None
    luck_score: float | None = None
    interpretation_score: float | None = None
    wuxing_series: list[dict[str, Any]] = field(default_factory=list)
    ten_god_series: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible ``data.score`` JSON."""
        payload: dict[str, Any] = {
            "success": self.success,
            "total_score": float(self.total_score),
            "strength_score": float(self.strength_score),
            "pattern_score": float(self.pattern_score),
            "ten_god_score": float(self.ten_god_score),
            "wuxing_score": float(self.wuxing_score),
            "grade": self.grade or "",
            "confidence": self.confidence or "",
            "recommendation": self.recommendation or "",
        }
        # Include zeros — frontend Đánh Giá must show explicit 0, not missing keys.
        if self.useful_god_score is not None:
            payload["useful_god_score"] = float(self.useful_god_score)
        if self.shensha_score is not None:
            payload["shensha_score"] = float(self.shensha_score)
        if self.luck_score is not None:
            payload["luck_score"] = float(self.luck_score)
        if self.interpretation_score is not None:
            payload["interpretation_score"] = float(self.interpretation_score)
        if self.wuxing_series:
            payload["wuxing_series"] = list(self.wuxing_series)
        if self.ten_god_series:
            payload["ten_god_series"] = list(self.ten_god_series)
        return payload


@dataclass(slots=True)
class PatternView:
    """Authoritative pattern slice for the production pipeline."""

    success: bool
    pattern: str
    cach_cuc: str
    score: float
    priority: int
    than: str = ""
    than_vuong_nhuoc: str = ""
    tong_cach: str = ""
    dung_than: str = ""
    hy_than: str = ""
    ky_than: str = ""
    dieu_hau: str = ""
    success_reason: str = ""
    winning_rule_id: str = ""
    evidence_compact: str = ""
    month_branch: str = ""
    month_main_qi: str = ""
    month_main_qi_ten_god: str = ""
    month_hidden_stems: list[str] = field(default_factory=list)
    day_master: str = ""
    penetration_exact: bool | None = None
    penetration_related: list[dict[str, Any]] = field(default_factory=list)
    candidate_patterns: list[str] = field(default_factory=list)
    fallback_used: bool = False
    ug_override_eligible: bool = False
    qualification_level: int | None = None
    detected_special_pattern: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible ``data.pattern`` JSON."""
        payload: dict[str, Any] = {
            "success": self.success,
            "pattern": self.pattern,
            "cach_cuc": self.cach_cuc,
            "score": float(self.score),
            "priority": int(self.priority),
            "than": self.than or "",
            "than_vuong_nhuoc": self.than_vuong_nhuoc or "",
            "tong_cach": self.tong_cach or "",
            "dung_than": self.dung_than or "",
            "hy_than": self.hy_than or "",
            "ky_than": self.ky_than or "",
            "dieu_hau": self.dieu_hau or "",
            "fallback_used": bool(self.fallback_used),
            "ug_override_eligible": bool(self.ug_override_eligible),
        }
        if self.qualification_level is not None:
            payload["qualification_level"] = int(self.qualification_level)
        if self.detected_special_pattern:
            payload["detected_special_pattern"] = self.detected_special_pattern
        if self.success_reason:
            payload["success_reason"] = self.success_reason
        if self.winning_rule_id:
            payload["winning_rule_id"] = self.winning_rule_id
        if self.evidence_compact:
            payload["evidence_compact"] = self.evidence_compact
        if self.month_branch:
            payload["month_branch"] = self.month_branch
        if self.month_main_qi:
            payload["month_main_qi"] = self.month_main_qi
        if self.month_main_qi_ten_god:
            payload["month_main_qi_ten_god"] = self.month_main_qi_ten_god
        if self.month_hidden_stems:
            payload["month_hidden_stems"] = list(self.month_hidden_stems)
        if self.day_master:
            payload["day_master"] = self.day_master
        if self.penetration_exact is not None:
            payload["penetration_exact"] = bool(self.penetration_exact)
        if self.penetration_related:
            payload["penetration_related"] = list(self.penetration_related)
        if self.candidate_patterns:
            payload["candidate_patterns"] = list(self.candidate_patterns)
        return payload


@dataclass(slots=True)
class UsefulGodView:
    """Authoritative useful-god slice for production pipeline."""

    useful_god: str = ""
    favorable_gods: list[str] = field(default_factory=list)
    unfavorable_gods: list[str] = field(default_factory=list)
    reasoning: str = ""
    confidence: float = 0.0
    matched_rules: list[str] = field(default_factory=list)
    useful_ten_god: str = ""
    useful_stem: str = ""
    useful_element: str = ""
    useful_display: str = ""
    favorable_roles: list[dict[str, str]] = field(default_factory=list)
    unfavorable_roles: list[dict[str, str]] = field(default_factory=list)
    favorable_display: str = ""
    unfavorable_display: str = ""
    canonical_favorable_display: str = ""
    winning_rule_id: str = ""
    winning_rule_group: str = ""
    candidate_list: list[dict[str, Any]] = field(default_factory=list)
    success: bool = True
    overall_incomplete: bool = False
    error: str = ""
    overall_useful_god: str = ""
    overall_candidate_list: list[dict[str, Any]] = field(default_factory=list)
    climate_candidate_list: list[dict[str, Any]] = field(default_factory=list)
    climate_candidate: str = ""
    climate_display: str = ""
    climate_stem: str = ""
    climate_element: str = ""
    climate_ten_god: str = ""
    climate_rule_id: str = ""
    climate_rule_group: str = ""
    climate_reason: str = ""
    climate_preference_label: str = ""
    short_reason: str = ""
    reason_archetype: str = ""
    customer_reason: dict[str, str] = field(default_factory=dict)
    hy_role_status: str = ""
    ky_scope_note: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible ``data.useful_god`` JSON."""
        return {
            "success": self.success,
            "overall_incomplete": self.overall_incomplete,
            "error": self.error or "",
            "useful_god": self.useful_god or "",
            "overall_useful_god": self.overall_useful_god or self.useful_god or "",
            "useful_ten_god": self.useful_ten_god or "",
            "useful_stem": self.useful_stem or "",
            "useful_element": self.useful_element or "",
            "useful_display": self.useful_display or "",
            "favorable_gods": list(self.favorable_gods),
            "unfavorable_gods": list(self.unfavorable_gods),
            "favorable_roles": [dict(item) for item in self.favorable_roles],
            "unfavorable_roles": [dict(item) for item in self.unfavorable_roles],
            "favorable_display": self.favorable_display or "",
            "canonical_favorable_display": self.canonical_favorable_display
            or self.favorable_display
            or "",
            "unfavorable_display": self.unfavorable_display or "",
            "winning_rule_id": self.winning_rule_id or "",
            "winning_rule_group": self.winning_rule_group or "",
            "candidate_list": [dict(item) for item in self.candidate_list],
            "overall_candidate_list": [dict(item) for item in self.overall_candidate_list],
            "climate_candidate_list": [dict(item) for item in self.climate_candidate_list],
            "reasoning": self.reasoning or "",
            "confidence": float(self.confidence),
            "matched_rules": list(self.matched_rules),
            "climate_candidate": self.climate_candidate or "",
            "climate_display": self.climate_display or "",
            "climate_stem": self.climate_stem or "",
            "climate_element": self.climate_element or "",
            "climate_ten_god": self.climate_ten_god or "",
            "climate_rule_id": self.climate_rule_id or "",
            "climate_rule_group": self.climate_rule_group or "",
            "climate_reason": self.climate_reason or "",
            "climate_preference_label": self.climate_preference_label or "",
            "short_reason": self.short_reason or "",
            "reason_archetype": self.reason_archetype or "",
            "customer_reason": dict(self.customer_reason or {}),
            "hy_role_status": self.hy_role_status or "",
            "ky_scope_note": self.ky_scope_note or "",
        }


@dataclass(slots=True)
class StrengthView:
    """Authoritative strength slice for production pipeline."""

    strength_level: str = "balanced"
    strength_score: float = 0.0
    season_score: float = 0.0
    root_score: float = 0.0
    support_score: float = 0.0
    drain_score: float = 0.0
    control_score: float = 0.0
    combination_score: float = 0.0
    special_score: float = 0.0
    raw_total: float = 0.0
    reasoning: str = ""
    evidence_compact: str = ""
    confidence: float = 0.0
    matched_rules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible ``data.strength`` JSON."""
        return {
            "strength_level": self.strength_level or "balanced",
            "strength_score": float(self.strength_score),
            "season_score": float(self.season_score),
            "root_score": float(self.root_score),
            "support_score": float(self.support_score),
            "drain_score": float(self.drain_score),
            "control_score": float(self.control_score),
            "combination_score": float(self.combination_score),
            "special_score": float(self.special_score),
            "raw_total": float(self.raw_total),
            "reasoning": self.reasoning or "",
            "evidence_compact": self.evidence_compact or "",
            "confidence": float(self.confidence),
            "matched_rules": list(self.matched_rules),
        }


@dataclass(slots=True)
class TemperatureView:
    """Authoritative temperature / Điều hậu slice. Score is intensity, not heat axis."""

    temperature_level: str = "warm"
    temperature_score: float = 0.0
    warm_score: float = 0.0
    cold_score: float = 0.0
    dry_score: float = 0.0
    humid_score: float = 0.0
    reasoning: str = ""
    confidence: float = 0.0
    matched_rules: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    climate_state: str = ""
    balancing_need: str = ""
    climate_state_label: str = ""
    balancing_need_label: str = ""
    evidence_compact: str = ""
    month_branch: str = ""
    season: str = ""
    score_semantic: str = "imbalance_intensity"

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible ``data.temperature`` JSON."""
        climate_state = self.climate_state or self.temperature_level or "warm"
        return {
            "temperature_level": climate_state,
            "climate_state": climate_state,
            "balancing_need": self.balancing_need or "",
            "climate_state_label": self.climate_state_label or "",
            "balancing_need_label": self.balancing_need_label or "",
            "evidence_compact": self.evidence_compact or "",
            "month_branch": self.month_branch or "",
            "season": self.season or "",
            "score_semantic": self.score_semantic or "imbalance_intensity",
            "temperature_score": float(self.temperature_score),
            "warm_score": float(self.warm_score),
            "cold_score": float(self.cold_score),
            "dry_score": float(self.dry_score),
            "humid_score": float(self.humid_score),
            "reasoning": self.reasoning or "",
            "confidence": float(self.confidence),
            "matched_rules": list(self.matched_rules),
            "recommendations": list(self.recommendations),
        }


@dataclass(slots=True)
class ReportView:
    """Authoritative report slice for the production pipeline."""

    title: str
    markdown: str
    html: str
    section_count: int

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible ``data.report`` JSON."""
        return {
            "title": self.title,
            "markdown": self.markdown,
            "html": self.html,
            "section_count": int(self.section_count),
        }


@dataclass(slots=True)
class NarrativeView:
    """Authoritative narrative slice for the production pipeline."""

    title: str
    markdown: str
    html: str
    section_count: int
    tone: str | None = None
    metrics: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible ``data.narrative`` JSON."""
        payload: dict[str, Any] = {
            "title": self.title,
            "markdown": self.markdown,
            "html": self.html,
            "section_count": int(self.section_count),
        }
        if self.tone:
            payload["tone"] = self.tone
        if self.metrics:
            payload["metrics"] = dict(self.metrics)
        return payload


@dataclass(slots=True)
class AnalysisResult:
    """
    Single production result object.

    Phase 2: ``bazi`` is authoritative.
    Phase 3: ``pattern`` is authoritative.
    Phase 4: ``score`` is authoritative.
    Phase 5: ``interpretation`` is authoritative.
    Phase 6: ``report`` and ``narrative`` are authoritative.
    """

    bazi: BaziView
    identity: CanonicalIdentity | None = None
    pattern: PatternView | None = None
    strength: StrengthView | None = None
    temperature: TemperatureView | None = None
    useful_god: UsefulGodView | None = None
    score: ScoreView | None = None
    interpretation: InterpretationView | None = None
    report: ReportView | None = None
    narrative: NarrativeView | None = None
    narrative_result: dict[str, Any] | None = None
    ten_gods_result: dict[str, Any] | None = None
    meta: AnalysisMeta = field(default_factory=AnalysisMeta)
    rule_context: dict[str, Any] = field(default_factory=dict)
    unified_context: dict[str, Any] = field(default_factory=dict)

    def bazi_dict(self) -> dict[str, Any]:
        """Serialize authoritative Bazi for ``data.bazi``."""
        return self.bazi.to_dict()

    def identity_dict(self) -> dict[str, Any]:
        """Serialize canonical ``data.identity`` (person / calendar / four pillars / …)."""
        if self.identity is None:
            return {}
        return self.identity.to_dict()

    def pattern_dict(self) -> dict[str, Any]:
        """Serialize authoritative Pattern for ``data.pattern``."""
        if self.pattern is None:
            return {}
        return self.pattern.to_dict()

    def score_dict(self) -> dict[str, Any]:
        """Serialize authoritative Score for ``data.score``."""
        if self.score is None:
            return {}
        return self.score.to_dict()

    def useful_god_dict(self) -> dict[str, Any]:
        """Serialize authoritative Useful God for ``data.useful_god``."""
        if self.useful_god is None:
            return {}
        return self.useful_god.to_dict()

    def strength_dict(self) -> dict[str, Any]:
        """Serialize authoritative Strength for ``data.strength``."""
        if self.strength is None:
            return {}
        return self.strength.to_dict()

    def temperature_dict(self) -> dict[str, Any]:
        """Serialize authoritative Temperature for ``data.temperature``."""
        if self.temperature is None:
            return {}
        return self.temperature.to_dict()

    def ten_gods_dict(self) -> dict[str, Any]:
        """Serialize canonical Ten Gods for ``data.ten_gods``."""
        return dict(self.ten_gods_result or {})

    def unified_context_dict(self) -> dict[str, Any]:
        """Serialize unified context for the public analyze payload."""
        return dict(self.unified_context or {})

    def interpretation_dict(self) -> dict[str, Any]:
        """Serialize authoritative Interpretation for ``data.interpretation``."""
        if self.interpretation is None:
            return {}
        return self.interpretation.to_dict()

    def report_dict(self) -> dict[str, Any]:
        """Serialize authoritative Report for ``data.report``."""
        if self.report is None:
            return {}
        return self.report.to_dict()

    def narrative_dict(self) -> dict[str, Any]:
        """Serialize authoritative Narrative for ``data.narrative``."""
        if self.narrative is None:
            return {}
        return self.narrative.to_dict()
