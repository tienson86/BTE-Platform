# Recommended Next Action / Change Backlog

**None of P1–P4 implemented in PILOT-1C.**

## P0 — Objective correctness

**None confirmed** for Strength taxonomy design (inherits PILOT-1B: no polarity/arithmetic bug).

## P1 — Taxonomy design

- Keep `strength_taxonomy_v2` candidate + symbolic T1–T6  
- Prefer profile-aware classification over score-only  
- Dual-publish plan with v1 mapping as projection only  

## P2 — Expert calibration

- Execute `EXPERT_CALIBRATION_PROTOCOL.md`  
- Dual-review CASE-0001, 0003, 0005, 0006  
- Record adjudicated `reference_label_v2`  

## P3 — Golden Dataset expansion

- Collect ≥5 charts per level + boundary/low-confidence/conflict cohorts  
- Preserve 0003/0005 as boundary twin exemplars  
- No fabricated births  

## P4 — Future implementation

- Only after IMPLEMENTATION_READY gate  
- Additive API fields; no silent Expected overwrite  
- General evidence policies (sitting branch, officer dedup) — never `if case_id`  

## Single NEXT_ACTION

Execute the expert calibration protocol on an expanded Strength Golden cohort before any production taxonomy code.
