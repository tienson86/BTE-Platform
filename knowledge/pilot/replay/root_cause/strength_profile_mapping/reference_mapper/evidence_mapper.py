"""Evidence mapping from observed runtime fields only."""

from __future__ import annotations

from typing import Any

from .ascii_utils import SCHEMA_VERSION
from .provenance_mapper import map_provenance
from .source_reader import RuntimeBundle


def map_evidence(bundle: RuntimeBundle) -> list[dict[str, Any]]:
    """Create StrengthEvidence records from available runtime observations."""
    records: list[dict[str, Any]] = []
    records.extend(_from_ledger(bundle))
    if not records:
        records.extend(_from_buckets_and_context(bundle))
    return records


def _mag_raw(value: float | None) -> dict[str, Any]:
    if value is None:
        return {
            "representation": "unknown",
            "ordinal": None,
            "categorical": None,
            "raw_contribution": None,
            "normalized": None,
            "bounded_contribution": None,
            "unit_note": None,
        }
    return {
        "representation": "raw_contribution",
        "ordinal": None,
        "categorical": None,
        "raw_contribution": value,
        "normalized": None,
        "bounded_contribution": None,
        "unit_note": "engine_bucket_or_ledger_score",
    }


def _polarity_from_runtime(runtime_polarity: str | None, score: float | None) -> str:
    if runtime_polarity == "strengthen":
        return "positive"
    if runtime_polarity == "weaken":
        return "negative"
    if score is None:
        return "unknown"
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"


def _direction_from_group(group: str | None, score: float | None) -> str:
    g = (group or "").lower()
    if g in {"season", "root", "support", "special", "combination"}:
        if score is None:
            return "unknown"
        if score > 0:
            return "support"
        if score < 0:
            return "pressure" if g == "season" else "drain" if g == "combination" else "pressure"
        return "neutral"
    if g in {"control"}:
        return "pressure"
    if g in {"drain", "flow"}:
        return "drain"
    return "unknown"


def _dimension_from_group(group: str | None, rule_id: str | None) -> str:
    g = (group or "").lower()
    rid = (rule_id or "").lower()
    if g == "season":
        return "seasonal_strength"
    if g == "root":
        return "rooting"
    if g == "support":
        if "an" in rid or rid.startswith("sup_002") or rid.startswith("sup_006"):
            return "resource_support"
        return "same_element_support"
    if g == "control":
        if "006" in rid or "that" in rid:
            return "officer_pressure"
        return "officer_pressure"
    if g in {"drain", "flow"}:
        return "output_drain"
    if g == "combination":
        return "combination"
    if g == "special":
        return "special_structure"
    return "other"


def _from_ledger(bundle: RuntimeBundle) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in bundle.ledger:
        rule_id = str(item.get("rule_id") or "UNKNOWN")
        group = str(item.get("group") or "other")
        score = item.get("score")
        try:
            score_f = float(score) if score is not None else None
        except (TypeError, ValueError):
            score_f = None
        evid_id = f"EV-{rule_id.upper().replace('_', '-')}"
        out.append(
            {
                "schema_version": SCHEMA_VERSION,
                "evidence_id": evid_id,
                "evidence_type": _evidence_type(group),
                "dimension": _dimension_from_group(group, rule_id),
                "source": "strength_evidence_ledger",
                "source_path": bundle.source_paths.get("evidence"),
                "direction": _direction_from_group(group, score_f),
                "magnitude": _mag_raw(score_f),
                "polarity": _polarity_from_runtime(item.get("runtime_polarity"), score_f),
                "confidence": "unknown",
                "provenance": map_provenance(
                    bundle,
                    provenance_class="engine_rule",
                    availability="observed",
                    rule_id=rule_id,
                    source_path=bundle.source_paths.get("evidence"),
                ),
                "explanation": item.get("reason"),
                "affected_element": bundle.context.get("day_master_element"),
                "affected_day_master": bundle.day_master,
                "pillar_scope": "unknown",
                "branch_scope": bundle.context.get("month_branch") or "unknown",
                "stem_scope": None,
                "seasonal_context": {"month_status": bundle.context.get("month_status")}
                if group == "season"
                else None,
                "interaction_context": None,
                "availability": "observed",
                "completeness": "partial",
                "information_loss": "compressed",
            }
        )
    return out


