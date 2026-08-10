# Expert Agreement Matrix

Expert labels are reference classifications, not automatic mathematical ground truth.

| Case | Expert Label | Runtime Label | Score Agreement | Band Agreement | Taxonomy Agreement | Confidence |
|---|---|---|---|---|---|---|
| 0001 | balanced / slightly weak | Thân vượng (strong) | No | No | No | 1.0 |
| 0002 | very strong | Thân vượng (strong) | Yes (direction) | Yes (coarse) | No | 1.0 |
| 0003 | slightly weak | Thân vượng (strong) | No | No | No | 1.0 |
| 0004 | strong | Thân vượng (strong) | Yes | Yes | Yes | 1.0 |
| 0005 | balanced / slightly strong | Thân vượng (strong) | Partial | No | No | 1.0 |
| 0006 | balanced / slightly weak | Trung hòa (balanced) | Partial (mid) | Partial | No | 1.0 |
| 0007 | strong | Thân vượng (strong) | Yes | Yes | Yes | 1.0 |

## Primary root-cause classification (exactly one per case)

| Case | Primary | Secondary | Rationale |
|---|---|---|---|
| 0001 | **EXPERT_DISAGREEMENT** | weighting / evidence-coverage (modeling) | No polarity-sign bug; arithmetic OK; expert mid/weak vs 0.87 strong |
| 0002 | **TAXONOMY_LIMITATION** | — | High score fits “very strong”; 3-band collapses label |
| 0003 | **THRESHOLD_ERROR** | TAXONOMY_LIMITATION, EXPERT_DISAGREEMENT | 0.66 cliff; soft expert “slightly weak” |
| 0004 | *(none — agree)* | — | PASS under coarse contract |
| 0005 | **TAXONOMY_LIMITATION** | THRESHOLD_ERROR | Expert mid-tilt; 0.66 strong cliff |
| 0006 | **TAXONOMY_LIMITATION** | EXPERT_DISAGREEMENT | Corrected chart mid-score; cannot say thiên nhược; **not** Calendar |
| 0007 | *(none — agree)* | observe Pattern follow vs strength | PASS under coarse contract |

### Category legend (unused as primary here)

| Code | Used? |
|---|---|
| SCORE_ERROR | Not as primary — no arithmetic defect |
| POLARITY_ERROR | Not used — no sign inversion |
| LABEL_MAPPING_ERROR | Not primary — labels correctly follow bands |
| CONFIDENCE_ERROR | Secondary systemic (all 1.0) |
| UPSTREAM_INPUT_ERROR | Not for Strength after PILOT-1A CASE-0006 correction |
| UNRESOLVED | Score *plausibility* of 0001 remains research-open, but primary class is expert disagreement vs current model |

---

## CASE-0006 special documentation

| Item | Value |
|---|---|
| Original fixture month | Đinh Tỵ |
| Corrected chart month | **Mậu Ngọ** |
| Reason | PILOT-1A: Mang Chủng solar-term month; expert Tỵ invalid under tiết khí SSOT |
| Strength on corrected chart | balanced / 0.50 / Trung hòa |
| Classification now | **TAXONOMY_LIMITATION** (not Calendar) |
| Golden Expected mutated? | **No** |
