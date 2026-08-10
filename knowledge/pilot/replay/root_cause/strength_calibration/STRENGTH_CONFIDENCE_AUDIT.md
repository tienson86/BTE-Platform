# Strength Confidence Audit

## Algorithm (current)

From `engines/strength_engine/scorer.py`:

```text
confidence = min(1.0, len(matched_rules) / 5.0)   # if any matches
if level_rule is not None:
    confidence = min(1.0, confidence + 0.2)
```

No use of:

- distance to band threshold  
- conflicting strengthen vs weaken mass  
- temperature/strength producer disagreement  
- follow-pattern vs strength conflict  

---

## Per-case confidence

| Case | n matched | Dist to nearest band edge | Ambiguity signals | Confidence | Reflects ambiguity? |
|---|---:|---:|---|---:|---|
| 0001 | 6 | 0.87−0.65=0.22 (deep strong) | Expert polarity conflict; temp engine≠context | 1.0 | **No** |
| 0002 | 6 | 0.24 deep strong | Taxonomy only | 1.0 | N/A |
| 0003 | 6 | **0.01** above strong | Boundary expert; heavy drain vs season/root | 1.0 | **No** |
| 0004 | 5 | 0.19 | Clear strong | 1.0 | Acceptable |
| 0005 | 7 | **0.01** above strong | Expert mid-tilt | 1.0 | **No** |
| 0006 | 4 | mid (0.50) | Taxonomy tilt | 1.0 | **No** (should be lower if tilt uncertain) |
| 0007 | 6 | 0.11 | Clear strong | 1.0 | Acceptable |

All seven cases → **1.0**.

---

## Findings

1. **CONFIDENCE_ISSUE: YES** — boundary cases 0003/0005 receive identical confidence to obvious strong charts.  
2. Confidence currently measures **rule-hit density**, not **classification certainty**.  
3. Do **not** change the algorithm in PILOT-1B.

## Recommendations only (P2)

1. Factor `distance_to_threshold` into confidence (e.g. reduce when `|score−0.65|<0.05` or `|score−0.35|<0.05`).  
2. Penalize when strengthen_mass and weaken_mass are both large (CASE-0003).  
3. Optionally expose `confidence_drivers` in metadata (NOT_EXPOSED today beyond scalar).  
4. Keep continuous score as SSOT; confidence should not override band, only qualify it.