def _evidence_type(group: str) -> str:
    g = group.lower()
    return {
        "season": "seasonal",
        "root": "rooting",
        "support": "support",
        "control": "pressure",
        "drain": "drain",
        "flow": "drain",
        "combination": "structural",
        "special": "structural",
    }.get(g, "other")


def _from_buckets_and_context(bundle: RuntimeBundle) -> list[dict[str, Any]]:
    """Synthetic results expose buckets + context without full ledger."""
    out: list[dict[str, Any]] = []
    buckets = bundle.profile_buckets
    mapping = [
        ("season", "seasonal", "seasonal_strength", "EV-BUCKET-SEASON"),
        ("root", "rooting", "rooting", "EV-BUCKET-ROOT"),
        ("support", "support", "same_element_support", "EV-BUCKET-SUPPORT"),
        ("drain", "drain", "output_drain", "EV-BUCKET-DRAIN"),
        ("control", "pressure", "officer_pressure", "EV-BUCKET-CONTROL"),
        ("combination", "structural", "combination", "EV-BUCKET-COMBINATION"),
        ("special", "structural", "special_structure", "EV-BUCKET-SPECIAL"),
    ]
    for key, etype, dim, evid_id in mapping:
        value = buckets.get(key)
        if value is None:
            continue
        # Skip exact zeros only if we still want presence? Keep zeros as observed neutral.
        out.append(
            {
                "schema_version": SCHEMA_VERSION,
                "evidence_id": evid_id,
                "evidence_type": etype,
                "dimension": dim,
                "source": "runtime.profile",
                "source_path": bundle.source_paths.get("result"),
                "direction": _direction_from_group(key, value),
                "magnitude": _mag_raw(value),
                "polarity": _polarity_from_runtime(None, value),
                "confidence": "unknown",
                "provenance": map_provenance(
                    bundle,
                    provenance_class="derived",
                    availability="observed",
                    source_path=bundle.source_paths.get("result"),
                ),
                "explanation": f"observed_{key}_bucket",
                "affected_element": bundle.context.get("day_master_element"),
                "affected_day_master": bundle.day_master,
                "pillar_scope": "unknown",
                "branch_scope": bundle.context.get("month_branch") or "unknown",
                "stem_scope": None,
                "seasonal_context": {"month_status": bundle.context.get("month_status"), "season": bundle.context.get("season")}
                if key == "season"
                else None,
                "interaction_context": None,
                "availability": "observed",
                "completeness": "partial",
                "information_loss": "compressed",
            }
        )
    # Context labels as categorical evidence (no invented magnitude).
    for field, dim, etype, evid_id in (
        ("root_level", "rooting", "rooting", "EV-CTX-ROOT-LEVEL"),
        ("support_type", "same_element_support", "support", "EV-CTX-SUPPORT-TYPE"),
        ("control_type", "officer_pressure", "pressure", "EV-CTX-CONTROL-TYPE"),
        ("drain_type", "output_drain", "drain", "EV-CTX-DRAIN-TYPE"),
    ):
        label = bundle.context.get(field)
        if not label:
            continue
        out.append(
            {
                "schema_version": SCHEMA_VERSION,
                "evidence_id": evid_id,
                "evidence_type": etype,
                "dimension": dim,
                "source": f"runtime.context.{field}",
                "source_path": bundle.source_paths.get("result") or bundle.source_paths.get("evidence"),
                "direction": "unknown",
                "magnitude": {
                    "representation": "categorical",
                    "ordinal": None,
                    "categorical": str(label),
                    "raw_contribution": None,
                    "normalized": None,
                    "bounded_contribution": None,
                    "unit_note": "context_label_only",
                },
                "polarity": "unknown",
                "confidence": "unknown",
                "provenance": map_provenance(
                    bundle,
                    provenance_class="derived",
                    availability="observed",
                ),
                "explanation": f"context_{field}",
                "affected_element": bundle.context.get("day_master_element"),
                "affected_day_master": bundle.day_master,
                "pillar_scope": "unknown",
                "branch_scope": bundle.context.get("month_branch") or "unknown",
                "stem_scope": None,
                "seasonal_context": None,
                "interaction_context": None,
                "availability": "observed",
                "completeness": "partial",
                "information_loss": "partially_preserved",
            }
        )
    return out
