"""Climate state and minimal Điều hậu need. Does not select Overall Useful God."""

from __future__ import annotations

from typing import Any

# Aligns with database/11_temperature/02_climate_rules.csv recommendations.
CLIMATE_STATES = frozenset({"cold", "cool", "warm", "hot"})

_SEASON_TO_CLIMATE: dict[str, str] = {
    "winter": "cold",
    "summer": "hot",
    "spring": "warm",
    "autumn": "cool",
}

_BALANCING_NEED: dict[str, str] = {
    "cold": "warming",
    "cool": "warming",
    "hot": "cooling",
    "warm": "balance",
}

CLIMATE_STATE_LABELS: dict[str, str] = {
    "cold": "Hàn",
    "cool": "Lương",
    "warm": "Ôn",
    "hot": "Nhiệt",
}

BALANCING_NEED_LABELS: dict[str, str] = {
    "warming": "Cần ôn ấm",
    "cooling": "Cần làm mát",
    "balance": "Cần cân Hỏa Thủy",
}

SEASON_LABELS: dict[str, str] = {
    "spring": "Xuân",
    "summer": "Hạ",
    "autumn": "Thu",
    "winter": "Đông",
}

# Same threshold already used by TemperatureScorer for CSV specials (spc_001–004).
_SPECIAL_OVERRIDE_PRIORITY = 105


def balancing_need_for(climate_state: str) -> str:
    """Map canonical climate_state to Điều hậu balancing need."""
    return _BALANCING_NEED.get(climate_state, "")


def resolve_climate_state(
    context: Any,
    primary_analysis: dict[str, Any],
) -> dict[str, Any]:
    """
    Climate direction from month-branch climate facts, not from temperature_score.

    Special CSV rules with priority >= 105 may reinforce or override the label
    when they carry an explicit temperature_level. Score thresholds do not.
    """
    climate_type = str(getattr(context, "climate_type", "") or "").strip()
    season = str(getattr(context, "season", "") or "").strip()
    month_branch = str(getattr(context, "month_branch", "") or "").strip()

    state = climate_type if climate_type in CLIMATE_STATES else ""
    source = "climate_type" if state else ""
    override_rule_id = ""

    if not state:
        mapped = _SEASON_TO_CLIMATE.get(season, "")
        if mapped:
            state = mapped
            source = "season"

    specials = list(primary_analysis.get("special_matches") or [])
    specials.sort(key=lambda item: int(item.get("priority") or 0), reverse=True)
    for rule in specials:
        hint = str(rule.get("temperature_level") or "").strip()
        if hint not in CLIMATE_STATES:
            continue
        if int(rule.get("priority") or 0) < _SPECIAL_OVERRIDE_PRIORITY:
            continue
        state = hint
        source = "special"
        override_rule_id = str(rule.get("rule_id") or "")
        break

    need = balancing_need_for(state)
    return {
        "climate_state": state,
        "climate_source": source,
        "special_override_rule_id": override_rule_id,
        "balancing_need": need,
        "climate_state_label": CLIMATE_STATE_LABELS.get(state, ""),
        "balancing_need_label": BALANCING_NEED_LABELS.get(need, ""),
        "season": season,
        "season_label": SEASON_LABELS.get(season, season),
        "month_branch": month_branch,
        "score_semantic": "imbalance_intensity",
    }


def compact_evidence(
    climate: dict[str, Any],
    *,
    winning_climate_rule_id: str = "",
) -> str:
    """Compact Điều hậu evidence. No tài vận / sức khỏe / nghề wording."""
    parts: list[str] = []
    branch = str(climate.get("month_branch") or "")
    if branch:
        parts.append(f"Nguyệt lệnh {branch}")
    season_label = str(climate.get("season_label") or "")
    if season_label:
        parts.append(f"mùa {season_label}")
    state_label = str(climate.get("climate_state_label") or "")
    if state_label:
        parts.append(f"khí hậu {state_label}")
    need_label = str(climate.get("balancing_need_label") or "")
    if need_label:
        parts.append(need_label)
    rule_id = winning_climate_rule_id or str(climate.get("special_override_rule_id") or "")
    if rule_id:
        parts.append(f"rule {rule_id}")
    return " · ".join(parts)


def winning_climate_rule_id(primary_analysis: dict[str, Any]) -> str:
    """Highest-priority matched climate CSV rule."""
    matches = list(primary_analysis.get("climate_matches") or [])
    if not matches:
        matches = list(primary_analysis.get("season_matches") or [])
    if not matches:
        return ""
    matches.sort(key=lambda item: int(item.get("priority") or 0), reverse=True)
    return str(matches[0].get("rule_id") or "")


def climate_aligned_recommendations(
    primary_analysis: dict[str, Any],
    climate_state: str,
) -> list[str]:
    """Recommendations from climate/season facts, not from score-based level rules."""
    recs: list[str] = []
    seen: set[str] = set()
    rows: list[dict[str, Any]] = []
    for key in ("climate_matches", "season_matches"):
        rows.extend(primary_analysis.get(key) or [])
    rows.sort(key=lambda item: int(item.get("priority") or 0), reverse=True)
    for rule in rows:
        level = str(rule.get("temperature_level") or "").strip()
        if level and climate_state and level != climate_state:
            # Keep same-axis season/climate recs (cold with cool is still warming).
            cold_axis = frozenset({"cold", "cool"})
            hot_axis = frozenset({"hot", "warm"})
            if not (
                (level in cold_axis and climate_state in cold_axis)
                or (level in hot_axis and climate_state in hot_axis)
            ):
                continue
        rec = str(rule.get("recommendation") or "").strip()
        if rec and rec not in seen:
            recs.append(rec)
            seen.add(rec)
        if len(recs) >= 5:
            break
    return recs
