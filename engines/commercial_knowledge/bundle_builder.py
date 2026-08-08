"""Build CommercialKnowledgeBundle from selected unit rows."""

from __future__ import annotations

from statistics import fmean
from typing import Any
from uuid import uuid4

from .models import (
    CONTRACT_ID,
    CONTRACT_VERSION,
    BundleItem,
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
            elif kind == "risk":
                warnings.append(item)
            elif kind in {"opportunity"} or "opportunity" in (row.get("opportunity_category") or ""):
                opportunities.append(item)

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

        confidences = [item.confidence for item in summaries]
        overall = round(fmean(confidences), 4) if confidences else 0.0
        if identity and recommendations:
            status = "complete"
        elif summaries:
            status = "partial"
        else:
            status = "empty"

        bundle_id = f"ckb-{run_id}" if run_id else f"ckb-{uuid4().hex[:12]}"
        signal_keys = tuple(sorted((signals or {}).keys()))
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
            confidence=overall,
            selected_units=tuple(summaries),
            dropped_units=tuple(
                DroppedUnit(knowledge_unit_id=unit_id, reason=reason)
                for unit_id, reason in dropped
                if unit_id in {
                    "KU-ID-001",
                    "KU-ST-001",
                    "KU-WK-001",
                    "KU-UG-001",
                    "KU-RC-001",
                }
                or reason != "not_in_wave_1_1_allow_list"
            ),
            traceability={
                "selected_knowledge_unit_ids": [item.knowledge_unit_id for item in summaries],
                "signal_keys": list(signal_keys),
                "chain": [
                    "knowledge_unit",
                    "evidence",
                    "interpretation_enrichment",
                    "narrative",
                    "portal",
                ],
            },
            metadata={
                "wave": "W-P0-1.1-CORE",
                "allow_list": sorted(
                    [
                        "KU-ID-001",
                        "KU-ST-001",
                        "KU-WK-001",
                        "KU-UG-001",
                        "KU-RC-001",
                    ]
                ),
                "run_id": run_id,
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
        return [
            {
                "text": item.text,
                "evidence_kind": item.evidence_kind,
                "knowledge_unit_id": item.knowledge_unit_id,
                "version": item.version,
                "component_targets": list(item.component_targets),
                "signal_refs": list(item.signal_refs),
                "confidence": item.confidence,
                "role": item.role,
            }
            for item in values
        ]

    return {
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
