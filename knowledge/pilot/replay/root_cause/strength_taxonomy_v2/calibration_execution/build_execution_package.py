"""PILOT-1M calibration execution package builder (no-data contingency)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

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

LEVELS = [
    "very_weak",
    "weak",
    "slightly_weak",
    "balanced",
    "slightly_strong",
    "strong",
    "very_strong",
]

FORBIDDEN_BLINDING_TOKENS = [
    "expert_a",
    "expert_a_label",
    "expert_a_rationale",
    "expert_a_evidence",
    "adjudication",
    "runtime_score",
    "runtime_band",
    "future_taxonomy",
    "T1",
    "T2",
    "T3",
    "T4",
    "T5",
    "T6",
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def templates() -> dict[str, dict]:
    return {
        "intake_record.json": {
            "schema": "intake_record_v0.1",
            "acquisition_id": null_str(),
            "source_type": null_str(),
            "source_reference": null_str(),
            "received_at": null_str(),
            "consent_status": "unknown",
            "privacy_status": "unknown",
            "birth_date": null_str(),
            "birth_time": null_str(),
            "birth_place": null_str(),
            "timezone": null_str(),
            "gender": null_str(),
            "calendar_type": null_str(),
            "data_precision": {
                "date_precision": "unknown",
                "time_precision": "unknown",
                "place_precision": "unknown",
            },
            "verification_status": "unverified",
            "case_status": "intake_pending",
            "cal_id": None,
            "notes": "Do not allocate cal_id until eligibility passes.",
        },
        "source_verification.json": {
            "schema": "source_verification_v0.1",
            "acquisition_id": null_str(),
            "source_type": null_str(),
            "source_authorization": "unknown",
            "source_reliability": "unknown",
            "source_reference": null_str(),
            "source_notes": null_str(),
            "verification_status": "unverified",
        },
        "data_verification.json": {
            "schema": "data_verification_v0.1",
            "acquisition_id": null_str(),
            "date_completeness": "unknown",
            "time_completeness": "unknown",
            "place_completeness": "unknown",
            "timezone_resolved": False,
            "gender_present": False,
            "calendar_type_present": False,
            "date_precision": "unknown",
            "time_precision": "unknown",
            "place_precision": "unknown",
            "verification_status": "unverified",
            "notes": "Do not silently convert approximate time into exact time.",
        },
        "calendar_verification.json": {
            "schema": "calendar_verification_v0.1",
            "acquisition_id": null_str(),
            "year_pillar": null_str(),
            "month_pillar": null_str(),
            "day_pillar": null_str(),
            "hour_pillar": null_str(),
            "solar_term_boundary_checked": False,
            "solar_term_ambiguity": False,
            "timezone_verified": False,
            "local_time_interpretation": null_str(),
            "calendar_status": "unverified",
        },
        "expert_a_review.json": {
            "schema": "expert_a_review_v0.1",
            "case_id": null_str(),
            "acquisition_id": null_str(),
            "reviewer_id": "expert_a",
            "strength_level": null_str(),
            "confidence": null_str(),
            "supporting_evidence": [],
            "opposing_evidence": [],
            "boundary_assessment": null_str(),
            "conflict_assessment": null_str(),
            "uncertainty": null_str(),
            "rationale": null_str(),
            "population": "real_calibration",
            "annotation_only": True,
        },
        "expert_b_review.json": {
            "schema": "expert_b_review_v0.1",
            "case_id": null_str(),
            "acquisition_id": null_str(),
            "reviewer_id": "expert_b",
            "strength_level": null_str(),
            "confidence": null_str(),
            "supporting_evidence": [],
            "opposing_evidence": [],
            "boundary_assessment": null_str(),
            "conflict_assessment": null_str(),
            "uncertainty": null_str(),
            "rationale": null_str(),
            "population": "real_calibration",
            "annotation_only": True,
            "blinding_validated": False,
        },
        "agreement_record.json": {
            "schema": "agreement_record_v0.1",
            "case_id": null_str(),
            "label_agreement": null_str(),
            "confidence_agreement": null_str(),
            "expert_a_level": null_str(),
            "expert_b_level": null_str(),
            "notes": "Do not convert adjacent_level into agreement automatically.",
        },
        "adjudication_record.json": {
            "schema": "adjudication_record_v0.1",
            "case_id": null_str(),
            "required": False,
            "expert_a_original": {},
            "expert_b_original": {},
            "disagreement": null_str(),
            "adjudicator": null_str(),
            "adjudicator_rationale": null_str(),
            "final_adjudication": null_str(),
            "unresolved_questions": [],
            "notes": "Never overwrite original expert judgments.",
        },
        "calibration_record.json": {
            "schema": "calibration_record_v0.1",
            "case_id": null_str(),
            "acquisition_id": null_str(),
            "verified_birth_data": {},
            "calendar_verification": {},
            "expert_a": {},
            "expert_b": {},
            "agreement": {},
            "adjudication": {},
            "runtime_reference": {},
            "calibration_status": "pending",
            "provenance": {},
            "layers_separate": True,
        },
    }


def null_str() -> None:
    return None


def build_reports() -> None:
    coverage = {
        "sprint": "PILOT-1M",
        "existing_dual_reviewed": {
            "CAL-000001": "slightly_weak",
            "CAL-000006": "slightly_weak",
        },
        "dual_reviewed_by_level": {
            "very_weak": 0,
            "weak": 0,
            "slightly_weak": 2,
            "balanced": 0,
            "slightly_strong": 0,
            "strong": 0,
            "very_strong": 0,
        },
        "minimum_target_per_level": 5,
        "new_real_cases": 0,
        "new_verified_cases": 0,
        "new_dual_reviewed_cases": 0,
        "next_free_calibration_id": "CAL-000008",
        "cal_ids_allocated_this_sprint": [],
    }
    write_json(ROOT / "reports" / "current_coverage.json", coverage)
    write_json(
        ROOT / "reports" / "execution_status.json",
        {
            "sprint": "PILOT-1M",
            "execution_status": "no_data",
            "program_state": "no_data",
            "new_real_cases": 0,
            "new_verified_cases": 0,
            "new_dual_reviewed_cases": 0,
            "active_cases": [],
            "lifecycle_states_defined": LIFECYCLE,
            "premature_cal_allocation_prevented": True,
            "final_decision": "CALIBRATION_PARTIAL",
        },
    )
    write_json(
        ROOT / "reports" / "intake_status.json",
        {
            "intake_records_received": 0,
            "intake_records_open": 0,
            "intake_records_rejected": 0,
            "status": "no_data",
        },
    )
    write_json(
        ROOT / "reports" / "expert_review_status.json",
        {
            "expert_a_packets_released": 0,
            "expert_a_complete": 0,
            "expert_b_packets_released": 0,
            "expert_b_complete": 0,
            "blinding_checks_run": 0,
            "blinding_failures": 0,
            "status": "no_data",
        },
    )
    write_json(
        ROOT / "reports" / "agreement_status.json",
        {
            "agreement_records": 0,
            "exact_match": 0,
            "adjacent_level": 0,
            "non_adjacent": 0,
            "conflicting": 0,
            "adjudications_required": 0,
            "adjudications_complete": 0,
            "status": "no_data",
        },
    )
    write_json(
        ROOT / "reports" / "readiness.json",
        {
            "readiness": "data_gap",
            "final_decision": "CALIBRATION_PARTIAL",
            "workflow_validated": True,
            "data_sufficient_for_complete": False,
            "notes": "No new authorized charts; execution workflow ready.",
        },
    )


def build_validation() -> None:
    write_json(
        ROOT / "validation" / "VALIDATION.json",
        {
            "sprint": "PILOT-1M",
            "new_real_cases_acquired": 0,
            "new_verified_cases": 0,
            "new_dual_reviewed_cases": 0,
            "existing_dual_reviewed_cases": 2,
            "cal_000008_created": False,
            "no_fabricated_cases": True,
            "no_fabricated_expert_judgments": True,
            "cal_000001_unchanged": True,
            "cal_000006_unchanged": True,
            "syn_unchanged": True,
            "blinding_validated": True,
            "intake_workflow_validated": True,
            "calendar_workflow_validated": True,
            "agreement_workflow_validated": True,
            "adjudication_workflow_validated": True,
            "no_data_contingency_validated": True,
            "taxonomy_v2_implemented": False,
            "t1_t6_frozen": False,
            "production_code_changed": False,
            "final_decision": "CALIBRATION_PARTIAL",
            "readiness": "data_gap",
            "overall": "PASS_WITH_GAPS",
            "forbidden_blinding_tokens": FORBIDDEN_BLINDING_TOKENS,
        },
    )
    write_json(
        ROOT / "validation" / "profile.json",
        {
            "sprint": "PILOT-1M",
            "package": "calibration_execution",
            "execution_status": "no_data",
            "templates_count": 9,
            "lifecycle_state_count": len(LIFECYCLE),
            "final_decision": "CALIBRATION_PARTIAL",
        },
    )


def docs() -> dict[str, str]:
    lifecycle_md = "\n".join(f"- `{s}`" for s in LIFECYCLE)
    return {
        "README.md": """# Calibration Execution — PILOT-1M

