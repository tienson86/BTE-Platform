"""Test-only adapter: ASCII synthetic pillars -> engine-facing BaZi chart.

Converts repository ASCII stem/branch tokens to the Vietnamese accented
labels the existing Strength Engine / context builder expect.

Does NOT invent birth datetime. Does NOT modify production engines.
"""

from __future__ import annotations

from typing import Any

from engines.bazi_engine.engine import BaziChart, HIDDEN, Pillar
from engines.bazi_engine.ten_god import ten_god_name

# Engine rules and STEM_META use Vietnamese diacritics. Map ASCII aliases
# to those canonical engine tokens without storing Han or non-ASCII in fixtures.
STEM_ENGINE_CANONICAL: dict[str, str] = {
    "canh": "Canh",
    "tan": "Tân",
    "nham": "Nhâm",
    "quy": "Quý",
    "giap": "Giáp",
    "at": "Ất",
    "binh": "Bính",
    "dinh": "Đinh",
    "mau": "Mậu",
    "ky": "Kỷ",
}

BRANCH_ENGINE_CANONICAL: dict[str, str] = {
    "ty": "Tý",
    "suu": "Sửu",
    "dan": "Dần",
    "mao": "Mão",
    "thin": "Thìn",
    "ti": "Tỵ",
    "ngo": "Ngọ",
    "mui": "Mùi",
    "than": "Thân",
    "dau": "Dậu",
    "tuat": "Tuất",
    "hoi": "Hợi",
}


def _normalize_token(token: str) -> str:
    return str(token or "").strip().lower()


def ascii_stem_to_engine(stem_ascii: str) -> str:
    """Map ASCII stem token to Strength/BaZi engine stem label."""
    key = _normalize_token(stem_ascii)
    if key not in STEM_ENGINE_CANONICAL:
        raise ValueError(f"unknown ascii stem: {stem_ascii!r}")
    return STEM_ENGINE_CANONICAL[key]


def ascii_branch_to_engine(branch_ascii: str) -> str:
    """Map ASCII branch token to Strength/BaZi engine branch label."""
    key = _normalize_token(branch_ascii)
    if key not in BRANCH_ENGINE_CANONICAL:
        raise ValueError(f"unknown ascii branch: {branch_ascii!r}")
    return BRANCH_ENGINE_CANONICAL[key]


def ascii_pillar_to_engine(pillar_ascii: str) -> Pillar:
    """Parse 'binh_ngo' into engine Pillar(stem, branch)."""
    raw = _normalize_token(pillar_ascii)
    if "_" not in raw:
        raise ValueError(f"pillar must be stem_branch ascii, got: {pillar_ascii!r}")
    stem_key, branch_key = raw.split("_", 1)
    return Pillar(
        stem=ascii_stem_to_engine(stem_key),
        branch=ascii_branch_to_engine(branch_key),
    )


def build_synthetic_bazi_chart(
    pillars: dict[str, str],
    *,
    day_master_ascii: str | None = None,
) -> BaziChart:
    """Build a synthetic BaziChart from ASCII pillar strings.

    No Gregorian birth datetime is invented. Ten-gods are computed from
    day-master stem vs other pillar stems only.
    """
    year_p = ascii_pillar_to_engine(pillars["year"])
    month_p = ascii_pillar_to_engine(pillars["month"])
    day_p = ascii_pillar_to_engine(pillars["day"])
    hour_p = ascii_pillar_to_engine(pillars["hour"])

    if day_master_ascii is not None:
        expected_dm = ascii_stem_to_engine(day_master_ascii)
        if day_p.stem != expected_dm:
            raise ValueError(
                f"day_master {day_master_ascii!r} != day pillar stem {day_p.stem!r}"
            )

    day_master = day_p.stem
    chart_pillars = [year_p, month_p, day_p, hour_p]
    hidden = [stem for pillar in chart_pillars for stem in HIDDEN[pillar.branch]]
    ten_gods = [
        "Nhật Chủ" if pillar is day_p else ten_god_name(day_master, pillar.stem)
        for pillar in chart_pillars
    ]
    return BaziChart(
        year_pillar=year_p,
        month_pillar=month_p,
        day_pillar=day_p,
        hour_pillar=hour_p,
        gender=None,
        hidden_stems=hidden,
        ten_gods=ten_gods,
        shensha=[],
    )


def context_snapshot_ascii(context: Any) -> dict[str, Any]:
    """Serialize selected context fields using ASCII-safe string conversion."""
    keys = [
        "day_master",
        "day_master_element",
        "month_branch",
        "month_status",
        "root_level",
        "support_type",
        "control_type",
        "drain_type",
        "season",
        "season_phase",
        "temperature_type",
        "root_count",
        "resource_count",
        "companion_count",
        "wealth_count",
        "officer_count",
        "output_count",
    ]
    out: dict[str, Any] = {}
    for key in keys:
        value = getattr(context, key, None)
        if isinstance(value, str):
            # Keep engine labels as-is for diagnostics; fixtures stay ASCII.
            out[key] = value
        else:
            out[key] = value
    return out
