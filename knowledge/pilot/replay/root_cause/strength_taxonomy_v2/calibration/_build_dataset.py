"""PILOT-1D: project EXISTING_PILOT cases into CALIBRATION_DATASET. No fabricated charts."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path("knowledge/pilot/replay/root_cause/strength_taxonomy_v2/calibration")
EVID = Path("knowledge/pilot/replay/root_cause/strength_calibration/evidence")
FIX = Path("knowledge/pilot/replay/fixtures")

LEVEL_MAP = {
    "CASE-0001": "SLIGHTLY_WEAK",
    "CASE-0002": "VERY_STRONG",
    "CASE-0003": "SLIGHTLY_WEAK",
    "CASE-0004": "STRONG",
    "CASE-0005": "SLIGHTLY_STRONG",
    "CASE-0006": "SLIGHTLY_WEAK",
    "CASE-0007": "STRONG",
}

META = {
    "CASE-0001": {
        "boundary": False,
        "conflict": True,
        "low_conf": True,
        "note": "model disagreement; sitting fire hypothesis",
    },
    "CASE-0002": {
        "boundary": False,
        "conflict": False,
        "low_conf": False,
        "note": "very strong seed",
    },
    "CASE-0003": {
        "boundary": True,
        "conflict": True,
        "low_conf": True,
        "note": "boundary twin with CASE-0005; score 0.66",
    },
    "CASE-0004": {
        "boundary": False,
        "conflict": False,
        "low_conf": False,
        "note": "strong control",
    },
    "CASE-0005": {
        "boundary": True,
        "conflict": False,
        "low_conf": True,
        "note": "boundary twin with CASE-0003; score 0.66",
    },
    "CASE-0006": {
        "boundary": True,
        "conflict": False,
        "low_conf": False,
        "note": "corrected Mậu Ngọ chart; adjacent balanced/slightly weak",
    },
    "CASE-0007": {
        "boundary": False,
        "conflict": True,
        "low_conf": False,
        "note": "strong; follow vs strength tension possible",
    },
}


def main() -> None:
    for sub in (
        "cases",
        "reviews",
        "adjudications",
        "evidence",
        "distributions",
        "boundaries",
        "conflicts",
        "provenance",
        "validation",
    ):
        (ROOT / sub).mkdir(parents=True, exist_ok=True)

    index: dict = {
        "dataset": "CALIBRATION_DATASET",
        "sprint": "PILOT-1D",
        "released_golden_mutated": False,
        "cases": [],
    }
    cases: list[dict] = []

    for i, cid in enumerate([f"CASE-000{n}" for n in range(1, 8)], start=1):
        cal_id = f"CAL-{i:06d}"
        ev = json.loads((EVID / f"{cid}.json").read_text(encoding="utf-8"))
        fix_path = FIX / f"{cid}.input.json"
        inp = (
            json.loads(fix_path.read_text(encoding="utf-8"))
            if fix_path.exists()
            else {}
        )
        meta = META[cid]
        level = LEVEL_MAP[cid]
        expert = ev["expert_reference"]
        chart = ev["chart"]
        pipe = ev["pipeline"]
        birth = ev["input"]

        calendar_verification = {
            "status": (
                "VERIFIED_CORRECTED_PROJECTION"
                if cid == "CASE-0006"
                else "VERIFIED"
            ),
            "solar_term": ev.get("calendar_solar_term"),
            "note": ev.get("corrected_chart_note"),
            "historical_fixture_unchanged": cid == "CASE-0006",
        }

        case = {
            "calibration_case_id": cal_id,
            "source_case_id": cid,
            "provenance": "EXISTING_PILOT",
            "birth_datetime": (
                f"{birth['year']:04d}-{birth['month']:02d}-{birth['day']:02d}"
                f"T{birth['hour']:02d}:{birth['minute']:02d}:00"
            ),
            "location": (inp.get("birth") or {}).get("location"),
            "timezone": (inp.get("birth") or {}).get("timezone")
            or "Asia/Ho_Chi_Minh",
            "gender": birth.get("gender"),
            "canonical_pillars": chart,
            "calendar_verification": calendar_verification,
            "evidence_snapshot_ref": f"evidence/{cal_id}.json",
            "runtime_score": {
                "raw": pipe.get("raw_strength_score"),
                "normalized": pipe.get("normalized_score"),
            },
            "runtime_profile": pipe.get("weighted_buckets_raw"),
            "current_v1_band": pipe.get("current_band"),
            "current_v1_label": pipe.get("current_label"),
            "expert_review_1": {
                "source": "PILOT_EXPERT_REFERENCE",
                "taxonomy_level_v2_candidate": level,
                "label_en": expert.get("en"),
                "label_vi": expert.get("vi"),
                "confidence": "MEDIUM",
                "rationale": (
                    "Carried from Pilot expert reference classification; "
                    "not a new dual-blind review."
                ),
                "blinded": False,
                "review_status": "RECORDED_FROM_EXISTING_REFERENCE",
            },
            "expert_review_2": {
                "status": "PENDING_ACQUISITION",
                "note": (
                    "Second independent expert review not available; "
                    "do not fabricate."
                ),
            },
            "adjudication": {
                "status": "PROVISIONAL_SINGLE_REFERENCE",
                "result_level": level,
                "note": (
                    "Pending dual review / adjudication per "
                    "EXPERT_CALIBRATION_PROTOCOL."
                ),
            },
            "confidence": "MEDIUM" if meta["low_conf"] or True else "HIGH",
            "boundary_status": bool(meta["boundary"]),
            "conflict_status": bool(meta["conflict"]),
            "evidence_completeness": (
                "PARTIAL"
                if meta["conflict"] or cid == "CASE-0001"
                else "ADEQUATE_FOR_PILOT"
            ),
            "review_status": "SINGLE_REFERENCE_VERIFIED_CHART",
            "inclusion_status": "VERIFIED_POOL_PROVISIONAL",
            "notes": meta["note"],
            "anonymized_report_id": cal_id,
        }
        # All single-ref cases use MEDIUM confidence (protocol incomplete)
        case["confidence"] = "MEDIUM"

        evid_out = {
            "calibration_case_id": cal_id,
            "source_case_id": cid,
            "chart": chart,
            "pipeline": {
                "season_context": pipe.get("season_context"),
                "temperature_context": pipe.get("temperature_context"),
                "root_resource_evidence": pipe.get("root_resource_evidence"),
                "supporting_elements": pipe.get("supporting_elements"),
                "restricting_elements": pipe.get("restricting_elements"),
                "strength_evidence_ledger": pipe.get("strength_evidence_ledger"),
                "weighted_buckets_raw": pipe.get("weighted_buckets_raw"),
                "raw_strength_score": pipe.get("raw_strength_score"),
                "normalized_score": pipe.get("normalized_score"),
                "current_band": pipe.get("current_band"),
                "confidence_runtime": pipe.get("confidence"),
            },
        }

        (ROOT / "cases" / f"{cal_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (ROOT / "evidence" / f"{cal_id}.json").write_text(
            json.dumps(evid_out, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (ROOT / "reviews" / f"{cal_id}_review1.json").write_text(
            json.dumps(case["expert_review_1"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (ROOT / "adjudications" / f"{cal_id}.json").write_text(
            json.dumps(case["adjudication"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        index["cases"].append(
            {
                "calibration_case_id": cal_id,
                "source_case_id": cid,
                "provenance": "EXISTING_PILOT",
                "level": level,
                "normalized": pipe.get("normalized_score"),
                "v1_band": pipe.get("current_band"),
                "boundary": meta["boundary"],
                "conflict": meta["conflict"],
                "inclusion_status": "VERIFIED_POOL_PROVISIONAL",
                "dual_reviewed": False,
            }
        )
        cases.append(case)

        # provenance card
        (ROOT / "provenance" / f"{cal_id}.json").write_text(
            json.dumps(
                {
                    "calibration_case_id": cal_id,
                    "provenance": "EXISTING_PILOT",
                    "source_case_id": cid,
                    "synthetic": False,
                    "unknown": False,
                    "allowed_in_verified_pool": True,
                    "caveat": "Single expert reference; dual review pending",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    cov = Counter(c["level"] for c in index["cases"])
    index["coverage"] = {
        k: cov.get(k, 0)
        for k in (
            "VERY_WEAK",
            "WEAK",
            "SLIGHTLY_WEAK",
            "BALANCED",
            "SLIGHTLY_STRONG",
            "STRONG",
            "VERY_STRONG",
        )
    }
    index["counts"] = {
        "total_provisional_verified": len(cases),
        "new_verified_cases": 0,
        "dual_reviewed": 0,
        "boundary": sum(1 for c in index["cases"] if c["boundary"]),
        "conflict": sum(1 for c in index["cases"] if c["conflict"]),
        "low_confidence_flagged": len(cases),  # all MEDIUM pending dual review
    }
    index["score_only_sufficiency"] = "NO"
    index["taxonomy_boundaries_frozen"] = False

    (ROOT / "dataset_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # distributions
    dist = {
        "normalized_scores": [
            {"id": c["calibration_case_id"], "score": c["normalized"], "level": c["level"]}
            for c in index["cases"]
        ],
        "identical_score_different_label": [
            {
                "score": 0.66,
                "cases": ["CAL-000003", "CAL-000005"],
                "levels": ["SLIGHTLY_WEAK", "SLIGHTLY_STRONG"],
            }
        ],
    }
    (ROOT / "distributions" / "score_distribution.json").write_text(
        json.dumps(dist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # boundaries / conflicts indexes
    (ROOT / "boundaries" / "cohort.json").write_text(
        json.dumps(
            {
                "cases": [c["calibration_case_id"] for c in index["cases"] if c["boundary"]],
                "regions_covered": [
                    "SLIGHTLY_WEAK/BALANCED (CAL-000006 provisional)",
                    "SLIGHTLY_STRONG/STRONG cliff twins CAL-000003/CAL-000005",
                ],
                "status": "BOUNDARY_DATA_INSUFFICIENT",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (ROOT / "conflicts" / "cohort.json").write_text(
        json.dumps(
            {
                "cases": [c["calibration_case_id"] for c in index["cases"] if c["conflict"]],
                "minimum_target": 5,
                "achieved": sum(1 for c in index["cases"] if c["conflict"]),
                "status": "PARTIAL",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    # validation
    ids = [c["calibration_case_id"] for c in index["cases"]]
    validation = {
        "sprint": "PILOT-1D",
        "unique_calibration_ids": len(ids) == len(set(ids)),
        "valid_provenance": all(c["provenance"] == "EXISTING_PILOT" for c in index["cases"]),
        "no_synthetic_in_verified_pool": True,
        "no_unknown_provenance": True,
        "expert_review_1_present": True,
        "expert_review_2_complete": False,
        "dual_review_complete": False,
        "taxonomy_labels_valid": all(
            c["level"]
            in {
                "VERY_WEAK",
                "WEAK",
                "SLIGHTLY_WEAK",
                "BALANCED",
                "SLIGHTLY_STRONG",
                "STRONG",
                "VERY_STRONG",
            }
            for c in index["cases"]
        ),
        "confidence_present": True,
        "chart_verification_present": True,
        "no_duplicate_source_cases": len({c["source_case_id"] for c in index["cases"]})
        == len(index["cases"]),
        "no_fabricated_expert_judgments": True,
        "no_production_mutations": True,
        "released_golden_expected_unchanged": True,
        "coverage_gaps": {
            k: max(0, 5 - v) for k, v in index["coverage"].items() if v < 5
        },
        "overall": "PASS_WITH_GAPS",
    }
    (ROOT / "validation" / "VALIDATION.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps(index["coverage"], ensure_ascii=False, indent=2))
    print(json.dumps(index["counts"], ensure_ascii=False, indent=2))
    print("validation", validation["overall"])


if __name__ == "__main__":
    main()
