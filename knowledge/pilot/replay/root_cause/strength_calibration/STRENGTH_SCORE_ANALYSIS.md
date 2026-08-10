# Strength Score Analysis

Mandatory separation: **score correctness** vs **label/taxonomy correctness**.

## Formula (exposed)

```text
raw_total = Σ matched_rule.score   # by score_target buckets
normalized = clamp((raw_total + baseline50) / scale100, 0, 1)
band = strong if normalized >= 0.65
     | weak   if normalized <= 0.35
     | balanced otherwise
label = level_rule.reason  # Thân vượng | Trung hòa | Thân nhược
```

Source: `engines/strength_engine/scorer.py`, `database/12_strength/06_priority_rules.csv`.

No separate “raw score before baseline” is published on `StrengthResult`; extraction recorded `raw_total` from scorer internals.

---

## Score vs label table

| Case | Raw Score | Normalized | Current Band | Current Label | Expert Label | Score Issue | Taxonomy Issue |
|---|---:|---:|---|---|---|---|---|
| 0001 | 37 | 0.87 | strong | Thân vượng | balanced / slightly weak | **Plausibility disputed** (arithmetic OK) | Secondary (cannot say thiên nhược) |
| 0002 | 39 | 0.89 | strong | Thân vượng | very strong | No (direction OK) | **Yes** (no very_strong) |
| 0003 | 16 | 0.66 | strong | Thân vượng | slightly weak | Borderline / disputed | **Yes** (no slightly_weak) |
| 0004 | 34 | 0.84 | strong | Thân vượng | strong | No | No |
| 0005 | 16 | 0.66 | strong | Thân vượng | balanced / slightly strong | Threshold cliff | **Yes** |
| 0006 | 0 | 0.50 | balanced | Trung hòa | balanced / slightly weak | No (mid OK) | **Yes** (no thiên nhược) |
| 0007 | 26 | 0.76 | strong | Thân vượng | strong | No | No |

### Column definitions used here

| Column | Meaning |
|---|---|
| Score Issue | Is normalized score / polarity plausible given classical intent *and* expert reference? Arithmetic bugs listed separately. |
| Taxonomy Issue | Would a finer band/label resolve disagreement even if score stayed similar? |

---

## A–E checks per case

### CASE-0001

| Question | Answer |
|---|---|
| A Raw score plausible? | Internally consistent with matched rules; **expert-implausible** as “slightly weak” |
| B Normalized plausible? | Same — 0.87 follows formula |
| C Band appropriate for score? | **Yes** (≥0.65 → strong) |
| D Label appropriate for band? | **Yes** (Thân vượng) |
| E Expert more granular? | **Yes** |

### CASE-0002

A/B yes (high strong). C/D yes for 3-band. E **yes** — needs very_strong.

### CASE-0003

A/B disputed vs expert. C yes for current thresholds (cliff). D yes for band. E yes.

### CASE-0004 / 0007

A–D yes. E no (expert = coarse strong).

### CASE-0005

A/B mid-strong components → 0.66. C yes under current cliff. D yes for band. E yes.

### CASE-0006 (corrected)

A/B yes for mid (raw 0 → 0.50). C/D yes. E yes (thiên nhược).

---

## Arithmetic verification (sample)

CASE-0001: `25+12+8-10-8+10 = 37`; `(37+50)/100 = 0.87` ✓  
CASE-0006: `-10+12+8-10 = 0`; `(0+50)/100 = 0.50` ✓  

**No normalization bug found.**

---

## Interpretation

1. Band mapping from score is mechanical and correct under published thresholds.  
2. Expert disagreements on 0002/0005/0006 are primarily **taxonomy**.  
3. CASE-0001 is **not** a band-mapping bug; it is a question whether the **score should be that high** (weights / evidence coverage) — unresolved as implementation defect.  
4. CASE-0003/0005 sit on the **0.65 cliff** — threshold sensitivity, not label-map bugs.
