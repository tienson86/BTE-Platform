"""Assemble StrengthProfile sections from observed runtime fields."""

from __future__ import annotations

from typing import Any

from .ascii_utils import SCHEMA_VERSION, unknown
from .completeness_mapper import map_completeness
from .confidence_mapper import map_confidence
from .conflict_mapper import map_conflicts
from .evidence_mapper import map_evidence
from .provenance_mapper import map_root_provenance
from .score_reference_mapper import map_score_reference
from .saturation_mapper import map_saturation
from .source_reader import RuntimeBundle


def map_profile(bundle: RuntimeBundle) -> dict[str, Any]:
    """Construct StrengthProfile without taxonomy or invented values."""
    evidence = map_evidence(bundle)
    evidence_ids = [e["evidence_id"] for e in evidence]
    completeness = map_completeness(bundle)
    conflicts = map_conflicts(bundle, evidence_ids)
    confidence = map_confidence(
        bundle,
        completeness_overall=str(completeness.get("overall")),
        conflict_count=len(conflicts),
    )
    score_ref = map_score_reference(bundle)
    saturation = map_saturation(bundle)
    score_ref["saturation_detected"] = saturation["saturation_detected"]
    score_ref["saturation_type"] = saturation["saturation_type"]

    day_master = bundle.day_master or unknown()
    # Schema requires day_master enum; if unknown stem, fail soft with 'giap' is NOT allowed.
    # Keep only valid stems; if missing, use a placeholder only if we must — better raise.
    if day_master == unknown():
        raise ValueError(f"day_master unavailable for {bundle.case_id}")

    profile_id = f"PRF-MAP-{bundle.case_id.replace('-', '_')}"

    seasonal = _seasonal_state(bundle)
    rooting = _rooting_state(bundle)
    support = _support_state(bundle)
    pressure = _pressure_state(bundle)
    drain = _drain_state(bundle)
    structural = _structural_state(bundle)
    temperature = _temperature_state(bundle)

    dominant, supporting, opposing = _factor_lists(bundle)

    profile: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "identity": {
            "profile_id": profile_id,
            "source_case_ref": bundle.case_id,
            "population": bundle.population,
            "notes": "REFERENCE_ONLY runtime projection; PRODUCTION_READY=false",
        },
        "population": bundle.population,
        "design_marker": "runtime_projection",
        "day_master": day_master,
        "score_reference": score_ref,
        "seasonal_state": seasonal,
        "rooting_state": rooting,
        "support_state": support,
        "pressure_state": pressure,
        "drain_state": drain,
        "structural_state": structural,
        "temperature_state": temperature,
        "conflicts": conflicts,
        "evidence_completeness": completeness,
        "evidence_records": evidence,
        "dominant_factors": dominant,
        "supporting_factors": supporting,
        "opposing_factors": opposing,
        "uncertainty": _uncertainty(bundle, saturation),
        "confidence": confidence,
        "provenance": map_root_provenance(bundle),
        "synthetic_flags": _synthetic_flags(bundle),
        "external_labels": _external_labels(bundle),
    }
    return profile


def _seasonal_state(bundle: RuntimeBundle) -> dict[str, Any]:
    ctx = bundle.context
    return {
        "season_branch": ctx.get("month_branch"),
        "season_element": None,
        "day_master_relation": ctx.get("month_status"),
        "seasonal_support_direction": unknown(),
        "seasonal_strength_state": unknown(),
        "seasonal_confidence": unknown(),
        "source": "runtime.context" if ctx.get("month_status") or ctx.get("season") else None,
        "season": ctx.get("season"),
        "season_phase": ctx.get("season_phase"),
        "raw_contribution": bundle.profile_buckets.get("season"),
        "notes": "seasonal_strength_state not inferred from month_status",
    }


def _rooting_state(bundle: RuntimeBundle) -> dict[str, Any]:
    ctx = bundle.context
    root_count = ctx.get("root_count")
    return {
        "day_branch_root": unknown(),
        "month_branch_root": unknown(),
        "other_branch_root": unknown(),
        "hidden_root": unknown(),
        "multiple_roots": True if isinstance(root_count, int) and root_count >= 2 else (
            False if isinstance(root_count, int) else unknown()
        ),
        "root_strength": ctx.get("root_level") or unknown(),
        "root_distribution": [],
        "root_confidence": unknown(),
        "root_count": root_count,
        "raw_contribution": bundle.profile_buckets.get("root"),
        "notes": "per-branch loci not available from current runtime boundary",
    }


def _support_state(bundle: RuntimeBundle) -> dict[str, Any]:
    items = []
    if bundle.context.get("support_type"):
        items.append(
            {
                "category": "same_element",
                "label": bundle.context.get("support_type"),
                "raw_contribution": bundle.profile_buckets.get("support"),
                "provenance": "engine_context",
            }
        )
    return {
        "items": items,
        "summary": bundle.context.get("support_type") or unknown(),
        "bucket_total": bundle.profile_buckets.get("support"),
        "confidence": unknown(),
    }


