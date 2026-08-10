# Expert Agreement Matrix (PILOT-1C)

Expert labels = **reference**, not automatic ground truth.  
Runtime = current v1 taxonomy + score from PILOT-1B extraction.

## Agreement categories

| Category | Meaning |
|---|---|
| EXACT_MATCH | Same coarse intent under v1 mapping and expert phrase |
| ADJACENT_MATCH | One soft step apart under v2 candidate (e.g. strong vs slightly strong) |
| WITHIN_TWO_LEVELS | Within two v2 steps |
| MODEL_DISAGREEMENT | Runtime model class conflicts with expert beyond adjacency |
| EXPERT_DISAGREEMENT | Reserved for multi-expert conflicts (N/A with single reference set) |
| INSUFFICIENT_EVIDENCE | Cannot judge fairly |

## Matrix

| Case | Expert (ref) | Runtime v1 | Score | v2 candidate if score-only* | Agreement | Drivers (A–J) |
|---|---|---|---:|---|---|---|
| 0001 | balanced / slightly weak | strong / Thân vượng | 0.87 | VERY_STRONG / STRONG | **MODEL_DISAGREEMENT** | B, D, E, G, J |
| 0002 | very strong | strong | 0.89 | VERY_STRONG | **ADJACENT_MATCH** (v1) / EXACT if v2 | A, D, E |
| 0003 | slightly weak | strong | 0.66 | SLIGHTLY_STRONG / STRONG cliff | **MODEL_DISAGREEMENT** | B, E, G, I, J |
| 0004 | strong | strong | 0.84 | STRONG / VERY_STRONG edge | **EXACT_MATCH** | A, D |
| 0005 | balanced / slightly strong | strong | 0.66 | same score as 0003 | **ADJACENT_MATCH** or MODEL | B, E, I |
| 0006 | slightly weak | balanced | 0.50 | BALANCED | **ADJACENT_MATCH** | B, E, J |
| 0007 | strong | strong | 0.76 | STRONG | **EXACT_MATCH** | A, E |

\*Score-only v2 is **illustrative and invalid as policy** — 0003/0005 prove profile is required.

## Driver codes

A score difference · B evidence composition · C evidence reliability · D root · E season · F temperature · G interaction · H pattern · I confidence · J expert interpretation

## Critical pair: 0.66 / 0.66

| | CASE-0003 | CASE-0005 |
|---|---|---|
| Score | 0.66 | 0.66 |
| Expert | slightly weak | slightly strong |
| Season | +25 Tướng | −10 Tù |
| Root | +22 | +30 |
| Drain | −23 | −11 |
| Support | 0 | +13 |

**Conclusion:** Expert distinction is **not** score difference (A). Primary explanations: **B evidence composition**, **E season**, **I confidence/boundary**. Taxonomy v2 must use profile.
