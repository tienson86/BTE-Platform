"""PILOT-1L Round-3 acquisition package builder (no fabricated cases)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VALIDATION = ROOT / "validation"
REPORTS = ROOT / "reports"
CASES = ROOT / "cases"
EXPERT = ROOT / "expert_review"

LEVELS = [
    "very_weak",
    "weak",
    "slightly_weak",
    "balanced",
    "slightly_strong",
    "strong",
    "very_strong",
]

# Existing dual-reviewed expert taxonomy (read-only reference; unchanged).
EXISTING_DUAL = {
    "CAL-000001": "slightly_weak",
    "CAL-000006": "slightly_weak",
}

MINIMUM_TARGET = 5
NEW_REAL = 0
NEW_VERIFIED = 0
NEW_DUAL = 0


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def coverage_rows() -> list[dict]:
    dual_counts = {level: 0 for level in LEVELS}
    for level in EXISTING_DUAL.values():
        dual_counts[level] += 1
    rows = []
    priority = {
        "very_weak": "P0",
        "weak": "P0",
        "balanced": "P0",
        "slightly_strong": "P1",
        "strong": "P1",
        "very_strong": "P2",
        "slightly_weak": "P1",  # partial existing; still short of gate
    }
    for level in LEVELS:
        dual = dual_counts[level]
        remaining = max(0, MINIMUM_TARGET - dual)
        rows.append(
            {
                "level": level,
                "dual_reviewed_count": dual,
                "expert_a_count": dual,  # both dual cases have A
                "expert_b_count": dual,
                "verified_real_count": dual,
                "data_gap": remaining > 0,
                "priority": priority[level],
                "minimum_target": MINIMUM_TARGET,
                "remaining_needed": remaining,
                "status": "partial_not_covered" if dual > 0 else "data_gap",
            }
        )
    return rows


def build() -> None:
    rows = coverage_rows()
    write_json(
        REPORTS / "coverage_matrix.json",
        {
            "sprint": "PILOT-1L",
            "round": 3,
            "minimum_target_per_level": MINIMUM_TARGET,
            "existing_dual_reviewed": list(EXISTING_DUAL.keys()),
            "new_real_cases": NEW_REAL,
            "new_cal_ids_created": [],
            "next_free_calibration_id": "CAL-000008",
            "rows": rows,
        },
    )
    write_json(
        VALIDATION / "VALIDATION.json",
        {
            "sprint": "PILOT-1L",
            "round": 3,
            "new_real_cases_acquired": NEW_REAL,
            "new_verified_cases": NEW_VERIFIED,
            "new_dual_reviewed_cases": NEW_DUAL,
            "existing_dual_reviewed_cases": 2,
            "no_fabricated_cases": True,
            "no_fabricated_expert_judgments": True,
            "cal_000001_unchanged": True,
            "cal_000006_unchanged": True,
            "syn_unchanged": True,
            "taxonomy_v2_implemented": False,
            "t1_t6_frozen": False,
            "production_code_changed": False,
            "final_decision": "CALIBRATION_PARTIAL",
            "readiness": "DATA_GAP",
            "overall": "PASS_WITH_GAPS",
        },
    )
    write_json(
        VALIDATION / "profile.json",
        {
            "sprint": "PILOT-1L",
            "round": 3,
            "acquisition_ids_created": 0,
            "cal_ids_created": 0,
            "queue_entries": 7,
            "priority_p0_levels": ["very_weak", "weak", "balanced"],
            "final_decision": "CALIBRATION_PARTIAL",
        },
    )
    for name, text in DOCS(rows).items():
        write(ROOT / name, text)
    write(CASES / "README.md", CASES_README)
    write(EXPERT / "README.md", EXPERT_README)
    print("PILOT-1L Round-3 package written (new_real_cases=0)")


def DOCS(rows: list[dict]) -> dict[str, str]:
    matrix_lines = [
        "| level | dual_reviewed_count | expert_a_count | expert_b_count | verified_real_count | data_gap | priority | minimum_target | remaining_needed | status |",
        "|---|---:|---:|---:|---:|---|---|---:|---:|---|",
    ]
    for r in rows:
        matrix_lines.append(
            f"| {r['level']} | {r['dual_reviewed_count']} | {r['expert_a_count']} | "
            f"{r['expert_b_count']} | {r['verified_real_count']} | "
            f"{'YES' if r['data_gap'] else 'NO'} | {r['priority']} | "
            f"{r['minimum_target']} | {r['remaining_needed']} | {r['status']} |"
        )
    matrix = "\n".join(matrix_lines)

    return {
        "README.md": """# Calibration Round 3 — PILOT-1L

**Mode:** Real expert case acquisition and dual-review process.  
**Not:** Taxonomy V2 implementation.  
**Not:** Strength Engine changes.

