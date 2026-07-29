"""
Liuri runtime validation against LIURI_SPEC.md.

Structural contracts: §§8–16. Mandatory input readiness: §32.
Interaction / Useful-God / Risk scoring deferred — Rule Database required;
no undocumented BaZi logic invented.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.rule_contract.signal_maps import BRANCH_HIDDEN

from .providers._common import STEMS

BRANCHES: frozenset[str] = frozenset(GanzhiAlgorithm.BRANCH)


@dataclass(frozen=True, slots=True)
class LiuriValidationResult:
    """Immutable validation outcome for one LiuriRuntime (LIURI_SPEC §32)."""

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
            "spec": "LIURI_SPEC.md",
            "sections": [
                "8_output_structure",
                "9_12_calendar_engine_daily_pillar",
                "13_hidden_stems",
                "14_ten_gods",
                "15_five_element_mapping",
                "16_seasonal_context_inherited",
                "32_validation_rules",
            ],
            "pending_spec_sections": [
                "17_25_interactions",
                "26_transformation",
                "27_28_useful_unfavorable_god",
                "29_risk_flags",
                "30_priority",
            ],
        }


def _attr(obj: Any, name: str, default: Any = None) -> Any:
    """Read attribute or mapping key."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def validate_liuri_runtime(
    liuri: Any | None,
    *,
    dayun: Any | None = None,
    liunian: Any | None = None,
    liuyue: Any | None = None,
) -> LiuriValidationResult:
    """
    Validate current Liuri (+ upstream readiness) per LIURI_SPEC.

    Fail-soft: never raises for rule failures.
    """
    errors: list[str] = []
    warnings: list[str] = []
    passed: list[str] = []
    failed: list[str] = []
    reasons: list[str] = []

    if liuri is None:
        return LiuriValidationResult(
            ok=False,
            errors=("liuri_calendar_engine_output_missing",),
            warnings=(),
            passed=(),
            failed=("liuri_present",),
            reasons=("liuri_runtime_missing",),
            confidence=None,
        )

    passed.append("liuri_present")

    year = _attr(liuri, "year")
    month = _attr(liuri, "month")
    day = _attr(liuri, "day")
    stem = _attr(liuri, "heavenly_stem")
    branch = _attr(liuri, "earthly_branch")
    ganzhi = _attr(liuri, "ganzhi")
    element = _attr(liuri, "element")
    yin_yang = _attr(liuri, "yin_yang")
    ten_god = _attr(liuri, "ten_god")
    hidden = _attr(liuri, "hidden_stems") or ()
    metadata = _attr(liuri, "metadata") or {}

    # §§9–12 — Calendar Engine daily pillar (immutable fields from provider)
    try:
        date_ok = (
            year is not None
            and month is not None
            and day is not None
            and int(year) > 0
            and 1 <= int(month) <= 12
            and 1 <= int(day) <= 31
        )
    except (TypeError, ValueError):
        date_ok = False
    if date_ok:
        passed.append("calendar_date_fields")
    else:
        failed.append("calendar_date_fields")
        errors.append("liuri_calendar_engine_output_incomplete")
        reasons.append("liuri_invalid_gregorian_date")

    if stem in STEMS:
        passed.append("stem_valid")
    else:
        failed.append("stem_valid")
        errors.append("liuri_invalid_daily_stem")
        reasons.append("liuri_invalid_stem")

    if branch in BRANCHES:
        passed.append("branch_valid")
    else:
        failed.append("branch_valid")
        errors.append("liuri_invalid_daily_branch")
        reasons.append("liuri_invalid_branch")

    if stem and branch:
        compact = str(ganzhi or "").replace(" ", "")
        if compact in {f"{stem}{branch}", f"{stem} {branch}".replace(" ", "")}:
            passed.append("ganzhi_consistent")
        else:
            failed.append("ganzhi_consistent")
            errors.append("liuri_ganzhi_mismatch")
            reasons.append("liuri_ganzhi_mismatch")
    else:
        failed.append("ganzhi_consistent")
        errors.append("liuri_ganzhi_missing")
        reasons.append("liuri_ganzhi_missing")

    source = metadata.get("source") if hasattr(metadata, "get") else None
    if source == "julian_day_ganzhi":
        passed.append("calendar_engine_source")
    else:
        failed.append("calendar_engine_source")
        warnings.append("liuri_calendar_source_metadata_unexpected")
        reasons.append("liuri_calendar_source_not_documented")

    # §13 Hidden stems
    expected_hidden = BRANCH_HIDDEN.get(str(branch), []) if branch else []
    hidden_list = list(hidden) if hidden is not None else []
    if expected_hidden and tuple(hidden_list) == tuple(expected_hidden):
        passed.append("hidden_stems_match_database")
    else:
        failed.append("hidden_stems_match_database")
        errors.append("liuri_hidden_stems_mismatch")
        reasons.append("liuri_004_hidden_stem_database_mismatch")

    # §14 Ten Gods
    if ten_god:
        passed.append("ten_god_present")
    else:
        failed.append("ten_god_present")
        errors.append("liuri_ten_god_missing")
        reasons.append("liuri_ten_god_missing")

    # §15 Five element mapping
    if element:
        passed.append("element_present")
    else:
        failed.append("element_present")
        errors.append("liuri_element_missing")
        reasons.append("liuri_element_missing")

    if yin_yang:
        passed.append("yin_yang_present")
    else:
        failed.append("yin_yang_present")
        errors.append("liuri_yin_yang_missing")
        reasons.append("liuri_yin_yang_missing")

    # §32 Mandatory upstream contexts
    if dayun is not None and _attr(dayun, "heavenly_stem") in STEMS:
        passed.append("dayun_context_ready")
    else:
        failed.append("dayun_context_ready")
        errors.append("liuri_dayun_context_missing")
        reasons.append("liuri_dayun_context_missing")

    if liunian is not None and _attr(liunian, "heavenly_stem") in STEMS:
        passed.append("liunian_context_ready")
    else:
        failed.append("liunian_context_ready")
        errors.append("liuri_liunian_context_missing")
        reasons.append("liuri_liunian_context_missing")

    if liuyue is not None and _attr(liuyue, "heavenly_stem") in STEMS:
        passed.append("liuyue_context_ready")
    else:
        failed.append("liuyue_context_ready")
        errors.append("liuri_liuyue_context_missing")
        reasons.append("liuri_liuyue_context_missing")

    # §32 Rule Database / Priority — not wired in Luck Engine evaluation layer
    warnings.append("liuri_rule_database_not_available")
    warnings.append("liuri_priority_rules_not_available")
    warnings.append("liuri_interaction_evaluation_deferred")
    # §16 Seasonal context inherited from Liuyue (do not recalculate)
    if liuyue is not None and _attr(liuyue, "solar_term"):
        passed.append("seasonal_context_inherited_from_liuyue")
    else:
        failed.append("seasonal_context_inherited_from_liuyue")
        warnings.append("liuri_seasonal_context_unavailable")
        reasons.append("liuri_seasonal_context_not_inherited")

    scored_passed = [
        p
        for p in passed
        if p
        not in {
            "calendar_engine_source",
        }
    ]
    # Confidence from structural + readiness checks only (exclude pure warnings)
    scored_total = len(scored_passed) + len(failed)
    confidence = (len(scored_passed) / scored_total) if scored_total else None
    ok = len(errors) == 0
    if ok and not reasons:
        reasons = ("liuri_validation_passed",)

    return LiuriValidationResult(
        ok=ok,
        errors=tuple(errors),
        warnings=tuple(warnings),
        passed=tuple(passed),
        failed=tuple(failed),
        reasons=tuple(reasons),
        confidence=confidence,
    )


