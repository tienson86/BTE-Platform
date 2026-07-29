"""
Dayun runtime validation against DAYUN_SPEC.md §§13–14.

Does not evaluate cát hung. Fail-soft: returns a result object, never raises
for rule failures.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm

STEMS: frozenset[str] = frozenset(GanzhiAlgorithm.STEM)
BRANCHES: frozenset[str] = frozenset(GanzhiAlgorithm.BRANCH)

# DAYUN_SPEC §8 / §14 — each Đại vận spans exactly 10 years.
DAYUN_SPAN_YEARS = 10
DAYUN_AGE_SPAN = 9  # inclusive start_age..end_age → 10 years


@dataclass(frozen=True, slots=True)
class DayunValidationResult:
    """Immutable validation outcome for one DayunRuntime / sequence."""

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
            "spec": "DAYUN_SPEC.md",
            "sections": ["13_validation_rules", "14_business_rules"],
        }


def _attr(obj: Any, name: str, default: Any = None) -> Any:
    """Read attribute or mapping key."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def validate_dayun_runtime(dayun: Any | None) -> DayunValidationResult:
    """
    Validate current Dayun (+ optional sequence) per DAYUN_SPEC §§13–14.

    Returns UNKNOWN-friendly result when ``dayun`` is missing.
    """
    if dayun is None:
        return DayunValidationResult(
            ok=False,
            passed=(),
            failed=("dayun_present",),
            reasons=("dayun_runtime_missing",),
            confidence=None,
        )

    passed: list[str] = ["dayun_present"]
    failed: list[str] = []
    reasons: list[str] = []

    stem = _attr(dayun, "heavenly_stem")
    branch = _attr(dayun, "earthly_branch")
    start_age = _attr(dayun, "start_age")
    end_age = _attr(dayun, "end_age")
    start_year = _attr(dayun, "start_year")
    end_year = _attr(dayun, "end_year")
    element = _attr(dayun, "element")
    yin_yang = _attr(dayun, "yin_yang")
    index = _attr(dayun, "index")

    # §13 đủ dữ liệu / §14 metadata tối thiểu trên runtime hiện tại
    required_ok = all(
        v is not None and v != ""
        for v in (stem, branch, start_age, end_age, start_year, end_year, index)
    )
    if required_ok:
        passed.append("required_fields")
    else:
        failed.append("required_fields")
        reasons.append("dayun_required_fields_incomplete")

    if stem in STEMS:
        passed.append("stem_valid")
    else:
        failed.append("stem_valid")
        reasons.append("dayun_stem_invalid")

    if branch in BRANCHES:
        passed.append("branch_valid")
    else:
        failed.append("branch_valid")
        reasons.append("dayun_branch_invalid")

    # §14: đúng một Can và một Chi (non-empty single values already checked)
    if stem and branch and stem in STEMS and branch in BRANCHES:
        passed.append("single_stem_branch")
    else:
        failed.append("single_stem_branch")
        reasons.append("dayun_stem_branch_contract_failed")

    # §8 / §14: đúng 10 năm (inclusive age/year windows)
    try:
        age_span_ok = int(end_age) - int(start_age) == DAYUN_AGE_SPAN
    except (TypeError, ValueError):
        age_span_ok = False
    if age_span_ok and int(start_age) >= 1:
        passed.append("age_window_valid")
    else:
        failed.append("age_window_valid")
        reasons.append("dayun_age_window_invalid")

    try:
        year_span_ok = int(end_year) - int(start_year) == DAYUN_AGE_SPAN
    except (TypeError, ValueError):
        year_span_ok = False
    if year_span_ok:
        passed.append("year_window_valid")
    else:
        failed.append("year_window_valid")
        reasons.append("dayun_year_window_invalid")

    if age_span_ok and year_span_ok:
        passed.append("span_ten_years")
    else:
        failed.append("span_ten_years")
        reasons.append("dayun_not_ten_year_span")

    # Optional enrichment fields (Heavenly / Earth layers)
    if element:
        passed.append("element_present")
    else:
        failed.append("element_present")
        reasons.append("dayun_element_missing")

    if yin_yang:
        passed.append("yin_yang_present")
    else:
        failed.append("yin_yang_present")
        reasons.append("dayun_yin_yang_missing")

    # Sequence continuity / unique indices when provider embeds sequence
    metadata = _attr(dayun, "metadata") or {}
    if hasattr(metadata, "get"):
        sequence = metadata.get("sequence") or []
    else:
        sequence = []

    if sequence:
        indices = [_attr(item, "index") for item in sequence]
        if len(indices) == len(set(indices)) and None not in indices:
            passed.append("sequence_unique")
        else:
            failed.append("sequence_unique")
            reasons.append("dayun_sequence_duplicate_or_missing_index")

        continuous = _sequence_continuous(sequence)
        if continuous:
            passed.append("sequence_continuous")
        else:
            failed.append("sequence_continuous")
            reasons.append("dayun_sequence_not_continuous")
    else:
        # Single pillar without sequence — continuity N/A for current only
        passed.append("sequence_unique")
        passed.append("sequence_continuous")

    total = len(passed) + len(failed)
    confidence = (len(passed) / total) if total else None
    ok = len(failed) == 0
    if ok and not reasons:
        reasons = ("dayun_validation_passed",)

    return DayunValidationResult(
        ok=ok,
        passed=tuple(passed),
        failed=tuple(failed),
        reasons=tuple(reasons),
        confidence=confidence,
    )