## Existing dual-reviewed (unchanged)

- CAL-000001
- CAL-000006

## Next free CAL ID

`CAL-000008` — create only when a real authorized chart passes intake.

## Round-3 outcome (this sprint)

No new authorized real charts were supplied.  
**new_real_cases = 0**. Acquisition queue and protocols are ready.
""",
        "ROUND_3_QUEUE.md": f"""# ROUND_3_QUEUE

**Sprint:** PILOT-1L  
**As of:** 2026-08-11  
**New charts received:** 0  
**Next free CAL ID:** `CAL-000008` (create only after authorized intake + calendar verification; do not reserve empty CAL records)

## Priority acquisition slots (ACQ IDs — not CAL IDs)

| acq_id | candidate_target | priority | status | remaining_needed | notes |
|---|---|---|---|---:|---|
| ACQ-R3-001 | very_weak | P0 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-002 | weak | P0 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-003 | balanced | P0 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-004 | slightly_strong | P1 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-005 | strong | P1 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-006 | very_strong | P2 | source_pending | 5 | ACQUISITION_TARGET_ONLY |
| ACQ-R3-007 | slightly_weak | P1 | source_pending | 3 | fill to gate=5; existing dual=2 |

candidate_target is **ACQUISITION_TARGET_ONLY**. It is not an expert label.

## Immediate ask

Deliver ≥3 authorized real charts for P0 targets (VERY_WEAK, WEAK, BALANCED) with consent, then calendar-verify and run Expert-A / blinded Expert-B.

## Coverage matrix

{matrix}
""",
        "ROUND_3_STATUS.md": """# ROUND_3_STATUS

**Decision:** `CALIBRATION_PARTIAL`  
**Readiness:** `DATA_GAP`  
**New real cases acquired:** **0**  
**New CAL IDs created:** **0**  
**Next free CAL ID:** `CAL-000008`

## Carry-forward

| Metric | Value |
|---|---:|
| Dual-reviewed | 2 (CAL-000001, CAL-000006) |
| Formal adjudications | 0 (both NOT_REQUIRED historically) |
| Next free ID | CAL-000008 |

## Round-3 outcomes

| Metric | Value |
|---|---:|
| Charts intake received | 0 |
| Calendar verified new | 0 |
| Expert-A completed (new) | 0 |
| Expert-B completed (new) | 0 |
| New dual-reviewed | 0 |

## Blockers

1. No authorized Round-3 birth charts supplied.
2. Fabrication forbidden.
3. Existing cases must not be relabeled to fill empty levels.
""",
        "ROUND_3_SOURCE_LOG.md": """# ROUND_3_SOURCE_LOG

| timestamp | source_event | result | notes |
|---|---|---|---|
| 2026-08-11 | round_3_open | no_charts_received | PILOT-1L started; queue prepared |
| 2026-08-11 | fabrication_check | pass | no fake CAL / expert labels created |

## Acceptable source categories (for future intake)

- user_provided_birth_data
- authorized_consultant_records
- authorized_historical_case_records
- authorized_anonymized_client_records
- public_case_material_lawful_and_verifiable

## Rejected / forbidden sources

- random invented dates
- synthetic charts as real
- ai_generated_charts_as_real
- unverified social claims
- copied labels without traceable source
""",
        "ROUND_3_REQUIREMENTS.md": """# ROUND_3_REQUIREMENTS

## Per missing level

| level | required_dual | current_dual | remaining | verification | expert_review | status |
|---|---:|---:|---:|---|---|---|
| very_weak | 5 | 0 | 5 | calendar_verified | dual blind | data_gap |
| weak | 5 | 0 | 5 | calendar_verified | dual blind | data_gap |
| slightly_weak | 5 | 2 | 3 | calendar_verified | dual blind | partial_not_covered |
| balanced | 5 | 0 | 5 | calendar_verified | dual blind | data_gap |
| slightly_strong | 5 | 0 | 5 | calendar_verified | dual blind | data_gap |
| strong | 5 | 0 | 5 | calendar_verified | dual blind | data_gap |
| very_strong | 5 | 0 | 5 | calendar_verified | dual blind | data_gap |

## Intake eligibility

source authorized · birth date · birth time (or explicit uncertain class) · birth place · timezone resolved · calendar verified · no unresolved solar-term ambiguity · not synthetic · not duplicate · privacy acceptable

## States

intake_pending → source_pending → data_incomplete → calendar_pending → calendar_verified → eligible_for_expert_a → expert_a_complete → eligible_for_expert_b → expert_b_complete → agreement_pending → adjudication_required | calibration_complete | rejected | withdrawn
""",
        "CALIBRATION_COVERAGE_ROUND_3.md": f"""# CALIBRATION_COVERAGE_ROUND_3

## Current real dual-reviewed

