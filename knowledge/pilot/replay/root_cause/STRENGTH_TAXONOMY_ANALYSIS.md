# Strength Taxonomy Analysis — Pilot CASE-0001 → CASE-0007

**Sprint:** PILOT-1A  
**Mode:** Analysis only — no taxonomy implementation  
**Architecture Freeze:** AF-1 unchanged  

Expert classifications below are **reference only**. They were not forced into runtime.

---

## 1. Published runtime contract (current)

| Layer | Value |
|---|---|
| Levels | `strong` \| `balanced` \| `weak` |
| Thresholds (`database/12_strength/06_priority_rules.csv`) | `strong ≥ 0.65`, `weak ≤ 0.35`, else `balanced` |
| Reasoning strings | `Thân vượng` / `Trung hòa` / `Thân nhược` |
| Pattern label map | `strong→Vượng`, `weak→Nhược`, `balanced→Trung hòa` |
| Score path | rule components → aggregate → clamp `[0,1]` → band → reasoning |
| Confidence | saturates at `1.0` when enough rules match (non-discriminative here) |

### Mandatory separation

For every case this report separates:

1. **Score correctness** — is `strength_score` / polarity plausible given evidence rules?  
2. **Label/taxonomy correctness** — can published bands express the expert phrase?

---

## 2. Trace template (all cases)

```text
Raw strength evidence (season / root / support / drain / control / special)
        ↓
Evidence aggregation (matched_rules + component scores)
        ↓
strength_score ∈ [0,1]
        ↓
strength_band (strong | balanced | weak)
        ↓
strength label / reasoning (Thân vượng | Trung hòa | Thân nhược)
        ↓
confidence
        ↓
Published contract (StrengthView / API strength_*)
```

Cause codes:

| Code | Meaning |
|---|---|
| A | incorrect raw evidence |
| B | incorrect weighting |
| C | incorrect score |
| D | incorrect band thresholds |
| E | insufficient taxonomy granularity |
| F | incorrect label mapping |
| G | confidence handling |
| H | contract mismatch |
| I | upstream Calendar/BaZi error |
| J | expert classification disagreement |

---

## 3. Case-by-case table

| Case | Expert reference | Actual level | Score | Reasoning | Score correctness | Label/taxonomy correctness | Causes | Notes |
|---|---|---|---:|---|---|---|---|---|
| 0001 | balanced / slightly weak (`Thân trung bình / thiên nhược`) | `strong` | 0.87 | Thân vượng | **FAIL (polarity)** | Secondary: cannot say thiên nhược | **B, C, J** (+possible A) | Not a taxonomy-only issue |
| 0002 | very strong (`Thân rất vượng`) | `strong` | 0.89 | Thân vượng | **PASS (direction)** | **FAIL granularity** | **E, F** | Score OK; no `very_strong` |
| 0003 | slightly weak (`Thân hơi nhược`) BOUNDARY | `strong` | 0.66 | Thân vượng | **SUSPECT** | **FAIL** (hơi unsupported) | **C, D, E, H, J** | Barely over 0.65; Pattern `Tòng Nhi` conflicts |
| 0004 | strong (`Thân vượng`) | `strong` | 0.84 | Thân vượng | **PASS** | **PASS** | — | Coarse band sufficient |
| 0005 | balanced / slightly strong (`Thân trung bình thiên vượng`) | `strong` | 0.66 | Thân vượng | **BORDERLINE** | **FAIL** (thiên vượng unsupported) | **D, E, F** | Threshold cliff at 0.65 |
| 0006 | balanced / slightly weak (`Thân trung bình thiên nhược`) | `balanced` | 0.50 | Trung hòa | Deferred after Calendar RCA | Mid-band tilt unsupported | **I then E** | Calendar RCA: expert month wrong; strength on **correct** Mậu Ngọ chart is mid. Expert strength still not expressible as thiên nhược |
| 0007 | strong (`Thân vượng`) | `strong` | 0.76 | Thân vượng | **PASS** | **PASS** | observe **H** | Pattern also emits `Tòng Tài` while strength strong |

### Component snapshots (from Pilot Replay results)