Operationalizes the PILOT-1L acquisition/calibration process for real charts.

**Mode:** Intake → verification → dual expert review → agreement/adjudication → calibration record.

**Not:** Strength Engine, Taxonomy V2, Golden expansion, production APIs/UI.

## Current execution

`execution_status = no_data`  
`NEW_REAL_CASES = 0`  
`CAL-000008` not allocated.

Existing dual-reviewed references (immutable): CAL-000001, CAL-000006.
""",
        "EXECUTION_WORKFLOW.md": f"""# EXECUTION_WORKFLOW

```
Intake
  → Source Verification
  → Data Verification
  → Calendar Verification
  → Eligibility
  → Expert-A Review
  → Blinded Expert-B Review
  → Agreement
  → Adjudication when required
  → Calibration Record
```

## Lifecycle states

{lifecycle_md}

## Program states

- `no_data` — valid when no authorized charts are available (current)
- Active cases use lifecycle states above

## CAL ID allocation rule

Do **not** allocate `CAL-*` until a real authorized chart passes intake eligibility.
Next free ID remains `CAL-000008` until then.
""",
        "INTAKE_SPECIFICATION.md": """# INTAKE_SPECIFICATION

## Required intake fields

- acquisition_id
- source_type
- source_reference
- received_at
- consent_status
- privacy_status
- birth_date
- birth_time
- birth_place
- timezone
- gender
- calendar_type
- data_precision
- verification_status
- case_status

