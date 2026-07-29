"""
Liunian runtime validation against LIUNIAN_SPEC.md (written sections).

Applies structural contracts from §§8–13 and Dayun-layer readiness (§18).
Does not invent combination / clash / Tai Sui tables (Rule Database required;
SPEC §§21–33 incomplete for scoring / full validation taxonomy).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.rule_contract.signal_maps import BRANCH_HIDDEN

STEMS: frozenset[str] = frozenset(GanzhiAlgorithm.STEM)
BRANCHES: frozenset[str] = frozenset(GanzhiAlgorithm.BRANCH)


@dataclass(frozen=True, slots=True)
class LiunianValidationResult:
    """Immutable validation outcome for one LiunianRuntime."""

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
            "spec": "LIUNIAN_SPEC.md",
            "sections": [
                "8_output_structure",
                "9_annual_pillar",
                "11_hidden_stems",
                "12_ten_gods",
                "13_five_element_mapping",
                "18_dayun_interaction_readiness",
            ],
            "pending_spec_sections": [
                "21_fu_yin",
                "27_annual_strength",
                "33_validation_rules",
            ],
        }


def _attr(obj: Any, name: str, default: Any = None) -> Any:
    """Read attribute or mapping key."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def validate_liunian_runtime(
    liunian: Any | None,
    *,
    dayun: Any | None = None,
) -> LiunianValidationResult:
    """
    Validate current Liunian (+ Dayun readiness) per written LIUNIAN_SPEC.

    Fail-soft: never raises for rule failures.
    """
    if liunian is None:
        return LiunianValidationResult(
            ok=False,
            passed=(),
            failed=("liunian_present",),
            reasons=("liunian_runtime_missing",),
            confidence=None,
        )

    passed: list[str] = ["liunian_present"]
    failed: list[str] = []
    reasons: list[str] = []

    year = _attr(liunian, "year")
    stem = _attr(liunian, "heavenly_stem")
    branch = _attr(liunian, "earthly_branch")
    ganzhi = _attr(liunian, "ganzhi")
    element = _attr(liunian, "element")
    yin_yang = _attr(liunian, "yin_yang")
    ten_god = _attr(liunian, "ten_god")
    hidden = _attr(liunian, "hidden_stems") or ()
    metadata = _attr(liunian, "metadata") or {}

    # §9 Annual pillar identity
    try:
        year_ok = year is not None and int(year) > 0
    except (TypeError, ValueError):
        year_ok = False
    if year_ok:
        passed.append("year_valid")
    else:
        failed.append("year_valid")
        reasons.append("liunian_001_invalid_year")

    if stem in STEMS:
        passed.append("stem_valid")
    else:
        failed.append("stem_valid")
        reasons.append("liunian_002_invalid_stem")

    if branch in BRANCHES:
        passed.append("branch_valid")
    else:
        failed.append("branch_valid")
        reasons.append("liunian_003_invalid_branch")

    expected_ganzhi = f"{stem} {branch}" if stem and branch else None
    if ganzhi and expected_ganzhi and str(ganzhi).replace(" ", "") == expected_ganzhi.replace(
        " ", ""
    ):
        passed.append("ganzhi_consistent")
    elif ganzhi and stem and branch:
        # Allow "StemBranch" or "Stem Branch"
        compact = str(ganzhi).replace(" ", "")
        if compact == f"{stem}{branch}":
            passed.append("ganzhi_consistent")
        else:
            failed.append("ganzhi_consistent")
            reasons.append("liunian_ganzhi_mismatch")
    else:
        failed.append("ganzhi_consistent")
        reasons.append("liunian_ganzhi_missing")

    # §11 Hidden stems
    expected_hidden = BRANCH_HIDDEN.get(str(branch), []) if branch else []
    hidden_list = list(hidden) if hidden is not None else []
    if expected_hidden and hidden_list:
        if tuple(hidden_list) == tuple(expected_hidden):
            passed.append("hidden_stems_match_database")
        else:
            # Order must follow database per SPEC §11
            failed.append("hidden_stems_match_database")
            reasons.append("liunian_004_missing_or_mismatched_hidden_stem")
    elif expected_hidden and not hidden_list:
        failed.append("hidden_stems_match_database")
        reasons.append("liunian_004_missing_hidden_stem")
    else:
        failed.append("hidden_stems_match_database")
        reasons.append("liunian_004_missing_hidden_stem")

    # §12 Ten Gods present on annual stem (label from provider)
    if ten_god:
        passed.append("ten_god_present")
    else:
        failed.append("ten_god_present")
        reasons.append("liunian_ten_god_missing")

    # §13 Five element mapping
    if element:
        passed.append("element_present")
    else:
        failed.append("element_present")
        reasons.append("liunian_element_missing")

    if yin_yang:
        passed.append("yin_yang_present")
    else:
        failed.append("yin_yang_present")
        reasons.append("liunian_yin_yang_missing")

    # §9–10 Li Chun based year metadata (provider contract)
    bazi_year = None
    if hasattr(metadata, "get"):
        bazi_year = metadata.get("bazi_year")
    if bazi_year is not None and year_ok and int(bazi_year) == int(year):
        passed.append("lichun_year_metadata")
    elif bazi_year is not None:
        failed.append("lichun_year_metadata")
        reasons.append("liunian_bazi_year_mismatch")
    else:
        failed.append("lichun_year_metadata")
        reasons.append("liunian_bazi_year_metadata_missing")

    # §18 Dayun interaction readiness (context present; no invented relations)
    if dayun is not None:
        dayun_stem = _attr(dayun, "heavenly_stem")
        dayun_branch = _attr(dayun, "earthly_branch")
        if dayun_stem in STEMS and dayun_branch in BRANCHES:
            passed.append("dayun_context_ready")
        else:
            failed.append("dayun_context_ready")
            reasons.append("liunian_006_dayun_not_found_or_incomplete")
    else:
        failed.append("dayun_context_ready")
        reasons.append("liunian_006_dayun_not_found")

    # Interaction / Tai Sui / Kong Wang results are SPEC-listed but rule tables
    # and §§21–33 are incomplete — do not invent; record as deferred checks.
    passed.append("interaction_tables_deferred_to_rule_database")

    total = len(passed) + len(failed)
    # Deferred pass should not inflate confidence unrealistically: exclude it
    scored_passed = [p for p in passed if p != "interaction_tables_deferred_to_rule_database"]
    scored_total = len(scored_passed) + len(failed)
    confidence = (len(scored_passed) / scored_total) if scored_total else None
    ok = len(failed) == 0
    if ok and not reasons:
        reasons = ("liunian_validation_passed",)

    return LiunianValidationResult(
        ok=ok,
        passed=tuple(passed),
        failed=tuple(failed),
        reasons=tuple(reasons),
        confidence=confidence,
    )


