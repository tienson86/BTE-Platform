"""Analysis engine adapter boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from applications.api.contracts.analyze_request import AnalyzeRequest
from applications.api.contracts.report_response import (
    AnalysisPayload,
    BasicInformationInfo,
    ChartPayload,
    FourPillarsInfo,
    HiddenStemsInfo,
    PatternInfo,
    PillarInfo,
    RelationshipInfo,
    ScoreInfo,
    StrengthInfo,
    SummaryInfo,
    UsefulGodInfo,
)
from applications.api.services.orchestrator import OrchestratorService


@dataclass(slots=True)
class AnalysisAdaptation:
    """Adapted chart and analysis sections from engine output."""

    chart: ChartPayload
    analysis: AnalysisPayload
    engine_payload: dict[str, Any]


def extract_birth_kwargs(request: AnalyzeRequest) -> dict[str, Any]:
    """Extract OrchestratorService birth kwargs from AnalyzeRequest.chart."""
    data = request.chart.model_dump()
    missing = [name for name in ("year", "month", "day") if data.get(name) is None]
    if missing:
        raise ValueError(f"chart missing required fields: {', '.join(missing)}")
    return {
        "year": int(data["year"]),
        "month": int(data["month"]),
        "day": int(data["day"]),
        "hour": int(data.get("hour") or 0),
        "minute": int(data.get("minute") or 0),
        "gender": data.get("gender"),
        "timezone": str(data.get("timezone") or "Asia/Ho_Chi_Minh"),
    }


def _as_dict(value: object) -> dict[str, Any]:
    """Return a dict payload or an empty dict."""
    return value if isinstance(value, dict) else {}


def _as_str(value: object) -> str | None:
    """Return a stripped string or None."""
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _as_float(value: object) -> float | None:
    """Return a float when conversion succeeds."""
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _map_pillar(pillar: object) -> PillarInfo:
    """Map engine pillar dict to PillarInfo."""
    data = _as_dict(pillar)
    return PillarInfo(
        stem=_as_str(data.get("stem")),
        branch=_as_str(data.get("branch")),
    )


def map_chart_payload(
    engine_payload: dict[str, Any],
    request: AnalyzeRequest,
) -> ChartPayload:
    """Adapt engine BaZi payload into ChartPayload."""
    bazi = _as_dict(engine_payload.get("bazi"))
    chart_input = request.chart.model_dump()
    year_pillar = _as_dict(bazi.get("year_pillar"))
    month_pillar = _as_dict(bazi.get("month_pillar"))
    day_pillar = _as_dict(bazi.get("day_pillar"))
    hour_pillar = _as_dict(bazi.get("hour_pillar"))
    return ChartPayload(
        four_pillars=FourPillarsInfo(
            year=_map_pillar(year_pillar),
            month=_map_pillar(month_pillar),
            day=_map_pillar(day_pillar),
            hour=_map_pillar(hour_pillar),
        ),
        hidden_stems=HiddenStemsInfo(
            year=[str(item) for item in (year_pillar.get("hidden_stems") or [])],
            month=[str(item) for item in (month_pillar.get("hidden_stems") or [])],
            day=[str(item) for item in (day_pillar.get("hidden_stems") or [])],
            hour=[str(item) for item in (hour_pillar.get("hidden_stems") or [])],
        ),
        luck_cycles=[],
        basic_information=BasicInformationInfo(
            gender=_as_str(chart_input.get("gender") or bazi.get("gender")),
            calendar_type=_as_str(chart_input.get("calendar_type")),
            timezone=_as_str(chart_input.get("timezone") or "Asia/Ho_Chi_Minh"),
            notes=[],
        ),
    )


def map_analysis_payload(engine_payload: dict[str, Any]) -> AnalysisPayload:
    """Adapt engine analysis slices into AnalysisPayload."""
    score = _as_dict(engine_payload.get("score"))
    strength = _as_dict(engine_payload.get("strength"))
    useful_god = _as_dict(engine_payload.get("useful_god"))
    pattern = _as_dict(engine_payload.get("pattern"))
    favorable = [str(item) for item in (useful_god.get("favorable_gods") or [])]
    return AnalysisPayload(
        scores=ScoreInfo(
            code=_as_str(score.get("grade")),
            label="score",
            value=_as_float(score.get("total_score")),
            summary=_as_str(score.get("recommendation")),
        ),
        strength=StrengthInfo(
            code=_as_str(strength.get("strength_level")),
            label="strength",
            value=_as_float(strength.get("strength_score")),
            summary=_as_str(strength.get("reasoning")),
        ),
        useful_god=UsefulGodInfo(
            code=_as_str(useful_god.get("useful_god")),
            label="useful_god",
            elements=favorable,
            summary=_as_str(useful_god.get("reasoning")),
        ),
        pattern=PatternInfo(
            code=_as_str(pattern.get("pattern") or pattern.get("cach_cuc")),
            label=_as_str(pattern.get("cach_cuc") or pattern.get("pattern")),
            summary=_as_str(pattern.get("tong_cach")),
        ),
        relationships=RelationshipInfo(
            code=None,
            label="relationships",
            summary=None,
        ),
        summary=SummaryInfo(
            code=_as_str(score.get("grade")),
            label="analysis_summary",
            text=_as_str(score.get("recommendation") or pattern.get("cach_cuc")),
        ),
    )


class AnalysisAdapter:
    """Isolates Analysis Engine integration via OrchestratorService."""

    def __init__(self, orchestrator: OrchestratorService | None = None) -> None:
        self._orchestrator = orchestrator or OrchestratorService()

    def execute(self, request: AnalyzeRequest) -> AnalysisAdaptation:
        """Run analysis engines through Score and adapt to contract sections."""
        birth = extract_birth_kwargs(request)
        engine_payload = self._orchestrator.run_stage("score", **birth)
        return AnalysisAdaptation(
            chart=map_chart_payload(engine_payload, request),
            analysis=map_analysis_payload(engine_payload),
            engine_payload=engine_payload,
        )
