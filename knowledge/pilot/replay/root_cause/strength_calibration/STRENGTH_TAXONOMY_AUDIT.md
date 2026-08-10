# Strength Taxonomy Audit

## Current implementation

| Aspect | Contract |
|---|---|
| Levels | `weak` \| `balanced` \| `strong` |
| Thresholds | `weak ≤ 0.35`; `strong ≥ 0.65`; else `balanced` |
| Score range | continuous `[0, 1]` after normalization |
| Labels (reasoning) | `Thân nhược` / `Trung hòa` / `Thân vượng` |
| Pattern map | `Nhược` / `Trung hòa` / `Vượng` |
| Published fields | `strength_level`, `strength_score`, component scores, `confidence`, `reasoning`, `matched_rules` |
| Config | `baseline=50`, `scale=100` |

### Boundary behavior

| Normalized score | Band |
|---|---|
| 0.35 | weak (inclusive) |
| 0.3500001 … 0.649999 | balanced |
| 0.65 | strong (inclusive) |

Observed Pilot cliff: **0.66** (CASE-0003, CASE-0005) → strong by **0.01**.

### Confidence behavior

See `STRENGTH_CONFIDENCE_AUDIT.md` — saturates quickly; not taxonomy-aware.

### Label mapping

| Level | Label |
|---|---|
| weak | Thân nhược |
| balanced | Trung hòa |
| strong | Thân vượng |

No mapping exists for: rất / hơi / thiên nhược / thiên vượng.

---

## Expert vocabulary comparison

| Expert phrase | Representable in 3-band? |
|---|---|
| very weak | No (collapses to weak) |
| weak | Yes |
| slightly weak | No |
| balanced | Yes |
| slightly strong | No |
| strong | Yes |
| very strong | No |

---

## Sufficiency verdict

**Current 3-band model is insufficient** if Pilot expert phrases remain acceptance criteria.

It **is** sufficient as a coarse product enum **only if** acceptance explicitly maps expert phrases → preferred bands and treats granularity gaps as non-failures (as Pilot Replay harness partially did for “rất vượng”).

### Justification for considering 7 levels

Supported by this sample:

- CASE-0002 needs intensity above strong  
- CASE-0003/0005 need near-threshold soft grades  
- CASE-0001/0006 need mid-band tilt language  

**Not yet statistically fitted** — only 7 charts. Candidate thresholds in `TAXONOMY_PROPOSAL.md` are **hypotheses**, not calibrated production rules.

### Taxonomy support status

**TAXONOMY_PARTIALLY_SUPPORTED**

- Conceptually justified by expert lexicon + observed score spread  
- Numerically **not** yet supported enough to freeze production thresholds from n=7 alone
