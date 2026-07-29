"""
Liuyue runtime validation against LIUYUE_SPEC.md (written sections).

Applies structural contracts from §§8–16 and Dayun/Liunian readiness (§§5–6).
Does not invent combination / clash / seasonal-strength tables
(SPEC §§21–36 incomplete; Rule Database required).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.rule_contract.signal_maps import BRANCH_HIDDEN

from .providers._common import MONTH_YIN_START_STEM, STEMS, month_stem_for

BRANCHES: frozenset[str] = frozenset(GanzhiAlgorithm.BRANCH)

# LIUYUE_SPEC §11 — Solar Month sequence (month_index 1 = Dần … 12 = Sửu).
MONTH_SEQUENCE: tuple[str, ...] = (
    "Dần",
    "Mão",
    "Thìn",
    "Tỵ",
    "Ngọ",
    "Mùi",
    "Thân",
    "Dậu",
    "Tuất",
    "Hợi",
    "Tý",
    "Sửu",
)

# Major solar terms that open each solar month (aligned with SolarTermEngine).
MONTH_START_TERMS: tuple[str, ...] = (
    "Lập Xuân",
    "Kinh Trập",
    "Thanh Minh",
    "Lập Hạ",
    "Mang Chủng",
    "Tiểu Thử",
    "Lập Thu",
    "Bạch Lộ",
    "Hàn Lộ",
    "Lập Đông",
    "Đại Tuyết",
    "Tiểu Hàn",
)


@dataclass(frozen=True, slots=True)
class LiuyueValidationResult:
    """Immutable validation outcome for one LiuyueRuntime."""

    ok: bool
    passed: tuple[str, ...]
    failed: tuple[str, ...]
    reasons: tuple[str, ...]
    confidence: float | None

    def to_dict(self) -> dict[str, Any]:
        """Serialize for evaluator metadata / structured summary."""
        return {
            "ok": self.ok,
            "passed": list(self.passed),
            "failed": list(self.failed),
            "reasons": list(self.reasons),
            "confidence": self.confidence,
            "spec": "LIUYUE_SPEC.md",
            "sections": [
                "8_output_structure",
                "9_monthly_determination_solar_terms",
                "11_monthly_sequence",
                "12_five_tiger_dunjia",
                "14_hidden_stems",
                "15_ten_gods",
                "16_five_element_mapping",
                "5_6_dayun_liunian_readiness",
            ],
            "pending_spec_sections": [
                "21_liunian_interaction",
                "26_seasonal_strength",
                "32_validation_rules",
            ],
        }


def _attr(obj: Any, name: str, default: Any = None) -> Any:
    """Read attribute or mapping key."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def validate_liuyue_runtime(
    liuyue: Any | None,
    *,
    dayun: Any | None = None,
    liunian: Any | None = None,
) -> LiuyueValidationResult:
    """
    Validate current Liuyue (+ Dayun/Liunian readiness) per written LIUYUE_SPEC.

    Fail-soft: never raises for rule failures.
    """
    if liuyue is None:
        return LiuyueValidationResult(
            ok=False,
            passed=(),
            failed=("liuyue_present",),
            reasons=("liuyue_runtime_missing",),
            confidence=None,
        )

    passed: list[str] = ["liuyue_present"]
    failed: list[str] = []
    reasons: list[str] = []

    year = _attr(liuyue, "year")
    month_index = _attr(liuyue, "month_index")
    stem = _attr(liuyue, "heavenly_stem")
    branch = _attr(liuyue, "earthly_branch")
    ganzhi = _attr(liuyue, "ganzhi")
    solar_term = _attr(liuyue, "solar_term")
    element = _attr(liuyue, "element")
    yin_yang = _attr(liuyue, "yin_yang")
    ten_god = _attr(liuyue, "ten_god")
    hidden = _attr(liuyue, "hidden_stems") or ()

    try:
        year_ok = year is not None and int(year) > 0
    except (TypeError, ValueError):
        year_ok = False
    if year_ok:
        passed.append("year_valid")
    else:
        failed.append("year_valid")
        reasons.append("liuyue_invalid_year")

    try:
        idx = int(month_index)
        index_ok = 1 <= idx <= 12
    except (TypeError, ValueError):
        idx = -1
        index_ok = False
    if index_ok:
        passed.append("month_index_valid")
    else:
        failed.append("month_index_valid")
        reasons.append("liuyue_invalid_month_index")

    # §11 Monthly sequence branch
    if index_ok and branch == MONTH_SEQUENCE[idx - 1]:
        passed.append("month_branch_sequence")
    else:
        failed.append("month_branch_sequence")
        reasons.append("liuyue_branch_not_in_solar_month_sequence")

    # §9–10 Solar term boundary (major term name present + matches index)
    if solar_term:
        passed.append("solar_term_present")
        if index_ok and solar_term == MONTH_START_TERMS[idx - 1]:
            passed.append("solar_term_matches_month")
        else:
            failed.append("solar_term_matches_month")
            reasons.append("liuyue_solar_term_mismatch_for_month_index")
    else:
        failed.append("solar_term_present")
        failed.append("solar_term_matches_month")
        reasons.append("liuyue_solar_term_missing")

    if stem in STEMS:
        passed.append("stem_valid")
    else:
        failed.append("stem_valid")
        reasons.append("liuyue_invalid_stem")

    if branch in BRANCHES:
        passed.append("branch_valid")
    else:
        failed.append("branch_valid")
        reasons.append("liuyue_invalid_branch")

    # Ganzhi consistency
    if stem and branch:
        compact = str(ganzhi or "").replace(" ", "")
        if compact in {f"{stem}{branch}", f"{stem} {branch}".replace(" ", "")}:
            passed.append("ganzhi_consistent")
        else:
            failed.append("ganzhi_consistent")
            reasons.append("liuyue_ganzhi_mismatch")
    else:
        failed.append("ganzhi_consistent")
        reasons.append("liuyue_ganzhi_missing")

    # §12 Five Tiger Dunjia — stem must match annual stem + month_index
    year_stem = _attr(liunian, "heavenly_stem") if liunian is not None else None
    if year_stem in MONTH_YIN_START_STEM and index_ok and stem in STEMS:
        expected_stem = month_stem_for(str(year_stem), idx)
        if stem == expected_stem:
            passed.append("five_tiger_dunjia")
        else:
            failed.append("five_tiger_dunjia")
            reasons.append("liuyue_stem_not_matching_five_tiger_dunjia")
    elif liunian is None:
        failed.append("five_tiger_dunjia")
        reasons.append("liuyue_liunian_required_for_stem_check")
    else:
        failed.append("five_tiger_dunjia")
        reasons.append("liuyue_cannot_verify_five_tiger_dunjia")

    # §14 Hidden stems
    expected_hidden = BRANCH_HIDDEN.get(str(branch), []) if branch else []
    hidden_list = list(hidden) if hidden is not None else []
    if expected_hidden and tuple(hidden_list) == tuple(expected_hidden):
        passed.append("hidden_stems_match_database")
    else:
        failed.append("hidden_stems_match_database")
        reasons.append("liuyue_hidden_stems_mismatch")

    # §15 Ten Gods
    if ten_god:
        passed.append("ten_god_present")
    else:
        failed.append("ten_god_present")
        reasons.append("liuyue_ten_god_missing")

    # §16 Five element mapping
    if element:
        passed.append("element_present")
    else:
        failed.append("element_present")
        reasons.append("liuyue_element_missing")

    if yin_yang:
        passed.append("yin_yang_present")
    else:
        failed.append("yin_yang_present")
        reasons.append("liuyue_yin_yang_missing")

    # §§5–6 Dayun / Liunian readiness
    if liunian is not None and _attr(liunian, "heavenly_stem") in STEMS:
        passed.append("liunian_context_ready")
    else:
        failed.append("liunian_context_ready")
        reasons.append("liuyue_liunian_context_missing")

    if dayun is not None and _attr(dayun, "heavenly_stem") in STEMS:
        passed.append("dayun_context_ready")
    else:
        failed.append("dayun_context_ready")
        reasons.append("liuyue_dayun_context_missing")

    passed.append("interaction_tables_deferred_to_rule_database")

    scored_passed = [
        p for p in passed if p != "interaction_tables_deferred_to_rule_database"
    ]
    scored_total = len(scored_passed) + len(failed)
    confidence = (len(scored_passed) / scored_total) if scored_total else None
    ok = len(failed) == 0
    if ok and not reasons:
        reasons = ("liuyue_validation_passed",)

    return LiuyueValidationResult(
        ok=ok,
        passed=tuple(passed),
        failed=tuple(failed),
        reasons=tuple(reasons),
        confidence=confidence,
    )


