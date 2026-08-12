"""Run production analysis engines — shared by report fixtures and E2E orchestrator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from applications.api.models.analysis_result import AnalysisMeta, AnalysisResult
from applications.api.services.bazi_truth import build_bazi_view, sync_chart_from_view
from applications.api.services.interpretation_truth import build_interpretation_view
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.pattern_truth import build_pattern_view
from applications.api.services.score_truth import build_score_view
from applications.api.services.strength_truth import build_strength_view
from applications.api.services.temperature_truth import build_temperature_view
from applications.api.services.useful_god_truth import build_useful_god_view
from engines.interpretation_engine.legacy_builder import InterpretationResult
from engines.pattern_engine.rule_context_bridge import (
    enrich_result_from_rule_context,
    enrich_rule_context_summaries,
    merge_upstream_into_rule_context,
)
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.report_engine.adapters.report_input_v1_adapter import ReportInputV1Source
from engines.report_engine.contracts.report_input_v1 import ReportProfileV1
from engines.strength_engine.utils.context_builder import build_strength_context
from engines.temperature_engine.utils.context_builder import build_temperature_context
from engines.ten_gods_engine.engine import TenGodsEngine
from engines.ten_gods_engine.models import TenGodsResult
from engines.useful_god_engine.utils.context_builder import build_useful_god_context

from applications.production.models import ProductionRequest


@dataclass(slots=True)
class EnginePipelineOutput:
    """Output from production engine chain."""

    analysis: AnalysisResult
    interpretation: InterpretationResult
    calendar: dict[str, Any]
    luck: dict[str, Any]
    ten_gods: TenGodsResult
    report_source: ReportInputV1Source
    stages: list[str]


class ProductionEngineRunner:
    """Execute Calendar → BaZi → Strength → Pattern → Useful God → Ten Gods."""

    def __init__(self, orchestrator: OrchestratorService | None = None) -> None:
        self._orch = orchestrator or OrchestratorService()
        self._ten_gods = TenGodsEngine()

    def run(self, request: ProductionRequest) -> EnginePipelineOutput:
        """Run full production engine chain for one birth request."""
        stages: list[str] = []
        orch = self._orch

        calendar = orch.calendar_engine.build(
            request.year,
            request.month,
            request.day,
            request.hour,
            request.minute,
        )
        stages.append("calendar")

        bazi_chart = orch.bazi_engine.build(calendar, gender=request.gender)
        bazi_view = build_bazi_view(bazi_chart)
        sync_chart_from_view(bazi_chart, bazi_view)
        stages.append("bazi")

        analysis = AnalysisResult(
            bazi=bazi_view,
            meta=AnalysisMeta(contract_version="1.0"),
        )

        pattern_context = build_pattern_context(bazi_chart, calendar=calendar)
        strength_context = build_strength_context(bazi_chart, calendar=calendar)
        strength_result = orch.strength_engine.calculate(strength_context)
        pattern_context.strength_level = strength_result.strength_level
        pattern_context.strength_score = strength_result.strength_score
        analysis.strength = build_strength_view(strength_result)
        stages.append("strength")

        temperature_context = build_temperature_context(
            bazi_chart,
            calendar=calendar,
            strength_level=strength_result.strength_level,
            strength_score=strength_result.strength_score,
        )
        temperature_result = orch.temperature_engine.calculate(temperature_context)
        pattern_context.temperature_type = temperature_result.to_pattern_temperature_type()
        analysis.temperature = build_temperature_view(temperature_result)
        stages.append("temperature")

        pattern_result = orch.pattern_engine.calculate(pattern_context)
        analysis.pattern = build_pattern_view(pattern_result)
        stages.append("pattern")

        useful_god_context = build_useful_god_context(pattern_context, pattern_result)
        useful_god_result = orch.useful_god_engine.calculate(useful_god_context)
        analysis.useful_god = build_useful_god_view(useful_god_result)
        stages.append("useful_god")

        published_rule_context = dict(pattern_result.rule_context or {})
        merge_upstream_into_rule_context(
            published_rule_context,
            useful_god=useful_god_result,
            strength=strength_result,
            temperature=temperature_result,
        )
        enrich_rule_context_summaries(published_rule_context, pattern=pattern_result)
        enrich_result_from_rule_context(pattern_result, published_rule_context)
        analysis.pattern = build_pattern_view(pattern_result)

        score_result = orch.score_engine.calculate(published_rule_context)
        interpretation_ctx = orch.score_engine.append_score_to_rule_context(
            published_rule_context,
            score_result,
        )
        enrich_rule_context_summaries(interpretation_ctx, pattern=pattern_result)
        enrich_result_from_rule_context(pattern_result, interpretation_ctx)
        analysis.pattern = build_pattern_view(pattern_result)
        analysis.score = build_score_view(score_result)
        stages.append("score")

        pillars = {
            "year": {"stem": bazi_view.year.stem, "branch": bazi_view.year.branch},
            "month": {"stem": bazi_view.month.stem, "branch": bazi_view.month.branch},
            "day": {"stem": bazi_view.day.stem, "branch": bazi_view.day.branch},
            "hour": {"stem": bazi_view.hour.stem, "branch": bazi_view.hour.branch},
        }
        ten_gods = self._ten_gods.calculate(
            day_master=bazi_view.day_master,
            pillars=pillars,
            case_id=request.case_id,
        )
        stages.append("ten_gods")

        luck_context = orch.luck_engine.build(
            calendar=calendar,
            bazi=bazi_chart,
            pattern=pattern_result,
            rule_context=published_rule_context,
            score=score_result,
        )
        stages.append("luck")

        all_rules = orch.interpretation_engine.load_knowledge_rules()
        matched_rules = orch.interpretation_engine.match_knowledge_rules(
            interpretation_ctx,
            all_rules,
        )
        scored_rules = orch.interpretation_engine.score_matched_rules(
            matched_rules,
            interpretation_ctx,
        )
        ordered_rules = orch.interpretation_engine.resolve_priority(
            scored_rules,
            interpretation_ctx,
        )
        interpretation_result = orch.interpretation_engine.build_from_resolved(
            ordered_rules,
            interpretation_ctx,
            all_rules=all_rules,
            matched_count=len(scored_rules),
            luck_context=luck_context,
        )
        analysis.interpretation = build_interpretation_view(interpretation_result)
        stages.append("interpretation_v1")

        calendar_payload = orch._shape_calendar(calendar, analysis.bazi_dict())
        profile = ReportProfileV1(
            full_name=request.full_name,
            gender=request.gender,
            birth_date=f"{request.year:04d}-{request.month:02d}-{request.day:02d}",
            birth_time=f"{request.hour:02d}:{request.minute:02d}",
            birth_place=request.birth_place,
            timezone=request.timezone,
        )
        report_source = ReportInputV1Source(
            analysis=analysis,
            interpretation=interpretation_result,
            calendar=calendar_payload,
            luck=luck_context.to_dict(),
            profile=profile,
            case_id=request.case_id,
            timezone=request.timezone,
            knowledge_version="v1.0",
        )

        return EnginePipelineOutput(
            analysis=analysis,
            interpretation=interpretation_result,
            calendar=calendar_payload,
            luck=luck_context.to_dict(),
            ten_gods=ten_gods,
            report_source=report_source,
            stages=stages,
        )
