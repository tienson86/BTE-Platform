"""Production AnalysisResult contract (Phase 2: Bazi slice authoritative)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible `data.bazi` JSON."""
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
            "shensha": list(self.shensha),
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

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible ``data.pattern`` JSON."""
        return {
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
        }


@dataclass(slots=True)
class UsefulGodView:
    """Authoritative useful-god slice for production pipeline."""

    useful_god: str = ""
    favorable_gods: list[str] = field(default_factory=list)
    unfavorable_gods: list[str] = field(default_factory=list)
    reasoning: str = ""
    confidence: float = 0.0
    matched_rules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible ``data.useful_god`` JSON."""
        return {
            "useful_god": self.useful_god or "",
            "favorable_gods": list(self.favorable_gods),
            "unfavorable_gods": list(self.unfavorable_gods),
            "reasoning": self.reasoning or "",
            "confidence": float(self.confidence),
            "matched_rules": list(self.matched_rules),
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
    reasoning: str = ""
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
            "reasoning": self.reasoning or "",
            "confidence": float(self.confidence),
            "matched_rules": list(self.matched_rules),
        }


@dataclass(slots=True)
class TemperatureView:
    """Authoritative temperature slice for production pipeline."""

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

    def to_dict(self) -> dict[str, Any]:
        """Portal-compatible ``data.temperature`` JSON."""
        return {
            "temperature_level": self.temperature_level or "warm",
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
    pattern: PatternView | None = None
    strength: StrengthView | None = None
    temperature: TemperatureView | None = None
    useful_god: UsefulGodView | None = None
    score: ScoreView | None = None
    interpretation: InterpretationView | None = None
    report: ReportView | None = None
    narrative: NarrativeView | None = None
    meta: AnalysisMeta = field(default_factory=AnalysisMeta)
    rule_context: dict[str, Any] = field(default_factory=dict)
    unified_context: dict[str, Any] = field(default_factory=dict)

    def bazi_dict(self) -> dict[str, Any]:
        """Serialize authoritative Bazi for ``data.bazi``."""
        return self.bazi.to_dict()

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

    def unified_context_dict(self) -> dict[str, Any]:
        """Serialize UnifiedAnalysisContext V2 for ``data.unified_context``."""
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
