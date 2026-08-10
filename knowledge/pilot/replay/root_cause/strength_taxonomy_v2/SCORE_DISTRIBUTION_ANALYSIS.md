# Score Distribution Analysis

## Observed normalized scores

```text
CAL-000006  0.50  SLIGHTLY_WEAK (expert) / balanced (v1)
CAL-000003  0.66  SLIGHTLY_WEAK
CAL-000005  0.66  SLIGHTLY_STRONG   ← identical score, different expert level
CAL-000007  0.76  STRONG
CAL-000004  0.84  STRONG
CAL-000001  0.87  SLIGHTLY_WEAK (expert) / strong (v1)  ← model disagreement
CAL-000002  0.89  VERY_STRONG
```

## Clustering

- Mid cluster: 0.50  
- Cliff pair: 0.66 / 0.66  
- Strong cluster: 0.76–0.89  

Gaps: no scores below 0.50; no dense BALANCED band; no VERY_WEAK/WEAK.

## Score-only sufficiency test

| Question | Answer |
|---|---|
| Similar scores, different expert levels? | **YES** — 0.66 → SLIGHTLY_WEAK vs SLIGHTLY_STRONG |
| Different scores, same expert level? | **YES** — STRONG at 0.76 and 0.84; SLIGHTLY_WEAK at 0.50, 0.66, 0.87 |
| Evidence composition explains 0.66 twin? | **YES** — opposite season signs; different drain/support |
| Profile dimensions needed? | **YES** |
| Confidence explains ambiguity? | Should — runtime conf=1.0 fails; design conf=MEDIUM |

### Verdict

**SCORE_ONLY_CLASSIFICATION = NO**

Taxonomy v2 must consume Strength Profile + boundary/confidence, not normalized score alone.

## Machine artifact

`calibration/distributions/score_distribution.json`
