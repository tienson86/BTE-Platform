"""Build UnifiedAnalysisContext from upstream engine results."""

from __future__ import annotations

import time
from typing import Any

from .models import (
    BaziSection,
    CalendarSection,
    ContextMetadata,
    ContextTraceEntry,
    PatternSection,
    StrengthSection,
    TemperatureSection,
    UnifiedAnalysisContext,
    UsefulGodSection,
)


class UnifiedContextBuilder:
    """Aggregate engine outputs into UnifiedAnalysisContext V2."""

    def build(
        self,
        *,
        calendar: Any = None,
        bazi: Any = None,
        strength: Any = None,
        temperature: Any = None,
        pattern: Any = None,
        useful_god: Any = None,
        trace: list[ContextTraceEntry] | None = None,
        extra_metadata: dict[str, Any] | None = None,
    ) -> UnifiedAnalysisContext:
        """Build unified context from engine result objects."""
        started = time.perf_counter()
        ctx = UnifiedAnalysisContext(
            calendar=self._build_calendar(calendar),
            bazi=self._build_bazi(bazi),
            strength=self._build_strength(strength),
            temperature=self._build_temperature(temperature),
            pattern=self._build_pattern(pattern),
            useful_god=self._build_useful_god(useful_god),
            metadata=ContextMetadata(
                trace=list(trace or []),
                extra=dict(extra_metadata or {}),
            ),
        )
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        ctx.metadata.trace.append(
            ContextTraceEntry(
                engine="context_engine",
                input_keys=[
                    k
                    for k, v in {
                        "calendar": calendar,
                        "bazi": bazi,
                        "strength": strength,
                        "temperature": temperature,
                        "pattern": pattern,
                        "useful_god": useful_god,
                    }.items()
                    if v is not None
                ],
                output_keys=[
                    "calendar",
                    "bazi",
                    "strength",
                    "temperature",
                    "pattern",
                    "useful_god",
                ],
                duration_ms=round(elapsed_ms, 3),
                success=True,
            )
        )
        return ctx

    @staticmethod
    def _build_calendar(calendar: Any) -> CalendarSection:
        if calendar is None:
            return CalendarSection()
        if isinstance(calendar, dict):
            raw = dict(calendar)
            return CalendarSection(
                solar_year=_int(raw.get("solar_year")),
                solar_month=_int(raw.get("solar_month")),
                solar_day=_int(raw.get("solar_day")),
                solar_hour=_int(raw.get("solar_hour")),
                solar_minute=_int(raw.get("solar_minute")),
                solar_term=_str(raw.get("solar_term")),
                lunar_year=_int(raw.get("lunar_year")),
                lunar_month=_int(raw.get("lunar_month")),
                lunar_day=_int(raw.get("lunar_day")),
                julian_day=_float(raw.get("julian_day")),
                raw=raw,
            )
        lunar = getattr(calendar, "lunar", None)
        return CalendarSection(
            solar_year=_int(getattr(calendar, "solar_year", None)),
            solar_month=_int(getattr(calendar, "solar_month", None)),
            solar_day=_int(getattr(calendar, "solar_day", None)),
            solar_hour=_int(getattr(calendar, "solar_hour", None)),
            solar_minute=_int(getattr(calendar, "solar_minute", None)),
            solar_term=_str(getattr(calendar, "solar_term", None)),
            lunar_year=_int(getattr(lunar, "year", None) if lunar else None),
            lunar_month=_int(getattr(lunar, "month", None) if lunar else None),
            lunar_day=_int(getattr(lunar, "day", None) if lunar else None),
            julian_day=_float(getattr(calendar, "julian_day", None)),
            raw={
                "solar_year": getattr(calendar, "solar_year", None),
                "solar_month": getattr(calendar, "solar_month", None),
                "solar_day": getattr(calendar, "solar_day", None),
                "solar_hour": getattr(calendar, "solar_hour", None),
                "solar_minute": getattr(calendar, "solar_minute", None),
            },
        )

    @staticmethod
    def _build_bazi(bazi: Any) -> BaziSection:
        if bazi is None:
            return BaziSection()
        if isinstance(bazi, dict):
            return BaziSection(
                day_master=_str(bazi.get("day_master")),
                day_master_element=_str(bazi.get("day_master_element")),
                month_branch=_str(bazi.get("month_branch")),
                ten_gods=list(bazi.get("ten_gods") or []),
                hidden_stems=list(bazi.get("hidden_stems") or []),
                raw=dict(bazi),
            )

        def _pillar(p: Any) -> str | None:
            if p is None:
                return None
            stem = getattr(p, "stem", "") or ""
            branch = getattr(p, "branch", "") or ""
            text = f"{stem} {branch}".strip()
            return text or None

        month_pillar = getattr(bazi, "month_pillar", None)
        month_branch = str(getattr(month_pillar, "branch", "") or "") or None

        from engines.bazi_engine.ten_god import STEM_META

        day_master = str(getattr(bazi, "day_master", "") or "")
        dm_meta = STEM_META.get(day_master, ("", ""))

        return BaziSection(
            day_master=day_master or None,
            day_master_element=dm_meta[0] if dm_meta else None,
            year_pillar=_pillar(getattr(bazi, "year_pillar", None)),
            month_pillar=_pillar(month_pillar),
            day_pillar=_pillar(getattr(bazi, "day_pillar", None)),
            hour_pillar=_pillar(getattr(bazi, "hour_pillar", None)),
            month_branch=month_branch,
            ten_gods=list(getattr(bazi, "ten_gods", []) or []),
            hidden_stems=list(getattr(bazi, "hidden_stems", []) or []),
            shensha=list(getattr(bazi, "shensha", []) or []),
            gender=str(getattr(bazi, "gender", "") or "") or None,
            raw={
                "day_master": day_master,
                "month_branch": month_branch,
            },
        )

    @staticmethod
    def _build_strength(strength: Any) -> StrengthSection:
        if strength is None:
            return StrengthSection()
        if isinstance(strength, dict):
            return StrengthSection(
                level=str(strength.get("strength_level") or strength.get("level") or "balanced"),
                score=float(strength.get("strength_score") or strength.get("score") or 0.0),
                season_score=float(strength.get("season_score") or 0.0),
                root_score=float(strength.get("root_score") or 0.0),
                support_score=float(strength.get("support_score") or 0.0),
                drain_score=float(strength.get("drain_score") or 0.0),
                control_score=float(strength.get("control_score") or 0.0),
                confidence=float(strength.get("confidence") or 0.0),
                matched_rules=list(strength.get("matched_rules") or []),
                reasoning=str(strength.get("reasoning") or ""),
                success=bool(strength.get("success", True)),
            )
        return StrengthSection(
            level=str(getattr(strength, "strength_level", "") or "balanced"),
            score=float(getattr(strength, "strength_score", 0.0) or 0.0),
            season_score=float(getattr(strength, "season_score", 0.0) or 0.0),
            root_score=float(getattr(strength, "root_score", 0.0) or 0.0),
            support_score=float(getattr(strength, "support_score", 0.0) or 0.0),
            drain_score=float(getattr(strength, "drain_score", 0.0) or 0.0),
            control_score=float(getattr(strength, "control_score", 0.0) or 0.0),
            confidence=float(getattr(strength, "confidence", 0.0) or 0.0),
            matched_rules=list(getattr(strength, "matched_rules", []) or []),
            reasoning=str(getattr(strength, "reasoning", "") or ""),
            success=bool(getattr(strength, "success", True)),
        )

    @staticmethod
    def _build_temperature(temperature: Any) -> TemperatureSection:
        if temperature is None:
            return TemperatureSection()
        if isinstance(temperature, dict):
            level = str(temperature.get("temperature_level") or temperature.get("level") or "warm")
            temp_type = str(temperature.get("type") or temperature.get("temperature_type") or level)
            return TemperatureSection(
                level=level,
                type=temp_type,
                score=float(temperature.get("temperature_score") or temperature.get("score") or 0.0),
                warm_score=float(temperature.get("warm_score") or 0.0),
                cold_score=float(temperature.get("cold_score") or 0.0),
                dry_score=float(temperature.get("dry_score") or 0.0),
                humid_score=float(temperature.get("humid_score") or 0.0),
                confidence=float(temperature.get("confidence") or 0.0),
                matched_rules=list(temperature.get("matched_rules") or []),
                reasoning=str(temperature.get("reasoning") or ""),
                recommendations=list(temperature.get("recommendations") or []),
                success=bool(temperature.get("success", True)),
            )
        level = str(getattr(temperature, "temperature_level", "") or "warm")
        temp_type = level
        if hasattr(temperature, "to_pattern_temperature_type"):
            temp_type = str(temperature.to_pattern_temperature_type())
        return TemperatureSection(
            level=level,
            type=temp_type,
            score=float(getattr(temperature, "temperature_score", 0.0) or 0.0),
            warm_score=float(getattr(temperature, "warm_score", 0.0) or 0.0),
            cold_score=float(getattr(temperature, "cold_score", 0.0) or 0.0),
            dry_score=float(getattr(temperature, "dry_score", 0.0) or 0.0),
            humid_score=float(getattr(temperature, "humid_score", 0.0) or 0.0),
            confidence=float(getattr(temperature, "confidence", 0.0) or 0.0),
            matched_rules=list(getattr(temperature, "matched_rules", []) or []),
            reasoning=str(getattr(temperature, "reasoning", "") or ""),
            recommendations=list(getattr(temperature, "recommendations", []) or []),
            success=bool(getattr(temperature, "success", True)),
        )

    @staticmethod
    def _build_pattern(pattern: Any) -> PatternSection:
        if pattern is None:
            return PatternSection()
        if isinstance(pattern, dict):
            main = str(pattern.get("main") or pattern.get("pattern") or pattern.get("main_pattern") or "")
            follow = pattern.get("follow") or pattern.get("follow_type")
            return PatternSection(
                main=main,
                follow=str(follow) if follow else None,
                name=str(pattern.get("name") or main),
                score=float(pattern.get("score") or 0.0),
                priority=int(pattern.get("priority") or 0),
                success=bool(pattern.get("success", True)),
                matched_rules=list(pattern.get("matched_rules") or []),
                description=str(pattern.get("description") or ""),
                follow_type=str(follow) if follow else None,
                main_pattern=main or None,
            )
        main = str(getattr(pattern, "pattern", "") or "")
        follow = getattr(pattern, "follow_type", None)
        return PatternSection(
            main=main,
            follow=str(follow) if follow else None,
            name=main,
            score=float(getattr(pattern, "score", 0.0) or 0.0),
            priority=int(getattr(pattern, "priority", 0) or 0),
            success=bool(getattr(pattern, "success", True)),
            matched_rules=list(getattr(pattern, "matched_rules", []) or []),
            description=str(getattr(pattern, "description", "") or ""),
            follow_type=str(follow) if follow else None,
            main_pattern=main or None,
        )

    @staticmethod
    def _build_useful_god(useful_god: Any) -> UsefulGodSection:
        if useful_god is None:
            return UsefulGodSection()
        if isinstance(useful_god, dict):
            return UsefulGodSection(
                primary=str(useful_god.get("primary") or useful_god.get("useful_god") or ""),
                favorable=list(useful_god.get("favorable") or useful_god.get("favorable_gods") or []),
                unfavorable=list(useful_god.get("unfavorable") or useful_god.get("unfavorable_gods") or []),
                confidence=float(useful_god.get("confidence") or 0.0),
                matched_rules=list(useful_god.get("matched_rules") or []),
                reasoning=str(useful_god.get("reasoning") or ""),
                success=bool(useful_god.get("success", True)),
            )
        return UsefulGodSection(
            primary=str(getattr(useful_god, "useful_god", "") or ""),
            favorable=list(getattr(useful_god, "favorable_gods", []) or []),
            unfavorable=list(getattr(useful_god, "unfavorable_gods", []) or []),
            confidence=float(getattr(useful_god, "confidence", 0.0) or 0.0),
            matched_rules=list(getattr(useful_god, "matched_rules", []) or []),
            reasoning=str(getattr(useful_god, "reasoning", "") or ""),
            success=bool(getattr(useful_god, "success", True)),
        )


def _int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
