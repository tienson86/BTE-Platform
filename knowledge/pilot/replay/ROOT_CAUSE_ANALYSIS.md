# Root Cause Analysis — Pilot Replay

## Method

For each failed/boundary case, identify the **first divergence layer**:

```text
Input → Validation → Calendar/BaZi → Strength → Follow → Transform
→ Decision → Luck → Interpretation → Report
```

Later layers are not blamed when an earlier layer already diverges.

## Per-case first divergence

| Case | Verdict | First divergence | Root cause class | Root cause |
|---|---|---|---|---|
| CASE-0001 | DISCREPANCY | Strength | ENGINE | Strength score 0.87 → strong / Thân vượng; expert expects thiên nhược |
| CASE-0002 | DISCREPANCY | Strength | CONTRACT | Expert “rất vượng”; engine taxonomy only strong/balanced/weak |
| CASE-0003 | BOUNDARY | Strength | BOUNDARY | Soft expert “hơi nhược”; actual strong 0.66; do not force |
| CASE-0004 | PASS | — | — | Pillars + Thân vượng match |
| CASE-0005 | DISCREPANCY | Strength | ENGINE/CONTRACT | Expert trung bình thiên vượng; actual strong at threshold 0.66 |
| CASE-0006 | DISCREPANCY | Calendar/BaZi | ENGINE/DATA | Month pillar Đinh Tỵ (expert) vs Mậu Ngọ (actual) |
| CASE-0007 | PASS | — | — | Pillars + Thân vượng match |
| CASE-0008 | REFERENCE_ONLY | Input | DATA | No birth datetime for orchestrator |
| CASE-0009 | BLOCKED | Input | DATA | No trusted transformation reference chart |

## Cross-cutting root causes

### RC-1 Strength taxonomy gap (CONTRACT)

Engine levels: `strong` | `balanced` | `weak`  
Expert vocabulary uses directional mid-bands and intensifiers (“thiên nhược/vượng”, “rất”, “hơi”).

Impact: CASE-0001/0002/0005 (and secondary on CASE-0006).

### RC-2 Strength polarity vs expert (ENGINE)

CASE-0001 actual is strongly vượng while expert expects thiên nhược. This is not only a label-mapping issue.

### RC-3 Month pillar mismatch (ENGINE/DATA)

CASE-0006 month stem/branch differs from expert-confirmed pillars under the provided solar datetime. Needs calendar/true-solar/solar-term investigation — without rewriting Expected.

### RC-4 Missing reference inputs (DATA)

CASE-0008/0009 cannot be replayed honestly without complete trusted inputs.

### RC-5 Missing producers / public surfaces (ARCHITECTURE — observe only)

- Transformation: NOT_PRODUCED on public path
- Decision: not wired into OrchestratorService
- Luck: computed then stripped from public payload

These are coverage gaps, not case-specific Expected overwrites.

### RC-6 Pattern follow signal semantics (ENGINE/CONTRACT)

`tong_cach` often equals main pattern label when follow is not detected (fallback), which can look like a follow label to naive consumers. Harness treats only explicit Tòng* markers as follow detection.

## What is not the root cause

- Interpretation/Report empty: they execute on runnable cases
- Portal absence: infrastructure for this run, not first divergence for expert strength cases
- External “Tòng Tài” on CASE-0008: reference only; not used as absolute truth

## Recommended ownership (next)

| Priority | Action | Owner hint |
|---|---|---|
| P0 | Investigate CASE-0006 month pillar with Calendar/BaZi traces | Engine Calendar/BaZi |
| P0 | Expert review of CASE-0001 strength polarity | Expert + Strength |
| P1 | Decide Strength V1 label contract vs expert vocabulary | Product / Knowledge |
| P1 | Collect CASE-0008 birth datetime + CASE-0009 verified chart | Pilot data |
| P2 | Contract decision on Luck/Decision/Transform public exposure | Architecture |
