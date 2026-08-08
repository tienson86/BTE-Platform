"""Merge CommercialKnowledgeBundle into Narrative inputs (enrich, do not replace)."""

from __future__ import annotations

import copy
from typing import Any

from .bundle_builder import career_selection_to_dict
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
    - Attaches Career Selection Assessment projection for Portal (no raw KUs).
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
    if bundle.career_selection and bundle.career_selection.knowledge_unit_ids:
        interpretation_out["career_selection_assessment"] = career_selection_to_dict(
            bundle.career_selection
        )
        interpretation_out["career_selection_capability_id"] = (
            bundle.career_selection.capability_id
        )
    return analysis_out, interpretation_out


def _section_title(evidence_kind: str, targets: tuple[str, ...]) -> str:
    """Title heuristics so Narrative component_selector can bind refs."""
    titles = {
        "identity": "Tổng quan danh tính thương mại",
        "strength": "Tổng quan điểm mạnh",
        "weakness": "Lưu ý điểm hạn chế",
        "explanation": "Lý giải dụng thần",
        "action": "Kế hoạch nghề 90 ngày",
        "career_direction": "Hướng nghề nghiệp",
        "career_environment": "Môi trường làm việc",
        "career_org_role": "Vai trò tổ chức",
        "career_lead_vs_spec": "Lãnh đạo hay chuyên gia",
        "career_path_mode": "Làm thuê hay độc lập",
        "career_advantage": "Lợi thế nghề",
        "career_risk": "Rủi ro nghề",
        "career_mitigation": "Giảm rủi ro nghề",
        "career_development": "Ưu tiên phát triển nghề",
        "career_timing": "Nhịp quyết định nghề",
    }
    if evidence_kind in titles:
        return titles[evidence_kind]
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
        pass

    career = bundle.career_selection
    if career and career.career_direction:
        # Soft-enrich identity-facing reasoning without wiping Analysis.
        direction = career.career_direction.text
        existing = str(strength.get("reasoning") or "").strip()
        if existing and direction not in existing:
            strength["reasoning"] = f"{direction} {existing}".strip()
        elif not existing:
            strength["reasoning"] = direction
        strength["commercial_career_direction"] = direction
        strength["commercial_knowledge_unit_id"] = career.career_direction.knowledge_unit_id

    if career and career.career_strengths:
        advantage = career.career_strengths.text
        existing = str(strength.get("reasoning") or "").strip()
        if existing and advantage not in existing:
            strength["reasoning"] = f"{existing} {advantage}".strip()
        elif not existing:
            strength["reasoning"] = advantage
        strength["commercial_career_strengths"] = advantage

    if career and career.career_risks:
        useful["commercial_weakness_text"] = career.career_risks.text
        strength["commercial_weakness_text"] = career.career_risks.text
        score["commercial_weakness"] = career.career_risks.text
        if career.career_mitigation:
            score["commercial_mitigation"] = career.career_mitigation.text

    if bundle.strengths and not (career and career.career_direction):
        commercial = bundle.strengths[0].text
        existing = str(strength.get("reasoning") or "").strip()
        if existing and not _is_commercial_marker(existing):
            strength["reasoning"] = f"{commercial} {existing}".strip()
        else:
            strength["reasoning"] = commercial
        strength["commercial_knowledge_unit_id"] = bundle.strengths[0].knowledge_unit_id

    if bundle.weaknesses and not (career and career.career_risks):
        commercial = bundle.weaknesses[0].text
        useful["unfavorable_gods"] = useful.get("unfavorable_gods") or []
        if isinstance(useful["unfavorable_gods"], list):
            useful["commercial_weakness_text"] = commercial
        strength.setdefault("commercial_weakness_text", commercial)
        score["commercial_weakness"] = commercial

    if bundle.useful_god:
        useful["commercial_explanation"] = bundle.useful_god[0].text
        useful["commercial_knowledge_unit_id"] = bundle.useful_god[0].knowledge_unit_id
        if not str(strength.get("reasoning") or "").strip():
            strength["reasoning"] = bundle.useful_god[0].text

    # Prefer Career 90-day action when present; else Wave 1.1 recommendations.
    rec_item = None
    if career and career.action_plan_90d:
        rec_item = career.action_plan_90d
    elif bundle.recommendations:
        rec_item = bundle.recommendations[0]
    if rec_item is not None:
        rec = rec_item.text
        existing_rec = str(score.get("recommendation") or "").strip()
        if existing_rec and _looks_like_code(existing_rec):
            score["recommendation"] = rec
            score["analytical_recommendation"] = existing_rec
        elif not existing_rec:
            score["recommendation"] = rec
        else:
            score["analytical_recommendation"] = existing_rec
            score["recommendation"] = rec
        score["commercial_knowledge_unit_id"] = rec_item.knowledge_unit_id
        useful["commercial_recommendation"] = rec


def _is_commercial_marker(text: str) -> bool:
    return (
        "Dụng thần" in text
        or "Nhật chủ" in text
        or "Điểm tựa" in text
        or "Họ nghề" in text
        or "Kế hoạch 90 ngày" in text
    )


def _looks_like_code(text: str) -> bool:
    """Heuristic: short token / enum-like analytical codes."""
    cleaned = text.strip()
    if len(cleaned) <= 12 and " " not in cleaned:
        return True
    return cleaned.isupper() or cleaned.islower() and len(cleaned.split()) == 1