def _sequence_continuous(sequence: list[Any]) -> bool:
    """Check no age/year gaps between consecutive Dayun pillars (§8 / §14)."""
    if len(sequence) < 2:
        return True
    ordered = sorted(sequence, key=lambda item: int(_attr(item, "index", -1)))
    for prev, curr in zip(ordered, ordered[1:]):
        try:
            if int(_attr(curr, "start_age")) != int(_attr(prev, "end_age")) + 1:
                return False
            if int(_attr(curr, "start_year")) != int(_attr(prev, "end_year")) + 1:
                return False
        except (TypeError, ValueError):
            return False
    return True


def dayun_runtime_snapshot(dayun: Any | None) -> dict[str, Any] | None:
    """
    Machine-readable DayunRuntime fields per DAYUN_SPEC §7.

    No interpretation — copies provider runtime only.
    """
    if dayun is None:
        return None
    to_dict = getattr(dayun, "to_dict", None)
    if callable(to_dict):
        payload = to_dict()
    elif isinstance(dayun, dict):
        payload = dict(dayun)
    else:
        payload = {
            "index": _attr(dayun, "index"),
            "start_age": _attr(dayun, "start_age"),
            "end_age": _attr(dayun, "end_age"),
            "start_year": _attr(dayun, "start_year"),
            "end_year": _attr(dayun, "end_year"),
            "heavenly_stem": _attr(dayun, "heavenly_stem"),
            "earthly_branch": _attr(dayun, "earthly_branch"),
            "element": _attr(dayun, "element"),
            "yin_yang": _attr(dayun, "yin_yang"),
            "ten_god": _attr(dayun, "ten_god"),
            "hidden_stems": list(_attr(dayun, "hidden_stems") or ()),
        }
    # Strip nested sequence from snapshot current; keep under collection key
    metadata = dict(payload.get("metadata") or {})
    sequence = metadata.pop("sequence", None)
    payload["metadata"] = {
        k: v
        for k, v in metadata.items()
        if k
        in {
            "kind",
            "direction",
            "from_month_ganzhi",
            "start_age_calc",
            "reference_year",
            "age_at_reference",
            "gender",
            "year_stem",
            "day_master",
            "sprint",
        }
    }
    return {
        "identity": {"index": payload.get("index")},
        "time": {
            "start_age": payload.get("start_age"),
            "end_age": payload.get("end_age"),
            "start_year": payload.get("start_year"),
            "end_year": payload.get("end_year"),
        },
        "heavenly_layer": {
            "heavenly_stem": payload.get("heavenly_stem"),
            "yin_yang": payload.get("yin_yang"),
            "five_element": payload.get("element"),
        },
        "earth_layer": {
            "earthly_branch": payload.get("earthly_branch"),
            "hidden_stems": payload.get("hidden_stems") or [],
        },
        "relationship": {
            "ten_god": payload.get("ten_god"),
        },
        "runtime_metadata": payload.get("metadata") or {},
        "sequence_count": len(sequence) if isinstance(sequence, list) else 0,
    }
