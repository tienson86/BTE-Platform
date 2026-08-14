"""Build CanonicalAnalysisContext from orchestrator or production outputs."""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.foundation.builders.engine_sources import EngineSources
from engines.interpretation_engine.foundation.canonical_context import (
    BaziContext,
    CalendarContext,
    CanonicalAnalysisContext,
    FengShuiContextSlice,
    FiveElementsContextSlice,
    IdentityContext,
    LuckContextSlice,
    PatternContextSlice,
    ScoreContextSlice,
    StrengthContextSlice,
    TemperatureContextSlice,
    TenGodsContextSlice,
    UsefulGodContextSlice,
)
from engines.interpretation_engine.foundation.ownership import DOMAIN_OWNERS


def build_canonical_analysis_context(
    *,
    payload: Mapping[str, Any] | None = None,
    analysis: Any | None = None,
    calendar: Mapping[str, Any] | None = None,
    luck: Mapping[str, Any] | None = None,
    five_elements: Mapping[str, Any] | None = None,
    feng_shui: Mapping[str, Any] | None = None,
    identity: Mapping[str, Any] | None = None,
    engine_sources: EngineSources | None = None,
) -> CanonicalAnalysisContext:
    """Normalize engine outputs into one immutable canonical context."""
    data = _resolve_payload(payload, analysis, calendar, luck, five_elements, feng_shui, identity)
    bazi = data["bazi"]
    strength = data["strength"]
    pattern = data["pattern"]
    useful = data["useful_god"]
    temperature = data["temperature"]
    score = data["score"]
    luck_payload = data["luck"]
    five = data["five_elements"]
    calendar_payload = data["calendar"]
    feng = data["feng_shui"]
    identity_payload = data["identity"]
    ten_gods_engine = engine_sources.ten_gods_result if engine_sources else None

    visible_labels = _visible_ten_god_labels(bazi, ten_gods_engine)
    position_count = len(ten_gods_engine.visible) if ten_gods_engine else len(visible_labels)
    hidden_count = len(ten_gods_engine.hidden) if ten_gods_engine else len(bazi.get("hidden_stems") or [])

    candidate_count = 0
    if engine_sources and engine_sources.useful_god_result is not None:
        candidate_count = len(getattr(engine_sources.useful_god_result, "candidate_list", []) or [])

    cycles = luck_payload.get("cycles") or []
    current = luck_payload.get("current_cycle") or {}
    current_gan_zhi = str(current.get("gan_zhi") or "")

    return CanonicalAnalysisContext(
        identity=IdentityContext(
            full_name=str(identity_payload.get("full_name") or ""),
            gender=str(identity_payload.get("gender") or ""),
            birth_datetime=str(identity_payload.get("birth_datetime") or ""),
            timezone=str(identity_payload.get("timezone") or "Asia/Ho_Chi_Minh"),
        ),
        calendar=CalendarContext(
            solar=str(calendar_payload.get("solar") or calendar_payload.get("birth_date") or ""),
            lunar=str(calendar_payload.get("lunar") or calendar_payload.get("lunar_date") or ""),
            timezone=str(calendar_payload.get("timezone") or identity_payload.get("timezone") or ""),
        ),
        bazi=BaziContext(
            year=_pillar_text(bazi, "year_pillar"),
            month=_pillar_text(bazi, "month_pillar"),
            day=_pillar_text(bazi, "day_pillar"),
            hour=_pillar_text(bazi, "hour_pillar"),
            day_master=str(bazi.get("day_master") or ""),
            day_master_element=str(bazi.get("day_master_element") or ""),
            day_master_yin_yang=str(bazi.get("day_master_yin_yang") or ""),
            shensha_names=tuple(str(item) for item in (bazi.get("shensha") or [])),
        ),
        strength=StrengthContextSlice(
            level=str(strength.get("strength_level") or ""),
            score=float(strength.get("strength_score") or 0.0),
            label=str(strength.get("reasoning") or ""),
            confidence=float(strength.get("confidence") or 0.0),
            evidence=(str(strength.get("reasoning") or ""),) if strength.get("reasoning") else (),
            rule_ids=tuple(str(item) for item in (strength.get("matched_rules") or [])),
            owner=DOMAIN_OWNERS["strength"],
        ),
        pattern=PatternContextSlice(
            selected=str(pattern.get("pattern") or ""),
            label=str(pattern.get("cach_cuc") or ""),
            confidence=float(pattern.get("score") or 0.0),
            evidence=(str(pattern.get("than_vuong_nhuoc") or ""),) if pattern.get("than_vuong_nhuoc") else (),
            rule_ids=(),
            owner=DOMAIN_OWNERS["pattern"],
        ),
        useful_god=UsefulGodContextSlice(
            selected=str(useful.get("useful_god") or ""),
            favorable_gods=tuple(str(item) for item in (useful.get("favorable_gods") or [])),
            unfavorable_gods=tuple(str(item) for item in (useful.get("unfavorable_gods") or [])),
            reason=str(useful.get("reasoning") or ""),
            confidence=float(useful.get("confidence") or 0.0),
            rule_ids=tuple(str(item) for item in (useful.get("matched_rules") or [])),
            candidate_count=candidate_count,
            owner=DOMAIN_OWNERS["useful_god"],
        ),
        five_elements=FiveElementsContextSlice(
            wood=_element_count(five, "wood"),
            fire=_element_count(five, "fire"),
            earth=_element_count(five, "earth"),
            metal=_element_count(five, "metal"),
            water=_element_count(five, "water"),
            dominant=str(five.get("dominant") or "") or None,
            missing=tuple(str(item) for item in (five.get("missing") or [])),
            owner=DOMAIN_OWNERS["five_elements"],
        ),
        temperature=TemperatureContextSlice(
            level=str(temperature.get("temperature_level") or ""),
            score=float(temperature.get("temperature_score") or 0.0),
            label=str(temperature.get("reasoning") or ""),
            recommendations=tuple(str(item) for item in (temperature.get("recommendations") or [])),
            rule_ids=tuple(str(item) for item in (temperature.get("matched_rules") or [])),
            owner=DOMAIN_OWNERS["temperature"],
        ),
        ten_gods=TenGodsContextSlice(
            visible_labels=visible_labels,
            position_count=position_count,
            hidden_count=hidden_count,
            owner=DOMAIN_OWNERS["ten_gods"],
        ),
        shensha_count=len(bazi.get("shensha") or []),
        luck=LuckContextSlice(
            available=bool(luck_payload.get("available")),
            direction=str(luck_payload.get("direction") or ""),
            start_age=_as_int(luck_payload.get("start_age")),
            cycle_count=len(cycles),
            current_gan_zhi=current_gan_zhi,
            owner=DOMAIN_OWNERS["luck"],
        ),
        feng_shui=FengShuiContextSlice(
            menh=str(feng.get("menh") or feng.get("menh_cung") or ""),
            cung=str(feng.get("cung") or feng.get("cung_menh") or ""),
            huong=str(feng.get("huong") or feng.get("huong_nha") or ""),
            owner=DOMAIN_OWNERS["feng_shui"],
        ),
        score=ScoreContextSlice(
            total_score=float(score.get("total_score") or 0.0),
            grade=str(score.get("grade") or ""),
            owner=DOMAIN_OWNERS["score"],
        ),
    )


