"""Customer-safe and Pack 07 snapshot views of MingJuDecisionResult."""

from __future__ import annotations

from typing import Any

from engines.mingju.models import MingJuDecisionResult, ProfileDimension
from engines.mingju.serialization import to_jsonable


def _dimension_public(item: ProfileDimension) -> dict[str, Any]:
    return {
        "dimension": item.dimension,
        "classification": item.classification,
        "score": item.score,
        "polarity": item.polarity,
    }


def to_public_dict(result: MingJuDecisionResult) -> dict[str, Any]:
    """Customer JSON. No traces, hashes, or debug IDs."""
    return {
        "schema_version": result.schema_version,
        "ruleset_version": result.ruleset_version,
        "status": result.status,
        "confidence": result.confidence,
        "pattern": {
            "id": result.pattern.pattern_id,
            "label": result.pattern.label,
            "family": result.pattern.family,
            "source": result.pattern.source,
        },
        "purity": {
            "state": result.purity.state,
            "classification": result.purity.classification,
            "score": result.purity.score,
        },
        "pattern_strength": {
            "state": result.pattern_strength.state,
            "classification": result.pattern_strength.classification,
            "score": result.pattern_strength.score,
        },
        "damage": [
            {
                "damage_type": item.damage_type,
                "source": item.source,
                "target": item.target,
                "severity": item.severity,
            }
            for item in result.damage.findings
        ],
        "rescue": [
            {
                "rescue_type": item.rescue_type,
                "source": item.source,
                "strength": item.strength,
            }
            for item in result.rescue.findings
        ],
        "integrity": {
            "state": result.integrity.state,
            "classification": result.integrity.classification,
            "score": result.integrity.score,
            "residual_damage": result.integrity.residual_damage,
        },
        "grade": {
            "grade": result.grade.grade,
            "score": result.grade.score,
            "integrity_state": result.grade.integrity_state,
            "basis": result.grade.basis,
        },
        "achievement": {
            "state": result.achievement.state,
            "dominant_capabilities": list(result.achievement.dominant_capabilities),
            "dimensions": [_dimension_public(item) for item in result.achievement.dimensions],
        },
        "wealth": {
            "state": result.wealth.state,
            "dimensions": [_dimension_public(item) for item in result.wealth.dimensions],
        },
        "career": {
            "state": result.career.state,
            "dominant_work_styles": list(result.career.dominant_work_styles),
            "dimensions": [_dimension_public(item) for item in result.career.dimensions],
        },
        "decision": {
            "headline": result.decision.headline,
            "summary": result.decision.summary,
            "strengths": list(result.decision.strengths),
            "risks": list(result.decision.risks),
            "conditions": list(result.decision.conditions),
        },
    }


def to_pack07_snapshot(result: MingJuDecisionResult) -> dict[str, Any]:
    """Structural identifiers consumed by Pack 07 attach_mc01_reference."""
    achievement_ref = ",".join(result.achievement.dominant_capabilities) or result.achievement.state
    wealth_ref = next(
        (
            f"{item.dimension}:{item.classification}"
            for item in result.wealth.dimensions
            if item.dimension == "wealth_creation"
        ),
        result.wealth.state,
    )
    career_ref = ",".join(result.career.dominant_work_styles) or result.career.state
    return {
        "schema_version": result.schema_version,
        "ruleset_version": result.ruleset_version,
        "result_id": result.result_id,
        "content_hash": result.content_hash,
        "status": result.status,
        "analysis_id": result.analysis_id,
        "chart_id": result.chart_id,
        "pattern": result.pattern.label or result.pattern.pattern_id,
        "pattern_id": result.pattern.pattern_id,
        "purity": result.purity.classification,
        "pattern_strength": result.pattern_strength.classification,
        "damage_ids": [item.damage_id for item in result.damage.findings],
        "rescue_ids": [item.rescue_id for item in result.rescue.findings],
        "damage": [
            {"damage_id": item.damage_id, "damage_type": item.damage_type, "severity": item.severity}
            for item in result.damage.findings
        ],
        "rescue": [
            {
                "rescue_id": item.rescue_id,
                "rescue_type": item.rescue_type,
                "target_damage_ids": list(item.target_damage_ids),
            }
            for item in result.rescue.findings
        ],
        "integrity": result.integrity.state,
        "grade": result.grade.grade,
        "achievement": achievement_ref,
        "wealth_profile": wealth_ref,
        "career_profile": career_ref,
        "source": "mingju_decision_engine",
        "source_versions": dict(result.source_versions),
    }


def customer_structure_labels(result: MingJuDecisionResult) -> dict[str, str]:
    """Vietnamese labels for existing Mệnh Cục presentation. Not a redesign."""
    purity = {
        "very_pure": "Rất thuần",
        "pure": "Thuần",
        "moderately_pure": "Thuần vừa",
        "mixed": "Pha tạp",
        "heavily_mixed": "Pha tạp mạnh",
        "structurally_impure": "Không thuần cấu trúc",
    }
    strength = {
        "very_strong": "Rất mạnh",
        "strong": "Mạnh",
        "moderate": "Vừa",
        "weak": "Yếu",
        "very_weak": "Rất yếu",
    }
    integrity = {
        "complete": "Toàn vẹn",
        "substantially_complete": "Gần toàn vẹn",
        "conditionally_complete": "Toàn vẹn có điều kiện",
        "mixed": "Hỗn hợp",
        "damaged_but_rescued": "Tổn thương đã cứu",
        "damaged": "Tổn thương",
        "failed": "Không giữ được",
    }
    return {
        "structural_purity": purity.get(result.purity.classification, ""),
        "structural_strength": strength.get(result.pattern_strength.classification, ""),
        "structural_integrity": integrity.get(result.integrity.state, ""),
        "structural_grade": result.grade.grade if result.grade.grade != "UNRESOLVED" else "",
        "customer_summary": result.decision.summary,
    }


def to_full_dict(result: MingJuDecisionResult) -> dict[str, Any]:
    """Internal full result including traces."""
    return to_jsonable(result)
