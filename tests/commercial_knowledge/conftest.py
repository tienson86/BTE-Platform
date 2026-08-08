"""Shared fixtures for commercial knowledge tests."""

from __future__ import annotations

from typing import Any


def strong_chart_with_useful_god() -> dict[str, Any]:
    """Analysis bag where ID/ST/UG/RC should match."""
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


def weak_chart_with_useful_god() -> dict[str, Any]:
    """Analysis bag where ID/WK/UG/RC should match."""
    return {
        "bazi": {"day_master": "Ất"},
        "pattern": {"cach_cuc": "Thương Quan", "ky_than": "Hỏa"},
        "strength": {
            "strength_level": "nhuoc",
            "strength_score": 32,
            "reasoning": "kích hoạt khi thân suy",
        },
        "useful_god": {
            "useful_god": "Mộc",
            "unfavorable_gods": ["Hỏa"],
            "confidence": 0.7,
        },
        "score": {"strength_score": 32, "grade": "C", "recommendation": "Mộc"},
    }


def chart_without_useful_god() -> dict[str, Any]:
    """Strong chart without useful god — UG/RC must drop."""
    return {
        "bazi": {"day_master": "Bính"},
        "pattern": {"cach_cuc": "Kiến Lộc"},
        "strength": {"strength_level": "vuong", "strength_score": 68},
        "useful_god": {},
        "score": {"strength_score": 68, "grade": "B"},
    }
