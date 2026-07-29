"""
Liushi runtime validation against LIUSHI_SPEC.md.

Structural contracts: §§8–17. Mandatory input readiness: §34.
Interaction / Useful-God / Risk scoring deferred — Rule Database required;
no undocumented BaZi logic invented.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.rule_contract.signal_maps import BRANCH_HIDDEN

from .providers._common import STEMS, hour_pillar_for

BRANCHES: frozenset[str] = frozenset(GanzhiAlgorithm.BRANCH)


@dataclass(frozen=True, slots=True)
class LiushiValidationResult:
    """Immutable validation outcome for one LiushiRuntime (LIUSHI_SPEC §34)."""

    ok: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    passed: tuple[str, ...]
    failed: tuple[str, ...]
    reasons: tuple[str, ...]
    confidence: float | None

    def to_dict(self) -> dict[str, Any]:
        """Serialize for evaluator metadata / structured summary."""
        return {
            "ok": self.ok,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "passed": list(self.passed),
            "failed": list(self.failed),
            "reasons": list(self.reasons),
            "confidence": self.confidence,
            "spec": "LIUSHI_SPEC.md",
            "sections": [
                "8_output_structure",
                "9_12_hourly_pillar_calendar",
                "13_hidden_stems",
                "14_ten_gods",
                "15_five_element_mapping",
                "16_seasonal_context_inherited",
                "17_daily_context_inherited",
                "34_validation_rules",
            ],
            "pending_spec_sections": [
                "18_28_interactions_transformation",
                "29_30_useful_unfavorable_god",
                "31_risk_flags",
                "32_priority",
            ],
        }


def _attr(obj: Any, name: str, default: Any = None) -> Any:
    """Read attribute or mapping key."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def validate_liushi_runtime(
    liushi: Any | None,
    *,
    dayun: Any | None = None,
    liunian: Any | None = None,
    liuyue: Any | None = None,
    liuri: Any | None = None,
) -> LiushiValidationResult:
    """
    Validate current Liushi (+ upstream readiness) per LIUSHI_SPEC.

    Fail-soft: never raises for rule failures.
    """
    errors: list[str] = []
    warnings: list[str] = []
    passed: list[str] = []
    failed: list[str] = []
    reasons: list[str] = []

    if liushi is None:
        return LiushiValidationResult(
            ok=False,
            errors=("liushi_calendar_engine_output_missing",),
            warnings=(),
            passed=(),
            failed=("liushi_present",),
            reasons=("liushi_runtime_missing",),
            confidence=None,
        )

    passed.append("liushi_present")

    year = _attr(liushi, "year")
    month = _attr(liushi, "month")
    day = _attr(liushi, "day")
    hour = _attr(liushi, "hour")
    minute = _attr(liushi, "minute")
    stem = _attr(liushi, "heavenly_stem")
    branch = _attr(liushi, "earthly_branch")
    ganzhi = _attr(liushi, "ganzhi")
    element = _attr(liushi, "element")
    yin_yang = _attr(liushi, "yin_yang")
    ten_god = _attr(liushi, "ten_god")
    hidden = _attr(liushi, "hidden_stems") or ()
    metadata = _attr(liushi, "metadata") or {}

    # §§9–12 Hourly pillar from calendar conversion
    try:
        datetime_ok = (
            year is not None
            and month is not None
            and day is not None
            and hour is not None
            and int(year) > 0
            and 1 <= int(month) <= 12
            and 1 <= int(day) <= 31
            and 0 <= int(hour) <= 23
        )
    except (TypeError, ValueError):
        datetime_ok = False
    if datetime_ok:
        passed.append("calendar_datetime_fields")
    else:
        failed.append("calendar_datetime_fields")
        errors.append("liushi_calendar_engine_output_incomplete")
        reasons.append("liushi_invalid_gregorian_datetime")

    try:
        minute_ok = minute is None or 0 <= int(minute) <= 59
    except (TypeError, ValueError):
        minute_ok = False
    if minute_ok:
        passed.append("minute_field_valid")
    else:
        failed.append("minute_field_valid")
        warnings.append("liushi_minute_out_of_range")
        reasons.append("liushi_invalid_minute")

    if stem in STEMS:
        passed.append("stem_valid")
    else:
        failed.append("stem_valid")
        errors.append("liushi_invalid_hourly_stem")
        reasons.append("liushi_invalid_stem")

    if branch in BRANCHES:
        passed.append("branch_valid")
    else:
        failed.append("branch_valid")
        errors.append("liushi_invalid_hourly_branch")
        reasons.append("liushi_invalid_branch")

    if stem and branch:
        compact = str(ganzhi or "").replace(" ", "")
        if compact in {f"{stem}{branch}", f"{stem} {branch}".replace(" ", "")}:
            passed.append("ganzhi_consistent")
        else:
            failed.append("ganzhi_consistent")
            errors.append("liushi_ganzhi_mismatch")
            reasons.append("liushi_ganzhi_mismatch")
    else:
        failed.append("ganzhi_consistent")
        errors.append("liushi_ganzhi_missing")
        reasons.append("liushi_ganzhi_missing")

    # §10 Five Rat Escape (五鼠遁) consistency vs day stem + hour
    day_stem = None
    if hasattr(metadata, "get"):
        day_stem = metadata.get("day_stem")
    if day_stem is None and liuri is not None:
        day_stem = _attr(liuri, "heavenly_stem")
    if day_stem in STEMS and datetime_ok and stem in STEMS and branch in BRANCHES:
        expected_stem, expected_branch = hour_pillar_for(str(day_stem), int(hour))
        if stem == expected_stem and branch == expected_branch:
            passed.append("five_rat_escape_consistent")
        else:
            failed.append("five_rat_escape_consistent")
            errors.append("liushi_five_rat_escape_mismatch")
            reasons.append("liushi_stem_branch_not_matching_ngu_thu_don")
    else:
        failed.append("five_rat_escape_consistent")
        errors.append("liushi_cannot_verify_five_rat_escape")
        reasons.append("liushi_day_stem_or_hour_unavailable_for_ngu_thu_don")

    source = metadata.get("source") if hasattr(metadata, "get") else None
    if source == "ngu_thu_don":
        passed.append("calendar_engine_source")
    else:
        failed.append("calendar_engine_source")
        warnings.append("liushi_calendar_source_metadata_unexpected")
        reasons.append("liushi_calendar_source_not_documented")

    # §13 Hidden stems
    expected_hidden = BRANCH_HIDDEN.get(str(branch), []) if branch else []
    hidden_list = list(hidden) if hidden is not None else []
    if expected_hidden and tuple(hidden_list) == tuple(expected_hidden):
        passed.append("hidden_stems_match_database")
    else:
        failed.append("hidden_stems_match_database")
        errors.append("liushi_hidden_stems_mismatch")
        reasons.append("liushi_hidden_stem_database_mismatch")

    # §14 Ten Gods
    if ten_god:
        passed.append("ten_god_present")
    else:
        failed.append("ten_god_present")
        errors.append("liushi_ten_god_missing")
        reasons.append("liushi_ten_god_missing")

    # §15 Five element mapping
    if element:
        passed.append("element_present")
    else:
        failed.append("element_present")
        errors.append("liushi_element_missing")
        reasons.append("liushi_element_missing")

    if yin_yang:
        passed.append("yin_yang_present")
    else:
        failed.append("yin_yang_present")
        errors.append("liushi_yin_yang_missing")
        reasons.append("liushi_yin_yang_missing")

    # §34 Mandatory upstream contexts
    if dayun is not None and _attr(dayun, "heavenly_stem") in STEMS:
        passed.append("dayun_context_ready")
    else:
        failed.append("dayun_context_ready")
        errors.append("liushi_dayun_context_missing")
        reasons.append("liushi_dayun_context_missing")

    if liunian is not None and _attr(liunian, "heavenly_stem") in STEMS:
        passed.append("liunian_context_ready")
    else:
        failed.append("liunian_context_ready")
        errors.append("liushi_liunian_context_missing")
        reasons.append("liushi_liunian_context_missing")

    if liuyue is not None and _attr(liuyue, "heavenly_stem") in STEMS:
        passed.append("liuyue_context_ready")
    else:
        failed.append("liuyue_context_ready")
        errors.append("liushi_liuyue_context_missing")
        reasons.append("liushi_liuyue_context_missing")

    if liuri is not None and _attr(liuri, "heavenly_stem") in STEMS:
        passed.append("liuri_context_ready")
    else:
        failed.append("liuri_context_ready")
        errors.append("liushi_liuri_context_missing")
        reasons.append("liushi_liuri_context_missing")

    # §16 Seasonal context inherited (do not recalculate)
    if liuyue is not None and _attr(liuyue, "solar_term"):
        passed.append("seasonal_context_inherited_from_liuyue")
    else:
        failed.append("seasonal_context_inherited_from_liuyue")
        warnings.append("liushi_seasonal_context_unavailable")
        reasons.append("liushi_seasonal_context_not_inherited")

    # §17 Daily context inherited from Liuri
    if liuri is not None and _attr(liuri, "ganzhi"):
        passed.append("daily_context_inherited_from_liuri")
    else:
        failed.append("daily_context_inherited_from_liuri")
        warnings.append("liushi_daily_context_unavailable")
        reasons.append("liushi_daily_context_not_inherited")

    warnings.append("liushi_rule_database_not_available")
    warnings.append("liushi_priority_rules_not_available")
    warnings.append("liushi_interaction_evaluation_deferred")
    warnings.append("liushi_hour_boundary_policy_uses_provider_default")

    scored_total = len(passed) + len(failed)
    confidence = (len(passed) / scored_total) if scored_total else None
    ok = len(errors) == 0
    if ok and not reasons:
        reasons = ("liushi_validation_passed",)

    return LiushiValidationResult(
        ok=ok,
        errors=tuple(errors),
        warnings=tuple(warnings),
        passed=tuple(passed),
        failed=tuple(failed),
        reasons=tuple(reasons),
        confidence=confidence,
    )


