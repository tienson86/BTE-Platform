"""Full report pipeline orchestration (Applications Layer only)."""

from __future__ import annotations

from typing import Any

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.interpretation_engine.engine import InterpretationEngine
from engines.narrative_engine.engine import NarrativeEngine
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine
from engines.report_engine.engine import ReportEngine
from engines.score_engine.engine import ScoreEngine

from applications.api.serializers import to_jsonable


class ReportPipelineService:
    """
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
        """Execute the WP8 report pipeline and return a JSON-friendly payload."""
        del timezone  # reserved for future calendar localization

        calendar = self.calendar_engine.build(year, month, day, hour, minute)
        bazi = self.bazi_engine.build(calendar, gender=gender)

        pattern_context = PatternContext(
            year_pillar=self._pillar_text(bazi.year_pillar),
            month_pillar=self._pillar_text(bazi.month_pillar),
            day_pillar=self._pillar_text(bazi.day_pillar),
            hour_pillar=self._pillar_text(bazi.hour_pillar),
            day_master=bazi.day_master,
            ten_gods={"list": list(bazi.ten_gods or [])},
            shensha=list(bazi.shensha or []),
        )
        pattern = self.pattern_engine.calculate(pattern_context)

        score = self.score_engine.calculate(
            {
                "calendar": calendar,
                "bazi": bazi,
                "pattern": pattern,
            }
        )

        interpretation = self.interpretation_engine.run(
            {
                "calendar": calendar,
                "bazi": bazi,
                "pattern": pattern,
                "score": score,
            }
        )
        report = self.report_engine.render(interpretation)
        narrative = self.narrative_engine.compose(interpretation, report)

        return {
            "pipeline": [
                "calendar",
                "bazi",
                "pattern",
                "score",
                "interpretation",
                "report",
                "narrative",
            ],
            "calendar": to_jsonable(calendar),
            "bazi": to_jsonable(bazi),
            "pattern": to_jsonable(pattern),
            "score": to_jsonable(score),
            "interpretation": {
                "summary": getattr(interpretation, "summary", ""),
                "sentence_count": getattr(interpretation, "sentence_count", 0),
                "section_count": getattr(interpretation, "section_count", 0),
                "matched_rule_count": getattr(interpretation, "matched_rule_count", 0),
                "resolved_rule_count": getattr(interpretation, "resolved_rule_count", 0),
                "confidence": getattr(interpretation, "confidence", 0),
            },
            "report": {
                "title": getattr(getattr(report, "metadata", None), "title", ""),
                "html": getattr(report, "html", ""),
                "markdown": getattr(report, "markdown", ""),
                "section_count": len(getattr(report, "sections", []) or []),
                "templates_used": getattr(report, "templates_used", []),
            },
            "narrative": {
                "title": getattr(narrative, "title", ""),
                "html": getattr(narrative, "html", ""),
                "markdown": getattr(narrative, "markdown", ""),
                "tone": getattr(narrative, "tone", ""),
                "metrics": getattr(narrative, "metrics", {}),
            },
        }

    @staticmethod
    def _pillar_text(pillar: Any) -> str:
        stem = getattr(pillar, "stem", "")
        branch = getattr(pillar, "branch", "")
        return f"{stem} {branch}".strip()
