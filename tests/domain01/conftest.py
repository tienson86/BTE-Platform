"""Golden Case analysis fixtures for Domain 01 production capabilities."""

from __future__ import annotations

from typing import Any

from engines.commercial_knowledge.models import (
    CAREER_SELECTION_ALLOW_LIST,
    PROMOTION_READINESS_ALLOW_LIST,
)

# Required Career Selection Assessment fields (capability contract).
CAREER_SELECTION_FIELDS: tuple[str, ...] = (
    "career_direction",
    "working_environment",
    "preferred_role",
    "leadership_posture",
    "employment_posture",
    "career_strengths",
    "career_risks",
    "career_mitigation",
    "development_focus",
    "timing_guidance",
    "action_plan_90d",
)

# Required Promotion Readiness Assessment fields.
PROMOTION_READINESS_FIELDS: tuple[str, ...] = (
    "promotion_readiness",
    "management_role_posture",
    "competency_gaps",
    "promotion_strengths",
    "advancement_posture",
    "timing_guidance",
    "advancement_window",
    "promotion_risks",
    "promotion_mitigation",
    "action_plan_90d",
)


def strong_employee_chart() -> dict[str, Any]:
    """D1-GC-STRONG-EMP / D1-GC-PROMOTE-READY — strong + useful god."""
    return {
        "bazi": {"day_master": "Giáp"},
        "pattern": {"cach_cuc": "Chính Quan", "dung_than": "Thủy"},
        "strength": {
            "strength_level": "vuong",
            "strength_score": 72,
            "reasoning": "matched rules strength table",
        },
        "useful_god": {
            "useful_god": "Thủy",
            "unfavorable_gods": [],
            "confidence": 0.8,
        },
        "score": {"strength_score": 72, "grade": "B+", "recommendation": "Thủy"},
    }


def weak_employee_chart() -> dict[str, Any]:
    """D1-GC-WEAK-EMP / D1-GC-PROMOTE-PREPARE — weak + enemy + useful god."""
    return {
        "bazi": {"day_master": "Ất"},
        "pattern": {"cach_cuc": "Thương Quan", "ky_than": "Hỏa", "dung_than": "Mộc"},
        "strength": {
            "strength_level": "nhuoc",
            "strength_score": 32,
            "reasoning": "structural thin band",
        },
        "useful_god": {
            "useful_god": "Mộc",
            "unfavorable_gods": ["Hỏa"],
            "confidence": 0.7,
        },
        "score": {"strength_score": 32, "grade": "C", "recommendation": "Mộc"},
    }


def mixed_employee_chart() -> dict[str, Any]:
    """D1-GC-MIXED-EMP / D1-GC-PROMOTE-MIXED — strong + enemy + useful god."""
    return {
        "bazi": {"day_master": "Bính"},
        "pattern": {"cach_cuc": "Kiến Lộc", "ky_than": "Thủy", "dung_than": "Thổ"},
        "strength": {
            "strength_level": "vuong",
            "strength_score": 68,
            "reasoning": "supported with opposition caution",
        },
        "useful_god": {
            "useful_god": "Thổ",
            "unfavorable_gods": ["Thủy"],
            "confidence": 0.75,
        },
        "score": {"strength_score": 68, "grade": "B", "recommendation": "Thổ"},
    }


def baseline_interpretation() -> dict[str, Any]:
    """Minimal Interpretation payload that must survive enrichment."""
    return {
        "sections": [
            {
                "section_id": "exec-base",
                "title": "Tóm tắt điều hành",
                "content": "Kết luận giải thích gốc từ Interpretation.",
            }
        ],
        "summary": "Baseline interpretation summary.",
    }


def assert_career_selection_complete(assessment: Any) -> None:
    """Assert all Career Selection Assessment fields are populated."""
    assert assessment is not None
    assert assessment.capability_id == "CAP-D1-CA-SEL"
    assert assessment.status in {"complete", "partial"}
    for field_name in CAREER_SELECTION_FIELDS:
        item = getattr(assessment, field_name)
        assert item is not None, f"missing field {field_name}"
        assert item.text.strip(), f"empty text for {field_name}"
        assert item.knowledge_unit_id in CAREER_SELECTION_ALLOW_LIST
    assert set(assessment.knowledge_unit_ids).issubset(CAREER_SELECTION_ALLOW_LIST)
    assert len(assessment.knowledge_unit_ids) == 11


def assert_promotion_readiness_complete(assessment: Any) -> None:
    """Assert all Promotion Readiness Assessment fields are populated."""
    assert assessment is not None
    assert assessment.capability_id == "CAP-D1-CA-PRO"
    assert assessment.status in {"complete", "partial"}
    for field_name in PROMOTION_READINESS_FIELDS:
        item = getattr(assessment, field_name)
        assert item is not None, f"missing field {field_name}"
        assert item.text.strip(), f"empty text for {field_name}"
        assert item.knowledge_unit_id in PROMOTION_READINESS_ALLOW_LIST
    assert set(assessment.knowledge_unit_ids).issubset(PROMOTION_READINESS_ALLOW_LIST)
    assert len(assessment.knowledge_unit_ids) == 10
