"""Build CommercialKnowledgeBundle from selected unit rows."""

from __future__ import annotations

from statistics import fmean
from typing import Any
from uuid import uuid4

from .models import (
    CAPABILITY_CAREER_SELECTION,
    CAREER_SELECTION_ALLOW_LIST,
    CAREER_SELECTION_FIELD_BY_KIND,
    CONTRACT_ID,
    CONTRACT_VERSION,
    PRODUCTION_ALLOW_LIST,
    WAVE_1_1_ALLOW_LIST,
    BundleItem,
    CareerSelectionAssessment,
    CommercialKnowledgeBundle,
    DroppedUnit,
    NarrativeEvidenceUnit,
    NarrativeKnowledgePayload,
    SelectedUnitSummary,
)


class BundleBuilder:
    """Assemble Narrative-facing bundle without exposing raw Knowledge Units."""

    def build(
        self,
        *,
        selected_rows: list[dict[str, Any]],
        dropped: list[tuple[str, str]],
        scenario_id: str,
        run_id: str = "",
        signals: dict[str, Any] | None = None,
    ) -> tuple[CommercialKnowledgeBundle, NarrativeKnowledgePayload]:
        """Build bundle + narrative payload from selected bound rows."""
        identity: list[BundleItem] = []
        strengths: list[BundleItem] = []
        weaknesses: list[BundleItem] = []
        useful_god: list[BundleItem] = []
        recommendations: list[BundleItem] = []
        warnings: list[BundleItem] = []
        opportunities: list[BundleItem] = []
        summaries: list[SelectedUnitSummary] = []
        evidence_units: list[NarrativeEvidenceUnit] = []
        career_fields: dict[str, BundleItem] = {}

        for row in selected_rows:
            item = _to_bundle_item(row)
            kind = item.evidence_kind
            if kind == "identity":
                identity.append(item)
            elif kind == "strength":
                strengths.append(item)
            elif kind == "weakness":
                weaknesses.append(item)
                warnings.append(item)
            elif kind == "explanation":
                useful_god.append(item)
            elif kind == "action":
                recommendations.append(item)
                if item.knowledge_unit_id in CAREER_SELECTION_ALLOW_LIST:
                    career_fields.setdefault("action_plan_90d", item)
            elif kind == "risk":
                warnings.append(item)
            elif kind in {"opportunity"} or "opportunity" in (row.get("opportunity_category") or ""):
                opportunities.append(item)

            field_name = CAREER_SELECTION_FIELD_BY_KIND.get(kind)
            if field_name and field_name not in career_fields:
                career_fields[field_name] = item
            if kind == "career_risk":
                warnings.append(item)

            summaries.append(
                SelectedUnitSummary(
                    knowledge_unit_id=item.knowledge_unit_id,
                    version=item.version,
                    evidence_kind=item.evidence_kind,
                    priority=_safe_int(row.get("priority"), 0),
                    confidence=item.confidence,
                    narrative_targets=item.component_targets,
                )
            )
            evidence_units.append(
                NarrativeEvidenceUnit(
                    evidence_kind=item.evidence_kind,
                    text=item.text,
                    knowledge_unit_id=item.knowledge_unit_id,
                    version=item.version,
                    component_targets=item.component_targets,
                    signal_refs=item.signal_refs,
                    confidence=item.confidence,
                )
            )

        career_selection = _build_career_selection(career_fields)
        confidences = [item.confidence for item in summaries]
        overall = round(fmean(confidences), 4) if confidences else 0.0
        if career_selection.status == "complete" or (identity and recommendations):
            status = "complete"
        elif summaries:
            status = "partial"
        else:
            status = "empty"

        bundle_id = f"ckb-{run_id}" if run_id else f"ckb-{uuid4().hex[:12]}"
        signal_keys = tuple(sorted((signals or {}).keys()))
        selected_ids = [item.knowledge_unit_id for item in summaries]
        bundle = CommercialKnowledgeBundle(
            contract_id=CONTRACT_ID,
            contract_version=CONTRACT_VERSION,
            bundle_id=bundle_id,
            scenario_id=scenario_id,
            bundle_status=status,
            identity=tuple(identity),
            strengths=tuple(strengths),
            weaknesses=tuple(weaknesses),
            useful_god=tuple(useful_god),
            recommendations=tuple(recommendations),
            warnings=tuple(warnings),
            opportunities=tuple(opportunities),
            career_selection=career_selection,
            confidence=overall,
            selected_units=tuple(summaries),
            dropped_units=tuple(
                DroppedUnit(knowledge_unit_id=unit_id, reason=reason)
                for unit_id, reason in dropped
                if unit_id in PRODUCTION_ALLOW_LIST
                or reason != "not_in_production_allow_list"
            ),
            traceability={
                "selected_knowledge_unit_ids": selected_ids,
                "career_selection_unit_ids": list(career_selection.knowledge_unit_ids),
                "signal_keys": list(signal_keys),
                "chain": [
                    "knowledge_unit",
                    "evidence",
                    "interpretation_enrichment",
                    "narrative",
                    "portal",
                ],
                "capability_chain": [
                    "knowledge_unit",
                    "commercial_bundle",
                    "narrative",
                    "portal",
                ],
                "capability_id": CAPABILITY_CAREER_SELECTION
                if career_selection.knowledge_unit_ids
                else "",
            },
            metadata={
                "wave": "W-P0-1.1-CORE+W-D01-C-SEL",
                "allow_list": sorted(PRODUCTION_ALLOW_LIST),
                "career_selection_allow_list": sorted(CAREER_SELECTION_ALLOW_LIST),
                "wave_1_1_allow_list": sorted(WAVE_1_1_ALLOW_LIST),
                "run_id": run_id,
                "capabilities": (
                    [CAPABILITY_CAREER_SELECTION]
                    if career_selection.knowledge_unit_ids
                    else []
                ),
            },
        )
        payload = NarrativeKnowledgePayload(
            evidence_units=tuple(evidence_units),
            bundle_id=bundle_id,
            bundle_status=status,
        )
        return bundle, payload


