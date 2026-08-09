"""Shared fixtures for Luck Timeline Foundation tests."""

from __future__ import annotations

from typing import Any

import pytest


@pytest.fixture
def analysis_snapshot() -> dict[str, Any]:
    """Frozen AX-2 shaped snapshot. Not a live pipeline run."""
    return {
        "pipeline_id": "canonical_analysis_pipeline",
        "pipeline_version": "2.0.0",
        "success": True,
        "seasonal": {"season": "Xuân", "season_phase": "mid", "month_branch": "Dần"},
        "strength": {"day_master": "Mậu", "strength_level": "strong", "strength_score": 78},
        "temperature": {
            "temperature_level": "mild",
            "day_master_element": "Thổ",
            "temperature_score": 48,
        },
        "pattern": {"principal_pattern": "Kiến Lộc"},
        "pattern_evaluation": {
            "pattern_quality": "good",
            "pattern_confidence": "high",
            "pattern_score": 82,
        },
        "useful_god": {
            "useful_god": "Giáp",
            "favorable_gods": ["Giáp"],
            "unfavorable_gods": ["Canh"],
        },
        "stage_order": [
            "calendar",
            "four_pillars",
            "seasonal",
            "strength",
            "temperature",
            "pattern",
            "pattern_evaluation",
            "useful_god",
        ],
    }


@pytest.fixture
def decision_snapshot() -> dict[str, Any]:
    """Frozen AX-3 shaped snapshot. Not a live pipeline run."""
    return {
        "pipeline_id": "canonical_decision_pipeline",
        "decision_pipeline_version": "1.0.0",
        "success": True,
        "final_useful_god": "Giáp",
        "final_favorable_gods": ["Giáp"],
        "final_unfavorable_gods": ["Canh"],
    }


@pytest.fixture
def natal_payload() -> dict[str, Any]:
    """Deterministic natal identity."""
    return {
        "chart_id": "CH-TEST-001",
        "year_pillar": "Giáp Tý",
        "month_pillar": "Bính Dần",
        "day_pillar": "Mậu Thìn",
        "hour_pillar": "Canh Ngọ",
        "gender": "male",
        "birth_year": 1990,
        "birth_month": 3,
        "birth_day": 15,
        "birth_hour": 12,
    }


@pytest.fixture
def continuous_timeline_payload(natal_payload: dict[str, Any]) -> dict[str, Any]:
    """Declared contiguous timeline slots. Not engine-calculated."""
    return {
        "timeline_id": "TL-TEST-001",
        "natal_chart": natal_payload,
        "major_cycles": [
            {
                "cycle_id": "CY-MAJOR-001",
                "layer": "major_luck",
                "periods": [
                    {
                        "period_id": "P-MAJOR-001",
                        "layer": "major_luck",
                        "sequence": 0,
                        "start_year": 1990,
                        "end_year": 1999,
                        "heavenly_stem": "Giáp",
                        "earthly_branch": "Tý",
                    },
                    {
                        "period_id": "P-MAJOR-002",
                        "layer": "major_luck",
                        "sequence": 1,
                        "start_year": 2000,
                        "end_year": 2009,
                        "heavenly_stem": "Ất",
                        "earthly_branch": "Sửu",
                    },
                ],
            }
        ],
        "annual_cycles": [
            {
                "cycle_id": "CY-ANNUAL-001",
                "layer": "annual_luck",
                "parent_period_id": "P-MAJOR-001",
                "periods": [
                    {
                        "period_id": "P-ANNUAL-001",
                        "layer": "annual_luck",
                        "sequence": 0,
                        "start_year": 1990,
                        "end_year": 1990,
                        "parent_period_id": "P-MAJOR-001",
                    },
                    {
                        "period_id": "P-ANNUAL-002",
                        "layer": "annual_luck",
                        "sequence": 1,
                        "start_year": 1991,
                        "end_year": 1991,
                        "parent_period_id": "P-MAJOR-001",
                    },
                ],
            }
        ],
        "monthly_cycles": [
            {
                "cycle_id": "CY-MONTH-001",
                "layer": "monthly_luck",
                "parent_period_id": "P-ANNUAL-001",
                "periods": [
                    {
                        "period_id": "P-MONTH-001",
                        "layer": "monthly_luck",
                        "sequence": 0,
                        "start_year": 1990,
                        "start_month": 1,
                        "end_year": 1990,
                        "end_month": 1,
                        "parent_period_id": "P-ANNUAL-001",
                    },
                    {
                        "period_id": "P-MONTH-002",
                        "layer": "monthly_luck",
                        "sequence": 1,
                        "start_year": 1990,
                        "start_month": 2,
                        "end_year": 1990,
                        "end_month": 2,
                        "parent_period_id": "P-ANNUAL-001",
                    },
                ],
            }
        ],
        "events": [
            {
                "event_id": "EV-001",
                "period_id": "P-MAJOR-001",
                "event_type": "start",
                "year": 1990,
            }
        ],
    }
