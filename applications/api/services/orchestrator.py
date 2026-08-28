"""Engine orchestration service (Applications Layer only).

Canonical runtime pipeline SSOT for BTE Platform V1.

Internal stages (always executed when needed):
Input → Calendar → BaZi → Feng Shui → Pattern → RuleContext → Score
→ Luck → Knowledge → Matching → Priority → Interpretation → Report → Delivery

Public API ``data.pipeline`` contract (only):
calendar → bazi → pattern → score → interpretation → report → narrative
"""

from __future__ import annotations

from datetime import datetime
import logging
from types import SimpleNamespace
from typing import Any, Literal

from engines.bazi_engine.engine import BaziEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.calendar_engine.engine import CalendarEngine
from engines.feng_shui_engine import FengShuiEngine, FengShuiEngineError
from engines.identity import build_canonical_identity
from engines.interpretation_engine.engine import InterpretationEngine
from engines.interpretation_engine.foundation import (
    EngineSources,
    build_interpretation_foundation,
)
from engines.luck_engine import LuckEngine
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.rule_context_bridge import (
    enrich_result_from_rule_context,
    enrich_rule_context_summaries,
    merge_upstream_into_rule_context,
)
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context
from engines.temperature_engine.engine import TemperatureEngine
from engines.temperature_engine.utils.context_builder import build_temperature_context
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.utils.context_builder import build_useful_god_context
from engines.report_engine.engine import ReportEngine
from engines.score_engine.engine import ScoreEngine
from engines.ten_gods_engine.engine import TenGodsEngine

from applications.api.exceptions import PipelineAPIError, ValidationAPIError
from applications.api.services.gender_truth import (
    gender_display_label,
    require_canonical_gender,
)
from applications.api.models.analysis_result import AnalysisMeta, AnalysisResult
from applications.api.services.bazi_truth import (
    bazi_source_fingerprint,
    build_bazi_view,
    sync_chart_from_view,
)
from applications.api.services.interpretation_truth import (
    build_interpretation_view,
    interpretation_source_fingerprint,
)
from applications.api.services.pattern_truth import (
    build_pattern_view,
    pattern_source_fingerprint,
)
from applications.api.services.strength_truth import (
    build_strength_view,
    strength_source_fingerprint,
)
from applications.api.services.temperature_truth import (
    build_temperature_view,
    temperature_source_fingerprint,
)
from applications.api.services.useful_god_truth import (
    build_useful_god_view,
    useful_god_source_fingerprint,
)
from applications.api.services.report_truth import (
    build_narrative_view,
    build_report_view,
    report_source_fingerprint,
)
from applications.api.services.integrated_narrative_publish import (
    publish_integrated_narrative,
)
from applications.api.services.narrative_result_truth import (
    build_narrative_result_dict,
    narrative_result_source_fingerprint,
)
from applications.api.services.score_truth import (
    build_score_view,
    score_source_fingerprint,
)
from applications.api.services.five_elements_truth import build_five_elements_payload
from applications.api.services.luck_truth import shape_luck_payload
from applications.api.services.ten_gods_truth import (
    shape_ten_gods_payload,
    ten_gods_source_fingerprint,
)
from applications.api.utils.pillars import pillar_text
from applications.api.utils.serializers import to_jsonable

logger = logging.getLogger(__name__)

# Public API stage names (including BC aliases).
Stage = Literal[
    "input",
    "calendar",
    "bazi",
    "feng_shui",
    "pattern",
    "rule_context",
    "score",
    "luck",
    "knowledge",
    "matching",
    "priority",
    "interpretation",
    "report",
    "delivery",
    "narrative",  # BC alias → delivery
    "analyze",
]

# Canonical internal stage order (narrative is not a contract stage).
PIPELINE_ORDER: tuple[str, ...] = (
    "input",
    "calendar",
    "bazi",
    "feng_shui",
    "pattern",
    "rule_context",
    "score",
    "luck",
    "knowledge",
    "matching",
    "priority",
    "interpretation",
    "report",
    "delivery",
)

