# Taxonomy Proposal (NOT IMPLEMENTED)

Status: **TAXONOMY_PARTIALLY_SUPPORTED**

Do **not** implement in PILOT-1B. Do **not** change production thresholds.

---

## Why consider expansion?

Observed normalized scores in this pilot set:

```text
0.50, 0.66, 0.66, 0.76, 0.84, 0.87, 0.89
```

Expert lexicon requires intensity and mid-tilt language the 3-band enum cannot carry.

---

## Candidate levels

| Level | Candidate score range | Rationale from this sample | Expert phrases |
|---|---|---|---|
| VERY_WEAK | ≤ 0.20 | No pilot point; keep classical floor symmetry with very_strong | rất nhược |
| WEAK | (0.20, 0.35] | Preserve current weak threshold | nhược |
| SLIGHTLY_WEAK | (0.35, 0.48] | Below mid; room for 0001-like targets *if* scores recalibrate later | hơi nhược / thiên nhược |
| BALANCED | (0.48, 0.55) | Centers on baseline-empty 0.50; holds CASE-0006 | trung bình / Trung hòa |
| SLIGHTLY_STRONG | [0.55, 0.65) | Captures mid-tilt without crossing current strong cliff | trung bình thiên vượng |
| STRONG | [0.65, 0.80) | Keeps current strong floor; holds 0007 (0.76) | vượng |
| VERY_STRONG | ≥ 0.80 | Separates 0002 (0.89) / 0001(0.87)/0004(0.84) intensity — **note conflict** | rất vượng |

### Conflict acknowledgment

Under these candidate cutovers, CASE-0001 (0.87) would map to VERY_STRONG while expert says slightly weak — **taxonomy alone cannot fix CASE-0001**. That case needs score/model review first (future sprint), not a label rename.

Therefore 7-level taxonomy is justified for **granularity of agreeing/near-agreeing scores**, not as a cure for polarity-vs-expert disputes.

---

## Alternative (often better with n=7)

Keep 3 bands + add:

```text
tilt: none | toward_weak | toward_strong
intensity: normal | very
```

Example: `strong + intensity=very` ≈ rất vượng; `balanced + tilt=toward_weak` ≈ thiên nhược.

This avoids over-fitting seven numeric edges on seven charts.

---

## Support statement

| Result | Choice |
|---|---|
| TAXONOMY_SUPPORTED | No — insufficient sample to freeze edges |
| **TAXONOMY_PARTIALLY_SUPPORTED** | **Yes** — lexicon gap proven; edges provisional |
| TAXONOMY_NOT_YET_SUPPORTED | No — gap is real |

---

## Gate for future implementation

Before any production taxonomy change:

1. ≥30 charts with expert grades  
2. Explicit contract version bump  
3. CASE-0001 model review completed or explicitly deferred  
4. No case-specific thresholds
