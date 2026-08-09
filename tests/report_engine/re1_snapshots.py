"""AX-2 / AX-3 / AX-4 / IX-1 shaped snapshots for RE-1 tests. Not live pipeline runs."""

from __future__ import annotations

from typing import Any


def ax2_snapshot() -> dict[str, Any]:
    """Frozen Canonical Analysis Result shape (AX-2 2.0.0)."""
    return {
        "pipeline_id": "canonical_analysis_pipeline",
        "pipeline_version": "2.0.0",
        "success": True,
        "seasonal": {"season": "Xuân"},
        "strength": {"strength_level": "strong"},
        "useful_god": {"useful_god": "Giáp"},
        "stage_order": ["seasonal", "strength", "useful_god"],
    }


def ax3_snapshot() -> dict[str, Any]:
    """Frozen Canonical Decision Result shape (AX-3 1.0.0)."""
    return {
        "pipeline_id": "canonical_decision_pipeline",
        "decision_pipeline_version": "1.0.0",
        "success": True,
        "final_useful_god": "Giáp",
        "final_favorable_gods": ["Giáp"],
        "final_unfavorable_gods": ["Canh"],
    }


def ax4_snapshot() -> dict[str, Any]:
    """Frozen Canonical Luck Result shape (AX-4 1.0.0)."""
    return {
        "pipeline_id": "canonical_luck_pipeline",
        "luck_pipeline_version": "1.0.0",
        "success": True,
        "overall_luck_result": {"luck_priority": {"value": "balanced"}},
        "component_versions": {
            "timeline": "1.0.0",
            "luck_analysis": "1.0.0",
            "luck_decision": "1.0.0",
        },
    }


def ix1_snapshot() -> dict[str, Any]:
    """Frozen Canonical Interpretation Result shape (IX-1 1.0.0)."""
    return {
        "pipeline_id": "canonical_interpretation_pipeline",
        "interpretation_pipeline_version": "1.0.0",
        "success": True,
        "foundation_result": {"interpretation_version": "1.0.0"},
        "knowledge_result": {"composition_version": "1.0.0"},
        "composition_result": {"assembly_version": "1.0.0"},
        "canonical_interpretation": {"assembly_version": "1.0.0"},
        "component_versions": {
            "interpretation_foundation": "1.0.0",
            "knowledge_selection_engine": "1.0.0",
            "interpretation_composition_engine": "1.0.0",
        },
    }