| Case | sea | root | support | drain | control | matched_rules (abbrev) |
|---|---:|---:|---:|---:|---:|---|
| 0001 | 0.25 | 0.12 | 0.08 | 0.0 | −0.18 | sea_002, root_003, sup_001, ctl_*, **spc_004** |
| 0002 | 0.25 | 0.30 | 0.08 | −0.06 | −0.18 | sea_002, root_001, … |
| 0003 | 0.25 | 0.22 | 0.0 | −0.23 | −0.08 | sea_002, root_002, flw_* … |
| 0004 | 0.10 | 0.30 | 0.08 | −0.08 | −0.06 | sea_003, root_001, … |
| 0005 | −0.10 | 0.30 | 0.13 | −0.11 | −0.06 | sea_004, root_001, … |
| 0006 | −0.10 | 0.12 | 0.08 | 0.0 | −0.10 | sea_004, root_003, … |
| 0007 | 0.35 | 0.22 | 0.0 | −0.13 | −0.18 | sea_001, root_002, … |

---

## 4. Score correctness vs label correctness (summary)

| Case | Score story | Label story |
|---|---|---|
| 0001 | Engine score is **opposite** expert polarity; fixing labels alone will **not** clear the case | 3-band mapping from score→`strong` is internally consistent |
| 0002 | High score consistent with “rất vượng” | Published contract collapses to `strong` / Thân vượng |
| 0003 | Near-threshold strong vs soft weak expert + follow conflict | “hơi nhược” not in enum |
| 0004 | Matches | Matches |
| 0005 | Mid-strong components; cliff into `strong` | Expert wants mid + tilt |
| 0006 | After Calendar RCA, score on Ngọ chart is mid (`0.50`) — plausible mid band | Cannot express thiên nhược; expert strength phrase remains finer than contract |
| 0007 | Matches expert strong | Matches; separate Pattern follow consistency issue |

---

## 5. Is the 3-band model sufficient for the published contract?

**For a coarse product API (`strong|balanced|weak`): partially yes.**  
CASE-0004 / CASE-0007 show plain “Thân vượng” can PASS.

**For Pilot expert acceptance vocabulary: no.**

Reasons:

1. Experts use ~5–7 linguistic grades (rất / vượng / trung bình thiên vượng / trung bình / thiên nhược / hơi nhược / nhược).  
2. Cases 0002 / 0005 fail (or soft-fail) even when score direction is roughly right → **taxonomy gap**.  
3. Case 0001 fails on **score polarity** → **not taxonomy-only**.  
4. Threshold cliff at **0.65** (0003 & 0005 both at 0.66) amplifies disputes (**D**).  
5. Confidence always `1.0` here → no soft-boundary signal (**G**).

---

## 6. CASE-0006 dependency on Calendar RCA

Calendar RCA conclusion: expert month **Đinh Tỵ** is incorrect under classical tiết khí; live **Mậu Ngọ** is correct. Strength must be judged on the **Ngọ** chart.

On that chart, runtime `balanced / 0.50 / Trung hòa` is a coarse mid-band result. Expert “thiên nhược” is still a **granularity** mismatch (E), not an upstream pillar bug (I resolved for month).

Do **not** treat CASE-0006 strength as an engine polarity failure equivalent to CASE-0001.

---

## 7. Recommended future taxonomy (DO NOT IMPLEMENT in PILOT-1A)

Keep continuous `strength_score` as SSOT. Expand published levels only in a future versioned contract:

| Proposed level | Approx score band | Expert phrase examples |
|---|---|---|
| `very_weak` | ≤ 0.20 | Thân rất nhược |
| `weak` | (0.20, 0.35] | Thân nhược |
| `slightly_weak` | (0.35, 0.45] | Thân hơi nhược / thiên nhược |
| `balanced` | (0.45, 0.55) | Thân trung bình / Trung hòa |
| `slightly_strong` | [0.55, 0.65) | Thân trung bình thiên vượng |
| `strong` | [0.65, 0.80) | Thân vượng |
| `very_strong` | ≥ 0.80 | Thân rất vượng |

Optional: `tilt ∈ {none, toward_weak, toward_strong}` instead of proliferating mid enums.

Also recommend (future sprints, not this one):

- Recalibrate weights / special rules for **CASE-0001** polarity (**B/C**)  
- Align Pattern follow vs Strength (0003/0007) (**H**)  
- Make confidence reflect near-threshold / cross-producer conflict (**G**)

---

## 8. Decision gate

| Question | Answer |
|---|---|
| Implement new taxonomy now? | **No** |
| Change Expected strength labels? | **No** |
| Engine patch required for taxonomy? | **No** (contract evolution, not silent bugfix) |
| Engine investigation warranted for CASE-0001 score? | **Yes** (future sprint; stop-before-fix still applies until defect proven vs expert disagreement) |

### CASE-0001 stop note

Polarity failure may be:

- genuine scoring defect, **or**  
- expert disagreement (**J**)

PILOT-1A does **not** patch Strength rules. Next sprint should audit `spc_004` / season weights with expert review before any code change.
