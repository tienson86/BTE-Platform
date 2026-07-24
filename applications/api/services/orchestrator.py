"""Engine orchestration service (Applications Layer only)."""

from __future__ import annotations

from typing import Any, Literal

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.interpretation_engine.engine import InterpretationEngine
from engines.narrative_engine.engine import NarrativeEngine
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine
from engines.report_engine.engine import ReportEngine
from engines.score_engine.engine import ScoreEngine

from applications.api.exceptions import PipelineAPIError
from applications.api.utils.pillars import pillar_text
from applications.api.utils.serializers import to_jsonable

Stage = Literal[
    "calendar",
    "bazi",
    "pattern",
    "score",
    "interpretation",
    "report",
    "narrative",
    "analyze",
]

PIPELINE_ORDER: tuple[Stage, ...] = (
    "calendar",
    "bazi",
    "pattern",
    "score",
    "interpretation",
    "report",
    "narrative",
)


class OrchestratorService:
    """
    Coordinates engine Public APIs only — no business logic.

    Pipeline:
    Calendar → Bazi → Pattern → Score → Interpretation → Report → Narrative
    """

    def __init__(self) -> None:
        self.calendar_engine = CalendarEngine()
        self.bazi_engine = BaziEngine()
        self.pattern_engine = PatternEngine()
        self.score_engine = ScoreEngine()
        self.interpretation_engine = InterpretationEngine()
        self.report_engine = ReportEngine()
        self.narrative_engine = NarrativeEngine()

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
        del timezone  # reserved for future calendar localization
        try:
            return self._run(
                stage=stage,
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                gender=gender,
            )
        except PipelineAPIError:
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
        """Full end-to-end analyze pipeline."""
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
    ) -> dict[str, Any]:
        stop_at = "narrative" if stage == "analyze" else stage
        if stop_at not in PIPELINE_ORDER:
            raise PipelineAPIError(f"Unknown stage: {stage}")

        stop_index = PIPELINE_ORDER.index(stop_at)
        completed: list[str] = []
        payload: dict[str, Any] = {"pipeline": []}

        calendar = self.calendar_engine.build(year, month, day, hour, minute)
        completed.append("calendar")
        payload["calendar"] = to_jsonable(calendar)
        if stop_index == 0:
            payload["pipeline"] = completed
            return payload

        bazi = self.bazi_engine.build(calendar, gender=gender)
        completed.append("bazi")
        payload["bazi"] = to_jsonable(bazi)
        if stop_index == 1:
            payload["pipeline"] = completed
            return payload

        pattern_context = PatternContext(
            year_pillar=pillar_text(bazi.year_pillar),
            month_pillar=pillar_text(bazi.month_pillar),
            day_pillar=pillar_text(bazi.day_pillar),
            hour_pillar=pillar_text(bazi.hour_pillar),
            day_master=bazi.day_master,
            ten_gods={"list": list(bazi.ten_gods or [])},
            shensha=list(bazi.shensha or []),
        )
        pattern = self.pattern_engine.calculate(pattern_context)
        completed.append("pattern")
        payload["pattern"] = to_jsonable(pattern)
        if stop_index == 2:
            payload["pipeline"] = completed
            return payload

        score = self.score_engine.calculate(
            {
                "calendar": calendar,
                "bazi": bazi,
                "pattern": pattern,
            }
        )
        completed.append("score")
        payload["score"] = to_jsonable(score)
        if stop_index == 3:
            payload["pipeline"] = completed
            return payload

        interpretation = self.interpretation_engine.run(
            {
                "calendar": calendar,
                "bazi": bazi,
                "pattern": pattern,
                "score": score,
            }
        )
        completed.append("interpretation")
        payload["interpretation"] = {
            "summary": getattr(interpretation, "summary", ""),
            "sentence_count": getattr(interpretation, "sentence_count", 0),
            "section_count": getattr(interpretation, "section_count", 0),
            "matched_rule_count": getattr(interpretation, "matched_rule_count", 0),
            "resolved_rule_count": getattr(interpretation, "resolved_rule_count", 0),
            "confidence": getattr(interpretation, "confidence", 0),
        }
        if stop_index == 4:
            payload["pipeline"] = completed
            return payload

        report = self.report_engine.render(interpretation)
        completed.append("report")
        payload["report"] = {
            "title": getattr(getattr(report, "metadata", None), "title", ""),
            "html": getattr(report, "html", ""),
            "markdown": getattr(report, "markdown", ""),
            "section_count": len(getattr(report, "sections", []) or []),
            "templates_used": getattr(report, "templates_used", []),
        }
        if stop_index == 5:
            payload["pipeline"] = completed
            return payload

        narrative = self.narrative_engine.compose(interpretation, report)
        completed.append("narrative")
        payload["narrative"] = {
            "title": getattr(narrative, "title", ""),
            "html": getattr(narrative, "html", ""),
            "markdown": getattr(narrative, "markdown", ""),
            "tone": getattr(narrative, "tone", ""),
            "metrics": getattr(narrative, "metrics", {}),
        }
        payload["pipeline"] = completed
        if stage == "analyze":
            payload["stage"] = "analyze"
        return payload


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
        """Run full pipeline through narrative (report endpoint semantics)."""
        return self.run_stage(
            "narrative",
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            gender=gender,
            timezone=timezone,
        )