def liuyue_runtime_snapshot(liuyue: Any | None) -> dict[str, Any] | None:
    """
    Machine-readable LiuyueRuntime fields per LIUYUE_SPEC §§7–8.

    No interpretation — copies provider runtime only.
    """
    if liuyue is None:
        return None
    to_dict = getattr(liuyue, "to_dict", None)
    if callable(to_dict):
        payload = to_dict()
    elif isinstance(liuyue, dict):
        payload = dict(liuyue)
    else:
        payload = {
            "year": _attr(liuyue, "year"),
            "month": _attr(liuyue, "month"),
            "month_index": _attr(liuyue, "month_index"),
            "ganzhi": _attr(liuyue, "ganzhi"),
            "heavenly_stem": _attr(liuyue, "heavenly_stem"),
            "earthly_branch": _attr(liuyue, "earthly_branch"),
            "solar_term": _attr(liuyue, "solar_term"),
            "element": _attr(liuyue, "element"),
            "yin_yang": _attr(liuyue, "yin_yang"),
            "ten_god": _attr(liuyue, "ten_god"),
            "hidden_stems": list(_attr(liuyue, "hidden_stems") or ()),
            "metadata": dict(_attr(liuyue, "metadata") or {}),
        }
    metadata = dict(payload.get("metadata") or {})
    metadata.pop("year_months", None)
    return {
        "monthly_pillar": {
            "year": payload.get("year"),
            "month": payload.get("month"),
            "month_index": payload.get("month_index"),
            "ganzhi": payload.get("ganzhi"),
            "heavenly_stem": payload.get("heavenly_stem"),
            "earthly_branch": payload.get("earthly_branch"),
            "solar_term": payload.get("solar_term"),
        },
        "hidden_stems": payload.get("hidden_stems") or [],
        "ten_gods": {"monthly_stem": payload.get("ten_god")},
        "five_elements": {
            "stem_element": payload.get("element"),
            "yin_yang": payload.get("yin_yang"),
        },
        "seasonal_influence": {
            "status": "UNKNOWN",
            "solar_term": payload.get("solar_term"),
            "reason": "liuyue_spec_section_17_26_incomplete_without_season_rules",
        },
        "interactions": {
            "stem_relations": [],
            "branch_relations": [],
            "hidden_stem_relations": [],
            "liunian_relations": [],
            "dayun_relations": [],
            "status": "UNKNOWN",
            "reason": "liuyue_spec_interaction_tables_require_rule_database",
        },
        "runtime_metadata": {
            k: metadata.get(k)
            for k in ("kind", "civil_year", "civil_month", "sprint")
            if k in metadata
        },
    }
