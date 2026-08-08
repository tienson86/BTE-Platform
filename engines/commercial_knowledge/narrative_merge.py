"""Merge CommercialKnowledgeBundle into Narrative inputs (enrich, do not replace)."""

from __future__ import annotations

import copy
from typing import Any

from .models import CommercialKnowledgeBundle, NarrativeKnowledgePayload


def enrich_narrative_inputs(
    *,
    analysis: dict[str, Any] | None,
    interpretation: dict[str, Any] | None,
    bundle: CommercialKnowledgeBundle,
    payload: NarrativeKnowledgePayload,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Enrich analysis/interpretation copies for Narrative compose.

    - Does not overwrite Interpretation conclusion fields with empty values.
    - Adds commercial sections and soft-enriches analysis prose fields.
    - Preserves original interpretation sections (append-only).
    """
    analysis_out = copy.deepcopy(analysis) if isinstance(analysis, dict) else {}
    interpretation_out = (
        copy.deepcopy(interpretation) if isinstance(interpretation, dict) else {}
    )

    sections = interpretation_out.get("sections")
    if not isinstance(sections, list):
        sections = []
        interpretation_out["sections"] = sections

    for unit in payload.evidence_units:
        section_id = f"ck-{unit.knowledge_unit_id}"
        title = _section_title(unit.evidence_kind, unit.component_targets)
        sections.append(
            {
                "id": section_id,
                "title": title,
                "body": unit.text,
                "knowledge_unit_id": unit.knowledge_unit_id,
                "version": unit.version,
                "evidence_kind": unit.evidence_kind,
                "source": "commercial_knowledge_bundle",
                "bundle_id": payload.bundle_id,
            }
        )

    _enrich_analysis_from_bundle(analysis_out, bundle)
    interpretation_out["commercial_knowledge_bundle_id"] = bundle.bundle_id
    interpretation_out["commercial_enrichment"] = True
    return analysis_out, interpretation_out


def _section_title(evidence_kind: str, targets: tuple[str, ...]) -> str:
    """Title heuristics so Narrative component_selector can bind refs."""
    if evidence_kind == "identity":
        return "Tổng quan danh tính thương mại"
    if evidence_kind == "strength":
        return "Tổng quan điểm mạnh"
    if evidence_kind == "weakness":
        return "Lưu ý điểm hạn chế"
    if evidence_kind == "explanation":
        return "Lý giải dụng thần"
    if evidence_kind == "action":
        return "Khuyến nghị hành động"
    if "warning" in targets:
        return "Lưu ý thương mại"
    return "Tri thức thương mại"


def _enrich_analysis_from_bundle(
    analysis: dict[str, Any],
    bundle: CommercialKnowledgeBundle,
) -> None:
    """Soft-enrich analysis fields Narrative source_factory already reads."""
    strength = analysis.setdefault("strength", {})
    if not isinstance(strength, dict):
        analysis["strength"] = {}
        strength = analysis["strength"]
    useful = analysis.setdefault("useful_god", {})
    if not isinstance(useful, dict):
        analysis["useful_god"] = {}
        useful = analysis["useful_god"]
    score = analysis.setdefault("score", {})
    if not isinstance(score, dict):
        analysis["score"] = {}
        score = analysis["score"]
    bazi = analysis.setdefault("bazi", {})
    if not isinstance(bazi, dict):
        analysis["bazi"] = {}
        bazi = analysis["bazi"]

    if bundle.identity and not bazi.get("day_master"):
        # Structural identity still required; do not invent day master labels.
        pass

    if bundle.strengths:
        # Enrich reasoning with commercial strength text (do not clear existing).
        commercial = bundle.strengths[0].text
        existing = str(strength.get("reasoning") or "").strip()
        if existing and not _is_commercial_marker(existing):
            strength["reasoning"] = f"{commercial} {existing}".strip()
        else:
            strength["reasoning"] = commercial
        strength["commercial_knowledge_unit_id"] = bundle.strengths[0].knowledge_unit_id

    if bundle.weaknesses:
        commercial = bundle.weaknesses[0].text
        # Provide commercial weakness as structured list text Narrative can surface.
        useful["unfavorable_gods"] = useful.get("unfavorable_gods") or []
        if isinstance(useful["unfavorable_gods"], list):
            # Keep analytical gods; attach commercial note separately.
            useful["commercial_weakness_text"] = commercial
        strength.setdefault("commercial_weakness_text", commercial)
        # Also seed explanation-style weakness via score side-channel for composers.
        score["commercial_weakness"] = commercial

    if bundle.useful_god:
        useful["commercial_explanation"] = bundle.useful_god[0].text
        useful["commercial_knowledge_unit_id"] = bundle.useful_god[0].knowledge_unit_id
        # Prefer commercial explanation as reasoning enrichment when empty.
        if not str(strength.get("reasoning") or "").strip():
            strength["reasoning"] = bundle.useful_god[0].text

    if bundle.recommendations:
        rec = bundle.recommendations[0].text
        # Enrich recommendation — do not wipe analytical useful_god code.
        existing_rec = str(score.get("recommendation") or "").strip()
        if existing_rec and _looks_like_code(existing_rec):
            score["recommendation"] = rec
            score["analytical_recommendation"] = existing_rec
        elif not existing_rec:
            score["recommendation"] = rec
        else:
            # Keep analytical sentence; commercial takes precedence for Narrative value.
            score["analytical_recommendation"] = existing_rec
            score["recommendation"] = rec
        score["commercial_knowledge_unit_id"] = bundle.recommendations[0].knowledge_unit_id
        useful["commercial_recommendation"] = rec


def _is_commercial_marker(text: str) -> bool:
    return "Dụng thần" in text or "Nhật chủ" in text or "Điểm tựa" in text


def _looks_like_code(text: str) -> bool:
    """Heuristic: short token / enum-like analytical codes."""
    cleaned = text.strip()
    if len(cleaned) <= 12 and " " not in cleaned:
        return True
    return cleaned.isupper() or cleaned.islower() and len(cleaned.split()) == 1
