#!/usr/bin/env python3
"""Validate PILOT-1E-B agreement/adjudication integrity."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAL = Path(__file__).resolve().parents[2] / "calibration"
TAXONOMY = [
    "VERY_WEAK",
    "WEAK",
    "SLIGHTLY_WEAK",
    "BALANCED",
    "SLIGHTLY_STRONG",
    "STRONG",
    "VERY_STRONG",
]
CASES = ("CAL-000001", "CAL-000006")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _distance(a: str, b: str) -> int:
    return abs(TAXONOMY.index(a) - TAXONOMY.index(b))


def validate() -> list[str]:
    errors: list[str] = []
    for cal_id in CASES:
        case = _load(CAL / "cases" / f"{cal_id}.json")
        rev1 = _load(CAL / "reviews" / f"{cal_id}_review1.json")
        rev2 = _load(CAL / "reviews" / f"{cal_id}_review2.json")
        adj_cal = _load(CAL / "adjudications" / f"{cal_id}.json")
        adj_key = "CASE_000001" if cal_id == "CAL-000001" else "CASE_000006"
        adj = _load(ROOT / f"{adj_key}_ADJUDICATION.json")

        a_level = rev1["taxonomy_level_v2_candidate"]
        b_level = rev2["taxonomy_level"]
        if case["expert_review_1"]["taxonomy_level_v2_candidate"] != a_level:
            errors.append(f"{cal_id}: Expert-A not preserved in case record")
        if rev2["reviewer_id"] != "EXPERT-B":
            errors.append(f"{cal_id}: Expert-B reviewer_id invalid")
        if b_level != "SLIGHTLY_WEAK" or rev2["confidence"] != "MEDIUM":
            errors.append(f"{cal_id}: Expert-B judgment mismatch")
        if rev2.get("rationale") is not None:
            errors.append(f"{cal_id}: Expert-B rationale must remain null (not supplied)")
        dist = _distance(a_level, b_level)
        if dist != 0:
            errors.append(f"{cal_id}: expected distance 0, got {dist}")
        if adj["agreement"]["expert_agreement"] != "EXACT_MATCH":
            errors.append(f"{cal_id}: agreement must be EXACT_MATCH")
        if adj["adjudication_status"] != "NOT_REQUIRED":
            errors.append(f"{cal_id}: adjudication_status must be NOT_REQUIRED")
        if adj.get("adjudicated_taxonomy_level") is not None:
            errors.append(f"{cal_id}: must not invent adjudicated taxonomy level")
        if adj_cal["adjudication_status"] != "NOT_REQUIRED":
            errors.append(f"{cal_id}: calibration adjudication mirror mismatch")
        if not case.get("dual_reviewed"):
            errors.append(f"{cal_id}: dual_reviewed flag missing")

    case6 = _load(CAL / "cases" / "CAL-000006.json")
    if case6["canonical_pillars"]["month"] != "Mậu Ngọ":
        errors.append("CAL-000006 month must remain Mậu Ngọ")

    return errors


def main() -> int:
    errors = validate()
    report = {
        "sprint": "PILOT-1E-B",
        "ok": not errors,
        "error_count": len(errors),
        "errors": errors,
        "checks": {
            "expert_a_preserved": True,
            "expert_b_preserved": True,
            "adjudication_not_overwriting_reviews": True,
            "agreement_distance_correct": True,
            "cal_000006_mau_ngo": True,
            "no_invented_adjudicated_levels": True,
        },
    }
    if errors:
        report["checks"] = {k: False for k in report["checks"]}
    out = Path(__file__).resolve().parent / "VALIDATION.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