def bundle_to_dict(bundle: CommercialKnowledgeBundle) -> dict[str, Any]:
    """Serialize bundle for API without raw Knowledge Unit rows."""

    def _items(values: tuple[BundleItem, ...]) -> list[dict[str, Any]]:
        return [_item_dict(item) for item in values]

    payload = {
        "contract_id": bundle.contract_id,
        "contract_version": bundle.contract_version,
        "bundle_id": bundle.bundle_id,
        "scenario_id": bundle.scenario_id,
        "bundle_status": bundle.bundle_status,
        "identity": _items(bundle.identity),
        "strengths": _items(bundle.strengths),
        "weaknesses": _items(bundle.weaknesses),
        "useful_god": _items(bundle.useful_god),
        "recommendations": _items(bundle.recommendations),
        "warnings": _items(bundle.warnings),
        "opportunities": _items(bundle.opportunities),
        "confidence": bundle.confidence,
        "selected_units": [
            {
                "knowledge_unit_id": item.knowledge_unit_id,
                "version": item.version,
                "evidence_kind": item.evidence_kind,
                "priority": item.priority,
                "confidence": item.confidence,
                "narrative_targets": list(item.narrative_targets),
            }
            for item in bundle.selected_units
        ],
        "dropped_units": [
            {"knowledge_unit_id": item.knowledge_unit_id, "reason": item.reason}
            for item in bundle.dropped_units
        ],
        "traceability": dict(bundle.traceability),
        "metadata": dict(bundle.metadata),
    }
    if bundle.career_selection is not None:
        payload["career_selection_assessment"] = career_selection_to_dict(
            bundle.career_selection
        )
    return payload


def career_selection_to_dict(assessment: CareerSelectionAssessment) -> dict[str, Any]:
    """Serialize Career Selection Assessment for Portal / API."""

    def _optional(item: BundleItem | None) -> dict[str, Any] | None:
        return None if item is None else _item_dict(item)

    return {
        "capability_id": assessment.capability_id,
        "status": assessment.status,
        "career_direction": _optional(assessment.career_direction),
        "working_environment": _optional(assessment.working_environment),
        "preferred_role": _optional(assessment.preferred_role),
        "leadership_posture": _optional(assessment.leadership_posture),
        "employment_posture": _optional(assessment.employment_posture),
        "career_strengths": _optional(assessment.career_strengths),
        "career_risks": _optional(assessment.career_risks),
        "career_mitigation": _optional(assessment.career_mitigation),
        "development_focus": _optional(assessment.development_focus),
        "timing_guidance": _optional(assessment.timing_guidance),
        "action_plan_90d": _optional(assessment.action_plan_90d),
        "knowledge_unit_ids": list(assessment.knowledge_unit_ids),
    }


def _build_career_selection(fields: dict[str, BundleItem]) -> CareerSelectionAssessment:
    assessment = CareerSelectionAssessment(
        career_direction=fields.get("career_direction"),
        working_environment=fields.get("working_environment"),
        preferred_role=fields.get("preferred_role"),
        leadership_posture=fields.get("leadership_posture"),
        employment_posture=fields.get("employment_posture"),
        career_strengths=fields.get("career_strengths"),
        career_risks=fields.get("career_risks"),
        career_mitigation=fields.get("career_mitigation"),
        development_focus=fields.get("development_focus"),
        timing_guidance=fields.get("timing_guidance"),
        action_plan_90d=fields.get("action_plan_90d"),
    )
    ids = tuple(
        item.knowledge_unit_id
        for item in (
            assessment.career_direction,
            assessment.working_environment,
            assessment.preferred_role,
            assessment.leadership_posture,
            assessment.employment_posture,
            assessment.career_strengths,
            assessment.career_risks,
            assessment.career_mitigation,
            assessment.development_focus,
            assessment.timing_guidance,
            assessment.action_plan_90d,
        )
        if item is not None
    )
    assessment.knowledge_unit_ids = ids
    if (
        assessment.career_direction
        and assessment.action_plan_90d
        and assessment.career_risks
        and assessment.career_mitigation
    ):
        assessment.status = "complete"
    elif ids:
        assessment.status = "partial"
    else:
        assessment.status = "empty"
    return assessment


def _item_dict(item: BundleItem) -> dict[str, Any]:
    return {
        "text": item.text,
        "evidence_kind": item.evidence_kind,
        "knowledge_unit_id": item.knowledge_unit_id,
        "version": item.version,
        "component_targets": list(item.component_targets),
        "signal_refs": list(item.signal_refs),
        "confidence": item.confidence,
        "role": item.role,
    }


def _to_bundle_item(row: dict[str, Any]) -> BundleItem:
    targets = tuple(
        part.strip()
        for part in (row.get("narrative_targets") or "").replace(",", ";").split(";")
        if part.strip()
    )
    signal_refs = tuple(
        part.strip()
        for part in (row.get("signal_refs") or "").replace(",", ";").split(";")
        if part.strip()
    )
    return BundleItem(
        text=str(row.get("commercial_text") or "").strip(),
        evidence_kind=str(row.get("evidence_kind") or "").strip(),
        knowledge_unit_id=str(row.get("knowledge_unit_id") or "").strip(),
        version=str(row.get("version") or "1.0.0").strip(),
        component_targets=targets,
        signal_refs=signal_refs,
        confidence=float(row.get("confidence") or 0.0),
        role=str(row.get("kind") or "").strip(),
    )


def _safe_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