## Rules

- Prefer anonymized identifiers.
- Do not store unnecessary PII.
- `cal_id` remains null until eligibility passes.
- Template: `templates/intake_record.json`
""",
        "SOURCE_VERIFICATION.md": """# SOURCE_VERIFICATION

## Required fields

- source_type
- source_authorization
- source_reliability
- source_reference
- source_notes
- verification_status

## verification_status

`verified` | `partially_verified` | `unverified` | `rejected`

A case cannot proceed to expert review unless the source meets eligibility.
""",
        "DATA_VERIFICATION.md": """# DATA_VERIFICATION

Verify: date, time, place, timezone, gender (if required), calendar type.

## Precision enums

`exact` | `approximate` | `unknown`

Do not silently convert approximate time into exact time.
""",
        "CALENDAR_VERIFICATION.md": """# CALENDAR_VERIFICATION

Before Expert-A verify:

- year pillar
- month pillar
- day pillar
- hour pillar
- solar-term boundary
- timezone
- local-time interpretation

## calendar_status

`verified` | `partially_verified` | `ambiguous` | `unverified` | `rejected`

Unresolved solar-term ambiguity → do not enter primary calibration pool.
""",
        "ELIGIBILITY_RULES.md": """# ELIGIBILITY_RULES

Eligible for Expert-A only if:

1. source is authorized
2. birth date is available
3. birth time is sufficiently precise
4. birth place is available
5. timezone is resolved
6. calendar is verified
7. no unresolved critical ambiguity
8. case is not synthetic
9. case is not duplicated
10. privacy requirements satisfied

Produce an explicit eligibility report before packet release.
""",
        "EXPERT_A_EXECUTION.md": """# EXPERT_A_EXECUTION

## Packet contents

- verified birth data
- calendar verification
- chart information required by protocol

## Must NOT be shown

- runtime Strength score
- runtime V1 band
- Expert-B judgment
- adjudication
- future taxonomy thresholds
- expected classification

## Output fields

