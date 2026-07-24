"""
RuleContext Builder

Build a normalized RuleContext dict from upstream engine results.

RuleMatcher consumes only RuleContext (+ RuleContract).
Does not modify Adapter / Matcher / Knowledge Base.
"""

from __future__ import annotations

from typing import Any, Mapping

from .models import RuleContext, normalize_context

# ---------------------------------------------------------------------------
# Stem / Branch → Five Elements
# ---------------------------------------------------------------------------

STEM_ELEMENT: dict[str, str] = {
    "Giáp": "wood",
    "Ất": "wood",
    "Bính": "fire",
    "Đinh": "fire",
    "Mậu": "earth",
    "Kỷ": "earth",
    "Canh": "metal",
    "Tân": "metal",
    "Nhâm": "water",
    "Quý": "water",
}

BRANCH_ELEMENT: dict[str, str] = {
    "Tý": "water",
    "Sửu": "earth",
    "Dần": "wood",
    "Mão": "wood",
    "Thìn": "earth",
    "Tỵ": "fire",
    "Ngọ": "fire",
    "Mùi": "earth",
    "Thân": "metal",
    "Dậu": "metal",
    "Tuất": "earth",
    "Hợi": "water",
}

ELEMENTS: tuple[str, ...] = ("wood", "fire", "earth", "metal", "water")

# Solar month → rough season / month command label (V1 heuristic)
MONTH_STATUS: dict[int, str] = {
    1: "Đắc lệnh",
    2: "Đắc lệnh",
    3: "Tướng",
    4: "Đắc lệnh",
    5: "Đắc lệnh",
    6: "Tướng",
    7: "Đắc lệnh",
    8: "Đắc lệnh",
    9: "Tướng",
    10: "Đắc lệnh",
    11: "Đắc lệnh",
    12: "Tướng",
}

SEASON_BY_MONTH: dict[int, str] = {
    1: "winter",
    2: "winter",
    3: "spring",
    4: "spring",
    5: "spring",
    6: "summer",
    7: "summer",
    8: "summer",
    9: "autumn",
    10: "autumn",
    11: "autumn",
    12: "winter",
}

# Minimum required top-level sections
REQUIRED_SECTIONS: tuple[str, ...] = (
    "calendar",
    "bazi",
    "pattern",
    "score",
    "luck",
    "shensha",
    "metadata",
)

# Expected signal namespaces for completeness reporting
EXPECTED_SIGNALS: tuple[str, ...] = (
    "bazi.day_master",
    "bazi.year_pillar",
    "bazi.month_pillar",
    "bazi.day_pillar",
    "bazi.hour_pillar",
    "bazi.month_branch",
    "pattern.main_pattern",
    "pattern.name",
    "pattern.status",
    "pattern.success",
    "wuxing.wood.status",
    "wuxing.fire.status",
    "wuxing.earth.status",
    "wuxing.metal.status",
    "wuxing.water.status",
    "wuxing.season",
    "strength.level",
    "strength.month_status",
    "month.status",
    "score.total_score",
    "facts",
)


