"""Build the 21 SYN-STR synthetic Strength stress fixtures (PILOT-1G)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATASETS = ROOT / "datasets"

CASES: list[dict] = [
    {
        "case_id": "SYN-STR-000001",
        "day_master": "quy",
        "pillars": {
            "year": "binh_ngo",
            "month": "giap_ngo",
            "day": "quy_ti",
            "hour": "mau_ngo",
        },
        "synthetic_expected_taxonomy": "very_weak",
        "evidence_profile": "extreme hoa dominance against thuy",
        "stress_purpose": "VERY_WEAK extreme: water day master under heavy fire season/structure",
    },
    {
        "case_id": "SYN-STR-000002",
        "day_master": "giap",
        "pillars": {
            "year": "mau_thin",
            "month": "ky_mui",
            "day": "giap_tuat",
            "hour": "mau_thin",
        },
        "synthetic_expected_taxonomy": "very_weak",
        "evidence_profile": "extreme tho dominance against moc",
        "stress_purpose": "VERY_WEAK extreme: wood day master under heavy earth pressure",
    },
    {
        "case_id": "SYN-STR-000003",
        "day_master": "binh",
        "pillars": {
            "year": "canh_than",
            "month": "tan_dau",
            "day": "binh_than",
            "hour": "canh_tuat",
        },
        "synthetic_expected_taxonomy": "very_weak",
        "evidence_profile": "extreme kim dominance against hoa",
        "stress_purpose": "VERY_WEAK extreme: fire day master under heavy metal dominance",
    },
    {
        "case_id": "SYN-STR-000004",
        "day_master": "at",
        "pillars": {
            "year": "canh_than",
            "month": "mau_ty",
            "day": "at_dau",
            "hour": "ky_suu",
        },
        "synthetic_expected_taxonomy": "weak",
        "evidence_profile": "weak moc with limited rooting",
        "stress_purpose": "WEAK: wood with scarce roots under metal/earth pressure",
    },
    {
        "case_id": "SYN-STR-000005",
        "day_master": "dinh",
        "pillars": {
            "year": "binh_than",
            "month": "canh_than",
            "day": "dinh_dau",
            "hour": "ky_suu",
        },
        "synthetic_expected_taxonomy": "weak",
        "evidence_profile": "weak hoa in strong kim environment",
        "stress_purpose": "WEAK: fire in autumn metal environment",
    },
    {
        "case_id": "SYN-STR-000006",
        "day_master": "nham",
        "pillars": {
            "year": "mau_tuat",
            "month": "ky_mui",
            "day": "nham_thin",
            "hour": "mau_tuat",
        },
        "synthetic_expected_taxonomy": "weak",
        "evidence_profile": "weak thuy under strong tho pressure",
        "stress_purpose": "WEAK: water under strong earth control",
    },
    {
        "case_id": "SYN-STR-000007",
        "day_master": "canh",
        "pillars": {
            "year": "binh_dan",
            "month": "tan_suu",
            "day": "canh_ngo",
            "hour": "mau_dan",
        },
        "synthetic_expected_taxonomy": "slightly_weak",
        "evidence_profile": "kim has support but faces moc/hoa pressure",
        "stress_purpose": "SLIGHTLY_WEAK: metal with support but wood/fire pressure",
    },
    {
        "case_id": "SYN-STR-000008",
        "day_master": "quy",
        "pillars": {
            "year": "mau_thin",
            "month": "dinh_ti",
            "day": "quy_ti",
            "hour": "nham_tuat",
        },
        "synthetic_expected_taxonomy": "slightly_weak",
        "evidence_profile": "thuy has limited support under hoa/tho pressure",
        "stress_purpose": "SLIGHTLY_WEAK: water with limited support under fire/earth",
    },
    {
        "case_id": "SYN-STR-000009",
        "day_master": "tan",
        "pillars": {
            "year": "giap_ngo",
            "month": "dinh_mui",
            "day": "tan_dau",
            "hour": "giap_ngo",
        },
        "synthetic_expected_taxonomy": "slightly_weak",
        "evidence_profile": "kim has direct root but faces strong hoa pressure",
        "stress_purpose": "SLIGHTLY_WEAK: metal rooted but under strong fire",
    },
    {
        "case_id": "SYN-STR-000010",
        "day_master": "mau",
        "pillars": {
            "year": "giap_ty",
            "month": "binh_dan",
            "day": "mau_thin",
            "hour": "canh_than",
        },
        "synthetic_expected_taxonomy": "balanced",
        "evidence_profile": "mixed five-element support and pressure",
        "stress_purpose": "BALANCED: mixed support and pressure across elements",
    },
    {
        "case_id": "SYN-STR-000011",
        "day_master": "giap",
        "pillars": {
            "year": "binh_ty",
            "month": "canh_ngo",
            "day": "giap_thin",
            "hour": "mau_than",
        },
        "synthetic_expected_taxonomy": "balanced",
        "evidence_profile": "balanced support, output and restriction",
        "stress_purpose": "BALANCED: support vs output/restriction roughly even",
    },
    {
        "case_id": "SYN-STR-000012",
        "day_master": "nham",
        "pillars": {
            "year": "dinh_mao",
            "month": "mau_ngo",
            "day": "nham_than",
            "hour": "canh_ty",
        },
        "synthetic_expected_taxonomy": "balanced",
        "evidence_profile": "thuy has strong support but faces seasonal hoa",
        "stress_purpose": "BALANCED: water support offset by seasonal fire",
    },
    {
        "case_id": "SYN-STR-000013",
        "day_master": "giap",
        "pillars": {
            "year": "nham_ty",
            "month": "tan_hoi",
            "day": "giap_thin",
            "hour": "mau_than",
        },
        "synthetic_expected_taxonomy": "slightly_strong",
        "evidence_profile": "strong water support with remaining metal/earth pressure",
        "stress_purpose": "SLIGHTLY_STRONG: wood fed by water with residual pressure",
    },
    {
        "case_id": "SYN-STR-000014",
        "day_master": "binh",
        "pillars": {
            "year": "canh_thin",
            "month": "quy_ti",
            "day": "binh_ngo",
            "hour": "giap_dan",
        },
        "synthetic_expected_taxonomy": "slightly_strong",
        "evidence_profile": "hoa has seasonal and rooting support but retains opposing forces",
        "stress_purpose": "SLIGHTLY_STRONG: fire season/root with opposing forces",
    },
    {
        "case_id": "SYN-STR-000015",
        "day_master": "mau",
        "pillars": {
            "year": "at_mao",
            "month": "dinh_mao",
            "day": "mau_thin",
            "hour": "nham_ty",
        },
        "synthetic_expected_taxonomy": "slightly_strong",
        "evidence_profile": "moc pressure exists but tho retains rooting and fire support",
        "stress_purpose": "SLIGHTLY_STRONG: earth rooted with fire support under wood",
    },
    {
        "case_id": "SYN-STR-000016",
        "day_master": "giap",
        "pillars": {
            "year": "giap_dan",
            "month": "at_mao",
            "day": "giap_thin",
            "hour": "quy_hoi",
        },
        "synthetic_expected_taxonomy": "strong",
        "evidence_profile": "strong moc with strong water support",
        "stress_purpose": "STRONG: wood season/structure with water resource",
    },
    {
        "case_id": "SYN-STR-000017",
        "day_master": "binh",
        "pillars": {
            "year": "binh_dan",
            "month": "dinh_ti",
            "day": "binh_ngo",
            "hour": "giap_ngo",
        },
        "synthetic_expected_taxonomy": "strong",
        "evidence_profile": "strong hoa with seasonal and structural support",
        "stress_purpose": "STRONG: fire with seasonal and structural support",
    },
    {
        "case_id": "SYN-STR-000018",
        "day_master": "canh",
        "pillars": {
            "year": "canh_than",
            "month": "tan_dau",
            "day": "canh_thin",
            "hour": "mau_than",
        },
        "synthetic_expected_taxonomy": "strong",
        "evidence_profile": "strong kim with multiple roots and support",
        "stress_purpose": "STRONG: metal with multiple roots and companion support",
    },
    {
        "case_id": "SYN-STR-000019",
        "day_master": "nham",
        "pillars": {
            "year": "nham_ty",
            "month": "quy_hoi",
            "day": "nham_ty",
            "hour": "tan_hoi",
        },
        "synthetic_expected_taxonomy": "very_strong",
        "evidence_profile": "extreme thuy dominance",
        "stress_purpose": "VERY_STRONG extreme: water dominance across pillars",
    },
    {
        "case_id": "SYN-STR-000020",
        "day_master": "giap",
        "pillars": {
            "year": "giap_dan",
            "month": "at_mao",
            "day": "giap_dan",
            "hour": "quy_mao",
        },
        "synthetic_expected_taxonomy": "very_strong",
        "evidence_profile": "extreme moc dominance",
        "stress_purpose": "VERY_STRONG extreme: wood dominance across pillars",
    },
    {
        "case_id": "SYN-STR-000021",
        "day_master": "binh",
        "pillars": {
            "year": "binh_dan",
            "month": "dinh_ti",
            "day": "binh_ngo",
            "hour": "dinh_ti",
        },
        "synthetic_expected_taxonomy": "very_strong",
        "evidence_profile": "extreme hoa dominance",
        "stress_purpose": "VERY_STRONG extreme: fire dominance across pillars",
    },
]


def build_case(spec: dict) -> dict:
    """Assemble full case schema from compact spec."""
    return {
        "case_id": spec["case_id"],
        "dataset_type": "SYNTHETIC_STRENGTH_STRESS",
        "calibration_eligible": False,
        "golden_eligible": False,
        "expert_calibration_eligible": False,
        "production_expected": False,
        "synthetic_pillars": True,
        "calendar_verified": False,
        "birth_datetime": None,
        "birth_location": None,
        "timezone": None,
        "day_master": spec["day_master"],
        "pillars": spec["pillars"],
        "synthetic_expected_taxonomy": spec["synthetic_expected_taxonomy"],
        "evidence_profile": spec["evidence_profile"],
        "stress_purpose": spec["stress_purpose"],
        "notes": [
            "Synthetic pillar structure only. Not a verified birth record.",
            "synthetic_expected_taxonomy is a stress-test label, not expert judgment.",
            "Not eligible for calibration, Golden Dataset, or production Expected.",
        ],
    }


def main() -> None:
    """Write datasets/SYN-STR-*.json and SYNTHETIC_DATASET_INDEX.json."""
    DATASETS.mkdir(parents=True, exist_ok=True)
    index_cases = []
    for spec in CASES:
        case = build_case(spec)
        path = DATASETS / f"{case['case_id']}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(case, handle, ensure_ascii=True, indent=2)
            handle.write("\n")
        index_cases.append(
            {
                "case_id": case["case_id"],
                "day_master": case["day_master"],
                "pillars": case["pillars"],
                "synthetic_expected_taxonomy": case["synthetic_expected_taxonomy"],
                "evidence_profile": case["evidence_profile"],
                "path": f"datasets/{case['case_id']}.json",
            }
        )

    index = {
        "sprint": "PILOT-1G",
        "dataset_name": "synthetic_strength_stress_v1",
        "dataset_type": "SYNTHETIC_STRENGTH_STRESS",
        "case_count": len(index_cases),
        "id_prefix": "SYN-STR",
        "calibration_eligible": False,
        "golden_eligible": False,
        "expert_calibration_eligible": False,
        "production_expected": False,
        "taxonomy_levels": [
            "very_weak",
            "weak",
            "slightly_weak",
            "balanced",
            "slightly_strong",
            "strong",
            "very_strong",
        ],
        "cases_per_level": 3,
        "cases": index_cases,
    }
    with (ROOT / "SYNTHETIC_DATASET_INDEX.json").open("w", encoding="utf-8") as handle:
        json.dump(index, handle, ensure_ascii=True, indent=2)
        handle.write("\n")
    print(f"wrote {len(index_cases)} cases")


if __name__ == "__main__":
    main()