def liushi_runtime_snapshot(
    liushi: Any | None,
    *,
    liuyue: Any | None = None,
    liuri: Any | None = None,
) -> dict[str, Any] | None:
    """
    Machine-readable LiushiRuntime fields per LIUSHI_SPEC §§7–8.

    No interpretation — copies provider runtime only.
    """
    if liushi is None:
        return None
    to_dict = getattr(liushi, "to_dict", None)
    if callable(to_dict):
        payload = to_dict()
    elif isinstance(liushi, dict):
        payload = dict(liushi)
    else:
        payload = {
            "year": _attr(liushi, "year"),
            "month": _attr(liushi, "month"),
            "day": _attr(liushi, "day"),
            "hour": _attr(liushi, "hour"),
            "minute": _attr(liushi, "minute"),
            "ganzhi": _attr(liushi, "ganzhi"),
            "heavenly_stem": _attr(liushi, "heavenly_stem"),
            "earthly_branch": _attr(liushi, "earthly_branch"),
            "element": _attr(liushi, "element"),
            "yin_yang": _attr(liushi, "yin_yang"),
            "ten_god": _attr(liushi, "ten_god"),
            "hidden_stems": list(_attr(liushi, "hidden_stems") or ()),
            "metadata": dict(_attr(liushi, "metadata") or {}),
        }
    metadata = dict(payload.get("metadata") or {})
    seasonal_term = _attr(liuyue, "solar_term") if liuyue is not None else None
    daily_ganzhi = _attr(liuri, "ganzhi") if liuri is not None else None
    return {
        "hourly_pillar": {
            "year": payload.get("year"),
            "month": payload.get("month"),
            "day": payload.get("day"),
            "hour": payload.get("hour"),
            "minute": payload.get("minute"),
            "ganzhi": payload.get("ganzhi"),
            "heavenly_stem": payload.get("heavenly_stem"),
            "earthly_branch": payload.get("earthly_branch"),
        },
        "hidden_stems": payload.get("hidden_stems") or [],
        "ten_gods": {"hourly_stem": payload.get("ten_god")},
        "five_elements": {
            "stem_element": payload.get("element"),
            "yin_yang": payload.get("yin_yang"),
        },
        "seasonal_context": {
            "status": "INHERITED" if seasonal_term else "UNKNOWN",
            "source": "liuyue",
            "solar_term": seasonal_term,
            "reason": (
                "liushi_spec_section_16_inherit_from_liuyue"
                if seasonal_term
                else "liushi_seasonal_context_unavailable"
            ),
        },
        "daily_context": {
            "status": "INHERITED" if daily_ganzhi else "UNKNOWN",
            "source": "liuri",
            "ganzhi": daily_ganzhi,
            "reason": (
                "liushi_spec_section_17_inherit_from_liuri"
                if daily_ganzhi
                else "liushi_daily_context_unavailable"
            ),
        },
        "interactions": {
            "stem_relations": [],
            "branch_relations": [],
            "hidden_stem_relations": [],
            "natal_relations": [],
            "dayun_relations": [],
            "liunian_relations": [],
            "liuyue_relations": [],
            "liuri_relations": [],
            "status": "UNKNOWN",
            "reason": "liushi_spec_interaction_tables_require_rule_database",
        },
        "risk_flags": {
            "status": "UNKNOWN",
            "reason": "liushi_spec_section_31_requires_priority_and_rule_database",
        },
        "runtime_metadata": {
            k: metadata.get(k)
            for k in ("kind", "source", "day_stem", "sprint")
            if k in metadata
        },
    }