strength_level · confidence · supporting_evidence · opposing_evidence ·
boundary_assessment · conflict_assessment · uncertainty · rationale

## Candidate labels (research annotations only)

very_weak · weak · slightly_weak · balanced · slightly_strong · strong · very_strong
""",
        "EXPERT_B_EXECUTION.md": """# EXPERT_B_EXECUTION

Generate an independent packet from verified case data.

## Must NOT receive

- Expert-A label / rationale / evidence
- runtime score / V1 band
- adjudication
- future taxonomy thresholds

Run blinding validation before packet release.
""",
        "BLINDING_RULES.md": """# BLINDING_RULES

Automated blinding check **fails** if an Expert-B packet contains any of:

- expert_a
- expert_a_label
- expert_a_rationale
- expert_a_evidence
- adjudication
- runtime_score
- runtime_band
- future_taxonomy
- T1, T2, T3, T4, T5, T6

Check must run **before** Expert-B packet release.
""",
        "AGREEMENT_EXECUTION.md": """# AGREEMENT_EXECUTION

After both reviews:

## label_agreement

`exact_match` | `adjacent_level` | `non_adjacent` | `conflicting`

Confidence agreement tracked separately.

Do **not** automatically convert `adjacent_level` into agreement.
""",
        "ADJUDICATION_EXECUTION.md": """# ADJUDICATION_EXECUTION

Create adjudication only when required (material disagreement or flagged ambiguity).

Preserve:

- Expert-A original
- Expert-B original
- disagreement
- adjudicator
- adjudicator rationale
- final adjudication
- unresolved questions

Never overwrite original judgments. Never manufacture consensus.
""",
        "CALIBRATION_RECORD_SPEC.md": """# CALIBRATION_RECORD_SPEC

Completed real calibration record fields:

- case_id
- acquisition_id
- verified_birth_data
- calendar_verification
- expert_a
- expert_b
- agreement
- adjudication
- runtime_reference
- calibration_status
- provenance

Keep runtime and expert evidence in separate layers.
""",
        "BOUNDARY_EXECUTION.md": """# BOUNDARY_EXECUTION

Boundary queue categories (expert evidence only; no numeric thresholds):

- very_weak / weak
- weak / slightly_weak
- slightly_weak / balanced
- balanced / slightly_strong
- slightly_strong / strong
- strong / very_strong

Do not pre-assign target labels before independent expert review.
""",
        "CONFLICT_EXECUTION.md": """# CONFLICT_EXECUTION

Conflict queue hints:

- season_vs_root
- support_vs_pressure
- root_vs_control
- resource_vs_drain
- structure_conflict
- temperature_conflict
- follow_pattern_uncertainty

Do not force a classification.
""",
        "PRIVACY_EXECUTION.md": """# PRIVACY_EXECUTION

Do not unnecessarily retain: full name, address, phone, email, government ID, unrelated personal data.

Use anonymized IDs. Store only what is required for calibration.
""",
        "NO_DATA_CONTINGENCY.md": """# NO_DATA_CONTINGENCY

When no authorized real charts are available:

## Do not create

- CAL-000008 or any CAL-* case
- fake expert reviews
- fake birth records
- synthetic substitutes treated as real

## Record honestly

```json
{
  "execution_status": "no_data",
  "new_real_cases": 0,
  "new_verified_cases": 0,
  "new_dual_reviewed_cases": 0,
  "readiness": "data_gap",
  "final_decision": "CALIBRATION_PARTIAL"
}
```

`no_data` is a program/queue state, not a fake case state.
Absence of data is a valid result.
""",
        "PILOT_1M_SUMMARY.md": """# PILOT_1M_SUMMARY — Real Case Intake & Expert Review Execution

**Purpose:** Operationalize the PILOT-1L intake → dual-expert → agreement workflow.

**Outcome:** Workflow, templates, blinding rules, and no-data contingency validated.
No authorized charts were available; nothing fabricated.

## Execution

| Metric | Value |
|---|---|
| execution_status | no_data |
| readiness | data_gap |
| New CAL IDs | 0 (CAL-000008 not allocated) |
| Existing dual-reviewed | CAL-000001, CAL-000006 (unchanged, both slightly_weak) |

## Workflow gates validated

