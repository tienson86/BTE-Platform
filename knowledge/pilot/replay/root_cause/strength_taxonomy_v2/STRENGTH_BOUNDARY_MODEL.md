# Strength Boundary Model (Design)

**Status:** DESIGN — not implemented  

## Principle

A boundary case must **not** be classified solely by a hard numeric threshold.

Classification near edges uses:

```text
score position
+ profile tilt
+ evidence consistency
+ confidence
→ taxonomy label (possibly soft) + confidence band
```

## Boundary types

| Boundary | Description | Behavior |
|---|---|---|
| Central balanced | Near T3–T4 | Prefer BALANCED unless clear tilt |
| Slightly weak | Near T2–T3 | Allow SLIGHTLY_WEAK with MEDIUM confidence |
| Slightly strong | Near T4–T5 | Allow SLIGHTLY_STRONG with MEDIUM confidence |
| Weak / very weak | Near T1 | Require strong evidence completeness for VERY_WEAK |
| Strong / very strong | Near T6 | Require intensity evidence (e.g. root 3) for VERY_STRONG |
| Insufficient evidence | Missing producers / sparse matches | Prefer UNRESOLVED / LOW confidence; avoid extreme labels |
| Conflicting evidence | Large strengthen AND weaken masses | Prefer adjacent soft label or BALANCED + LOW/MEDIUM; never max confidence |

## Hard threshold ban (near edges)

Example anti-pattern (current v1 risk):

```text
0.649 → balanced
0.650 → strong
```

v2 requirement: if `|score − Ti| < δ` (δ to be calibrated), apply **boundary protocol**:

1. Inspect profile tilt  
2. Cap confidence ≤ MEDIUM  
3. Optionally publish `boundary_flag: true`  
4. Allow expert adjudication in Golden set  

## Pilot illustrations

| Case | Why boundary-relevant |
|---|---|
| 0003 | score 0.66; heavy drain vs season/root; expert slightly weak |
| 0005 | score 0.66; different profile; expert slightly strong |
| 0006 | mid 0.50; expert thiên nhược tilt |

## Insufficient / conflicting evidence outputs

| Condition | Taxonomy action | Confidence |
|---|---|---|
| Evidence completeness low | Avoid VERY_* | VERY_LOW / LOW |
| Strengthen ≈ weaken large | Soft mid / adjacent | MEDIUM or LOW |
| Upstream calendar uncertain | Defer or flag | LOW |
| Pattern follow contradicts strength | Publish both; lower confidence | MEDIUM or LOW |
