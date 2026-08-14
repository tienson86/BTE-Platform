"""Frozen domain ownership map — engines own analytical truth."""

from __future__ import annotations

from typing import Final

DOMAIN_OWNERS: Final[dict[str, str]] = {
    "strength": "StrengthEngine",
    "pattern": "PatternEngine",
    "useful_god": "UsefulGodEngine",
    "temperature": "TemperatureEngine",
    "ten_gods": "TenGodsEngine",
    "shensha": "ShenShaService",
    "luck": "LuckEngine",
    "five_elements": "RuleContext.wuxing",
    "score": "ScoreEngine",
    "bazi": "BaziEngine",
    "calendar": "CalendarEngine",
    "feng_shui": "FengShuiEngine",
}
