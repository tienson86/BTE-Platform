# Strength Taxonomy v2 (Candidate Design)

**Version identifier (proposed, not activated):** `strength_taxonomy_v2.0.0-candidate`  
**Current production:** `strength_taxonomy_v1` — 3 bands (`weak` / `balanced` / `strong`)  
**Status:** DESIGN ONLY — thresholds provisional / mostly symbolic  

## Score vs taxonomy vs profile vs confidence

| Concept | Answers |
|---|---|
| Score | How much strength is measured? (continuous) |
| Profile | Why? (multi-dimensional evidence) |
| Taxonomy | How classify? (ordinal label) |
| Confidence | How certain? |

**Forbidden collapse:** `score → label` without profile/boundary/confidence.

## Candidate levels

| ID | Vietnamese display | Semantic meaning | Score interval | Evidence characteristics | Confidence expectation | Adjacent relationship |
|---|---|---|---|---|---|---|
| `VERY_WEAK` | Thân rất nhược | Extreme weakness | below **T1** | Season death/prison dominant; weak/no root; heavy restriction | MEDIUM–HIGH if evidence complete | Weaker than WEAK |
| `WEAK` | Thân nhược | Clear weakness | T1–T2 | Net negative profile; weak root | MEDIUM–HIGH | Between VERY_WEAK and SLIGHTLY_WEAK |
| `SLIGHTLY_WEAK` | Thân hơi nhược / thiên nhược | Mild weak tilt | T2–T3 | Near mid; restriction/output ≥ support; or mid score with weak tilt profile | Often MEDIUM (boundary) | Soft edge of BALANCED |
| `BALANCED` | Thân trung bình / Trung hòa | Central equilibrium | T3–T4 | Near baseline; opposing masses similar | MEDIUM–HIGH if consistent | Center |
| `SLIGHTLY_STRONG` | Thân trung bình thiên vượng | Mild strong tilt | T4–T5 | Near mid; support/root ≥ restriction; season not death | Often MEDIUM | Soft edge of BALANCED |
| `STRONG` | Thân vượng | Clear strength | T5–T6 | Positive net; solid root and/or season | MEDIUM–HIGH | Below VERY_STRONG |
| `VERY_STRONG` | Thân rất vượng | Extreme strength | above **T6** | Strong root (3 chi) + supportive season; restriction limited relative to support | MEDIUM–HIGH | Stronger than STRONG |

## Symbolic thresholds (preferred until calibrated)

```text
VERY_WEAK | WEAK | SLIGHTLY_WEAK | BALANCED | SLIGHTLY_STRONG | STRONG | VERY_STRONG
          T1     T2              T3         T4                T5       T6
```

| Threshold | Meaning | Evidence required to estimate |
|---|---|---|
| T1 | very_weak / weak | ≥5 expert very_weak + weak charts |
| T2 | weak / slightly_weak | ≥5 each side + boundary set |
| T3 | slightly_weak / balanced | includes mid-tilt experts |
| T4 | balanced / slightly_strong | includes mid-tilt experts |
| T5 | slightly_strong / strong | includes 0.65-region charts |
| T6 | strong / very_strong | includes intensity-graded strong charts |

**Do not freeze T1–T6 from n=7.** Illustrative only if mapped to current scores later.

## Why 7 levels are justified (lexicon) but not numerically frozen

| Justification | Support |
|---|---|
| Expert vocabulary needs intensity + tilt | PILOT-1B |
| Identical scores ≠ identical expert labels | 0003 vs 0005 at 0.66 |
| Coarse v1 loses “rất vượng” | CASE-0002 |
| Numeric edges from n=7 | **Not supported** |

**Taxonomy support:** PARTIALLY_SUPPORTED (semantics yes; edges no).

## Compatibility note

CASE-0001 (score 0.87, expert slightly weak) shows taxonomy cannot “fix” model/expert disputes by relabeling alone. Profile + evidence review remain required.

## Versioning fields (future contract)

```text
taxonomy_version: "v1" | "v2"
strength_level_v1: weak|balanced|strong
strength_level_v2: VERY_WEAK|...|VERY_STRONG   # when implemented
strength_score: float
strength_profile: object
strength_confidence: HIGH|MEDIUM|LOW|...
```
