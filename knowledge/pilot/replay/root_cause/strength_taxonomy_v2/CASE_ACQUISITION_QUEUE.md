# CASE Acquisition Queue

**Rule:** Do not fabricate charts or expert labels.  
**Purpose:** Close coverage gaps for Taxonomy v2 calibration.

## Priority queue

| Queue ID | Target level | Boundary | Evidence profile target | Expert review | Priority | Status |
|---|---|---|---|---|---|---|
| AQ-001 | VERY_WEAK | VERY_WEAK/WEAK | season death/prison; weak root | dual | P0 | OPEN |
| AQ-002 | VERY_WEAK | — | extreme weakness | dual | P0 | OPEN |
| AQ-003 | WEAK | WEAK/SLIGHTLY_WEAK | clear net negative | dual | P0 | OPEN |
| AQ-004 | WEAK | — | weak with some root | dual | P0 | OPEN |
| AQ-005 | BALANCED | SLIGHTLY_WEAK/BALANCED | mid opposing masses | dual | P0 | OPEN |
| AQ-006 | BALANCED | BALANCED/SLIGHTLY_STRONG | mid tilt none | dual | P0 | OPEN |
| AQ-007 | SLIGHTLY_WEAK | — | fill to ≥5 (need +2) | dual | P1 | OPEN |
| AQ-008 | SLIGHTLY_STRONG | — | fill to ≥5 (need +4) | dual | P1 | OPEN |
| AQ-009 | STRONG | SLIGHTLY_STRONG/STRONG | fill to ≥5 (need +3) | dual | P1 | OPEN |
| AQ-010 | VERY_STRONG | STRONG/VERY_STRONG | intensity + root 3 | dual | P1 | OPEN |
| AQ-011 | any | conflict cohort | season≠root polarity | dual | P1 | OPEN |
| AQ-012 | any | conflict | resource vs output | dual | P2 | OPEN |
| AQ-013 | any | low confidence | incomplete producers | dual | P2 | OPEN |
| AQ-014 | — | dual-review backlog | re-review CAL-000001…007 | expert 2 | P0 | OPEN |

## Existing seeds (not queue items)

CAL-000001…007 already in calibration dataset as EXISTING_PILOT.

## Acquisition sources (allowed)

- EXPERT_SUPPLIED real charts  
- VERIFIED_REFERENCE charts with documented provenance  
- EXISTING_GOLDEN inputs **only if** expert Strength labels are newly collected (Expected not mutated here)

## Forbidden

- SYNTHETIC treated as ground truth  
- UNKNOWN provenance  
- Invented expert rationales/confidence