def liuri_runtime_snapshot(
    liuri: Any | None,
    *,
    liuyue: Any | None = None,
) -> dict[str, Any] | None:
    """
    Machine-readable LiuriRuntime fields per LIURI_SPEC §§7–8.

    No interpretation — copies provider runtime only.
    """
    if liuri is None:
        return None
    to_dict = getattr(liuri, "to_dict", None)
    if callable(to_dict):
        payload = to_dict()
    elif isinstance(liuri, dict):
        payload = dict(liuri)
    else:
        payload = {
            "year": _attr(liuri, "year"),
            "month": _attr(liuri, "month"),
            "day": _attr(liuri, "day"),
            "ganzhi": _attr(liuri, "ganzhi"),
            "heavenly_stem": _attr(liuri, "heavenly_stem"),
            "earthly_branch": _attr(liuri, "earthly_branch"),
            "element": _attr(liuri, "element"),
            "yin_yang": _attr(liuri, "yin_yang"),
            "ten_god": _attr(liuri, "ten_god"),
            "hidden_stems": list(_attr(liuri, "hidden_stems") or ()),
            "metadata": dict(_attr(liuri, "metadata") or {}),
        }
    metadata = dict(payload.get("metadata") or {})
    seasonal_term = _attr(liuyue, "solar_term") if liuyue is not None else None
    return {
        "daily_pillar": {
            "year": payload.get("year"),
            "month": payload.get("month"),
            "day": payload.get("day"),
            "ganzhi": payload.get("ganzhi"),
            "heavenly_stem": payload.get("heavenly_stem"),
            "earthly_branch": payload.get("earthly_branch"),
        },
        "hidden_stems": payload.get("hidden_stems") or [],
        "ten_gods": {"daily_stem": payload.get("ten_god")},
        "five_elements": {
            "stem_element": payload.get("element"),
            "yin_yang": payload.get("yin_yang"),
        },
        "seasonal_context": {
            "status": "INHERITED" if seasonal_term else "UNKNOWN",
            "source": "liuyue",
            "solar_term": seasonal_term,
            "reason": (
                "liuri_spec_section_16_inherit_from_liuyue"
                if seasonal_term
                else "liuri_seasonal_context_unavailable"
            ),
        },
        "interactions": {
            "stem_relations": [],
            "branch_relations": [],
            "hidden_stem_relations": [],
            "natal_relations": [],
            "liuyue_relations": [],
            "liunian_relations": [],
            "dayun_relations": [],
            "status": "UNKNOWN",
            "reason": "liuri_spec_interaction_tables_require_rule_database",
        },
        "risk_flags": {
            "status": "UNKNOWN",
            "reason": "liuri_spec_section_29_requires_priority_and_rule_database",
        },
        "runtime_metadata": {
            k: metadata.get(k)
            for k in ("kind", "source", "sprint")
            if k in metadata
        },
    }
