"""
RuleContext Builder

Build a normalized RuleContext dict from upstream engine results.

RuleMatcher consumes only RuleContext (+ RuleContract).
Does not modify Adapter / Matcher / Knowledge Base.
"""

from __future__ import annotations

from typing import Any, Mapping

from .models import RuleContext, normalize_context
from . import signal_maps as maps

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
    "strength.root_level",
    "strength.support_type",
    "strength.control_type",
    "month.status",
    "score.total_score",
    "ten_gods.status",
    "ten_gods.items",
    "useful_god.status",
    "shensha.status",
    "luck.available",
    "temperature.status",
    "root.level",
    "support.type",
    "control.type",
    "hidden_stems.flat",
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
        useful_god: Any = None,
        temperature: Any = None,
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
            If omitted, falls back to ``bazi.shensha`` then classical maps.
        useful_god:
            Useful-god result object / dict (optional).
        temperature:
            Temperature result object / dict (optional).
        metadata:
            Extra metadata merged into context.metadata.
        """
        context: dict[str, Any] = {
            "calendar": self._build_calendar(calendar),
            "bazi": self._build_bazi(bazi),
            "pattern": self._build_pattern(pattern),
            "score": self._build_score(score),
            "luck": self._build_luck(luck),
            "metadata": dict(metadata or {}),
        }

        # Derived signal namespaces (Rule Contract V1 / WP2D)
        context["wuxing"] = self._build_wuxing(bazi, context["calendar"])
        context["hidden_stems"] = self._build_hidden_stems(bazi, context["bazi"])
        context["ten_gods"] = self._build_ten_gods(bazi, context["bazi"])
        context["shensha"] = self._build_shensha(shensha, bazi, context["bazi"])
        context["strength"] = self._build_strength(
            bazi, context["calendar"], score, context["bazi"], context["hidden_stems"]
        )
        context["root"] = {
            "level": context["strength"].get("root_level"),
            "status": context["strength"].get("root_level"),
        }
        context["support"] = {
            "type": context["strength"].get("support_type"),
            "status": context["strength"].get("support_type"),
        }
        context["control"] = {
            "type": context["strength"].get("control_type"),
            "status": context["strength"].get("control_type"),
        }
        context["month"] = self._build_month(context["calendar"], context["bazi"])
        context["useful_god"] = self._build_useful_god(
            score,
            useful_god,
            context["pattern"],
            context["bazi"],
            context["hidden_stems"],
            context["ten_gods"],
        )
        context["temperature"] = self._build_temperature(temperature)
        context["facts"] = self._build_facts(context)
        context["special"] = {"case_name": None}
        context["rule"] = {"status": "READY"}

        # Flat aliases used by Priority FIELD_COMPARE / Adapter
        context["day_master"] = context["bazi"].get("day_master")
        context["strength_score"] = context["strength"].get("score", 0.0)
        context["birth_season"] = context["wuxing"].get("season")

        # Temperature numeric compares (Priority); None until Temperature engine
        for key in ("cold_score", "hot_score", "damp_score", "dry_score"):
            context[key] = (context["temperature"] or {}).get(key)

        # Priority ConditionMatcher reads top-level keys when facts is a dict
        for key, value in context["facts"].items():
            if value is True and key not in context:
                context[key] = True

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
                "category": None,
                "month_commander_match": None,
                "month_support_match": None,
                "season_alignment": None,
                "day_master_support": None,
                "visible_count": None,
                "visibility_ratio": None,
                "supported_count": None,
                "destroyed_count": None,
                "clash_count": None,
                "combination_status": None,
                "transformation": None,
                "purity": None,
                "consistency": None,
                "structure_completeness": None,
                "classic_validation": None,
            }

        success = bool(getattr(pattern, "success", False))
        name = getattr(pattern, "pattern", None)
        error = getattr(pattern, "error", None)
        status = "SUCCESS" if success and name else ("FAIL" if error else "UNKNOWN")

        def _attr(key: str, default: Any = None) -> Any:
            return getattr(pattern, key, default)

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
            "follow_type": _attr("follow_type"),
            "category": _attr("category"),
            "month_commander_match": _attr("month_commander_match"),
            "month_support_match": _attr("month_support_match"),
            "season_alignment": _attr("season_alignment"),
            "day_master_support": _attr("day_master_support"),
            "visible_count": _attr("visible_count"),
            "visibility_ratio": _attr("visibility_ratio"),
            "supported_count": _attr("supported_count"),
            "destroyed_count": _attr("destroyed_count"),
            "clash_count": _attr("clash_count"),
            "combination_status": _attr("combination_status"),
            "transformation": _attr("transformation"),
            "purity": _attr("purity"),
            "consistency": _attr("consistency"),
            "structure_completeness": _attr("structure_completeness"),
            "classic_validation": _attr("classic_validation"),
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
            return {
                "available": False,
                "pillars": [],
                "status": None,
                "phase": None,
                "support": None,
                "attack": None,
            }
        if isinstance(luck, dict):
            data = dict(luck)
            data.setdefault("available", True)
            data.setdefault("status", data.get("status"))
            return data
        return {
            "available": True,
            "raw": normalize_context(luck),
            "status": getattr(luck, "status", None),
            "pillars": list(getattr(luck, "pillars", []) or []),
            "phase": getattr(luck, "phase", None),
            "support": getattr(luck, "support", None),
            "attack": getattr(luck, "attack", None),
        }

    def _build_shensha(
        self,
        shensha: Any,
        bazi: Any,
        bazi_section: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        stars: list[str] = []
        if shensha is None and bazi is not None:
            stars = list(getattr(bazi, "shensha", []) or [])
        elif isinstance(shensha, list):
            stars = [str(item) for item in shensha]
        elif isinstance(shensha, dict):
            nested = shensha.get("stars") or shensha.get("items") or []
            stars = [str(item) for item in nested]
            result = {
                "available": True,
                "stars": stars,
                "status": "PRESENT" if stars else "MISSING",
                "star": stars[0] if stars else None,
            }
            for key, value in shensha.items():
                if key not in result:
                    result[key] = value
            for star in stars:
                result[self._slug(star)] = {"status": "PRESENT", "name": star}
            return result
        elif shensha is not None:
            stars = list(getattr(shensha, "stars", getattr(shensha, "items", [])) or [])
            names_fn = getattr(shensha, "names", None)
            if callable(names_fn):
                stars = list(names_fn() or stars)

        # WP2D: classical presence map from day master + chart branches
        if not stars and bazi_section:
            stars = self._detect_shensha_stars(bazi_section)

        result: dict[str, Any] = {
            "available": bool(stars),
            "stars": stars,
            "status": "PRESENT" if stars else "MISSING",
            "star": stars[0] if stars else None,
        }
        for star in stars:
            result[self._slug(star)] = {"status": "PRESENT", "name": star}
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
            "combination_type": None,
            "clash_type": None,
            "special_case": None,
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
        bazi_section: Mapping[str, Any] | None = None,
        hidden_stems: Mapping[str, Any] | None = None,
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

        root_level, support_type, control_type = self._map_root_support_control(
            bazi_section or {},
            hidden_stems or {},
        )

        return {
            "level": level,
            "month_status": month_status,
            "root_level": root_level,
            "support_type": support_type,
            "control_type": control_type,
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

    def _build_hidden_stems(
        self,
        bazi: Any,
        bazi_section: Mapping[str, Any],
    ) -> dict[str, Any]:
        flat = list(bazi_section.get("hidden_stems") or [])
        if not flat and bazi is not None:
            flat = list(getattr(bazi, "hidden_stems", []) or [])

        by_pillar: dict[str, list[str]] = {}
        for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"):
            pillar = bazi_section.get(key) or {}
            branch = pillar.get("branch")
            by_pillar[key] = list(maps.BRANCH_HIDDEN.get(branch or "", []))

        return {
            "flat": flat,
            "items": flat,
            "by_pillar": by_pillar,
            "status": "PRESENT" if flat else "MISSING",
            "count": len(flat),
        }

    def _build_ten_gods(
        self,
        bazi: Any,
        bazi_section: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        bazi_section = bazi_section or {}
        items = self._derive_ten_god_items(bazi_section)
        if not items and bazi is not None:
            items = list(getattr(bazi, "ten_gods", []) or [])

        unique = list(dict.fromkeys(items))
        by_name: dict[str, dict[str, Any]] = {}
        for name in unique:
            by_name[name] = {"status": "PRESENT", "name": name, "present": True}

        month_hidden_gods = self._month_hidden_ten_gods(bazi_section)
        all_present = set(unique) | set(month_hidden_gods)

        def _flag(name: str) -> dict[str, bool]:
            present = name in all_present
            return {"visible": present, "present": present, "destroyed": False}

        return {
            "items": items,
            "unique": unique,
            "status": "PRESENT" if items else "MISSING",
            "name": unique[0] if unique else None,
            "structure": None,
            "month_hidden_ten_gods": month_hidden_gods,
            "month_commander_ten_god": (
                month_hidden_gods[0] if month_hidden_gods else None
            ),
            "visible_ten_gods": unique,
            "destroyed_ten_gods": [],
            "zheng_guan": _flag("Chính Quan"),
            "qi_sha": _flag("Thất Sát"),
            "zheng_cai": _flag("Chính Tài"),
            "pian_cai": _flag("Thiên Tài"),
            "zheng_yin": _flag("Chính Ấn"),
            "pian_yin": _flag("Thiên Ấn"),
            "shi_shen": _flag("Thực Thần"),
            "shang_guan": _flag("Thương Quan"),
            "bi_jian": _flag("Tỷ Kiên"),
            "jie_cai": _flag("Kiếp Tài"),
            "by_name": by_name,
            **by_name,
        }

    def _build_useful_god(
        self,
        score: Any,
        useful_god: Any,
        pattern: Mapping[str, Any],
        bazi_section: Mapping[str, Any],
        hidden_stems: Mapping[str, Any],
        ten_gods: Mapping[str, Any],
    ) -> dict[str, Any]:
        score_value = 0.0
        if score is not None:
            score_value = float(getattr(score, "useful_god_score", 0.0) or 0.0)

        result: dict[str, Any] = {
            "status": None,
            "name": None,
            "element": None,
            "role": None,
            "favorable": [],
            "unfavorable": [],
            "score": score_value,
            "in_stem": False,
            "in_branch": False,
            "in_hidden": False,
        }

        # Prefer explicit upstream useful-god payload
        if useful_god is not None:
            if isinstance(useful_god, dict):
                result.update({k: v for k, v in useful_god.items() if v is not None})
            else:
                result["name"] = getattr(useful_god, "useful_god", None) or getattr(
                    useful_god, "name", None
                )
                result["status"] = getattr(useful_god, "status", result["status"])
                result["element"] = getattr(useful_god, "element", None)
                result["favorable"] = list(getattr(useful_god, "favorable", []) or [])
                result["unfavorable"] = list(
                    getattr(useful_god, "unfavorable", []) or []
                )

        # Map from pattern + chart pillars when upstream useful-god absent
        if result["name"] is None:
            pattern_key = str(pattern.get("name") or pattern.get("main_pattern") or "")
            result["name"] = maps.PATTERN_USEFUL_GOD.get(pattern_key.lower())

        if result["name"] is None and ten_gods.get("name"):
            # Fallback: first derived ten god (presence only)
            result["name"] = None

        god_name = result.get("name")
        if god_name:
            locations = self._locate_ten_god(
                god_name, bazi_section, hidden_stems, ten_gods
            )
            result["in_stem"] = locations["in_stem"]
            result["in_branch"] = locations["in_branch"]
            result["in_hidden"] = locations["in_hidden"]
            result["status"] = self._useful_status_phrase(locations)
        elif score_value > 0:
            result["status"] = "PRESENT"
        elif result["status"] is None:
            result["status"] = None

        return result

    def _build_temperature(self, temperature: Any) -> dict[str, Any]:
        """
        Temperature namespace for Knowledge Base.

        No Temperature engine in platform → leave numeric/profile fields None
        unless an upstream payload is supplied.
        """
        stubs = {
            "status": None,
            "result": None,
            "index": None,
            "profile": None,
            "humidity": None,
            "humidity_index": None,
            "climate_pattern": None,
            "severity": None,
            "cold_score": None,
            "hot_score": None,
            "damp_score": None,
            "dry_score": None,
            "cold_min": None,
            "cold_max": None,
            "hot_min": None,
            "hot_max": None,
            "adjustment_mode": None,
            "priority_group": None,
        }
        if temperature is None:
            return stubs
        if isinstance(temperature, dict):
            data = dict(stubs)
            data.update(temperature)
            data.setdefault("status", data.get("result"))
            return data
        data = dict(stubs)
        for key in stubs:
            value = getattr(temperature, key, None)
            if value is not None:
                data[key] = value
        return data

    def _build_facts(self, context: Mapping[str, Any]) -> dict[str, bool]:
        """
        Boolean facts for Priority + Score Adapter.

        WP3: map Knowledge Base fact keys from existing RuleContext signals only.
        Pipeline/meta facts stay False. Temperature/combination geometry stay
        False/None until upstream engines provide data.
        """
        pattern = context.get("pattern") or {}
        strength = context.get("strength") or {}
        bazi = context.get("bazi") or {}
        calendar = context.get("calendar") or {}
        wuxing = context.get("wuxing") or {}
        useful = context.get("useful_god") or {}
        ten_gods = context.get("ten_gods") or {}
        temperature = context.get("temperature") or {}
        shensha = context.get("shensha") or {}
        luck = context.get("luck") or {}
        score = context.get("score") or {}

        level = strength.get("level")
        score_value = float(strength.get("score") or 0.0)
        pattern_ok = pattern.get("status") == "SUCCESS"
        pattern_name = str(pattern.get("name") or pattern.get("main_pattern") or "")
        pattern_key = pattern_name.lower().replace(" ", "_")
        unique = set(ten_gods.get("unique") or [])
        unique |= set(ten_gods.get("month_hidden_ten_gods") or [])

        has_useful = bool(useful.get("name")) and useful.get("status") not in {
            None,
            "MISSING",
            "Không có Dụng thần",
        }

        facts: dict[str, bool] = {
            # Core
            "pattern_identified": bool(pattern.get("main_pattern")),
            "pattern_confirmed": bool(pattern.get("main_pattern")),
            "pattern_da_xac_dinh": bool(pattern.get("main_pattern")),
            "pattern_success": pattern_ok,
            "pattern_missing": not bool(pattern.get("main_pattern")),
            "has_day_master": bool(bazi.get("day_master")),
            "day_master_strength_calculated": level not in {None, "unknown"},
            "than_vuong_nhuoc_da_xac_dinh": level not in {None, "unknown"},
            "than_score_da_tinh": level not in {None, "unknown"} or score_value > 0,
            "temperature_profile_calculated": temperature.get("status") is not None
            or temperature.get("result") is not None,
            "combination_rule_valid": False,
            "combination_confirmed": False,
        }

        # Strength level maps (no new calc)
        facts["strong_day_master"] = level == "strong"
        facts["strength_vuong"] = level == "strong"
        facts["weak_day_master"] = level == "weak"
        facts["strength_nhuoc"] = level == "weak"
        facts["balanced_day_master"] = level == "balanced"
        facts["strength_balanced"] = level == "balanced"
        facts["day_master_extremely_strong"] = score_value >= 80
        facts["day_master_extremely_weak"] = 0 < score_value <= 20
        facts["extremely_strong_day_master"] = facts["day_master_extremely_strong"]
        facts["extremely_weak_day_master"] = facts["day_master_extremely_weak"]

        # Wuxing presence
        for element in ELEMENTS:
            status = ((wuxing.get(element) or {}).get("status"))
            facts[f"wuxing_{element}_present"] = status in {
                "PRESENT",
                "STRONG",
                "EXCESS",
            }

        # Calendar / season availability
        facts["solar_term_available"] = bool(calendar.get("solar_term"))
        facts["month_branch_available"] = bool(bazi.get("month_branch"))
        facts["lunar_month_available"] = bool(calendar.get("lunar"))
        facts["season_confirmed"] = bool(wuxing.get("season"))
        facts["season_resolved"] = bool(wuxing.get("season"))
        facts["season_support_available"] = bool(wuxing.get("season"))
        facts["pattern_in_season"] = pattern_ok and wuxing.get("season_status") == "IN_SEASON"
        facts["pattern_out_of_season"] = pattern_ok and not facts["pattern_in_season"]
        facts["season_support_pattern"] = facts["pattern_in_season"]
        facts["season_pattern_support"] = facts["pattern_in_season"]

        # Ten-god presence (from derived chart gods)
        facts["quan_tinh_ton_tai"] = "Chính Quan" in unique
        facts["that_sat_ton_tai"] = "Thất Sát" in unique
        facts["tai_tinh_ton_tai"] = bool({"Chính Tài", "Thiên Tài"} & unique)
        facts["an_tinh_ton_tai"] = bool({"Chính Ấn", "Thiên Ấn"} & unique)
        facts["ty_kiep_ton_tai"] = bool({"Tỷ Kiên", "Kiếp Tài"} & unique)
        facts["thuong_quan_ton_tai"] = "Thương Quan" in unique
        facts["xuat_tinh_ton_tai"] = bool({"Thực Thần", "Thương Quan"} & unique)
        facts["that_sat_manh"] = False
        facts["quan_tinh_on_dinh"] = facts["quan_tinh_ton_tai"] and pattern_ok
        facts["xuat_tinh_manh"] = False
        facts["an_tinh_manh"] = False
        facts["ty_kiep_manh"] = False

        # Pattern name → knowledge facts
        facts["standard_pattern"] = pattern_ok
        facts["special_pattern"] = False
        facts["secondary_pattern_detected"] = False
        facts["multiple_patterns"] = False
        facts["pattern_candidate"] = bool(pattern.get("main_pattern"))
        facts["pattern_hop_le"] = pattern_ok
        facts["kha_nang_thanh_cach_da_xac_dinh"] = pattern_ok

        pattern_fact_map = {
            "chinh_quan": "pattern_la_chinh_quan_cach",
            "that_sat": "pattern_la_that_sat_cach",
            "chinh_tai": "pattern_la_tai_cach",
            "thien_tai": "pattern_la_tai_cach",
            "thuc_than": "pattern_la_thuc_than_cach",
            "thuong_quan": "pattern_la_thuong_quan_cach",
            "chinh_an": "pattern_la_an_cach",
            "thien_an": "pattern_la_thien_an_cach",
            "ty_kien": "pattern_la_ty_kiep_cach",
            "kiep_tai": "pattern_la_ty_kiep_cach",
        }
        for key, fact_name in pattern_fact_map.items():
            facts[fact_name] = pattern_key == key

        facts["pattern_la_xuat_tinh_cach"] = pattern_key in {
            "thuc_than",
            "thuong_quan",
        }
        facts["quan_tinh_thanh_cach"] = pattern_ok and pattern_key == "chinh_quan"
        facts["that_sat_thanh_cach"] = pattern_ok and pattern_key == "that_sat"
        facts["tai_tinh_thanh_cach"] = pattern_ok and pattern_key in {
            "chinh_tai",
            "thien_tai",
        }
        facts["xuat_tinh_thanh_cach"] = pattern_ok and facts["pattern_la_xuat_tinh_cach"]
        facts["an_tinh_thanh_cach"] = pattern_ok and pattern_key in {
            "chinh_an",
            "thien_an",
        }
        facts["ty_kiep_thanh_cach"] = pattern_ok and pattern_key in {
            "ty_kien",
            "kiep_tai",
        }

        # Useful god maps
        facts["useful_god_found"] = bool(useful.get("name"))
        facts["dung_than_da_xac_dinh"] = bool(useful.get("name"))
        facts["useful_god_active"] = has_useful
        facts["hy_than_da_xac_dinh"] = bool(useful.get("favorable"))
        facts["ky_than_da_xac_dinh"] = bool(useful.get("unfavorable"))
        facts["harmful_god_present"] = bool(useful.get("unfavorable"))
        facts["useful_god_blocked"] = useful.get("status") in {
            "MISSING",
            "Không có Dụng thần",
        }
        facts["useful_god_supported"] = bool(
            useful.get("in_stem") or useful.get("in_branch") or useful.get("in_hidden")
        )
        facts["useful_god_controlled"] = False

        # Shensha / luck analysis flags (presence of analysis, not quality)
        facts["than_sat_da_phan_tich"] = shensha.get("status") in {
            "PRESENT",
            "MISSING",
        }
        facts["dai_van_da_phan_tich"] = bool(luck.get("available"))
        facts["luu_nien_da_phan_tich"] = bool(
            luck.get("annual") or luck.get("yearly") or luck.get("luu_nien")
        )

        # Score quality tokens for Adapter BOOLEAN_FACT_KEY
        facts["HỢP_CÁCH"] = pattern_ok
        facts["HỮU_DỤNG"] = bool(
            has_useful or (pattern_ok and ten_gods.get("status") == "PRESENT")
        )
        facts["HỮU_CHẾ"] = bool(pattern.get("has_control")) and (
            "Thất Sát" in unique
        )
        for token in (
            "VÔ_DỤNG",
            "VÔ_CHẾ",
            "QUÁ_NHIỀU",
            "PHÁ_TÀI",
            "PHÙ_PHIẾM",
            "BỊ_PHÁ",
            "KIẾN_QUAN",
            "TRANH_TÀI",
            "ĐOẠT_THỰC",
            "ĐOẠT_TÀI",
        ):
            facts.setdefault(token, False)

        # Pattern score bands (from pattern.score when available)
        pattern_score = float(pattern.get("score") or 0.0)
        total_score = float(score.get("total_score") or 0.0)
        facts["pattern_high_score"] = pattern_score >= 70 or total_score >= 70
        facts["pattern_low_score"] = 0 < pattern_score <= 30 or (
            0 < total_score <= 30
        )
        facts["strength_pattern_support"] = pattern_ok and level in {
            "strong",
            "balanced",
        }
        facts["strength_pattern_conflict"] = pattern_ok and level == "weak"

        # Follow / tong / combination / temperature geometry — upstream required
        for key in (
            "tong_vuong_confirmed",
            "tong_nhuoc_confirmed",
            "tong_tai_confirmed",
            "tong_sat_confirmed",
            "hoa_khi_confirmed",
            "follow_output_element",
            "follow_resource_element",
            "follow_dominant_element",
            "unable_to_self_support",
            "wealth_element_dominant",
            "day_master_cannot_resist",
            "wealth_structure_complete",
            "officer_killing_dominant",
            "cannot_counter_killing",
            "heavenly_stem_transform",
            "earthly_branch_support",
            "season_support_transform",
            "heavenly_stem_combination_found",
            "earthly_branch_six_combination_found",
            "three_harmony_found",
            "three_meeting_found",
            "meeting_rule_valid",
            "half_combination_found",
            "half_meeting_found",
            "earthly_branch_clash_found",
            "heavenly_stem_clash_found",
            "harm_relation_found",
            "punishment_relation_found",
            "destruction_relation_found",
            "temperature_balanced",
            "temperature_excess_cold",
            "temperature_excess_hot",
            "chart_cold",
            "chart_hot",
            "special_pattern_da_xac_nhan",
            "special_pattern_hop_le",
            "pattern_la_tong_cach",
            "pattern_la_tong_vuong",
            "pattern_la_tong_nhuoc",
            "pattern_la_hoa_khi",
            "pattern_la_special_pattern",
            "tong_cach_thuan",
            "tong_cach_on_dinh",
            # Pipeline meta — stay False
            "no_priority_rule_matched",
            "conflicting_priority_rules",
            "manual_review_required",
            "unsupported_case",
            "interpretation_ready",
            "report_ready",
            "du_lieu_hop_le",
            "co_rule_xung_dot",
            "khong_tim_thay_rule_phu_hop",
            "khong_the_ket_luan",
            "xu_ly_hoan_tat",
            "ket_qua_da_tong_hop",
            "tong_hop_hoan_tat",
        ):
            facts.setdefault(key, False)

        return facts

    # =========================================================
    # WP2D mapping helpers (chart data → signals, no new engines)
    # =========================================================

    def _month_hidden_ten_gods(self, bazi_section: Mapping[str, Any]) -> list[str]:
        """Ten gods of month-branch hidden stems relative to day master."""
        day_master = bazi_section.get("day_master")
        month_branch = bazi_section.get("month_branch")
        if not day_master or not month_branch:
            return []
        gods: list[str] = []
        for stem in maps.BRANCH_HIDDEN.get(month_branch, []):
            god = self._ten_god_between(day_master, stem)
            if god:
                gods.append(god)
        return list(dict.fromkeys(gods))

    def _derive_ten_god_items(self, bazi_section: Mapping[str, Any]) -> list[str]:
        day_master = bazi_section.get("day_master")
        if not day_master or day_master not in maps.STEM_META:
            return []

        items: list[str] = []
        for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"):
            pillar = bazi_section.get(key) or {}
            stem = pillar.get("stem")
            if not stem:
                continue
            # Day pillar stem vs day master is always Friend for the day itself
            if key == "day_pillar":
                items.append("Nhật Chủ")
                continue
            god = self._ten_god_between(day_master, stem)
            if god:
                items.append(god)
        return items

    def _ten_god_between(self, day_master: str, other_stem: str) -> str | None:
        if day_master not in maps.STEM_META or other_stem not in maps.STEM_META:
            return None
        dm_el, dm_yang = maps.STEM_META[day_master]
        other_el, other_yang = maps.STEM_META[other_stem]

        if other_el == dm_el:
            role = "same"
        elif other_el == maps.GENERATES[dm_el]:
            role = "output"
        elif dm_el == maps.GENERATES[other_el]:
            role = "resource"
        elif other_el == maps.CONTROLS[dm_el]:
            role = "wealth"
        elif dm_el == maps.CONTROLS[other_el]:
            role = "officer"
        else:
            return None

        yang_name, yin_name = maps.TEN_GOD_MATRIX[dm_el][role]
        # Same polarity as day master → first name; opposite → second
        if dm_yang == other_yang:
            return yang_name
        return yin_name

    def _map_root_support_control(
        self,
        bazi_section: Mapping[str, Any],
        hidden_stems: Mapping[str, Any],
    ) -> tuple[str | None, str | None, str | None]:
        day_master = bazi_section.get("day_master")
        if not day_master or day_master not in maps.STEM_META:
            return None, None, None

        dm_el, _ = maps.STEM_META[day_master]
        root_branches = 0
        for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"):
            branch = (bazi_section.get(key) or {}).get("branch")
            hidden = maps.BRANCH_HIDDEN.get(branch or "", [])
            if any(
                maps.STEM_META.get(stem, (None, None))[0] == dm_el for stem in hidden
            ):
                root_branches += 1

        root_level: str | None = "Vô căn"
        if root_branches == 0:
            flat = hidden_stems.get("flat") or []
            if any(maps.STEM_META.get(stem, (None, None))[0] == dm_el for stem in flat):
                root_level = "Thông căn tàng can"
            else:
                root_level = "Vô căn"
        else:
            for threshold, label in maps.ROOT_LEVEL_LABELS:
                if root_branches >= threshold:
                    root_level = label
                    break

        support_type: str | None = None
        control_type: str | None = None
        for key in ("year_pillar", "month_pillar", "hour_pillar"):
            stem = (bazi_section.get(key) or {}).get("stem")
            if not stem or stem not in maps.STEM_META:
                continue
            god = self._ten_god_between(day_master, stem)
            if god in {"Tỷ Kiên", "Kiếp Tài"} and support_type is None:
                support_type = maps.SUPPORT_LABELS["same"]
            elif god in {"Chính Ấn", "Thiên Ấn"} and support_type is None:
                support_type = maps.SUPPORT_LABELS["resource"]
            elif god in {"Chính Quan", "Thất Sát"} and control_type is None:
                control_type = maps.CONTROL_LABELS["officer"]
            elif god in {"Thực Thần", "Thương Quan"} and control_type is None:
                control_type = maps.CONTROL_LABELS["output"]
            elif god in {"Chính Tài", "Thiên Tài"} and control_type is None:
                control_type = maps.CONTROL_LABELS["wealth"]

        if support_type is None:
            # Stem/branch presence of same element
            for key in ("year_pillar", "month_pillar", "hour_pillar"):
                stem = (bazi_section.get(key) or {}).get("stem")
                if stem and maps.STEM_META.get(stem, (None, None))[0] == dm_el:
                    support_type = maps.SUPPORT_LABELS["stem"]
                    break

        return root_level, support_type, control_type

    def _detect_shensha_stars(self, bazi_section: Mapping[str, Any]) -> list[str]:
        day_master = bazi_section.get("day_master")
        branches = [
            (bazi_section.get(key) or {}).get("branch")
            for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar")
        ]
        branches = [b for b in branches if b]
        year_branch = (bazi_section.get("year_pillar") or {}).get("branch")
        stars: list[str] = []

        if day_master in maps.TIAN_YI_BRANCHES:
            targets = maps.TIAN_YI_BRANCHES[day_master]
            if any(branch in targets for branch in branches):
                stars.append("Thiên Ất Quý Nhân")
                stars.append("Thiên Ất")

        if day_master in maps.WEN_CHANG_BRANCH:
            if maps.WEN_CHANG_BRANCH[day_master] in branches:
                stars.append("Văn Xương")

        if day_master in maps.LU_SHEN_BRANCH:
            if maps.LU_SHEN_BRANCH[day_master] in branches:
                stars.append("Lộc Thần")

        if year_branch and year_branch in maps.HONG_LUAN_OPPOSITE:
            target = maps.HONG_LUAN_OPPOSITE[year_branch]
            if target in branches:
                stars.append("Hồng Loan")
                # Thiên Hỷ is opposite of Hồng Loan in many schools
                stars.append("Thiên Hỷ")

        day_branch = (bazi_section.get("day_pillar") or {}).get("branch")
        if day_branch in maps.HUA_GAI_BRANCHES:
            stars.append("Hoa Cái")

        if day_master in maps.YANG_REN_BRANCH:
            if maps.YANG_REN_BRANCH[day_master] in branches:
                stars.append("Dương Nhẫn")

        month_branch = bazi_section.get("month_branch")
        stems = [
            (bazi_section.get(key) or {}).get("stem")
            for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar")
        ]
        if month_branch in maps.TIAN_DE_BRANCH:
            token = maps.TIAN_DE_BRANCH[month_branch]
            if token in stems or token in branches:
                stars.append("Thiên Đức")
                stars.append("Thiên Đức Quý Nhân")
        if month_branch in maps.YUE_DE_STEM:
            token = maps.YUE_DE_STEM[month_branch]
            if token in stems:
                stars.append("Nguyệt Đức")
                stars.append("Nguyệt Đức Quý Nhân")

        # Deduplicate preserving order
        return list(dict.fromkeys(stars))

    def _locate_ten_god(
        self,
        god_name: str,
        bazi_section: Mapping[str, Any],
        hidden_stems: Mapping[str, Any],
        ten_gods: Mapping[str, Any],
    ) -> dict[str, bool]:
        day_master = bazi_section.get("day_master")
        in_stem = False
        in_branch = False
        in_hidden = False

        for key in ("year_pillar", "month_pillar", "hour_pillar"):
            stem = (bazi_section.get(key) or {}).get("stem")
            if stem and day_master and self._ten_god_between(day_master, stem) == god_name:
                in_stem = True

        for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"):
            branch = (bazi_section.get(key) or {}).get("branch")
            for hidden in maps.BRANCH_HIDDEN.get(branch or "", []):
                if day_master and self._ten_god_between(day_master, hidden) == god_name:
                    in_hidden = True
                    # Main hidden stem often treated as branch presence
                    mains = maps.BRANCH_HIDDEN.get(branch or "", [])[:1]
                    if mains == [hidden]:
                        in_branch = True

        # Also trust derived ten_gods list presence
        if god_name in (ten_gods.get("unique") or []):
            in_stem = True

        # Month branch main qi as branch presence
        month_branch = bazi_section.get("month_branch")
        main_hidden = (maps.BRANCH_HIDDEN.get(month_branch or "", []) or [None])[0]
        if (
            main_hidden
            and day_master
            and self._ten_god_between(day_master, main_hidden) == god_name
        ):
            in_branch = True

        return {
            "in_stem": in_stem,
            "in_branch": in_branch,
            "in_hidden": in_hidden,
        }

    @staticmethod
    def _useful_status_phrase(locations: Mapping[str, bool]) -> str | None:
        in_stem = bool(locations.get("in_stem"))
        in_branch = bool(locations.get("in_branch"))
        in_hidden = bool(locations.get("in_hidden"))
        if in_stem and in_branch:
            return "Dụng thần đầy đủ Can Chi"
        if in_stem and in_hidden:
            return "Hai Dụng thần đồng thời"
        if in_stem:
            return "Dụng thần xuất hiện Thiên Can"
        if in_branch:
            return "Dụng thần xuất hiện Địa Chi"
        if in_hidden:
            return "Dụng thần trong Tàng Can"
        return "Không có Dụng thần"

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