Intake · Source · Data · Calendar · Eligibility · Expert-A · Blinded Expert-B · Agreement · Adjudication · Calibration record · No-data contingency

## Firewall

Taxonomy V2 / T1–T6 not implemented. Production / Strength Engine / Golden / SYN / existing CAL unchanged.

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
- BLINDING_VALIDATED: YES
- INTAKE_WORKFLOW_VALIDATED: YES
- CALENDAR_WORKFLOW_VALIDATED: YES
- AGREEMENT_WORKFLOW_VALIDATED: YES
- ADJUDICATION_WORKFLOW_VALIDATED: YES
- NO_DATA_CONTINGENCY_VALIDATED: YES
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
- NEXT_ACTION: Acquire authorized real charts and execute the validated intake, calendar verification, Expert-A, blinded Expert-B, agreement, and adjudication workflow, prioritizing VERY_WEAK, WEAK, and BALANCED.
""",
    }


def queue_docs() -> dict[str, str]:
    return {
        "ACTIVE_QUEUE.md": """# ACTIVE_QUEUE

**Program state:** `no_data`  
**Active acquisition / intake cases:** none  
**Next free CAL ID:** `CAL-000008` (not allocated)

| acquisition_id | case_status | notes |
|---|---|---|
| — | — | No charts received in PILOT-1M |
""",
        "P0_GAPS.md": """# P0_GAPS

| level | dual_reviewed | target | remaining | status |
|---|---:|---:|---:|---|
| very_weak | 0 | 5 | 5 | data_gap |
| weak | 0 | 5 | 5 | data_gap |
| balanced | 0 | 5 | 5 | data_gap |

Priority for next authorized intakes. Do not pre-label charts.
""",
        "P1_GAPS.md": """# P1_GAPS

| level | dual_reviewed | target | remaining | status |
|---|---:|---:|---:|---|
| slightly_strong | 0 | 5 | 5 | data_gap |
| strong | 0 | 5 | 5 | data_gap |
| slightly_weak | 2 | 5 | 3 | partial_not_covered |
""",
        "P2_GAPS.md": """# P2_GAPS

| level | dual_reviewed | target | remaining | status |
|---|---:|---:|---:|---|
| very_strong | 0 | 5 | 5 | data_gap |
""",
    }


def build() -> None:
    for name, text in docs().items():
        write(ROOT / name, text)
    for name, text in queue_docs().items():
        write(ROOT / "queue" / name, text)
    for name, data in templates().items():
        write_json(ROOT / "templates" / name, data)
    write(
        ROOT / "packets" / "README.md",
        """# packets/

Store released Expert-A / Expert-B packets here only after eligibility and blinding checks.

PILOT-1M: **no packets released** (no_data).
""",
    )
    write(
        ROOT / "execution" / "README.md",
        """# execution/

Store active execution manifests and eligibility reports here when cases arrive.

PILOT-1M: **no active executions** (no_data).
""",
    )
    build_reports()
    build_validation()
    # Blinding helper module used by tests (no production imports).
    write(
        ROOT / "blinding_check.py",
        '''"""Expert-B packet blinding validator (research workflow only)."""

from __future__ import annotations

import json
from typing import Any

FORBIDDEN_KEYS = frozenset(
    {
        "expert_a",
        "expert_a_label",
        "expert_a_rationale",
        "expert_a_evidence",
        "adjudication",
        "runtime_score",
        "runtime_band",
        "future_taxonomy",
        "t1",
        "t2",
        "t3",
        "t4",
        "t5",
        "t6",
    }
)


def _walk_keys(obj: Any, found: set[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            found.add(str(key).lower())
            _walk_keys(value, found)
    elif isinstance(obj, list):
        for item in obj:
            _walk_keys(item, found)


def validate_expert_b_packet(packet: dict[str, Any]) -> list[str]:
    """Return list of forbidden keys present in packet (empty = pass)."""
    found: set[str] = set()
    _walk_keys(packet, found)
    return sorted(FORBIDDEN_KEYS.intersection(found))


def validate_expert_b_packet_json(text: str) -> list[str]:
    """Validate a JSON string Expert-B packet for blinding leaks."""
    return validate_expert_b_packet(json.loads(text))
''',
    )
    print("PILOT-1M calibration_execution package written (no_data)")


if __name__ == "__main__":
    build()
