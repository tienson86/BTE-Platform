"""
Kiểm tra / nhận diện Tòng Cách từ chart signals.
"""

from __future__ import annotations

from typing import Any

from engines.bazi_engine.ten_god import STEM_META, ten_god_name


SUPPORT_GODS = frozenset({"Tỷ Kiên", "Kiếp Tài", "Chính Ấn", "Thiên Ấn"})
WEALTH_GODS = frozenset({"Chính Tài", "Thiên Tài"})
OFFICER_GODS = frozenset({"Chính Quan"})
KILLING_GODS = frozenset({"Thất Sát"})
OUTPUT_GODS = frozenset({"Thực Thần", "Thương Quan"})
RESOURCE_GODS = frozenset({"Chính Ấn", "Thiên Ấn"})
SAME_GODS = frozenset({"Tỷ Kiên", "Kiếp Tài"})

# Classical follow labels used by Score / Portal
FOLLOW_BY_CATEGORY: dict[str, str] = {
    "wealth": "Tòng Tài",
    "officer": "Tòng Quan",
    "killing": "Tòng Sát",
    "output": "Tòng Nhi",
    "resource": "Tòng Ấn",
    "same": "Tòng Vượng",
}

FOLLOW_PATTERNS = frozenset(FOLLOW_BY_CATEGORY.values()) | {
    "Tòng Thế",
    "Tòng Quan",
    "Tòng Sát",
    "Tòng Tài",
    "Tòng Nhi",
    "Tòng Ấn",
    "Tòng Vượng",
    "Tòng Cường",
}

# Support share below this → candidate Tòng Nhược family
_WEAK_SUPPORT_RATIO = 0.25
# Support share above this → candidate Tòng Vượng
_STRONG_SUPPORT_RATIO = 0.70


class FollowPatternCalculator:
    """Detect follow-pattern type from PatternContext / chart signals."""

    FOLLOW_PATTERNS = FOLLOW_PATTERNS

    def evaluate(self, pattern: str) -> bool:
        """Return True when ``pattern`` is already a known follow label."""
        return pattern in self.FOLLOW_PATTERNS

    def detect(self, context: Any) -> str | None:
        """
        Derive follow_type from day-master support vs dominant ten-god family.

        Returns a Vietnamese Tòng label, or None when not a follow chart.
        """
        day_master = getattr(context, "day_master", None) or ""
        if not day_master or day_master not in STEM_META:
            return None

        counts = self._count_god_families(context, day_master)
        total = sum(counts.values())
        if total <= 0:
            return None

        support = counts["same"] + counts["resource"]
        support_ratio = support / total

        if support_ratio >= _STRONG_SUPPORT_RATIO:
            return FOLLOW_BY_CATEGORY["same"]

        if support_ratio > _WEAK_SUPPORT_RATIO:
            return None

        # Extremely weak day master — follow the dominant opposing force
        opposing = {
            "wealth": counts["wealth"],
            "officer": counts["officer"],
            "killing": counts["killing"],
            "output": counts["output"],
            "resource": counts["resource"],
        }
        dominant = max(opposing, key=opposing.get)
        if opposing[dominant] <= 0:
            return None
        # Require clear dominance (≥ half of non-support, or absolute ≥ 2)
        non_support = total - support
        if opposing[dominant] < 2 and (
            non_support == 0 or opposing[dominant] / non_support < 0.5
        ):
            return None
        return FOLLOW_BY_CATEGORY.get(dominant)

    def _count_god_families(
        self,
        context: Any,
        day_master: str,
    ) -> dict[str, int]:
        """Count ten-god families from stems + hidden stems (exclude day stem)."""
        counts = {
            "same": 0,
            "resource": 0,
            "wealth": 0,
            "officer": 0,
            "killing": 0,
            "output": 0,
        }
        for god in self._iter_gods(context, day_master):
            if god in SAME_GODS:
                counts["same"] += 1
            elif god in RESOURCE_GODS:
                counts["resource"] += 1
            elif god in WEALTH_GODS:
                counts["wealth"] += 1
            elif god in OFFICER_GODS:
                counts["officer"] += 1
            elif god in KILLING_GODS:
                counts["killing"] += 1
            elif god in OUTPUT_GODS:
                counts["output"] += 1
        return counts

    def _iter_gods(self, context: Any, day_master: str) -> list[str]:
        """Collect ten-god labels from pillars and hidden stems."""
        gods: list[str] = []

        # Explicit ten_gods list on context
        ten_gods = getattr(context, "ten_gods", None) or {}
        if isinstance(ten_gods, dict):
            items = ten_gods.get("list") or ten_gods.get("items") or []
            for item in items:
                text = str(item or "").strip()
                if text and text != "Nhật Chủ":
                    gods.append(text)
        elif isinstance(ten_gods, list):
            for item in ten_gods:
                text = str(item or "").strip()
                if text and text != "Nhật Chủ":
                    gods.append(text)

        # Stem gods from pillars (year/month/hour)
        for attr in ("year_pillar", "month_pillar", "hour_pillar"):
            pillar = getattr(context, attr, None)
            stem = self._pillar_stem(pillar)
            if stem:
                god = ten_god_name(day_master, stem)
                if god:
                    gods.append(god)

        # Hidden stems from bazi chart when available
        bazi = getattr(context, "bazi", None)
        hidden = list(getattr(bazi, "hidden_stems", []) or []) if bazi else []
        for stem in hidden:
            god = ten_god_name(day_master, str(stem))
            if god:
                gods.append(god)

        return gods

    @staticmethod
    def _pillar_stem(pillar: Any) -> str | None:
        if pillar is None:
            return None
        if isinstance(pillar, str):
            parts = pillar.strip().split()
            return parts[0] if parts else None
        return getattr(pillar, "stem", None)
