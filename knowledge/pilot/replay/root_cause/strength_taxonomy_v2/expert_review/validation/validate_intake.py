#!/usr/bin/env python3
"""Validate Expert-B intake packets (PILOT-1E-A). Does not invent Expert-B judgments."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAL_ROOT = Path(__file__).resolve().parents[2] / "calibration"
CASES = ("CASE_0001", "CASE_0006")
CAL_IDS = {"CASE_0001": "CAL-000001", "CASE_0006": "CAL-000006"}

FORBIDDEN_PACKET_SUBSTRINGS = [
    "Expert-A classification",
    "expert_review_1",
    "taxonomy_level_v2_candidate",
    "PROVISIONAL_SINGLE_REFERENCE",
    "adjudicated classification",
    "Đinh Tỵ",
    "Dinh Ty",
    "normalized_score",
    "current_band",
    "Thân vượng",
    "correct answer",
]


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate() -> list[str]:
    errors: list[str] = []
    index = _load(CAL_ROOT / "dataset_index.json")
    known = {row["calibration_case_id"] for row in index["cases"]}

    for folder, cal_id in CAL_IDS.items():
        if cal_id not in known:
            _fail(errors, f"missing calibration case {cal_id}")
        case_dir = ROOT / folder
        form = _load(case_dir / "REVIEW_FORM.json")
        manifest = _load(case_dir / "BLINDING_MANIFEST.json")
        packet = (case_dir / "REVIEW_PACKET.md").read_text(encoding="utf-8")
        case_json = _load(CAL_ROOT / "cases" / f"{cal_id}.json")

        if form.get("review_status") != "PENDING":
            _fail(errors, f"{cal_id}: review_status must be PENDING")
        for field in ("taxonomy_level", "confidence", "rationale"):
            if form.get(field) is not None:
                _fail(errors, f"{cal_id}: {field} must be null")
        if form.get("reviewer_id") != "EXPERT-B":
            _fail(errors, f"{cal_id}: reviewer_id must be EXPERT-B")
        if not manifest.get("expert_a_absent_from_blinded_packet"):
            _fail(errors, f"{cal_id}: Expert-A must be absent from blinded packet")
        if not manifest.get("adjudication_absent_from_blinded_packet"):
            _fail(errors, f"{cal_id}: adjudication must be absent from blinded packet")
        if not case_json.get("calendar_verification"):
            _fail(errors, f"{cal_id}: calendar_verification missing in case record")
        if not case_json.get("canonical_pillars"):
            _fail(errors, f"{cal_id}: canonical_pillars missing")
        for needle in FORBIDDEN_PACKET_SUBSTRINGS:
            if needle.lower() in packet.lower():
                _fail(errors, f"{cal_id}: forbidden substring in packet: {needle}")

        if cal_id == "CAL-000006":
            month = form["chart_verification"]["four_pillars"]["month"]
            if month != "Mậu Ngọ":
                _fail(errors, "CAL-000006: canonical month must be Mậu Ngọ")

    comparison = _load(ROOT / "comparison" / "COMPARISON_READY.json")
    if comparison.get("status") != "AWAITING_EXPERT_B":
        _fail(errors, "comparison status must be AWAITING_EXPERT_B")
    if comparison.get("adjudication_performed") is not False:
        _fail(errors, "adjudication_performed must be false")

    return errors


def main() -> int:
    errors = validate()
    report = {
        "sprint": "PILOT-1E-A",
        "ok": not errors,
        "error_count": len(errors),
        "errors": errors,
    }
    out = Path(__file__).resolve().parent / "VALIDATION.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
