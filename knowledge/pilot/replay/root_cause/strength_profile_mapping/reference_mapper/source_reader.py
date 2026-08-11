"""Normalize heterogeneous runtime records into a common bundle (read-only)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .ascii_utils import to_ascii_branch, to_ascii_element, to_ascii_stem


@dataclass
class RuntimeBundle:
    """Normalized view of already-computed runtime evidence."""

    case_id: str
    population: str
    day_master: str | None
    raw_score: float | None
    normalized_score: float | None
    published_score: float | None
    current_v1_band: str | None
    runtime_confidence: float | None
    profile_buckets: dict[str, float | None] = field(default_factory=dict)
    component_scores: dict[str, float | None] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    matched_rules: list[str] = field(default_factory=list)
    ledger: list[dict[str, Any]] = field(default_factory=list)
    temperature: dict[str, Any] = field(default_factory=dict)
    expert_external: dict[str, Any] | None = None
    synthetic_external: dict[str, Any] | None = None
    source_paths: dict[str, str] = field(default_factory=dict)
    calendar_status: str | None = None


def from_synthetic_result(doc: dict[str, Any]) -> RuntimeBundle:
    """Build bundle from PILOT-1G synthetic result JSON."""
    runtime = doc.get("runtime") or {}
    ctx = runtime.get("context") or {}
    day_master = to_ascii_stem(doc.get("day_master")) or to_ascii_stem(ctx.get("day_master"))
    return RuntimeBundle(
        case_id=str(doc["case_id"]),
        population="synthetic_stress",
        day_master=day_master,
        raw_score=_num(runtime.get("raw_total")),
        normalized_score=_num(runtime.get("score")),
        published_score=_num(runtime.get("score")),
        current_v1_band=_band(runtime.get("v1_band")),
        runtime_confidence=_num(runtime.get("confidence")),
        profile_buckets=_float_dict(runtime.get("profile") or {}),
        component_scores=_float_dict(runtime.get("component_scores") or {}),
        context=_normalize_context(ctx),
        matched_rules=[str(x) for x in (runtime.get("matched_rules") or [])],
        ledger=[],
        temperature={
            "temperature_type": ctx.get("temperature_type"),
            "source": "strength_context.temperature_type",
        },
        expert_external=None,
        synthetic_external={
            "synthetic_expected_taxonomy": doc.get("synthetic_expected_taxonomy"),
            "evidence_profile": doc.get("evidence_profile"),
            "synthetic": True,
            "calibration_eligible": False,
            "golden_eligible": False,
            "expert_calibration_eligible": False,
        },
        source_paths={
            "result": f"knowledge/pilot/replay/synthetic_strength/results/{doc['case_id']}.json"
        },
        calendar_status="not_verified" if doc.get("calendar_verified") is False else None,
    )


def from_calibration_case(case: dict[str, Any], evidence: dict[str, Any]) -> RuntimeBundle:
    """Build bundle from CAL case + evidence snapshot (read-only)."""
    case_id = str(case.get("calibration_case_id") or evidence.get("calibration_case_id"))
    pipe = evidence.get("pipeline") or {}
    season_ctx = pipe.get("season_context") or {}
    root_ev = pipe.get("root_resource_evidence") or {}
    temp_ctx = pipe.get("temperature_context") or {}
    chart = evidence.get("chart") or case.get("canonical_pillars") or {}
    day_master = to_ascii_stem(chart.get("day_master"))

    context = {
        "day_master": day_master,
        "day_master_element": None,
        "month_branch": to_ascii_branch(season_ctx.get("month_branch")),
        "month_status": season_ctx.get("month_status"),
        "root_level": root_ev.get("root_level"),
        "support_type": root_ev.get("support_type"),
        "control_type": None,
        "drain_type": None,
        "season": season_ctx.get("season"),
        "season_phase": season_ctx.get("season_phase"),
        "temperature_type": temp_ctx.get("from_strength_context"),
        "root_count": root_ev.get("root_count"),
        "resource_count": None,
        "companion_count": None,
        "wealth_count": None,
        "officer_count": None,
        "output_count": None,
    }

    # Derive control_type only if ledger exposes one explicitly (no invention).
    for item in pipe.get("strength_evidence_ledger") or []:
        if item.get("group") == "control" and item.get("reason"):
            # keep first observed control reason as opaque label; not remapped
            if context["control_type"] is None:
                context["control_type"] = item.get("reason")

    runtime_score = case.get("runtime_score") or {}
    return RuntimeBundle(
        case_id=case_id,
        population="real_calibration",
        day_master=day_master,
        raw_score=_num(runtime_score.get("raw") if runtime_score else pipe.get("raw_strength_score")),
        normalized_score=_num(
            runtime_score.get("normalized") if runtime_score else pipe.get("normalized_score")
        ),
        published_score=_num(
            runtime_score.get("normalized") if runtime_score else pipe.get("normalized_score")
        ),
        current_v1_band=_band(case.get("current_v1_band") or pipe.get("current_band")),
        runtime_confidence=_num(pipe.get("confidence_runtime")),
        profile_buckets=_float_dict(case.get("runtime_profile") or pipe.get("weighted_buckets_raw") or {}),
        component_scores={},
        context=context,
        matched_rules=[
            str(i.get("rule_id"))
            for i in (pipe.get("strength_evidence_ledger") or [])
            if i.get("rule_id")
        ],
        ledger=list(pipe.get("strength_evidence_ledger") or []),
        temperature={
            "from_strength_context": temp_ctx.get("from_strength_context"),
            "from_temperature_engine": temp_ctx.get("from_temperature_engine"),
            "note": temp_ctx.get("note"),
        },
        expert_external={
            "expert_review_1": case.get("expert_review_1"),
            "expert_review_2": case.get("expert_review_2"),
            "agreement": case.get("agreement"),
            "note": "external calibration metadata only; not runtime confidence",
        },
        synthetic_external=None,
        source_paths={
            "case": f"knowledge/pilot/replay/root_cause/strength_taxonomy_v2/calibration/cases/{case_id}.json",
            "evidence": f"knowledge/pilot/replay/root_cause/strength_taxonomy_v2/calibration/evidence/{case_id}.json",
        },
        calendar_status=(case.get("calendar_verification") or {}).get("status"),
    )


def _num(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _band(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in {"weak", "balanced", "strong"}:
        return text
    return None


def _float_dict(data: dict[str, Any]) -> dict[str, float | None]:
    out: dict[str, float | None] = {}
    for key, value in data.items():
        out[str(key)] = _num(value)
    return out


def _normalize_context(ctx: dict[str, Any]) -> dict[str, Any]:
    return {
        "day_master": to_ascii_stem(ctx.get("day_master")),
        "day_master_element": to_ascii_element(ctx.get("day_master_element")),
        "month_branch": to_ascii_branch(ctx.get("month_branch")),
        "month_status": ctx.get("month_status"),
        "root_level": ctx.get("root_level"),
        "support_type": ctx.get("support_type"),
        "control_type": ctx.get("control_type"),
        "drain_type": ctx.get("drain_type"),
        "season": ctx.get("season"),
        "season_phase": ctx.get("season_phase"),
        "temperature_type": ctx.get("temperature_type"),
        "root_count": ctx.get("root_count"),
        "resource_count": ctx.get("resource_count"),
        "companion_count": ctx.get("companion_count"),
        "wealth_count": ctx.get("wealth_count"),
        "officer_count": ctx.get("officer_count"),
        "output_count": ctx.get("output_count"),
    }
