"""Merge CommercialKnowledgeBundle into Narrative inputs (enrich, do not replace)."""

from __future__ import annotations

import copy
from typing import Any

from .bundle_builder import career_selection_to_dict, promotion_readiness_to_dict
from .commercial_presentation import (
    build_executive_composition,
    commercialize_customer_text,
    format_primary_recommendation,
    format_secondary_promotion_milestone,
)
from .models import CommercialKnowledgeBundle, NarrativeKnowledgePayload
from .signal_projection import project_analysis_signals


def enrich_narrative_inputs(
    *,
    analysis: dict[str, Any] | None,
    interpretation: dict[str, Any] | None,
    bundle: CommercialKnowledgeBundle,
    payload: NarrativeKnowledgePayload,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Enrich analysis/interpretation copies for Narrative compose.

    Commercial V1 polish:
    - Career Strategy is primary Recommendation.
    - Promotion is secondary milestone only.
    - Executive Summary is 1 central + ≤3 supporting + 1 conclusion.
    - Customer-facing wording is commercialized (no technical BaZi dump).
    """
    analysis_out = copy.deepcopy(analysis) if isinstance(analysis, dict) else {}
    interpretation_out = (
        copy.deepcopy(interpretation) if isinstance(interpretation, dict) else {}
    )
    signals = project_analysis_signals(analysis_out)

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
                "body": commercialize_customer_text(unit.text, signals),
                "knowledge_unit_id": unit.knowledge_unit_id,
                "version": unit.version,
                "evidence_kind": unit.evidence_kind,
                "source": "commercial_knowledge_bundle",
                "bundle_id": payload.bundle_id,
            }
        )

    _enrich_analysis_from_bundle(analysis_out, bundle, signals)
    interpretation_out["commercial_knowledge_bundle_id"] = bundle.bundle_id
    interpretation_out["commercial_enrichment"] = True

    career = bundle.career_selection
    promotion = bundle.promotion_readiness
    executive = build_executive_composition(career, promotion)
    primary = format_primary_recommendation(career=career)
    secondary = format_secondary_promotion_milestone(promotion)

    interpretation_out["commercial_executive_summary"] = executive
    interpretation_out["primary_recommendation"] = primary
    if secondary:
        interpretation_out["secondary_career_milestone"] = secondary

    if career and career.knowledge_unit_ids:
        interpretation_out["career_selection_assessment"] = career_selection_to_dict(
            career
        )
        interpretation_out["career_selection_capability_id"] = career.capability_id
        interpretation_out["career_selection_label"] = "Career Selection Assessment"
    if promotion and promotion.knowledge_unit_ids:
        interpretation_out["promotion_readiness_assessment"] = (
            promotion_readiness_to_dict(promotion)
        )
        interpretation_out["promotion_readiness_capability_id"] = (
            promotion.capability_id
        )
        interpretation_out["promotion_readiness_label"] = (
            "Promotion Readiness Assessment"
        )
    return analysis_out, interpretation_out


def _section_title(evidence_kind: str, targets: tuple[str, ...]) -> str:
    """Title heuristics so Narrative component_selector can bind refs."""
    titles = {
        "identity": "Tổng quan danh tính thương mại",
        "strength": "Tổng quan điểm mạnh",
        "weakness": "Lưu ý điểm hạn chế",
        "explanation": "Lý giải trục hỗ trợ",
        "action": "Kế hoạch nghề 90 ngày",
        "career_direction": "Career Selection — hướng nghề",
        "career_environment": "Career Selection — môi trường",
        "career_org_role": "Career Selection — vai trò",
        "career_lead_vs_spec": "Career Selection — tư thế chuyên môn",
        "career_path_mode": "Career Selection — làm thuê hay độc lập",
        "career_advantage": "Career Selection — lợi thế",
        "career_risk": "Career Selection — rủi ro",
        "career_mitigation": "Career Selection — giảm rủi ro",
        "career_development": "Career Selection — phát triển",
        "career_timing": "Career Selection — nhịp quyết định",
        "promotion_readiness": "Promotion Readiness — sẵn sàng",
        "promotion_mgmt_role": "Promotion Readiness — vai trò quản lý",
        "promotion_competency_gaps": "Promotion Readiness — khoảng trống năng lực",
        "promotion_strengths": "Promotion Readiness — lợi thế",
        "promotion_posture": "Promotion Readiness — tư thế",
        "promotion_timing": "Promotion Readiness — nhịp",
        "promotion_window": "Promotion Readiness — cửa sổ",
        "promotion_risk": "Promotion Readiness — rủi ro",
        "promotion_mitigation": "Promotion Readiness — giảm rủi ro",
        "promotion_action_90d": "Promotion Readiness — mốc 90 ngày",
    }
    if evidence_kind in titles:
        return titles[evidence_kind]
    if "warning" in targets:
        return "Lưu ý thương mại"
    return "Tri thức thương mại"


def _enrich_analysis_from_bundle(
    analysis: dict[str, Any],
    bundle: CommercialKnowledgeBundle,
    signals: dict[str, Any] | None = None,
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

    career = bundle.career_selection
    promotion = bundle.promotion_readiness
    executive = build_executive_composition(career, promotion)
    primary = format_primary_recommendation(
        career=career,
        wave_recommendation=(
            bundle.recommendations[0].text if bundle.recommendations else ""
        ),
    )
    secondary = format_secondary_promotion_milestone(promotion)

    # P0-03: replace dense concatenation with structured Exec composition.
    if executive.get("composed_text"):
        strength["reasoning"] = executive["composed_text"]
        strength["commercial_executive_summary"] = executive
        if career and career.career_direction:
            strength["commercial_knowledge_unit_id"] = (
                career.career_direction.knowledge_unit_id
            )

    if career and career.career_strengths:
        strength["commercial_career_strengths"] = commercialize_customer_text(
            career.career_strengths.text, signals
        )
    if career and career.career_direction:
        strength["commercial_career_direction"] = commercialize_customer_text(
            career.career_direction.text, signals
        )

    if career and career.career_risks:
        risk_text = commercialize_customer_text(career.career_risks.text, signals)
        useful["commercial_weakness_text"] = risk_text
        strength["commercial_weakness_text"] = risk_text
        score["commercial_weakness"] = risk_text
        if career.career_mitigation:
            score["commercial_mitigation"] = commercialize_customer_text(
                career.career_mitigation.text, signals
            )

    # Promotion metadata only — must not overwrite Exec reasoning.
    if promotion and promotion.promotion_readiness:
        strength["commercial_promotion_readiness"] = commercialize_customer_text(
            promotion.promotion_readiness.text, signals
        )
    if promotion and promotion.promotion_risks:
        useful["commercial_promotion_risk"] = commercialize_customer_text(
            promotion.promotion_risks.text, signals
        )
        score["commercial_promotion_risk"] = useful["commercial_promotion_risk"]
        if promotion.promotion_mitigation:
            score["commercial_promotion_mitigation"] = commercialize_customer_text(
                promotion.promotion_mitigation.text, signals
            )

    if bundle.strengths and not (career and career.career_direction):
        commercial = commercialize_customer_text(bundle.strengths[0].text, signals)
        existing = str(strength.get("reasoning") or "").strip()
        if existing and not _is_commercial_marker(existing):
            strength["reasoning"] = f"{commercial} {existing}".strip()
        else:
            strength["reasoning"] = commercial
        strength["commercial_knowledge_unit_id"] = bundle.strengths[0].knowledge_unit_id

    if bundle.weaknesses and not (career and career.career_risks):
        commercial = commercialize_customer_text(bundle.weaknesses[0].text, signals)
        useful["unfavorable_gods"] = useful.get("unfavorable_gods") or []
        if isinstance(useful["unfavorable_gods"], list):
            useful["commercial_weakness_text"] = commercial
        strength.setdefault("commercial_weakness_text", commercial)
        score["commercial_weakness"] = commercial

    if bundle.useful_god:
        useful["commercial_explanation"] = commercialize_customer_text(
            bundle.useful_god[0].text, signals
        )
        useful["commercial_knowledge_unit_id"] = bundle.useful_god[0].knowledge_unit_id

    # P0-01 / P0-05: Career Strategy is primary Rec (structured).
    if primary.get("composed_text"):
        existing_rec = str(score.get("recommendation") or "").strip()
        if existing_rec and _looks_like_code(existing_rec):
            score["analytical_recommendation"] = existing_rec
        elif existing_rec and not score.get("analytical_recommendation"):
            score["analytical_recommendation"] = existing_rec
        score["recommendation"] = primary["composed_text"]
        score["primary_recommendation"] = primary
        score["commercial_knowledge_unit_id"] = (
            career.action_plan_90d.knowledge_unit_id
            if career and career.action_plan_90d
            else score.get("commercial_knowledge_unit_id")
        )
        useful["commercial_recommendation"] = primary["composed_text"]
    elif bundle.recommendations:
        # Wave 1.1-only recommendation path.
        rec_item = bundle.recommendations[0]
        rec = commercialize_customer_text(rec_item.text, signals)
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

    # P0-01: Promotion is secondary milestone only.
    if secondary:
        score["secondary_recommendation"] = secondary["composed_text"]
        score["secondary_career_milestone"] = secondary
        useful["commercial_secondary_milestone"] = secondary["composed_text"]


def _is_commercial_marker(text: str) -> bool:
    return (
        "trục hỗ trợ" in text
        or "Dụng thần" in text
        or "nền tảng ngày" in text
        or "Nhật chủ" in text
        or "Điểm tựa" in text
        or "Họ nghề" in text
        or "What:" in text
        or "Kế hoạch 90 ngày" in text
    )


def _looks_like_code(text: str) -> bool:
    """Heuristic: short token / enum-like analytical codes."""
    cleaned = text.strip()
    if len(cleaned) <= 12 and " " not in cleaned:
        return True
    return cleaned.isupper() or cleaned.islower() and len(cleaned.split()) == 1