| case_id | expert_level | agreement | notes |
|---|---|---|---|
| CAL-000001 | slightly_weak | exact_match | unchanged |
| CAL-000006 | slightly_weak | exact_match | unchanged |

## New verified / dual-reviewed this round

**0**

## By expert level (dual-reviewed)

{matrix}

## Agreement / confidence / boundary / conflict

| Cohort | Count | Notes |
|---|---:|---|
| Exact match (dual) | 2 | both slightly_weak |
| Adjacent / non-adjacent new | 0 | no new dual reviews |
| Boundary dual | 0–1 historical candidates | BOUNDARY_DATA_GAP |
| Conflict dual | 1 historical (CAL-000001 model conflict) | still short of target |
| Expert LOW confidence dual | 0 | DATA_GAP |

## Remaining gaps

All seven levels remain below the ≥5 dual-reviewed gate.  
P0 gaps: VERY_WEAK, WEAK, BALANCED.

## Acquisition blockers

No authorized charts delivered in Round 3.
""",
        "ROUND_3_CALIBRATION_READINESS.md": """# ROUND_3_CALIBRATION_READINESS

**Status:** `DATA_GAP`

| Gate | Result |
|---|---|
| ≥5 dual-reviewed per level | FAIL |
| P0 levels covered | FAIL |
| New Round-3 dual reviews | 0 |
| Taxonomy freeze | NOT ALLOWED |

Allowed readiness labels used: **DATA_GAP** (also implies overall CALIBRATION_PARTIAL).

Do **not** claim CALIBRATION_COMPLETE.
""",
        "BOUNDARY_CASE_QUEUE.md": """# BOUNDARY_CASE_QUEUE

Priority boundary regions (acquisition targets only):

| boundary_region | target_dual | current | status |
|---|---:|---:|---|
| very_weak_weak | 2 | 0 | data_gap |
| weak_slightly_weak | 2 | 0 | data_gap |
| slightly_weak_balanced | 2 | 0–1 hist | data_gap |
| balanced_slightly_strong | 2 | 0 | data_gap |
| slightly_strong_strong | 2 | 0 | data_gap |
| strong_very_strong | 2 | 0 | data_gap |

No numeric thresholds. No pre-labeling as expert truth.
""",
        "CONFLICT_CASE_QUEUE.md": """# CONFLICT_CASE_QUEUE

Seek cases with observable conflict patterns (acquisition hints only):

| conflict_hint | status |
|---|---|
| seasonal_support_vs_structural_pressure | source_pending |
| strong_roots_vs_strong_control | source_pending |
| support_vs_drain | source_pending |
| structural_ambiguity | source_pending |
| temperature_conflict | source_pending |
| follow_pattern_ambiguity | source_pending |

Do not force a target taxonomy label.
""",
        "EXPERT_REVIEW_PROTOCOL.md": """# EXPERT_REVIEW_PROTOCOL

## Shared questions (Expert-A and Expert-B)

1. Overall Strength level?
2. Three strongest supporting factors?
3. Three strongest opposing factors?
4. Near a boundary?
5. Structural conflicts?
6. Confidence?
7. What evidence would change the assessment?

## Rules

- Do not instruct experts to match runtime.
- Do not impose BTE scoring methodology.
- Candidate vocabulary (research annotations only): very_weak, weak, slightly_weak, balanced, slightly_strong, strong, very_strong.
- Labels are NOT runtime taxonomy implementation.
""",
        "EXPERT_A_TEMPLATE.md": """# EXPERT_A_TEMPLATE

```text
case_id:
reviewer_id: expert_a
strength_level:   # very_weak|weak|slightly_weak|balanced|slightly_strong|strong|very_strong
confidence:       # high|medium|low|unknown
rationale:
key_supporting_evidence:
  - 
  - 
  - 
key_opposing_evidence:
  - 
  - 
  - 
boundary_notes:
uncertainty_notes:
would_change_if:
```
""",
        "EXPERT_B_TEMPLATE.md": """# EXPERT_B_TEMPLATE

```text
case_id:
reviewer_id: expert_b
strength_level:   # very_weak|weak|slightly_weak|balanced|slightly_strong|strong|very_strong
confidence:       # high|medium|low|unknown
rationale:
key_supporting_evidence:
  - 
  - 
  - 
key_opposing_evidence:
  - 
  - 
  - 
boundary_notes:
uncertainty_notes:
would_change_if:
```

## Blinding checklist (must be true before packet delivery)

- [ ] Expert-A label hidden
- [ ] Expert-A rationale hidden
- [ ] runtime score hidden
- [ ] runtime v1 band hidden
- [ ] taxonomy thresholds hidden
- [ ] adjudication result hidden

Packet contains only verified chart information + review protocol.
""",
        "AGREEMENT_PROTOCOL.md": """# AGREEMENT_PROTOCOL

