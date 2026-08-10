# Data Requirements — Calibration Case Intake

## Required fields (every acquired case)

| Field | Required | Gate if missing |
|---|---|---|
| calibration_case_id | Yes | Reject intake |
| provenance | Yes (known class) | INCOMPLETE / reject UNKNOWN |
| source_reference | Yes | INCOMPLETE |
| anonymized_subject_label | Yes | Use CAL-id only |
| birth_date | Yes | INCOMPLETE |
| birth_time | Yes (or explicit unknown-hour policy) | PENDING_REVIEW if uncertain |
| location | Yes | INCOMPLETE |
| timezone | Yes | PENDING_REVIEW if unresolved |
| gender | Yes | INCOMPLETE |
| calendar_convention | Yes (tiết khí SSOT) | PENDING_REVIEW |
| four_pillars | Yes (after verify) | PENDING_REVIEW |
| calendar_verification | Yes = VERIFIED | Else not VERIFIED pool |
| solar_term_verification | Yes | PENDING_REVIEW |
| evidence_snapshot | Yes | PENDING_REVIEW |
| runtime_strength_score | Prefer | Record if Orchestrator available |
| runtime_strength_band | Prefer | Record if available |
| runtime_confidence | Prefer | Record if available |
| expert_review_1 | Yes for verified | PENDING_REVIEW |
| expert_review_2 | Yes for dual-reviewed / coverage gate | PENDING_REVIEW |
| adjudication | When protocol requires | PENDING_REVIEW |
| boundary_status | Yes | default false |
| conflict_status | Yes | default false |
| evidence_completeness | Yes | COMPLETE / PARTIAL / INCOMPLETE |
| review_status | Yes | — |
| inclusion_status | Yes | VERIFIED only if gates pass |

## Expert review payload

```text
reviewer_id: EXPERT-A | EXPERT-B
calibration_case_id
taxonomy_level: VERY_WEAK | WEAK | SLIGHTLY_WEAK | BALANCED | SLIGHTLY_STRONG | STRONG | VERY_STRONG
confidence: HIGH | MEDIUM | LOW
rationale: free text (main evidence)
key_strengthen_evidence: []
key_weaken_evidence: []
checklist_considered: season, roots, resource, companion, output, restriction, temperature, interactions, ...
blinded: true|false
runtime_score_seen: false (preferred on first pass)
```

## Verified pool gate

A case may enter **VERIFIED** only if:

1. Provenance known and not UNKNOWN/SYNTHETIC-as-truth  
2. Calendar + solar term verified  
3. Evidence snapshot present  
4. Expert 1 classification + rationale + confidence present  
5. No fabricated fields  
6. Privacy: no sensitive PII in published reports  

A case counts toward **dual-reviewed coverage** only if Expert 2 is also complete (independent).

Otherwise use:

- `PENDING_REVIEW`
- `INCOMPLETE`
- `VERIFIED_POOL_PROVISIONAL` (legacy single-reference seeds only)

## Workflow order

```text
Raw birth data
→ Calendar verification
→ Canonical four pillars
→ Strength evidence snapshot
→ Expert-A (blind)
→ Expert-B (blind)
→ Agreement class
→ Adjudication if required
→ Inclusion decision
```
