"""Shared constants for Round-3 tests."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "validation"
REPORTS = ROOT / "reports"
CASES = ROOT / "cases"
EXPERT = ROOT / "expert_review"  # Expert-A/B packets only when real reviews exist
CAL_DIR = ROOT.parents[0] / "calibration" / "cases"
SYN_DIR = ROOT.parents[2] / "synthetic_strength" / "datasets"
REQUIRED_DOCS = [
    "README.md",
    "ROUND_3_QUEUE.md",
    "ROUND_3_STATUS.md",
    "ROUND_3_SOURCE_LOG.md",
    "ROUND_3_REQUIREMENTS.md",
    "CALIBRATION_COVERAGE_ROUND_3.md",
    "ROUND_3_CALIBRATION_READINESS.md",
    "BOUNDARY_CASE_QUEUE.md",
    "CONFLICT_CASE_QUEUE.md",
    "EXPERT_REVIEW_PROTOCOL.md",
    "EXPERT_A_TEMPLATE.md",
    "EXPERT_B_TEMPLATE.md",
    "AGREEMENT_PROTOCOL.md",
    "ADJUDICATION_PROTOCOL.md",
    "PRIVACY_GUIDE.md",
    "SOURCE_VERIFICATION_GUIDE.md",
    "CALENDAR_VERIFICATION_GUIDE.md",
    "PILOT_1L_SUMMARY.md",
]
LEVELS = [
    "very_weak",
    "weak",
    "slightly_weak",
    "balanced",
    "slightly_strong",
    "strong",
    "very_strong",
]
