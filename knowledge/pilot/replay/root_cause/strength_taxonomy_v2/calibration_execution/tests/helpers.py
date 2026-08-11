"""Shared paths for PILOT-1M execution tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "validation"
REPORTS = ROOT / "reports"
TEMPLATES = ROOT / "templates"
PACKETS = ROOT / "packets"
EXECUTION = ROOT / "execution"
QUEUE = ROOT / "queue"
CAL_DIR = ROOT.parents[0] / "calibration" / "cases"
SYN_DIR = ROOT.parents[2] / "synthetic_strength" / "datasets"

REQUIRED_DOCS = [
    "README.md",
    "EXECUTION_WORKFLOW.md",
    "INTAKE_SPECIFICATION.md",
    "SOURCE_VERIFICATION.md",
    "DATA_VERIFICATION.md",
    "CALENDAR_VERIFICATION.md",
    "ELIGIBILITY_RULES.md",
    "EXPERT_A_EXECUTION.md",
    "EXPERT_B_EXECUTION.md",
    "BLINDING_RULES.md",
    "AGREEMENT_EXECUTION.md",
    "ADJUDICATION_EXECUTION.md",
    "CALIBRATION_RECORD_SPEC.md",
    "BOUNDARY_EXECUTION.md",
    "CONFLICT_EXECUTION.md",
    "PRIVACY_EXECUTION.md",
    "NO_DATA_CONTINGENCY.md",
    "PILOT_1M_SUMMARY.md",
]

REQUIRED_TEMPLATES = [
    "intake_record.json",
    "source_verification.json",
    "data_verification.json",
    "calendar_verification.json",
    "expert_a_review.json",
    "expert_b_review.json",
    "agreement_record.json",
    "adjudication_record.json",
    "calibration_record.json",
]

LIFECYCLE = [
    "intake_pending",
    "source_verification",
    "data_verification",
    "calendar_verification",
    "eligibility_review",
    "ready_for_expert_a",
    "expert_a_in_progress",
    "expert_a_complete",
    "ready_for_expert_b",
    "expert_b_in_progress",
    "expert_b_complete",
    "agreement_review",
    "adjudication_required",
    "adjudication_complete",
    "calibration_complete",
    "rejected",
    "withdrawn",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