def _resolve_payload(
    payload: Mapping[str, Any] | None,
    analysis: Any | None,
    calendar: Mapping[str, Any] | None,
    luck: Mapping[str, Any] | None,
    five_elements: Mapping[str, Any] | None,
    feng_shui: Mapping[str, Any] | None,
    identity: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Merge orchestrator payload and AnalysisResult views."""
    if payload is not None:
        return {
            "bazi": dict(payload.get("bazi") or {}),
            "strength": dict(payload.get("strength") or {}),
            "pattern": dict(payload.get("pattern") or {}),
            "useful_god": dict(payload.get("useful_god") or {}),
            "temperature": dict(payload.get("temperature") or {}),
            "score": dict(payload.get("score") or {}),
            "luck": dict(payload.get("luck") or luck or {}),
            "five_elements": dict(payload.get("five_elements") or five_elements or {}),
            "calendar": dict(payload.get("calendar") or calendar or {}),
            "feng_shui": dict(payload.get("feng_shui") or feng_shui or {}),
            "identity": dict(payload.get("input") or identity or {}),
        }
    if analysis is None:
        raise ValueError("analysis or payload required")
    return {
        "bazi": _view_dict(analysis, "bazi"),
        "strength": _view_dict(analysis, "strength"),
        "pattern": _view_dict(analysis, "pattern"),
        "useful_god": _view_dict(analysis, "useful_god"),
        "temperature": _view_dict(analysis, "temperature"),
        "score": _view_dict(analysis, "score"),
        "luck": dict(luck or {}),
        "five_elements": dict(five_elements or {}),
        "calendar": dict(calendar or {}),
        "feng_shui": dict(feng_shui or {}),
        "identity": dict(identity or {}),
    }


def _view_dict(analysis: Any, attr: str) -> dict[str, Any]:
    """Read AnalysisResult view as dict."""
    view = getattr(analysis, attr, None)
    if view is None:
        return {}
    if hasattr(view, "to_dict"):
        return dict(view.to_dict())
    if isinstance(view, Mapping):
        return dict(view)
    return {}


def _pillar_text(bazi: Mapping[str, Any], key: str) -> str:
    """Format pillar as 'Can Chi'."""
    pillar = bazi.get(key) or {}
    if not isinstance(pillar, Mapping):
        return ""
    stem = str(pillar.get("stem") or "")
    branch = str(pillar.get("branch") or "")
    return f"{stem} {branch}".strip()


def _element_count(five: Mapping[str, Any], key: str) -> int | None:
    """Read element count from five_elements payload."""
    counts = five.get("counts") or {}
    if isinstance(counts, Mapping) and key in counts:
        value = counts[key]
        return int(value) if isinstance(value, (int, float)) else None
    entry = five.get(key) or {}
    if isinstance(entry, Mapping):
        value = entry.get("count")
        return int(value) if isinstance(value, (int, float)) else None
    return None


def _visible_ten_god_labels(bazi: Mapping[str, Any], ten_gods_engine: Any | None) -> tuple[str, ...]:
    """Prefer TenGodsEngine visible labels over simplified bazi list."""
    if ten_gods_engine is not None:
        return tuple(item.ten_god for item in ten_gods_engine.visible)
    return tuple(str(item) for item in (bazi.get("ten_gods") or []))


def _as_int(value: Any) -> int | None:
    """Coerce optional int."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
