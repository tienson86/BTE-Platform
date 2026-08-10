# Acquisition Queue (Operational)

**Sprint:** PILOT-1E  
**Rule:** Do not fabricate charts or expert labels. Mark `DATA_GAP` when unavailable.  
**Next CAL ID:** `CAL-000008` (do not reassign prior IDs)

## Active targets

| target_id | taxonomy_target | boundary_target | evidence_profile | required_provenance | required_expert_review | priority | status | source | acquisition_date | verification_status |
|---|---|---|---|---|---|---|---|---|---|---|
| AQ-001 | VERY_WEAK | VERY_WEAK/WEAK | season death/prison; weak root | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P0 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-002 | VERY_WEAK | — | extreme weakness | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P0 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-003 | WEAK | WEAK/SLIGHTLY_WEAK | clear net negative | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P0 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-004 | WEAK | — | weak with some root | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P0 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-005 | BALANCED | SLIGHTLY_WEAK/BALANCED | mid opposing masses | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P0 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-006 | BALANCED | BALANCED/SLIGHTLY_STRONG | mid tilt none | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P0 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-007 | SLIGHTLY_WEAK | — | fill to ≥5 (need +2 dual) | EXPERT_SUPPLIED / EXISTING_PILOT dual | dual | P1 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-008 | SLIGHTLY_STRONG | — | fill to ≥5 (need +4 dual) | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P1 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-009 | STRONG | SLIGHTLY_STRONG/STRONG | fill to ≥5 (need +3 dual) | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P1 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-010 | VERY_STRONG | STRONG/VERY_STRONG | intensity + root | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P1 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-011 | any | conflict cohort | season≠root polarity | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P1 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-012 | any | conflict | resource vs output | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P2 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-013 | any | low confidence | incomplete / ambiguous | EXPERT_SUPPLIED or VERIFIED_REFERENCE | dual | P2 | OPEN / DATA_GAP | — | — | NOT_STARTED |
| AQ-014 | backlog | dual-review | re-review CAL-000001…007 | EXISTING_PILOT | expert 2 + adjudicate if needed | P0 | OPEN / DATA_GAP | EXISTING_PILOT | — | CHART_VERIFIED; EXPERT_2_PENDING |
| AQ-015 | CASE-0001 focus | conflict | sitting Ngọ + officer hypotheses | EXISTING_PILOT | dual | P0 | OPEN / DATA_GAP | EXISTING_PILOT | — | CHART_VERIFIED; EXPERT_2_PENDING |
| AQ-016 | CASE-0006 focus | SLIGHTLY_WEAK/BALANCED | corrected Mậu Ngọ projection | EXISTING_PILOT | dual | P0 | OPEN / DATA_GAP | EXISTING_PILOT | — | CALENDAR_CORRECTED; EXPERT_2_PENDING |

## Intake procedure

1. Register source in `SOURCE_REGISTER.md`.  
2. Collect fields per `DATA_REQUIREMENTS.md`.  
3. Assign next free `CAL-######`.  
4. Calendar-verify → evidence snapshot → Expert-A (blind) → Expert-B (blind) → agreement → adjudicate if required.  
5. Update `ACQUISITION_STATUS.md` and `calibration/dataset_index.json`.

## Status vocabulary

| Status | Meaning |
|---|---|
| OPEN | Target still needed |
| DATA_GAP | No verified real case available yet |
| INTAKE | Raw data received; verification in progress |
| PENDING_REVIEW | Chart OK; expert review incomplete |
| DUAL_COMPLETE | Two independent reviews recorded |
| VERIFIED | Meets verified-pool gates (incl. dual when required) |
| REJECTED | Failed provenance / calendar / privacy gate |