# Public orchestration contract exposed on API ``data.pipeline``.
PUBLIC_PIPELINE_ORDER: tuple[str, ...] = (
    "calendar",
    "bazi",
    "pattern",
    "score",
    "interpretation",
    "report",
    "narrative",
)

# Internal completed-stage name → public pipeline label (omit if None).
_PUBLIC_STAGE_ALIAS: dict[str, str] = {
    "calendar": "calendar",
    "bazi": "bazi",
    "pattern": "pattern",
    "score": "score",
    "interpretation": "interpretation",
    "report": "report",
    "delivery": "narrative",
}

# Keys that may exist internally but must not appear on public API payloads.
_INTERNAL_PAYLOAD_KEYS: frozenset[str] = frozenset(
    {
        "input",
        "feng_shui",
        "rule_context",
        "unified_context",
        "knowledge",
        "matching",
        "priority",
        "delivery",
        "_luck_raw",
    }
)

# Map legacy API stage names onto PIPELINE_ORDER stop points.
_STAGE_ALIASES: dict[str, str] = {
    "narrative": "delivery",
    "analyze": "delivery",
}


class OrchestratorService:
    """
    Coordinates engine Public APIs only — no business logic.

    Canonical SSOT pipeline (Score → Luck → Interpretation).
    """

    def __init__(self) -> None:
        self.calendar_engine = CalendarEngine()
        self.bazi_engine = BaziEngine()
        self.feng_shui_engine = FengShuiEngine()
        self.pattern_engine = PatternEngine()
        self.strength_engine = StrengthEngine()
        self.temperature_engine = TemperatureEngine()
        self.useful_god_engine = UsefulGodEngine()
        self.score_engine = ScoreEngine()
        self.luck_engine = LuckEngine()
        self.interpretation_engine = InterpretationEngine()
        self.report_engine = ReportEngine()
        self.ten_gods_engine = TenGodsEngine()

    def _shape_calendar(
        self,
        calendar: Any,
        bazi_data: dict[str, Any] | None = None,
        feng_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a portal-friendly Calendar view from canonical CalendarResult."""
        data = to_jsonable(calendar)
        if not isinstance(data, dict):
            return {}
        lunar = data.get("lunar") if isinstance(data.get("lunar"), dict) else {}
        lunar_can_chi = data.get("lunar_can_chi") if isinstance(data.get("lunar_can_chi"), dict) else {}
        if lunar.get("year_can_chi") and not data.get("lunar_year_can_chi"):
            data["lunar_year_can_chi"] = lunar.get("year_can_chi")
        if lunar_can_chi.get("year"):
            data["year_can_chi"] = lunar_can_chi["year"]
        elif lunar.get("year_can_chi"):
            data["year_can_chi"] = lunar["year_can_chi"]
        if bazi_data:
            bazi_can_chi: dict[str, str] = {}
            for part in ("year", "month", "day", "hour"):
                pillar = bazi_data.get(f"{part}_pillar") or {}
                text = f"{pillar.get('stem', '')} {pillar.get('branch', '')}".strip()
                if text:
                    bazi_can_chi[part] = text
            if bazi_can_chi:
                data["bazi_can_chi"] = bazi_can_chi
        if feng_data:
            for key in ("cung_phi", "menh_quai", "nhom_trach", "gua_name"):
                if feng_data.get(key):
                    data[key] = feng_data[key]
        return data

    def run_stage(
        self,
        stage: Stage,
        *,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        gender: str | None = None,
        timezone: str = "Asia/Ho_Chi_Minh",
    ) -> dict[str, Any]:
        """Run the pipeline through ``stage`` (inclusive) and return JSON data."""
        try:
            return self._run(
                stage=stage,
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                gender=gender,
                timezone=timezone,
            )
        except PipelineAPIError:
            raise
        except ValidationAPIError:
            raise
        except Exception as exc:
            raise PipelineAPIError(
                f"Pipeline failed at stage '{stage}': {exc}",
                details={"stage": stage},
            ) from exc

    def analyze(
        self,
        *,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        gender: str | None = None,
        timezone: str = "Asia/Ho_Chi_Minh",
    ) -> dict[str, Any]:
        """Full end-to-end analyze pipeline through Delivery (Stage 12)."""
        return self.run_stage(
            "analyze",
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            gender=gender,
            timezone=timezone,
        )

    def _resolve_stop(self, stage: Stage) -> str:
        """Map request stage / alias to a PIPELINE_ORDER stop name."""
        if stage in _STAGE_ALIASES:
            return _STAGE_ALIASES[stage]
        if stage in PIPELINE_ORDER:
            return stage
        raise PipelineAPIError(f"Unknown stage: {stage}")

    @staticmethod
    def _public_pipeline(completed: list[str]) -> list[str]:
        """Project internal completed stages onto the public pipeline contract."""
        public: list[str] = []
        for stage in completed:
            name = _PUBLIC_STAGE_ALIAS.get(stage)
            if name and name not in public:
                public.append(name)
        # Preserve canonical public order for stability.
        order = {name: index for index, name in enumerate(PUBLIC_PIPELINE_ORDER)}
        public.sort(key=lambda name: order.get(name, len(order)))
        return public

    def _finalize_public_payload(
        self,
        payload: dict[str, Any],
        completed: list[str],
        *,
        analysis: AnalysisResult | None = None,
    ) -> dict[str, Any]:
        """
        Publish only the public orchestration contract.

        Internal stages continue to run; their names and payloads are stripped
        from the API response.
        """
        integrated = publish_integrated_narrative(payload)
        payload["integrated_narrative"] = integrated
        if analysis is not None:
            analysis.integrated_narrative = integrated
            analysis.identity = build_canonical_identity(
                bazi=analysis.bazi,
                calendar=payload.get("calendar"),
                input_fields=payload.get("input"),
                bone_weight=payload.get("bone_weight") or payload.get("can_xuong"),
                luck=payload.get("luck"),
                luck_engine_raw=payload.get("_luck_raw"),
                interpretation=payload.get("interpretation"),
                narrative=payload.get("narrative_result"),
            )
            payload["identity"] = analysis.identity_dict()
        elif payload.get("calendar"):
            payload["identity"] = build_canonical_identity(
                calendar=payload.get("calendar"),
                input_fields=payload.get("input"),
            ).to_dict()
        for key in _INTERNAL_PAYLOAD_KEYS:
            payload.pop(key, None)
        payload["pipeline"] = self._public_pipeline(completed)
        return payload

    def _pillars_from_bazi(self, bazi_view: Any) -> dict[str, dict[str, str]]:
        """Copy four-pillar stems and branches for TenGodsEngine."""
        return {
            "year": {
                "stem": bazi_view.year_pillar.stem,
                "branch": bazi_view.year_pillar.branch,
            },
            "month": {
                "stem": bazi_view.month_pillar.stem,
                "branch": bazi_view.month_pillar.branch,
            },
            "day": {
                "stem": bazi_view.day_pillar.stem,
                "branch": bazi_view.day_pillar.branch,
            },
            "hour": {
                "stem": bazi_view.hour_pillar.stem,
                "branch": bazi_view.hour_pillar.branch,
            },
        }

    def _calculate_ten_gods(
        self,
        bazi_view: Any,
        *,
        case_id: str | None = None,
    ) -> Any:
        """Run canonical TenGodsEngine once. Does not recalculate Day Master."""
        return self.ten_gods_engine.calculate(
            day_master=bazi_view.day_master,
            pillars=self._pillars_from_bazi(bazi_view),
            case_id=case_id or None,
        )

    def _narrative_pipeline_source(
        self,
        *,
        analysis: AnalysisResult,
        calendar: Any,
        feng_view: dict[str, Any] | None,
        pattern_context: Any,
        pattern_result: Any,
        useful_god_result: Any,
        strength_result: Any,
        temperature_result: Any,
        published_rule_context: dict[str, Any],
        luck_context: Any,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        gender: str,
        timezone: str,
        run_id: str,
        ten_gods: Any | None = None,
    ) -> SimpleNamespace:
        """Assemble already-run engine outputs for Narrative Composer V2.

        Does not recalculate Pattern, Strength, Useful God, or Ten Gods.
        """
        if ten_gods is None:
            ten_gods = self._calculate_ten_gods(analysis.bazi, case_id=run_id)
        calendar_payload = self._shape_calendar(
            calendar,
            analysis.bazi_dict(),
            feng_view,
        )
        luck_payload = shape_luck_payload(luck_context)
        five_elements_payload = build_five_elements_payload(
            published_rule_context.get("wuxing") or {}
        )
        foundation = build_interpretation_foundation(
            analysis=analysis,
            calendar=calendar_payload,
            luck=luck_payload,
            five_elements=five_elements_payload,
            feng_shui=feng_view or {},
            identity={
                "full_name": "",
                "gender": gender,
                "birth_datetime": (
                    f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}"
                ),
                "timezone": timezone,
            },
            engine_sources=EngineSources(
                useful_god_result=useful_god_result,
                strength_result=strength_result,
                temperature_result=temperature_result,
                ten_gods_result=ten_gods,
                pattern_context=pattern_context,
                pattern_result=pattern_result,
                rule_context=published_rule_context,
            ),
            pattern_dieu_hau=analysis.pattern.dieu_hau if analysis.pattern else "",
        )
        return SimpleNamespace(
            analysis=analysis,
            interpretation_foundation=foundation,
            strength_result=strength_result,
            pattern_context=pattern_context,
            pattern_result=pattern_result,
            ten_gods=ten_gods,
        )


    def _run(
        self,
        *,
        stage: Stage,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        gender: str | None,
        timezone: str = "Asia/Ho_Chi_Minh",
    ) -> dict[str, Any]:
        stop_at = self._resolve_stop(stage)
        stop_index = PIPELINE_ORDER.index(stop_at)
        completed: list[str] = []
        payload: dict[str, Any] = {"pipeline": []}
        analysis: AnalysisResult | None = None
        ten_gods_engine_result = None
        logger.info(
            "pipeline.start stage=%s birth=%04d-%02d-%02d %02d:%02d gender=%s",
            stage,
            year,
            month,
            day,
            hour,
            minute,
            gender,
        )

        # ----- Stage 0: Input Validation -----
        try:
            datetime(year, month, day, hour, minute)
        except ValueError as exc:
            raise PipelineAPIError(
                f"Invalid birth datetime: {exc}",
                details={"stage": "input"},
            ) from exc
        if stop_index >= PIPELINE_ORDER.index("luck"):
            gender = require_canonical_gender(gender)
        completed.append("input")
        payload["input"] = {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "gender": gender,
            "gender_label": gender_display_label(gender) if gender else "",
            "validated": True,
        }
        if stop_index == 0:
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 1: Calendar -----
        calendar = self.calendar_engine.build(
            year,
            month,
            day,
            hour,
            minute,
            timezone_name=timezone,
        )
        completed.append("calendar")
        payload["calendar"] = self._shape_calendar(calendar)
        if stop_index == 1:
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 2: BaZi -----
        bazi_chart = self.bazi_engine.build(calendar, gender=gender)
        bazi_view = build_bazi_view(bazi_chart)
        sync_chart_from_view(bazi_chart, bazi_view)
        analysis = AnalysisResult(
            bazi=bazi_view,
            meta=AnalysisMeta(
                contract_version="1.0",
                bazi_source=bazi_source_fingerprint(),
            ),
        )
        completed.append("bazi")
        bazi_payload = analysis.bazi_dict()
        payload["bazi"] = bazi_payload
        payload["bazi_source"] = analysis.meta.bazi_source
        if stop_index == 2:
            payload["calendar"] = self._shape_calendar(calendar, bazi_payload, None)
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 3: Feng Shui (optional soft-fail) -----
        lunar = getattr(calendar, "lunar", None)
        feng_year = getattr(lunar, "year", None) or year
        feng_view: dict[str, Any] | None
        try:
            feng = self.feng_shui_engine.calculate(year=int(feng_year), gender=gender)
            feng_view = feng.to_dict()
            payload["feng_shui"] = feng_view
        except FengShuiEngineError:
            feng_view = None
            payload["feng_shui"] = None
        payload["calendar"] = self._shape_calendar(calendar, bazi_payload, feng_view)
        completed.append("feng_shui")
        if stop_index == 3:
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 3.5: Strength (before Pattern; feeds PatternContext) -----
        pattern_context = build_pattern_context(bazi_chart, calendar=calendar)
        strength_context = build_strength_context(bazi_chart, calendar=calendar)
        strength_result = self.strength_engine.calculate(strength_context)
        pattern_context.strength_level = strength_result.strength_level
        pattern_context.strength_score = strength_result.strength_score
        analysis.strength = build_strength_view(strength_result)

        # ----- Stage 3.6: Temperature (before Pattern; feeds PatternContext) -----
        temperature_context = build_temperature_context(
            bazi_chart,
            calendar=calendar,
            strength_level=strength_result.strength_level,
            strength_score=strength_result.strength_score,
        )
        temperature_result = self.temperature_engine.calculate(temperature_context)
        # G1-06: Useful God reads canonical G1-04 climate_state via overlay.
        pattern_context.temperature_type = (
            temperature_result.useful_god_temperature_overlay()
        )
        analysis.temperature = build_temperature_view(temperature_result)

        # ----- Stage 4: Pattern (recognition only) -----
        pattern_result = self.pattern_engine.calculate(pattern_context)
        useful_god_context = build_useful_god_context(pattern_context, pattern_result)
        useful_god_result = self.useful_god_engine.calculate(useful_god_context)
        analysis.useful_god = build_useful_god_view(useful_god_result)
        analysis.meta.pattern_source = pattern_source_fingerprint()
        completed.append("pattern")
        if stop_index == 4:
            analysis.pattern = build_pattern_view(pattern_result)
            payload["pattern"] = analysis.pattern_dict()
            payload["strength"] = analysis.strength_dict()
            payload["strength_source"] = strength_source_fingerprint()
            payload["temperature"] = analysis.temperature_dict()
            payload["temperature_source"] = temperature_source_fingerprint()
            payload["useful_god"] = analysis.useful_god_dict()
            payload["useful_god_source"] = useful_god_source_fingerprint()
            payload["pattern_source"] = analysis.meta.pattern_source
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 5: Consume Pattern-published RuleContext (never rebuild) -----
        published_rule_context = dict(pattern_result.rule_context or {})
        if not published_rule_context:
            raise PipelineAPIError(
                "Pattern Engine did not publish RuleContext.",
            )
        # Overlay UsefulGod / live Strength / Temperature without rebuild.
        merge_upstream_into_rule_context(
            published_rule_context,
            useful_god=useful_god_result,
            strength=strength_result,
            temperature=temperature_result,
        )
        enrich_rule_context_summaries(
            published_rule_context,
            pattern=pattern_result,
        )
        enrich_result_from_rule_context(pattern_result, published_rule_context)
        analysis.unified_context = {}
        analysis.pattern = build_pattern_view(pattern_result)
        analysis.rule_context = dict(published_rule_context)
        analysis.meta.rule_context_built_once = True
        completed.append("rule_context")
        payload["pattern"] = analysis.pattern_dict()
        payload["strength"] = analysis.strength_dict()
        payload["strength_source"] = strength_source_fingerprint()
        payload["temperature"] = analysis.temperature_dict()
        payload["temperature_source"] = temperature_source_fingerprint()
        payload["useful_god"] = analysis.useful_god_dict()
        payload["useful_god_source"] = useful_god_source_fingerprint()
        payload["pattern_source"] = analysis.meta.pattern_source
        payload["rule_context"] = {
            "published": True,
            "sections": sorted(str(k) for k in published_rule_context.keys()),
        }
        payload["unified_context"] = analysis.unified_context_dict()
        if stop_index == 5:
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 6: Score (no mutation of published RuleContext) -----
        score_result = self.score_engine.calculate(published_rule_context)
        interpretation_ctx = self.score_engine.append_score_to_rule_context(
            published_rule_context,
            score_result,
        )
        # Refresh Cách Cục labels from canonical Strength (Score must not remap).
        enrich_rule_context_summaries(interpretation_ctx, pattern=pattern_result)
        enrich_result_from_rule_context(pattern_result, interpretation_ctx)
        analysis.pattern = build_pattern_view(pattern_result)
        payload["pattern"] = analysis.pattern_dict()
        score_view = build_score_view(score_result)
        analysis.score = score_view
        # Keep AnalysisResult.rule_context as Stage 5 publish (immutable snapshot).
        analysis.rule_context = dict(published_rule_context)
        analysis.meta.score_source = score_source_fingerprint()
        completed.append("score")
        payload["score"] = analysis.score_dict()
        payload["score_source"] = analysis.meta.score_source
        payload["five_elements"] = build_five_elements_payload(
            published_rule_context.get("wuxing") or {}
        )
        ten_gods_engine_result = self._calculate_ten_gods(
            analysis.bazi,
            case_id=str(payload.get("request_id") or ""),
        )
        ten_gods_payload = shape_ten_gods_payload(ten_gods_engine_result)
        analysis.ten_gods_result = ten_gods_payload
        payload["ten_gods"] = ten_gods_payload
        payload["ten_gods_source"] = ten_gods_source_fingerprint()
        logger.info(
            "pipeline.score total=%.2f grade=%s",
            payload["score"].get("total_score", 0.0),
            payload["score"].get("grade", ""),
        )
        if stop_index == 6:
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 7: Luck (separate LuckContext; never mutates RuleContext) -----
        luck_context = self.luck_engine.build(
            calendar=calendar,
            bazi=bazi_chart,
            pattern=pattern_result,
            rule_context=published_rule_context,
            score=score_result,
        )
        completed.append("luck")
        payload["_luck_raw"] = luck_context.to_dict()
        payload["luck"] = shape_luck_payload(luck_context)
        if stop_index == 7:
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 8: Knowledge -----
        all_rules = self.interpretation_engine.load_knowledge_rules()
        completed.append("knowledge")
        payload["knowledge"] = {"rule_count": len(all_rules)}
        if stop_index == 8:
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 9: Matching -----
        matched_rules = self.interpretation_engine.match_knowledge_rules(
            interpretation_ctx,
            all_rules,
        )
        scored_rules = self.interpretation_engine.score_matched_rules(
            matched_rules,
            interpretation_ctx,
        )
        completed.append("matching")
        payload["matching"] = {"matched_count": len(matched_rules)}
        if stop_index == 9:
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 10: Priority -----
        ordered_rules = self.interpretation_engine.resolve_priority(
            scored_rules,
            interpretation_ctx,
        )
        completed.append("priority")
        payload["priority"] = {
            "resolved_count": len(ordered_rules),
            **dict(self.interpretation_engine._last_priority_resolution),
        }
        if stop_index == 10:
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 11: Interpretation (LuckContext optional) -----
        interpretation_result = self.interpretation_engine.build_from_resolved(
            ordered_rules,
            interpretation_ctx,
            all_rules=all_rules,
            matched_count=len(scored_rules),
            luck_context=luck_context,
        )
        interpretation_view = build_interpretation_view(interpretation_result)
        analysis.interpretation = interpretation_view
        analysis.meta.interpretation_source = interpretation_source_fingerprint()
        completed.append("interpretation")
        payload["interpretation"] = analysis.interpretation_dict()
        payload["interpretation_source"] = analysis.meta.interpretation_source
        # Canonical NarrativeResult V2 — Pack 05 is legacy fallback only.
        analysis_bag = {
            "bazi": payload.get("bazi") or {},
            "pattern": payload.get("pattern") or {},
            "strength": payload.get("strength") or {},
            "useful_god": payload.get("useful_god") or {},
            "score": payload.get("score") or {},
        }
        narrative_engine_output = self._narrative_pipeline_source(
            analysis=analysis,
            calendar=calendar,
            feng_view=feng_view,
            pattern_context=pattern_context,
            pattern_result=pattern_result,
            useful_god_result=useful_god_result,
            strength_result=strength_result,
            temperature_result=temperature_result,
            published_rule_context=published_rule_context,
            luck_context=luck_context,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            gender=gender or "",
            timezone=timezone,
            run_id=str(payload.get("request_id") or ""),
            ten_gods=ten_gods_engine_result,
        )
        narrative_result_payload = build_narrative_result_dict(
            analysis=analysis_bag,
            interpretation=payload.get("interpretation") or {},
            run_id=str(payload.get("request_id") or ""),
            engine_output=narrative_engine_output,
        )
        analysis.narrative_result = narrative_result_payload
        payload["narrative_result"] = narrative_result_payload
        payload["narrative_result_source"] = narrative_result_source_fingerprint()
        logger.info(
            "pipeline.interpretation sections=%s narrative_result_status=%s",
            payload["interpretation"].get("section_count", 0),
            narrative_result_payload.get("status"),
        )
        if stop_index == 11:
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 12: Report (consumes already-built NarrativeResult) -----
        include_narrative = stop_index >= 13
        report_result = self.report_engine.render_from_analysis(
            analysis,
            include_narrative=include_narrative,
            narrative_result=narrative_result_payload,
        )
        report_view = build_report_view(report_result)
        analysis.report = report_view
        analysis.meta.report_source = report_source_fingerprint()
        completed.append("report")
        payload["report"] = analysis.report_dict()
        payload["report_source"] = analysis.meta.report_source
        if stop_index == 12:
            return self._finalize_public_payload(payload, completed, analysis=analysis)

        # ----- Stage 13: Delivery -----
        narrative_view = build_narrative_view(report_result)
        analysis.narrative = narrative_view
        completed.append("delivery")
        payload["narrative"] = analysis.narrative_dict()
        payload["delivery"] = {
            "format": "json",
            "includes_narrative": True,
        }
        if stage == "analyze":
            payload["stage"] = "analyze"
        logger.info(
            "pipeline.done stage=%s pattern_keys=%s interpretation_keys=%s",
            stage,
            sorted(payload.get("pattern", {}).keys()),
            sorted(payload.get("interpretation", {}).keys()),
        )
        return self._finalize_public_payload(payload, completed, analysis=analysis)


# Backward-compatible WP8 name.
class ReportPipelineService(OrchestratorService):
    """Alias for WP8 ``ReportPipelineService``."""

    def run(
        self,
        *,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        gender: str | None = None,
        timezone: str = "Asia/Ho_Chi_Minh",
    ) -> dict[str, Any]:
        """Run full pipeline through Delivery (Stage 12)."""
        return self.run_stage(
            "delivery",
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            gender=gender,
            timezone=timezone,
        )