## Label agreement

exact_match | adjacent_level | non_adjacent | conflicting

Do not convert adjacent_level into agreement automatically.

## Confidence agreement

Tracked separately from label agreement.
""",
        "ADJUDICATION_PROTOCOL.md": """# ADJUDICATION_PROTOCOL

Create adjudication only when experts disagree materially or case is flagged ambiguous.

Preserve:

- expert_a original
- expert_b original
- disagreement
- adjudicator judgment
- rationale
- resolution / unresolved questions

Never overwrite original expert judgments.  
Never manufacture consensus.  
Never choose runtime label to “fix” disagreement.
""",
        "PRIVACY_GUIDE.md": """# PRIVACY_GUIDE

Do not unnecessarily store: full names, addresses, phones, emails, government IDs, unrelated PII.

Prefer: case identifier, birth date/time/place granularity, gender if required, calendar basis, timezone, source classification.

Anonymize machine-readable calibration datasets.
""",
        "SOURCE_VERIFICATION_GUIDE.md": """# SOURCE_VERIFICATION_GUIDE

Every source needs a classification and authorization trail.

Record: source_precision, time_precision, place_precision, timezone_verified, birth_time_verified.

Do not assume supplied Four Pillars are correct — verify from birth data.
""",
        "CALENDAR_VERIFICATION_GUIDE.md": """# CALENDAR_VERIFICATION_GUIDE

Verify before expert review:

Gregorian date · local time · timezone · solar-term boundary · year/month/day/hour pillars.

Status: calendar_verified | calendar_unverified

Solar-term boundary ambiguity → do not enter main calibration pool until documented/resolved.
""",
        "PILOT_1L_SUMMARY.md": f"""# PILOT_1L_SUMMARY — Real Expert Case Acquisition & Calibration Round 3

**Purpose:** Acquire verified real BaZi cases and dual-expert reviews for missing Strength calibration levels.

**Outcome:** No authorized real charts were delivered in Round 3. Per no-data contingency: nothing fabricated; queue and protocols prepared; DATA_GAP recorded.

## Carry-forward

| Item | Value |
|---|---|
| Existing dual-reviewed | CAL-000001, CAL-000006 (unchanged) |
| Next free CAL ID | CAL-000008 |
| New CAL IDs created | 0 |

## Coverage (dual-reviewed)

| Level | Dual | Target | Gap |
|---|---:|---:|---:|
| very_weak | 0 | 5 | 5 |
| weak | 0 | 5 | 5 |
| slightly_weak | 2 | 5 | 3 |
| balanced | 0 | 5 | 5 |
| slightly_strong | 0 | 5 | 5 |
| strong | 0 | 5 | 5 |
| very_strong | 0 | 5 | 5 |

## Firewall

Taxonomy V2 / T1–T6 not implemented. Strength Engine / Golden / SYN / existing CAL unchanged.

---

Status:
- NEW_REAL_CASES_ACQUIRED: 0
- NEW_VERIFIED_CASES: 0
- NEW_DUAL_REVIEWED_CASES: 0
- EXISTING_DUAL_REVIEWED_CASES: 2
- VERY_WEAK_COVERAGE: 0
- WEAK_COVERAGE: 0
- SLIGHTLY_WEAK_COVERAGE: 2
- BALANCED_COVERAGE: 0
- SLIGHTLY_STRONG_COVERAGE: 0
- STRONG_COVERAGE: 0
- VERY_STRONG_COVERAGE: 0
- BOUNDARY_CASES: 0
- CONFLICT_CASES: 0
- EXPERT_AGREEMENT_COMPLETE: NO
- ADJUDICATION_REQUIRED: NO
- T1_T6_FROZEN: NO
- TAXONOMY_V2_IMPLEMENTED: NO
- PRODUCTION_CODE_CHANGED: NO
- STRENGTH_ENGINE_CHANGED: NO
- KNOWLEDGE_PACKAGES_CHANGED: NO
- GOLDEN_EXPECTED_CHANGED: NO
- CALIBRATION_DATA_CHANGED: NO
- AF1_CHANGED: NO
- TEST_REGRESSION: NO

Final Decision:
CALIBRATION_PARTIAL

Recommendation:
- NEXT_ACTION: Continue acquiring verified real charts and independent dual expert reviews, prioritizing VERY_WEAK, WEAK, and BALANCED coverage gaps.
""",
    }


CASES_README = """# cases/

Place completed CAL-* case folders here only after authorized intake + calendar verification.

Round 3: **no new CAL-* records created**.

Do not create empty CAL-000008 placeholders.
"""

EXPERT_README = """# expert_review/

Store Expert-A / Expert-B packets and blinded manifests here when reviews begin.

Round 3: **no expert judgments fabricated**.
"""


if __name__ == "__main__":
    build()