def liunian_runtime_snapshot(liunian: Any | None) -> dict[str, Any] | None:
    """
    Machine-readable LiunianRuntime fields per LIUNIAN_SPEC §§7–8.

    No interpretation — copies provider runtime only.
    """
    if liunian is None:
        return None
    to_dict = getattr(liunian, "to_dict", None)
    if callable(to_dict):
        payload = to_dict()
    elif isinstance(liunian, dict):
        payload = dict(liunian)
    else:
        payload = {
            "year": _attr(liunian, "year"),
            "ganzhi": _attr(liunian, "ganzhi"),
            "heavenly_stem": _attr(liunian, "heavenly_stem"),
            "earthly_branch": _attr(liunian, "earthly_branch"),
            "element": _attr(liunian, "element"),
            "yin_yang": _attr(liunian, "yin_yang"),
            "ten_god": _attr(liunian, "ten_god"),
            "hidden_stems": list(_attr(liunian, "hidden_stems") or ()),
            "metadata": dict(_attr(liunian, "metadata") or {}),
        }
    metadata = dict(payload.get("metadata") or {})
    metadata.pop("nearby_years", None)
    return {
        "annual_pillar": {
            "year": payload.get("year"),
            "ganzhi": payload.get("ganzhi"),
            "heavenly_stem": payload.get("heavenly_stem"),
            "earthly_branch": payload.get("earthly_branch"),
        },
        "hidden_stems": payload.get("hidden_stems") or [],
        "ten_gods": {
            "annual_stem": payload.get("ten_god"),
        },
        "five_elements": {
            "stem_element": payload.get("element"),
            "yin_yang": payload.get("yin_yang"),
        },
        "interactions": {
            "stem_relations": [],
            "branch_relations": [],
            "hidden_stem_relations": [],
            "dayun_relations": [],
            "status": "UNKNOWN",
            "reason": "liunian_spec_interaction_tables_require_rule_database",
        },
        "tai_sui": {
            "status": "UNKNOWN",
            "reason": "liunian_spec_section_19_incomplete_without_special_rules_db",
        },
        "kong_wang": {
            "status": "UNKNOWN",
            "reason": "liunian_spec_section_20_incomplete_without_void_rules",
        },
        "runtime_metadata": {
            k: metadata.get(k)
            for k in ("kind", "civil_year", "bazi_year", "sprint")
            if k in metadata
        },
    }