class RuleContextBuilder:
    """
    Build RuleContext from Calendar / Bazi / Pattern / Score (+ optional luck/shensha).
    """

    def build(
        self,
        *,
        calendar: Any = None,
        bazi: Any = None,
        pattern: Any = None,
        score: Any = None,
        luck: Any = None,
        shensha: Any = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Build a RuleContext dict.

        Parameters
        ----------
        calendar:
            CalendarResult (optional).
        bazi:
            BaziChart (optional).
        pattern:
            PatternResult (optional).
        score:
            ScoreResult (optional).
        luck:
            Luck result object / dict (optional).
        shensha:
            Shensha result object / dict / list (optional).
            If omitted, falls back to ``bazi.shensha`` when available.
        metadata:
            Extra metadata merged into context.metadata.
        """
        context: dict[str, Any] = {
            "calendar": self._build_calendar(calendar),
            "bazi": self._build_bazi(bazi),
            "pattern": self._build_pattern(pattern),
            "score": self._build_score(score),
            "luck": self._build_luck(luck),
            "shensha": self._build_shensha(shensha, bazi),
            "metadata": dict(metadata or {}),
        }

        # Derived signal namespaces (Rule Contract V1)
        context["wuxing"] = self._build_wuxing(bazi, context["calendar"])
        context["strength"] = self._build_strength(bazi, context["calendar"], score)
        context["month"] = self._build_month(context["calendar"], context["bazi"])
        context["ten_gods"] = self._build_ten_gods(bazi)
        context["useful_god"] = self._build_useful_god(score)
        context["facts"] = self._build_facts(context)
        context["rule"] = {"status": "READY"}

        # Flat aliases used by Priority FIELD_COMPARE / Adapter
        context["day_master"] = context["bazi"].get("day_master")
        context["strength_score"] = context["strength"].get("score", 0.0)
        context["birth_season"] = context["wuxing"].get("season")

        return context

    # =========================================================
    # Completeness
    # =========================================================

    def completeness(self, context: Mapping[str, Any]) -> dict[str, Any]:
        """
        Report which required sections / signals are present.
        """
        missing_sections = [
            key for key in REQUIRED_SECTIONS if key not in context
        ]
        present_signals: list[str] = []
        missing_signals: list[str] = []

        for path in EXPECTED_SIGNALS:
            if path == "facts":
                ok = isinstance(context.get("facts"), (dict, set, list))
            else:
                ok = self._has_path(context, path)
            if ok:
                present_signals.append(path)
            else:
                missing_signals.append(path)

        total = len(EXPECTED_SIGNALS)
        coverage = round(100.0 * len(present_signals) / total, 1) if total else 0.0

        return {
            "missing_sections": missing_sections,
            "present_signals": present_signals,
            "missing_signals": missing_signals,
            "coverage_percent": coverage,
            "complete": not missing_sections and not missing_signals,
        }

    # =========================================================
    # Section builders
    # =========================================================

    def _build_calendar(self, calendar: Any) -> dict[str, Any]:
        if calendar is None:
            return {}
        term = getattr(calendar, "solar_term", None)
        term_name = getattr(term, "name", term)
        return {
            "solar_year": getattr(calendar, "solar_year", None),
            "solar_month": getattr(calendar, "solar_month", None),
            "solar_day": getattr(calendar, "solar_day", None),
            "solar_hour": getattr(calendar, "solar_hour", None),
            "solar_minute": getattr(calendar, "solar_minute", None),
            "julian_day": getattr(calendar, "julian_day", None),
            "solar_term": term_name,
            "lunar": self._safe_str(getattr(calendar, "lunar", None)),
            "solar": self._safe_str(getattr(calendar, "solar", None)),
        }

    def _build_bazi(self, bazi: Any) -> dict[str, Any]:
        if bazi is None:
            return {}

        year = self._pillar_dict(getattr(bazi, "year_pillar", None))
        month = self._pillar_dict(getattr(bazi, "month_pillar", None))
        day = self._pillar_dict(getattr(bazi, "day_pillar", None))
        hour = self._pillar_dict(getattr(bazi, "hour_pillar", None))
        day_master = getattr(bazi, "day_master", None) or day.get("stem")

        return {
            "day_master": day_master,
            "gender": getattr(bazi, "gender", None),
            "year_pillar": year,
            "month_pillar": month,
            "day_pillar": day,
            "hour_pillar": hour,
            "month_branch": month.get("branch"),
            "day_branch": day.get("branch"),
            "hidden_stems": list(getattr(bazi, "hidden_stems", []) or []),
            "ten_gods": list(getattr(bazi, "ten_gods", []) or []),
            "shensha": list(getattr(bazi, "shensha", []) or []),
        }

    def _build_pattern(self, pattern: Any) -> dict[str, Any]:
        if pattern is None:
            return {
                "main_pattern": None,
                "name": None,
                "status": None,
                "success": None,
                "score": 0.0,
                "priority": 0,
                "matched_rules": [],
                "not_destroyed": None,
                "has_control": None,
                "type": None,
                "follow_type": None,
            }

        success = bool(getattr(pattern, "success", False))
        name = getattr(pattern, "pattern", None)
        error = getattr(pattern, "error", None)
        status = "SUCCESS" if success and name else ("FAIL" if error else "UNKNOWN")

        return {
            "main_pattern": name,
            "name": name,
            "status": status,
            "success": success,
            "score": float(getattr(pattern, "score", 0.0) or 0.0),
            "priority": int(getattr(pattern, "priority", 0) or 0),
            "matched_rules": list(getattr(pattern, "matched_rules", []) or []),
            "error": error,
            "not_destroyed": success,
            "has_control": success,
            "type": name,
            "follow_type": None,
        }

    def _build_score(self, score: Any) -> dict[str, Any]:
        if score is None:
            return {
                "total_score": 0.0,
                "wuxing_score": 0.0,
                "strength_score": 0.0,
                "ten_god_score": 0.0,
                "pattern_score": 0.0,
                "useful_god_score": 0.0,
                "shensha_score": 0.0,
                "luck_score": 0.0,
                "grade": "",
                "confidence": "",
                "success": None,
                "modules": [],
            }

        data = normalize_context(score) if not isinstance(score, dict) else dict(score)
        return {
            "total_score": float(data.get("total_score", 0.0) or 0.0),
            "wuxing_score": float(data.get("wuxing_score", 0.0) or 0.0),
            "strength_score": float(data.get("strength_score", 0.0) or 0.0),
            "ten_god_score": float(data.get("ten_god_score", 0.0) or 0.0),
            "pattern_score": float(data.get("pattern_score", 0.0) or 0.0),
            "useful_god_score": float(data.get("useful_god_score", 0.0) or 0.0),
            "shensha_score": float(data.get("shensha_score", 0.0) or 0.0),
            "luck_score": float(data.get("luck_score", 0.0) or 0.0),
            "grade": data.get("grade", "") or "",
            "confidence": data.get("confidence", "") or "",
            "recommendation": data.get("recommendation", "") or "",
            "success": data.get("success"),
            "modules": list(data.get("modules", []) or []),
            "confidence_value": self._confidence_to_value(data.get("confidence")),
        }

    def _build_luck(self, luck: Any) -> dict[str, Any]:
        if luck is None:
            return {"available": False, "pillars": [], "status": None}
        if isinstance(luck, dict):
            data = dict(luck)
            data.setdefault("available", True)
            return data
        return {
            "available": True,
            "raw": normalize_context(luck),
            "status": getattr(luck, "status", None),
        }

    def _build_shensha(self, shensha: Any, bazi: Any) -> dict[str, Any]:
        stars: list[str] = []
        if shensha is None and bazi is not None:
            stars = list(getattr(bazi, "shensha", []) or [])
        elif isinstance(shensha, list):
            stars = [str(item) for item in shensha]
        elif isinstance(shensha, dict):
            nested = shensha.get("stars") or shensha.get("items") or []
            stars = [str(item) for item in nested]
            # Also promote star entries already shaped as status maps
            result = {
                "available": True,
                "stars": stars,
                "status": "PRESENT" if stars else "MISSING",
            }
            for key, value in shensha.items():
                if key not in result:
                    result[key] = value
            return result
        elif shensha is not None:
            stars = list(getattr(shensha, "stars", getattr(shensha, "items", [])) or [])

        result: dict[str, Any] = {
            "available": bool(stars),
            "stars": stars,
            "status": "PRESENT" if stars else "MISSING",
        }
        for star in stars:
            slug = self._slug(star)
            result[slug] = {"status": "PRESENT", "name": star}
        return result

    # =========================================================
    # Signal builders
    # =========================================================

    def _build_wuxing(self, bazi: Any, calendar: Mapping[str, Any]) -> dict[str, Any]:
        counts = {element: 0 for element in ELEMENTS}
        if bazi is not None:
            for pillar in getattr(bazi, "pillars", []) or []:
                stem = getattr(pillar, "stem", None)
                branch = getattr(pillar, "branch", None)
                if stem in STEM_ELEMENT:
                    counts[STEM_ELEMENT[stem]] += 1
                if branch in BRANCH_ELEMENT:
                    counts[BRANCH_ELEMENT[branch]] += 1
            for hidden in getattr(bazi, "hidden_stems", []) or []:
                if hidden in STEM_ELEMENT:
                    counts[STEM_ELEMENT[hidden]] += 1

        wuxing: dict[str, Any] = {
            "season": SEASON_BY_MONTH.get(int(calendar.get("solar_month") or 0))
            if calendar.get("solar_month")
            else None,
            "season_status": None,
            "balance_level": None,
            "balance_ratio": None,
            "element": None,
            "status": None,
            "counts": counts,
        }

        statuses = []
        for element in ELEMENTS:
            count = counts[element]
            if count <= 0:
                status = "MISSING"
            elif count == 1:
                status = "PRESENT"
            elif count == 2:
                status = "STRONG"
            else:
                status = "EXCESS"
            wuxing[element] = {"status": status, "count": count}
            statuses.append(status)

        # Aggregate hint
        if all(item == "MISSING" for item in statuses):
            wuxing["status"] = "MISSING"
        elif "EXCESS" in statuses:
            wuxing["status"] = "EXCESS"
        elif "STRONG" in statuses:
            wuxing["status"] = "STRONG"
        else:
            wuxing["status"] = "PRESENT"

        month = calendar.get("solar_month")
        if month:
            wuxing["season_status"] = "IN_SEASON"

        return wuxing

    def _build_strength(
        self,
        bazi: Any,
        calendar: Mapping[str, Any],
        score: Any,
    ) -> dict[str, Any]:
        month = int(calendar.get("solar_month") or 0)
        month_status = MONTH_STATUS.get(month)
        score_value = 0.0
        if score is not None:
            score_value = float(getattr(score, "strength_score", 0.0) or 0.0)

        # Very light heuristic until Score module produces real strength
        if score_value >= 70:
            level = "strong"
        elif score_value >= 40:
            level = "balanced"
        elif score_value > 0:
            level = "weak"
        else:
            level = "unknown"

        return {
            "level": level,
            "month_status": month_status,
            "root_level": None,
            "support_type": None,
            "control_type": None,
            "score": score_value,
        }

    def _build_month(
        self,
        calendar: Mapping[str, Any],
        bazi: Mapping[str, Any],
    ) -> dict[str, Any]:
        month = int(calendar.get("solar_month") or 0)
        return {
            "status": MONTH_STATUS.get(month),
            "solar_month": month or None,
            "branch": bazi.get("month_branch"),
        }

    def _build_ten_gods(self, bazi: Any) -> dict[str, Any]:
        if bazi is None:
            return {"items": [], "status": None}
        items = list(getattr(bazi, "ten_gods", []) or [])
        return {
            "items": items,
            "status": "PRESENT" if items else "MISSING",
            "name": items[0] if items else None,
            "zheng_guan": {"visible": False, "present": False},
            "qi_sha": {"visible": False, "present": False},
        }

    def _build_useful_god(self, score: Any) -> dict[str, Any]:
        if score is None:
            return {"status": None, "score": 0.0}
        value = float(getattr(score, "useful_god_score", 0.0) or 0.0)
        return {
            "status": "PRESENT" if value > 0 else "MISSING",
            "score": value,
        }

    def _build_facts(self, context: Mapping[str, Any]) -> dict[str, bool]:
        """Boolean facts for Priority-style matching."""
        pattern = context.get("pattern") or {}
        strength = context.get("strength") or {}
        bazi = context.get("bazi") or {}
        wuxing = context.get("wuxing") or {}

        facts = {
            "pattern_identified": bool(pattern.get("main_pattern")),
            "pattern_success": pattern.get("status") == "SUCCESS",
            "has_day_master": bool(bazi.get("day_master")),
            "day_master_strength_calculated": strength.get("level") not in {
                None,
                "unknown",
            },
            "temperature_profile_calculated": False,
            "combination_rule_valid": False,
        }

        # Strength extremes from score heuristic
        score_value = float(strength.get("score") or 0.0)
        facts["day_master_extremely_strong"] = score_value >= 80
        facts["day_master_extremely_weak"] = 0 < score_value <= 20

        # Element presence facts
        for element in ELEMENTS:
            status = ((wuxing.get(element) or {}).get("status"))
            facts[f"wuxing_{element}_present"] = status in {
                "PRESENT",
                "STRONG",
                "EXCESS",
            }

        return facts

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _pillar_dict(pillar: Any) -> dict[str, Any]:
        if pillar is None:
            return {}
        return {
            "stem": getattr(pillar, "stem", None),
            "branch": getattr(pillar, "branch", None),
            "label": (
                f"{getattr(pillar, 'stem', '')}"
                f"{getattr(pillar, 'branch', '')}"
            ).strip()
            or None,
        }

    @staticmethod
    def _safe_str(value: Any) -> str | None:
        if value is None:
            return None
        return str(value)

    @staticmethod
    def _slug(text: str) -> str:
        import re

        cleaned = re.sub(r"\s+", "_", text.strip().lower())
        cleaned = re.sub(r"[^a-z0-9_]+", "", cleaned)
        return cleaned or "item"

    @staticmethod
    def _confidence_to_value(raw: Any) -> float | None:
        if raw is None or raw == "":
            return None
        try:
            return float(raw)
        except (TypeError, ValueError):
            mapping = {
                "high": 0.9,
                "medium": 0.6,
                "low": 0.3,
            }
            return mapping.get(str(raw).strip().lower())

    @staticmethod
    def _has_path(context: Mapping[str, Any], path: str) -> bool:
        current: Any = context
        for part in path.split("."):
            if not isinstance(current, Mapping) or part not in current:
                return False
            current = current[part]
        return current is not None and current != "" and current != []


def build_rule_context(**kwargs: Any) -> RuleContext:
    """Helper function — build RuleContext via RuleContextBuilder."""
    return RuleContextBuilder().build(**kwargs)