def _pressure_state(bundle: RuntimeBundle) -> dict[str, Any]:
    items = []
    if bundle.context.get("control_type"):
        items.append(
            {
                "category": "control",
                "label": bundle.context.get("control_type"),
                "raw_contribution": bundle.profile_buckets.get("control"),
                "provenance": "engine_context",
            }
        )
    return {
        "items": items,
        "summary": bundle.context.get("control_type") or unknown(),
        "bucket_total": bundle.profile_buckets.get("control"),
        "officer_count": bundle.context.get("officer_count"),
        "wealth_count": bundle.context.get("wealth_count"),
        "confidence": unknown(),
    }


def _drain_state(bundle: RuntimeBundle) -> dict[str, Any]:
    items = []
    if bundle.context.get("drain_type"):
        items.append(
            {
                "category": "output",
                "label": bundle.context.get("drain_type"),
                "raw_contribution": bundle.profile_buckets.get("drain"),
                "provenance": "engine_context",
            }
        )
    return {
        "items": items,
        "summary": bundle.context.get("drain_type") or unknown(),
        "bucket_total": bundle.profile_buckets.get("drain"),
        "output_count": bundle.context.get("output_count"),
        "confidence": unknown(),
    }


def _structural_state(bundle: RuntimeBundle) -> dict[str, Any]:
    items = []
    for rule in bundle.matched_rules:
        if rule.startswith("cmb_") or rule.startswith("spc_"):
            items.append(
                {
                    "type": "combination" if rule.startswith("cmb_") else "special_structure",
                    "rule_id": rule,
                    "resolution_status": "probable",
                    "participating_pillars": unknown(),
                    "participating_elements": unknown(),
                    "direction": unknown(),
                    "effect_on_strength": unknown(),
                    "confidence": unknown(),
                    "provenance": "matched_rules",
                }
            )
    return {
        "items": items,
        "combination_bucket": bundle.profile_buckets.get("combination"),
        "special_bucket": bundle.profile_buckets.get("special"),
        "clash": not_available_struct(),
        "punishment": not_available_struct(),
        "harm": not_available_struct(),
        "destruction": not_available_struct(),
        "follow_pattern": not_available_struct(),
        "summary": "partial_from_matched_rules" if items else "not_available",
        "confidence": unknown(),
    }


def not_available_struct() -> dict[str, Any]:
    return {"status": "not_available", "resolution_status": "not_applicable"}


def _temperature_state(bundle: RuntimeBundle) -> dict[str, Any]:
    temp = bundle.temperature or {}
    strength_temp = temp.get("from_strength_context") or temp.get("temperature_type")
    engine_temp = temp.get("from_temperature_engine")
    conflict = False
    if isinstance(engine_temp, dict) and strength_temp:
        eng_level = engine_temp.get("temperature_level")
        # only mark conflict when both present and string-differ; no semantic remapping
        if eng_level and str(eng_level).lower() != str(strength_temp).lower():
            # cold vs hot are different tokens — observable conflict
            conflict = True
    return {
        "temperature_state": strength_temp or unknown(),
        "heat_evidence": engine_temp if isinstance(engine_temp, dict) else None,
        "cold_evidence": strength_temp if strength_temp in {"cold"} else None,
        "dryness_evidence": None,
        "moisture_evidence": None,
        "temperature_conflict": conflict,
        "confidence": unknown(),
        "provenance": "strength_context_and_optional_temperature_engine",
        "notes": temp.get("note"),
    }


def _factor_lists(bundle: RuntimeBundle) -> tuple[list[str], list[str], list[str]]:
    supporting: list[str] = []
    opposing: list[str] = []
    for key, value in bundle.profile_buckets.items():
        if value is None:
            continue
        if value > 0:
            supporting.append(f"{key}:{value}")
        elif value < 0:
            opposing.append(f"{key}:{value}")
    dominant = (supporting + opposing)[:5]
    return dominant, supporting, opposing


def _uncertainty(bundle: RuntimeBundle, saturation: dict[str, Any]) -> str:
    parts = []
    if saturation.get("saturation_detected") is True:
        parts.append("score_saturation_observed")
    if bundle.population == "synthetic_stress":
        parts.append("synthetic_population")
    if not bundle.ledger and bundle.population == "synthetic_stress":
        parts.append("ledger_not_in_synthetic_result")
    parts.append("per_branch_root_loci_not_available")
    return ";".join(parts)


def _synthetic_flags(bundle: RuntimeBundle) -> dict[str, Any] | None:
    if bundle.population != "synthetic_stress":
        return None
    return {
        "synthetic": True,
        "calibration_eligible": False,
        "golden_eligible": False,
        "expert_calibration_eligible": False,
    }


def _external_labels(bundle: RuntimeBundle) -> dict[str, Any] | None:
    labels: dict[str, Any] = {
        "synthetic_expected_taxonomy": None,
        "expert_taxonomy_candidate": None,
        "note": "external only; not StrengthProfile taxonomy",
    }
    if bundle.synthetic_external:
        labels["synthetic_expected_taxonomy"] = bundle.synthetic_external.get(
            "synthetic_expected_taxonomy"
        )
    if bundle.expert_external:
        er1 = bundle.expert_external.get("expert_review_1") or {}
        er2 = bundle.expert_external.get("expert_review_2") or {}
        labels["expert_taxonomy_candidate"] = (
            er2.get("taxonomy_level")
            or er1.get("taxonomy_level_v2_candidate")
        )
        if isinstance(labels["expert_taxonomy_candidate"], str):
            labels["expert_taxonomy_candidate"] = labels["expert_taxonomy_candidate"].lower()
    return labels
