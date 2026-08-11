"""PILOT-1H diagnostic package builder (read-only w.r.t. production).

Writes reports under knowledge/pilot/replay/root_cause/strength_model_diagnostic/.
Does not modify Strength Engine, rules, calibration, Golden, or synthetic fixtures.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
VALIDATION = ROOT / "validation"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def build() -> None:
    write(ROOT / "README.md", README)
    write(ROOT / "STRENGTH_EVIDENCE_DIMENSION_MATRIX.md", EVIDENCE_MATRIX)
    write(ROOT / "SCORE_TRACE_ANALYSIS.md", SCORE_TRACE)
    write(ROOT / "SCORE_SATURATION_ANALYSIS.md", SATURATION)
    write(ROOT / "VERY_WEAK_BOUNDARY_ANALYSIS.md", VERY_WEAK)
    write(ROOT / "BALANCED_PROFILE_ANALYSIS.md", BALANCED)
    write(ROOT / "TAXONOMY_RESOLUTION_ANALYSIS.md", TAXONOMY_RES)
    write(ROOT / "SCORE_COLLISION_ANALYSIS.md", COLLISION)
    write(ROOT / "SUPPORT_PRESSURE_DIAGNOSTIC.md", SUPPORT_PRESSURE)
    write(ROOT / "SEASONAL_WEIGHTING_DIAGNOSTIC.md", SEASONAL)
    write(ROOT / "ROOTING_DIAGNOSTIC.md", ROOTING)
    write(ROOT / "STRENGTH_PROFILE_REQUIREMENTS.md", PROFILE_REQ)
    write(ROOT / "TAXONOMY_BOUNDARY_ANALYSIS.md", BOUNDARY)
    write(ROOT / "V1_TO_V2_PROJECTION_ANALYSIS.md", V1V2)
    write(ROOT / "CONFIDENCE_MODEL_DIAGNOSTIC.md", CONFIDENCE)
    write(ROOT / "SYNTHETIC_EXPECTATION_AUDIT.md", SYN_AUDIT)
    write(ROOT / "REAL_CALIBRATION_DIAGNOSTIC.md", REAL_CAL)
    write(ROOT / "STRENGTH_MODEL_DIAGNOSTIC_SUMMARY.md", SUMMARY)
    write(ROOT / "PRE_IMPLEMENTATION_RECOMMENDATIONS.md", PRE_IMPL)
    write(ROOT / "PILOT_1H_SUMMARY.md", PILOT_SUMMARY)
    write(ROOT / "VALIDATION.md", VALIDATION_MD)

    write_json(REPORTS / "evidence_matrix.json", EVIDENCE_MATRIX_JSON)
    write_json(REPORTS / "score_trace.json", SCORE_TRACE_JSON)
    write_json(REPORTS / "saturation.json", SATURATION_JSON)
    write_json(REPORTS / "boundary_analysis.json", BOUNDARY_JSON)
    write_json(REPORTS / "collision_analysis.json", COLLISION_JSON)
    write_json(REPORTS / "profile_requirements.json", PROFILE_JSON)
    write_json(REPORTS / "confidence_analysis.json", CONFIDENCE_JSON)
    write_json(REPORTS / "synthetic_audit.json", SYN_AUDIT_JSON)
    write_json(VALIDATION / "VALIDATION.json", VALIDATION_JSON)
    write_json(VALIDATION / "profile.json", PROFILE_META_JSON)
    print("PILOT-1H diagnostic package written")


README = """# Strength Model Diagnostic — PILOT-1H

**Mode:** DIAGNOSTIC DESIGN only. Production Strength behavior unchanged.

## Populations (strictly separate)

| Population | IDs | Role |
|---|---|---|
| REAL_CALIBRATION | CAL-000001, CAL-000006 (dual-reviewed); other CAL-* provisional only | Expert-backed |
| SYNTHETIC_STRESS | SYN-STR-000001..000021 | Diagnostic stress labels only |
| RUNTIME_REFERENCE | engine outputs on both | Observations, not truth |

Never merge into one calibration metric.

## Scope

Allowed: read-only analysis + reports under this folder.  
Forbidden: engine/rules/thresholds/Golden/Knowledge/AF-1/calibration label edits.

## Key read-only sources

- `../strength_calibration/`
- `../strength_taxonomy_v2/` (+ calibration, acquisition, expert_review, adjudication)
- `../../synthetic_strength/`
- `database/12_strength/` (read-only)
- `engines/strength_engine/` (read-only)
"""

EVIDENCE_MATRIX = """# STRENGTH_EVIDENCE_DIMENSION_MATRIX

**Sprint:** PILOT-1H  
**Sources:** `database/12_strength/*`, `engines/strength_engine/utils/context_builder.py`, `scorer.py` (read-only)

## Score pipeline (observed)

```text
StrengthContext fields (builder)
  -> rule match (season/root/support/control/drain/combination/special)
  -> raw bucket sum
  -> normalized = clamp((raw + baseline50) / scale100, 0, 1)
  -> v1 band via level rules (weak<=0.35, strong>=0.65, else balanced)
```

## Matrix

| Dimension | Exists | Used in score | Weight visible | Direction | Granularity | Loss of information | Diagnostic source |
|---|---|---|---|---|---|---|---|
| seasonal_strength | YES | YES | YES (CSV score) | +/- via month_status | 5 ordinals (Dac lenh..Tu) | Branch identity / phase lost after month_status | 01_season_rules; context.month_status |
| month_branch_support | PARTIAL | INDIRECT | via month_status / month_branch_ten_god | mixed | coarse | Month branch as support vs season collapsed | context_builder; special rules |
| day_branch_root | PARTIAL | YES (in root_count) | via root_level ladder | + if same element hidden | count-of-branches | Day vs other branch not published separately | root_rules; _compute_root |
| other_branch_root | PARTIAL | YES (in root_count) | same ladder | + | count | Which branches root is lost in label | root_rules |
| same_element_support | YES | YES | YES | + | single support_type winner | Multiple supports collapsed to one type | support_rules; _detect_support_type |
| resource_support | YES | YES | YES | + | type + contains Chinh An | Magnitude of resource mass coarse | sup_002/sup_006 |
| output_drain | YES | YES | YES | - | drain_type + contains | Overlaps control output path | flow_rules + ctl_002 |
| wealth_pressure | YES | YES | YES | - | drain/control wealth labels | Wealth vs officer not profiled separately in score | flow/control |
| officer_pressure | YES | YES | YES | - | control_type + That Sat contains | Possible double-count with control_type | ctl_001/ctl_006 |
| hidden_stem_support | PARTIAL | YES (root/support path) | via root_level / hidden lists | + | hidden in root only | Hidden stem as support vs pressure not typed | HIDDEN map; root |
| hidden_stem_pressure | NO | NO | NO | UNKNOWN | none | Sitting branch pressure (e.g. day-branch fire) not a scored dimension | PILOT evidence model gap |
| temperature | CONTEXT ONLY | NO (not in buckets) | NO | UNKNOWN | season-derived cold/hot/warm | TemperatureEngine separate; not in strength sum | context.temperature_type |
| combination | YES | YES | YES | +/- | companion/resource/officer counts | True gan-zhi hop/hoa not modeled; count proxies | 07_special cmb_* |
| clash | RULE HINT | NO active dedicated | NO | UNKNOWN | none in active CSV beyond control root-destroyed label | Xung not independently scored | ctl_004 label exists; builder rarely sets |
| punishment | NO | NO | NO | UNKNOWN | none | Not in strength DB | README / CSV audit |
| harm | NO | NO | NO | UNKNOWN | none | Not in strength DB | CSV audit |
| destruction | NO | NO | NO | UNKNOWN | none | Not in strength DB | CSV audit |
| special_structure | YES | YES | YES | +/- / level override | special rules | High-priority special can override level | 07_special_rules |
| follow_pattern | NO in Strength | NO | NO | UNKNOWN | Pattern Engine later | Follow not strength-score input | architecture |
| transformation | PARTIAL | via combination labels | limited | mixed | coarse | Hop hoa sinh than / mat goc labels only | support/control special |
| other structural evidence | PARTIAL | YES (special/combo) | YES | mixed | rule-based | Confidence non-discriminative (often 1.0) | scorer confidence formula |

## Q1 answer (what the score measures)

The published `strength_score` is a **normalized sum of matched rule contributions** across seven buckets:

season + root + support + drain + control + combination + special

It is **primarily** driven by:

1. seasonal month_status ordinal
2. root_level ladder (including vo can penalty)
3. a single support_type (+ optional An/Ty contains bonuses)
4. control_type / officer contains penalties
5. drain_type / output-wealth contains / drain_count
6. occasional special/combination bonuses

It is **not** a full multi-factor BaZi strength profile. Hidden sitting pressure, clash/punishment/harm, TemperatureEngine, and follow structures are largely outside the sum.
"""

SCORE_TRACE = """# SCORE_TRACE_ANALYSIS

**Sprint:** PILOT-1H  
**Normalization (read-only):** `(raw_total + 50) / 100` clamped to `[0, 1]`  
**Bands:** weak `<=0.35`, strong `>=0.65`, else balanced

## REAL_CALIBRATION

### CAL-000001

| Field | Value |
|---|---|
| population | REAL_CALIBRATION |
| day_master | canh |
| expert_label_if_available | SLIGHTLY_WEAK (Expert-A + Expert-B EXACT_MATCH) |
| expected_label_if_synthetic | N/A |
| raw_score | 37.0 |
| normalized_score | 0.87 |
| current_band | strong |
| major_support_factors | season Tuong +25; root 1-chi +12; companion support +8; special An cold +10 |
| major_pressure_factors | control Quan/That Sat -18 |
| seasonal_factor | +25 (Tuong / winter) |
| rooting_factor | +12 (Thong can 1 chi) |
| support_factor | +8 |
| pressure_factor | -18 control; drain 0 |
| information_loss | Sitting day-branch ngo fire not a separate scored pressure; support/pressure sources collapsed into buckets; expert polarity opposite runtime |
| diagnostic_notes | MODEL_DISAGREEMENT; same pillar family as SYN-STR-000007 |

### CAL-000006

| Field | Value |
|---|---|
| population | REAL_CALIBRATION |
| day_master | quy |
| expert_label_if_available | SLIGHTLY_WEAK (dual EXACT_MATCH) |
| expected_label_if_synthetic | N/A |
| raw_score | 0.0 |
| normalized_score | 0.50 |
| current_band | balanced |
| major_support_factors | root +12; support +8 |
| major_pressure_factors | season Tu -10; control -10 |
| seasonal_factor | -10 |
| rooting_factor | +12 |
| support_factor | +8 |
| pressure_factor | -10 |
| information_loss | Mid-band tilt (thien nhuoc) not expressible; profile near zero-sum |
| diagnostic_notes | Adjacent MODEL_DISAGREEMENT; BOUNDARY_CANDIDATE |

## SYNTHETIC_STRESS

### SYN-STR-000001 (very_weak)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | quy |
| expected_label_if_synthetic | very_weak |
| expert_label_if_available | N/A |
| raw_score | -49.0 |
| normalized_score | 0.01 |
| current_band | weak |
| major_support_factors | none (support 0) |
| major_pressure_factors | vo can -20; season Tu -10; drain -13; control -6 |
| seasonal_factor | -10 |
| rooting_factor | -20 |
| support_factor | 0 |
| pressure_factor | -19 combined drain+control |
| information_loss | Extreme intensity named only as weak |
| diagnostic_notes | Strong directional extreme; floor nearly hit |

### SYN-STR-000004 (weak)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | at |
| expected_label_if_synthetic | weak |
| expert_label_if_available | N/A |
| raw_score | -8.0 |
| normalized_score | 0.42 |
| current_band | balanced |
| major_support_factors | season Tuong +25; combination special +8 |
| major_pressure_factors | vo can -20; drain -11; control -10 |
| seasonal_factor | +25 (dominates) |
| rooting_factor | -20 |
| support_factor | 0 |
| pressure_factor | -21 |
| information_loss | Weak intent offset by positive season into balanced |
| diagnostic_notes | SEASONAL_WEIGHTING_GAP vs synthetic expectation |

### SYN-STR-000007 (slightly_weak)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | canh |
| expected_label_if_synthetic | slightly_weak |
| expert_label_if_available | N/A (mirrors CAL-000001 structure) |
| raw_score | 37.0 |
| normalized_score | 0.87 |
| current_band | strong |
| major_support_factors | season +25; root +12; support +8; special +10 |
| major_pressure_factors | control -18 |
| seasonal_factor | +25 |
| rooting_factor | +12 |
| support_factor | +8 |
| pressure_factor | -18 |
| information_loss | Moc/hoa pressure not fully represented vs season/An boost |
| diagnostic_notes | SUPPORT_PRESSURE_GAP; runtime identical family to CAL-000001 |

### SYN-STR-000010 (balanced)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | mau |
| expected_label_if_synthetic | balanced |
| expert_label_if_available | N/A |
| raw_score | -11.0 |
| normalized_score | 0.39 |
| current_band | balanced |
| major_support_factors | root 3-chi +30; An support +10 |
| major_pressure_factors | season Tu -25; control -18; drain -8 |
| seasonal_factor | -25 |
| rooting_factor | +30 |
| support_factor | +10 |
| pressure_factor | -26 |
| information_loss | Strong opposing masses cancel into one mid band |
| diagnostic_notes | Equilibrium via cancellation, not quiet chart |

### SYN-STR-000015 (slightly_strong)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | mau |
| expected_label_if_synthetic | slightly_strong |
| expert_label_if_available | N/A |
| raw_score | -19.0 |
| normalized_score | 0.31 |
| current_band | weak |
| major_support_factors | support An +15; root +12 |
| major_pressure_factors | season Tu -25; drain -11; control -10 |
| seasonal_factor | -25 |
| rooting_factor | +12 |
| support_factor | +15 |
| pressure_factor | -21 |
| information_loss | Synthetic tilt vs death-season dominance |
| diagnostic_notes | TAXONOMY_RESOLUTION_GAP; also possible SYNTHETIC_EXPECTATION_REVIEW |

### SYN-STR-000018 (strong)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | canh |
| expected_label_if_synthetic | strong |
| expert_label_if_available | N/A |
| raw_score | 82.0 |
| normalized_score | 1.00 |
| current_band | strong |
| major_support_factors | Dac lenh +35; root 2-chi +22; support +13; combo +12 |
| major_pressure_factors | none observed |
| seasonal_factor | +35 |
| rooting_factor | +22 |
| support_factor | +13 |
| pressure_factor | 0 |
| information_loss | Raw headroom above 50 clipped by normalization |
| diagnostic_notes | Ceiling case within STRONG cohort |

### SYN-STR-000019 (very_strong)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | nham |
| expected_label_if_synthetic | very_strong |
| expert_label_if_available | N/A |
| raw_score | 107.0 |
| normalized_score | 1.00 |
| current_band | strong |
| major_support_factors | Dac lenh +35; root +22; support +18; special/combo +32 |
| major_pressure_factors | none observed |
| seasonal_factor | +35 |
| rooting_factor | +22 |
| support_factor | +18 |
| pressure_factor | 0 |
| information_loss | Raw 107 vs 018 raw 82 both publish 1.00; intensity lost |
| diagnostic_notes | Score saturation + taxonomy projection collapse |
"""

SATURATION = """# SCORE_SATURATION_ANALYSIS

**Sprint:** PILOT-1H  
**Focus:** SYN-STR-000019 / 000020 / 000021 (and STRONG peers)

## Observed

| case_id | synthetic_expected | raw_total | normalized | v1_band |
|---|---|---:|---:|---|
| SYN-STR-000018 | strong | 82.0 | 1.000 | strong |
| SYN-STR-000020 | very_strong | 87.0 | 1.000 | strong |
| SYN-STR-000021 | very_strong | 98.0 | 1.000 | strong |
| SYN-STR-000019 | very_strong | 107.0 | 1.000 | strong |
| SYN-STR-000014 | slightly_strong | UNKNOWN_OR_HIGH | 1.000 | strong |
| SYN-STR-000016 | strong | UNKNOWN_OR_HIGH | 1.000 | strong |
| SYN-STR-000017 | strong | UNKNOWN_OR_HIGH | 1.000 | strong |

(Raw for 019/020/021/018 from PILOT-1G results; 014/016/017 also publish 1.000.)

## Mechanism A — score saturation

Formula: `normalized = clamp((raw + 50) / 100, 0, 1)`.

Any `raw >= 50` yields `normalized = 1.0`.

VERY_STRONG extremes have raw 87..107 → **all clipped**.

Cause class:

- **normalization clipping / insufficient published dynamic range** (primary)
- weighted sum can still grow in raw space (ranking exists pre-clamp)
- not primarily missing evidence (these charts already match many strengthen rules)

## Mechanism B — taxonomy projection collapse

Even without clamp, v1 only publishes `strong` for scores `>= 0.65`.

`very_strong` cannot appear on the contract.

Therefore:

| Problem | Independent? | Evidence |
|---|---|---|
| A score saturation | YES | raw 82 vs 107 both → 1.000 |
| B taxonomy projection collapse | YES | no very_strong enum in v1 |

They are **not the same problem**. Fixing only band labels would not restore intensity ranking once score is clipped to 1.0. Exposing raw_total / unclamped score / profile intensity could restore ranking without renaming taxonomy.

## Conclusion

VERY_STRONG vs STRONG is currently **NOT DISTINGUISHABLE** on published score+band.  
Raw totals remain ordered: 019(107) > 021(98) > 020(87) > 018(82).
"""

VERY_WEAK = """# VERY_WEAK_BOUNDARY_ANALYSIS

**Sprint:** PILOT-1H  
**Cases:** SYN-STR-000001, 000002, 000003

## Observed

| case_id | raw | score | v1 | root_level | season | notes |
|---|---:|---:|---|---|---|---|
| 000001 | -49 | 0.010 | weak | Vo can | Tu | near floor |
| 000003 | -25 | 0.250 | weak | 1 chi | Tu | mid-weak |
| 000002 | -15 | 0.350 | weak | 2 chi | Tu | weak threshold edge |

## Findings

1. **Score retains ranking information** inside weak: 0.010 < 0.250 < 0.350.
2. **0.01–0.35 region has meaningful internal variation** driven mainly by rooting recovery under shared Tu season.
3. **v1 weak threshold collapses naming**: all three are only `weak`; no `very_weak`.
4. **000002 sits on the weak ceiling (0.35)** — boundary fragile; one more strengthen point would flip to balanced.
5. **Profile can distinguish without changing score**: vo-can vs 2-chi root already separates 000001 from 000002 while band stays weak.

## Additional dimensions needed?

Not required to *rank* these three on score. Required to *name* VERY_WEAK and to avoid threshold-edge flips. Candidate: rooting_state + pressure_state + evidence_conflict in a profile layer.

## Synthetic caveat

Expectations are stress labels, not expert truth. Directional weakness is plausible; exact VERY_WEAK vs WEAK cut is uncalibrated (DATA_GAP for real dual-reviewed VERY_WEAK = 0).
"""

BALANCED = """# BALANCED_PROFILE_ANALYSIS

**Sprint:** PILOT-1H  
**Cases:** SYN-STR-000010, 000011, 000012 (all runtime balanced)

## Profiles (raw buckets)

| case | score | season | root | support | drain | control | character |
|---|---:|---:|---:|---:|---:|---:|---|
| 000010 | 0.39 | -25 | +30 | +10 | -8 | -18 | death season vs triple root |
| 000011 | 0.43 | +10 | +12 | 0 | -13 | -16 | mild season, output/officer drain |
| 000012 | 0.52 | -10 | +22 | +10 | -6 | -14 | Tu season, dual root + An |

## Findings

1. **Balanced is reachable via different internal states** (cancellation vs quieter mid).
2. **000010 is not a quiet equilibrium** — large opposing masses cancel.
3. **Multiple internal states collapse into one v1 band** — profile required to explain *why* balanced.
4. Match to synthetic `balanced` is useful for stress testing but does not prove expert BALANCED coverage (real dual-reviewed BALANCED = 0).

## Genuine equilibrium?

Partially. Score near 0.5 can mean either low-activity mid or high-conflict cancellation. Current contract cannot tell them apart.
"""

TAXONOMY_RES = """# TAXONOMY_RESOLUTION_ANALYSIS

**Sprint:** PILOT-1H  
**Focus mismatches:** SYN-STR-000008, 000009, 000015 (TAXONOMY_RESOLUTION_GAP)

## Case diagnostics

### SYN-STR-000008

- synthetic: slightly_weak → projected v1 weak
- runtime: balanced @ 0.39
- profile: Tu season, 1-chi root, companion support, wealth drain, officer control
- likely causes: **threshold placement** (just above 0.35) + **tilt not expressible**; synthetic expectation may be plausible but unproven
- not automatic proof synthetic label is correct

### SYN-STR-000009

- synthetic: slightly_weak → projected v1 weak
- runtime: strong @ 0.67
- profile: Tuong season +12 root outweighs modest wealth/officer pressure
- likely causes: **evidence compression** (hoa pressure under-specified) + **season dominance**; possible **SYNTHETIC_EXPECTATION_REVIEW** if fire pressure was intended to dominate root/season

### SYN-STR-000015

- synthetic: slightly_strong → projected v1 strong
- runtime: weak @ 0.31
- profile: death season -25 dominates despite An support
- likely causes: **seasonal dominance** + possible **over-specified synthetic expectation** (review flag)
- conflicting evidence present; score chooses net negative

## Synthesis

| Cause | 000008 | 000009 | 000015 |
|---|---|---|---|
| score compression | PARTIAL | NO | NO |
| evidence compression | PARTIAL | YES | PARTIAL |
| threshold placement | YES | YES (0.65 cliff) | YES (0.35 cliff) |
| missing profile dimensions | YES | YES | YES |
| conflicting evidence | YES | YES | YES |
| synthetic expectation limitations | POSSIBLE | POSSIBLE | LIKELY |

Do not treat synthetic labels as expert truth. These cases diagnose resolution limits and expectation quality.
"""

COLLISION = """# SCORE_COLLISION_ANALYSIS

**Sprint:** PILOT-1H  
**Populations kept separate.**

## SYNTHETIC_STRESS — similar score, different synthetic taxonomy

| case_a | case_b | score_a | score_b | score_distance | label_a | label_b | population | evidence_profile_difference | interpretation |
|---|---|---:|---:|---:|---|---|---|---|---|
| SYN-STR-000008 | SYN-STR-000010 | 0.39 | 0.39 | 0.00 | slightly_weak | balanced | SYNTHETIC_STRESS | 008 mild Tu+support vs 010 death-season vs triple-root cancellation | SCORE_ONLY cannot separate tilt vs cancellation |
| SYN-STR-000014 | SYN-STR-000019 | 1.00 | 1.00 | 0.00 | slightly_strong | very_strong | SYNTHETIC_STRESS | both ceilinged; raw differs if exposed | published score collision under clamp |
| SYN-STR-000018 | SYN-STR-000019 | 1.00 | 1.00 | 0.00 | strong | very_strong | SYNTHETIC_STRESS | raw 82 vs 107 | intensity lost after normalization |

## SYNTHETIC_STRESS — different score, same synthetic taxonomy

| case_a | case_b | score_a | score_b | score_distance | label_a | label_b | population | evidence_profile_difference | interpretation |
|---|---|---:|---:|---:|---|---|---|---|---|
| SYN-STR-000001 | SYN-STR-000002 | 0.01 | 0.35 | 0.34 | very_weak | very_weak | SYNTHETIC_STRESS | vo can vs 2-chi root | same stress label spans wide score |
| SYN-STR-000007 | SYN-STR-000008 | 0.87 | 0.39 | 0.48 | slightly_weak | slightly_weak | SYNTHETIC_STRESS | strong season/An chart vs mid cancellation | synthetic tilt label unstable vs score |
| SYN-STR-000013 | SYN-STR-000015 | 0.86 | 0.31 | 0.55 | slightly_strong | slightly_strong | SYNTHETIC_STRESS | strong vs death-season | expectation cohort internally inconsistent vs runtime |

## REAL_CALIBRATION — similar score / expert relations

| case_a | case_b | score_a | score_b | score_distance | label_a | label_b | population | evidence_profile_difference | interpretation |
|---|---|---:|---:|---:|---|---|---|---|---|
| CAL-000001 | CAL-000006 | 0.87 | 0.50 | 0.37 | SLIGHTLY_WEAK | SLIGHTLY_WEAK | REAL_CALIBRATION | strong positive season/special vs near-zero sum | **different score, same expert taxonomy** |
| CAL-000001 | SYN-STR-000007 | 0.87 | 0.87 | 0.00 | SLIGHTLY_WEAK (expert) | slightly_weak (synthetic) | CROSS-REF only | same pillar family | runtime agrees with itself; experts disagree with runtime |

Provisional PILOT notes (not dual-reviewed): historical CASE-0003 vs CASE-0005 both ~0.66 with different expert tilts remain the classic score-collision illustration from earlier sprints (RUNTIME_REFERENCE / provisional), not merged into dual-reviewed metrics.

## Verdict

**SCORE_ONLY = NOT_SUFFICIENT** for seven-level taxonomy.  
Collisions appear in synthetic stress and are reinforced by n=2 real dual-reviewed cases sharing SLIGHTLY_WEAK across 0.50–0.87.
"""

SUPPORT_PRESSURE = """# SUPPORT_PRESSURE_DIAGNOSTIC

**Sprint:** PILOT-1H  
**Cases:** CAL-000001, CAL-000006, SYN-STR-000007, SYN-STR-000008

## Preservation checklist

| Property | Current score behavior |
|---|---|
| magnitude | PARTIAL — bucket sums only |
| direction | YES — signed contributions |
| source | LOST after aggregation (rules list helps; profile buckets coarse) |
| type | PARTIAL — single support_type / control_type winners |
| confidence | NOT preserved per factor (global confidence often 1.0) |

## Case contrasts

### CAL-000001 / SYN-STR-000007

Support mass (season/root/companion/special) outweighs officer pressure in the sum → `strong` @ 0.87.  
Experts (real) / synthetic expect slightly_weak. Score preserves net magnitude/direction of the *sum*, not the interpretive priority experts give to moc/hoa pressure / sitting fire.

### CAL-000006

Near cancellation: support+root ≈ season+control → balanced @ 0.50. Experts still SLIGHTLY_WEAK (tilt). Score loses tilt once net ≈ 0.

### SYN-STR-000008

Support present but season/control/drain keep net slightly negative → balanced @ 0.39. Synthetic slightly_weak wants weak-side naming.

## Conclusion

Support vs pressure are **present as signed buckets** but **source/type/confidence are compressed**. A profile layer should keep support_state and pressure_state as first-class vectors, not only net score.
"""

SEASONAL = """# SEASONAL_WEIGHTING_DIAGNOSTIC

**Sprint:** PILOT-1H  
**Primary case:** SYN-STR-000004 (+ supporting traces)

## SYN-STR-000004

- synthetic weak / limited rooting
- season Tuong **+25** while root Vo can **-20**
- net raw -8 → balanced 0.42
- mismatch category SEASONAL_WEIGHTING_GAP

## Structural observations (no numeric retune)

1. Season is a **single ordinal** (5 states) — coarse vs full month-branch semantics.
2. Positive season can **dominate** vo-can weakness into mid band.
3. Branch-level identity and phase exist on context (`season`, `season_phase`) but **score uses month_status only**.
4. Contextual interactions (season × root × sitting) are mostly absent except special rules.
5. Season is not always wrong; it is **structurally coarse** and can **overpower** rooting/pressure narratives.

## Recommendation class

Identify structural coarseness only. **Do not** recommend a numeric weight change in this sprint.
"""

ROOTING = """# ROOTING_DIAGNOSTIC

**Sprint:** PILOT-1H  
**Sources:** context_builder `_compute_root`, `02_root_rules.csv`

## Distinctions

| Distinction | Currently distinguished? | How |
|---|---|---|
| direct root | PARTIAL | hidden stem element match per branch counted |
| hidden root | PARTIAL | `Thong can tang can` if flat hidden only |
| multiple roots | YES | 1 / 2 / 3+ chi ladder |
| weak root | PARTIAL | only via lower ladder / tang can / vo can |
| seasonal root | NO separate | season scored apart from root |
| remote support | NO | not modeled as rooting |

## Loss

Which branches provide root is not published. Day-branch vs month-branch rooting is not separated. Root destroyed (xung) label exists in control rules but is rarely set by builder.

## Design implication

Profile should expose `rooting_state` with count, loci, and quality — without rewriting score in this sprint.
"""

PROFILE_REQ = """# STRENGTH_PROFILE_REQUIREMENTS

**Sprint:** PILOT-1H  
**Status:** REQUIREMENTS ONLY — do not implement

## Conceptual stack

```text
Evidence -> Weighting -> Score -> Profile -> Taxonomy -> Confidence -> Contract
```

Score remains useful continuous measure. Profile explains composition/conflict. Taxonomy classifies. Confidence qualifies.

## Candidate dimensions

| Dimension | Purpose | Source | Value type | Available now | Currently lost | Why taxonomy may need it |
|---|---|---|---|---|---|---|
| season_state | month command / phase | month_status, season, season_phase | enum + optional phase | PARTIAL | branch identity | separates death-season cancellation from quiet mid |
| rooting_state | where/how rooted | root_level, root_count, branch loci | enum + count + loci | PARTIAL | loci | VERY_WEAK vs WEAK intensity |
| support_state | companion/resource mass | support_type, resource/companion lists | vector | PARTIAL | multi-source | tilt vs net |
| pressure_state | officer/wealth/output | control/drain lists | vector | PARTIAL | sitting hidden pressure | expert disagreements |
| drain_state | leakage detail | drain_type, counts | enum + count | PARTIAL | overlap with control | slightly_* edges |
| structural_state | special/combo/follow | special matches; Pattern later | flags | PARTIAL | follow not in strength | overrides |
| temperature_state | climate framing | context vs TemperatureEngine | enum + source tag | CONTEXT | dual sources | winter An special interactions |
| evidence_conflict | opposing large masses | bucket signs/magnitudes | bool/score | DERIVABLE | not published | balanced cancellation vs quiet |
| evidence_completeness | missing dimensions | builder coverage | enum/float | PARTIAL | not on contract | confidence |
| confidence | certainty of label | completeness, conflict, calendar, boundary | enum/float | WEAK (often 1.0) | non-discriminative | boundary publishing |

## Necessity verdict

**Profile layer REQUIRED** before Taxonomy v2 implementation. Score alone is NOT_SUFFICIENT (collisions, saturation, dual-reviewed disagreement).
"""

BOUNDARY = """# TAXONOMY_BOUNDARY_ANALYSIS

**Sprint:** PILOT-1H  
**No frozen numeric thresholds.**

| Boundary | Available evidence | Current score behavior | Current v1 band | Profile evidence availability | Boundary observability | Real calibration coverage | Synthetic coverage | Confidence | Data gap |
|---|---|---|---|---|---|---|---|---|---|
| VERY_WEAK <-> WEAK | root/season extremes | scores 0.01–0.35 ranked | all weak | PARTIAL | PARTIALLY_OBSERVABLE | 0 dual-reviewed | 3 SYN very_weak | LOW | DATA_GAP (real) |
| WEAK <-> SLIGHTLY_WEAK | mid-weak profiles | 0.35 cliff | weak/balanced | PARTIAL | PARTIALLY_OBSERVABLE | 0 | SYN weak/slightly_weak | LOW | DATA_GAP |
| SLIGHTLY_WEAK <-> BALANCED | tilt vs mid | 0.35–0.65 | weak/balanced/strong mix | PARTIAL | OBSERVABLE on synthetic; contested on real | n=2 both SLIGHTLY_WEAK | SYN 008/010 collision | MEDIUM diagnostic / LOW calibrate | DATA_GAP |
| BALANCED <-> SLIGHTLY_STRONG | mid-strong tilt | 0.65 cliff | balanced/strong | PARTIAL | PARTIALLY_OBSERVABLE | 0 dual BALANCED/SLIGHTLY_STRONG | SYN balanced + slightly_strong | LOW | DATA_GAP |
| SLIGHTLY_STRONG <-> STRONG | intensity | ceiling + cliff | strong | PARTIAL | PARTIALLY_OBSERVABLE | provisional only | SYN 014 vs 016 | LOW | DATA_GAP |
| STRONG <-> VERY_STRONG | raw intensity | both publish 1.0 strong | strong | raw exists, unpublished | PARTIALLY_OBSERVABLE in raw; NOT on published score | 0 dual VERY_STRONG | 3 SYN very_strong | LOW | DATA_GAP + saturation |

T1–T6 remain **unfrozen**.
"""

V1V2 = """# V1_TO_V2_PROJECTION_ANALYSIS

**Sprint:** PILOT-1H  
**Conceptual only — not implemented**

## Coarse projection (design compatibility)

| v2 candidate | -> v1 |
|---|---|
| very_weak | weak |
| weak | weak |
| slightly_weak | weak |
| balanced | balanced |
| slightly_strong | strong |
| strong | strong |
| very_strong | strong |

## Distinctions impossible under current 3-band contract

1. very_weak vs weak  
2. weak vs slightly_weak  
3. slightly_weak vs balanced (tilt)  
4. balanced vs slightly_strong (tilt)  
5. slightly_strong vs strong  
6. strong vs very_strong  

## Additional impossibility from score clamp

Even a future v2 mapper cannot recover STRONG vs VERY_STRONG from published `strength_score` alone once both are 1.000 — needs raw_total, unclamped score, or profile intensity.

## Implication

v1 remains coarse API compatibility. v2 requires additive fields + profile, not a silent remap of `strength_level`.
"""

CONFIDENCE = """# CONFIDENCE_MODEL_DIAGNOSTIC

**Sprint:** PILOT-1H  
**No implementation**

## Current behavior (observed)

`confidence = min(1, matched_rules/5) (+0.2 if level_rule)`.  
Many pilot/synthetic traces saturate at **1.0**, including MODEL_DISAGREEMENT cases.

## Should confidence depend on?

| Factor | Should depend? | Now? |
|---|---|---|
| score stability | SHOULD | NO |
| evidence completeness | YES | NO |
| evidence conflict | YES | NO |
| structural ambiguity | YES | NO |
| calendar certainty | YES (real cases) | NO in strength confidence |
| taxonomy boundary proximity | YES | NO |

## Design note

Confidence must not equal "enough rules matched". Dual-reviewed CAL-000001 shows high runtime confidence with expert disagreement — confidence should fall near boundaries and conflicts.
"""

SYN_AUDIT = """# SYNTHETIC_EXPECTATION_AUDIT

**Sprint:** PILOT-1H  
**Rule:** Do not change synthetic fixtures. Do not promote to calibration.

| case_id | synthetic_expected | Audit flag | structurally_plausible | clearly_extreme | ambiguous | useful_for_stress | potentially_over_specified | notes |
|---|---|---|---|---|---|---|---|---|
| SYN-STR-000001 | very_weak | OK | YES | YES | NO | YES | NO | near floor; strong diagnostic |
| SYN-STR-000002 | very_weak | SYNTHETIC_EXPECTATION_REVIEW | YES | PARTIAL | YES | YES | PARTIAL | rooted 2-chi; may be WEAK not VERY_WEAK |
| SYN-STR-000003 | very_weak | OK | YES | YES | LOW | YES | NO | directional extreme |
| SYN-STR-000004 | weak | SYNTHETIC_EXPECTATION_REVIEW | YES | NO | YES | YES | PARTIAL | season Tuong fights vo can |
| SYN-STR-000005 | weak | OK | YES | NO | LOW | YES | NO | aligns weak |
| SYN-STR-000006 | weak | OK | YES | NO | LOW | YES | NO | aligns weak |
| SYN-STR-000007 | slightly_weak | OK_STRESS | YES | NO | YES | YES | NO | mirrors CAL-000001; useful cross-pop |
| SYN-STR-000008 | slightly_weak | SYNTHETIC_EXPECTATION_REVIEW | YES | NO | YES | YES | PARTIAL | near balanced; tilt ambiguous |
| SYN-STR-000009 | slightly_weak | SYNTHETIC_EXPECTATION_REVIEW | YES | NO | YES | YES | YES | runtime strong; expectation may overstate weakness |
| SYN-STR-000010 | balanced | OK | YES | NO | LOW | YES | NO | cancellation balanced |
| SYN-STR-000011 | balanced | OK | YES | NO | LOW | YES | NO | mid profile |
| SYN-STR-000012 | balanced | OK | YES | NO | LOW | YES | NO | mid profile |
| SYN-STR-000013 | slightly_strong | OK_STRESS | YES | NO | YES | YES | PARTIAL | runtime strong coarse match |
| SYN-STR-000014 | slightly_strong | SYNTHETIC_EXPECTATION_REVIEW | YES | NO | YES | YES | YES | score 1.0; may be STRONG/VERY_STRONG stress |
| SYN-STR-000015 | slightly_strong | SYNTHETIC_EXPECTATION_REVIEW | YES | NO | YES | YES | YES | death season; expectation likely over-specified |
| SYN-STR-000016 | strong | OK | YES | NO | LOW | YES | NO | ceiling strong |
| SYN-STR-000017 | strong | OK | YES | NO | LOW | YES | NO | ceiling strong |
| SYN-STR-000018 | strong | OK | YES | NO | LOW | YES | NO | raw below very_strong peers |
| SYN-STR-000019 | very_strong | OK | YES | YES | NO | YES | NO | extreme dominance |
| SYN-STR-000020 | very_strong | OK | YES | YES | NO | YES | NO | extreme dominance |
| SYN-STR-000021 | very_strong | OK | YES | YES | NO | YES | NO | extreme dominance |

Review-flagged cases remain valid **stress probes**; they are not expert truth.
"""

REAL_CAL = """# REAL_CALIBRATION_DIAGNOSTIC

**Sprint:** PILOT-1H  
**n = 2 dual-reviewed** — do not generalize beyond this sample.

## CAL-000001

| Field | Value |
|---|---|
| Expert-A | SLIGHTLY_WEAK / MEDIUM (pilot reference; not new blind) |
| Expert-B | SLIGHTLY_WEAK / MEDIUM (VALIDATED) |
| Agreement | EXACT_MATCH |
| Confidence | MEDIUM |
| Rationale | Expert-B rationale not supplied (not invented); Expert-A carried reference |
| Runtime | strong / 0.87 |
| Model relation | MODEL_DISAGREEMENT |

## CAL-000006

| Field | Value |
|---|---|
| Expert-A | SLIGHTLY_WEAK / MEDIUM (reference) |
| Expert-B | SLIGHTLY_WEAK / MEDIUM (VALIDATED) |
| Agreement | EXACT_MATCH |
| Confidence | MEDIUM |
| Rationale | Expert-B rationale not supplied; canonical month mau_ngo |
| Runtime | balanced / 0.50 |
| Model relation | MODEL_DISAGREEMENT (adjacent) |

## Limits

- Both dual-reviewed labels are SLIGHTLY_WEAK only.
- No dual-reviewed VERY_WEAK / WEAK / BALANCED / SLIGHTLY_STRONG / STRONG / VERY_STRONG.
- Same expert taxonomy spans scores 0.50–0.87 → score-only insufficient even at n=2.
- Calibration records were **not modified** in this sprint.
"""

SUMMARY = """# STRENGTH_MODEL_DIAGNOSTIC_SUMMARY

**Sprint:** PILOT-1H

## Answers

1. **Is the current score useful?** YES — as a continuous net strength index from season/root/support/drain/control/special rules. Directional extremes mostly move the right way on synthetic stress.

2. **Is the score sufficient for 7 levels?** NO — SCORE_ONLY = NOT_SUFFICIENT (collisions, clamp, 3-band contract, n=2 expert disagreements).

3. **Is a profile layer required?** YES — above existing Strength Engine outputs; do not replace score.

4. **Which evidence dimensions are currently lost?** Sitting hidden pressure; clash/punishment/harm; TemperatureEngine; multi-source support/pressure detail; root loci; follow; per-factor confidence; raw intensity after clamp.

5. **Is the current score saturated?** YES on the high end for published normalized score (`raw>=50` → 1.0). Low end retains more range.

6. **Which boundaries are observable?** PARTIALLY — VERY_WEAK ranking inside weak; balanced cancellation vs quiet mid; STRONG/VERY_STRONG in raw only.

7. **Which boundaries are data-gapped?** Essentially all seven-level cuts for **real dual-reviewed** coverage (only SLIGHTLY_WEAK dual-reviewed).

8. **Which synthetic results are most diagnostic?** 000001 (floor), 000004 (season vs root), 000007 (cross-link to CAL-000001), 000008/000010 (score collision), 000015 (expectation vs season), 000019–000021 (ceiling).

9. **What must be measured before Taxonomy v2?** Dual-reviewed coverage across levels; profile dimensions; collision set; boundary cases; confidence model inputs; raw/unclamped intensity policy.

10. **What must NOT be changed yet?** Engine code, rule weights, thresholds, Golden Expected, production taxonomy v2, AF-1, synthetic→expert promotion.
"""

PRE_IMPL = """# PRE_IMPLEMENTATION_RECOMMENDATIONS

**Sprint:** PILOT-1H

## MUST_HAVE_BEFORE_IMPLEMENTATION

- Additional real dual-reviewed cases across missing levels (esp. VERY_WEAK, WEAK, BALANCED, STRONG/VERY_STRONG)
- Evidence/profile audit published as design contract (this sprint starts it)
- Score collision analysis maintained as living set
- Boundary evidence with expert agreement (not synthetic alone)
- Confidence model design (conflict, completeness, calendar, boundary proximity)
- Taxonomy coverage gates (≥ dual-reviewed per level before freezing T1–T6)

## SHOULD_HAVE

- Expose raw_total / unclamped diagnostics in pilot tooling (not production retune)
- Sitting-branch / hidden pressure evidence design
- Separate support_state vs pressure_state vectors
- Synthetic expectation review pass (mark only; do not silently edit)

## OPTIONAL

- Richer combination/clash design notes
- Temperature source unification design
- Follow-pattern handoff contract with Pattern Engine

## DO_NOT_DO_YET

- Threshold tuning
- Score weight tuning
- Engine rewrite
- Production taxonomy v2
- Golden Dataset promotion of synthetic or provisional labels
- Freezing T1–T6
- Treating synthetic expectations as expert truth
"""

PILOT_SUMMARY = """# PILOT_1H_SUMMARY — Strength Model Diagnostic & Taxonomy Boundary Analysis

**Purpose:** Diagnose what the current Strength score measures, where information is lost, and what is required before Taxonomy v2 — without changing production behavior.

## Populations analyzed

- REAL_CALIBRATION dual-reviewed: CAL-000001, CAL-000006 (n=2)
- SYNTHETIC_STRESS: SYN-STR-000001..000021 (n=21)
- RUNTIME_REFERENCE: existing engine outputs (observation only)

## Headline conclusions

- Score is a useful net index of season/root/support/drain/control/special rules.
- Score is **not** sufficient for seven-level taxonomy.
- Published score **saturates** at 1.000 for raw>=50 (STRONG vs VERY_STRONG lost).
- Taxonomy projection collapse is a **separate** problem from score clamp.
- Profile layer is **required** before implementation.
- Real dual-reviewed coverage remains a **DATA_GAP** outside SLIGHTLY_WEAK.

## No-patch gate

Only paths under `knowledge/pilot/replay/root_cause/strength_model_diagnostic/` are in scope for this sprint.

---

Status:
- REAL_DUAL_REVIEWED_CASES: 2
- SYNTHETIC_CASES_ANALYZED: 21
- SCORE_TRACE_COMPLETED: YES
- SCORE_SATURATION_ANALYZED: YES
- VERY_WEAK_BOUNDARY_ANALYZED: YES
- BALANCED_PROFILE_ANALYZED: YES
- SCORE_COLLISION_ANALYZED: YES
- SUPPORT_PRESSURE_ANALYZED: YES
- SEASONAL_WEIGHTING_ANALYZED: YES
- ROOTING_ANALYZED: YES
- PROFILE_REQUIREMENTS_DEFINED: YES
- TAXONOMY_BOUNDARIES_FROZEN: NO
- PRODUCTION_CODE_CHANGED: NO
- STRENGTH_ENGINE_CHANGED: NO
- KNOWLEDGE_PACKAGES_CHANGED: NO
- GOLDEN_EXPECTED_CHANGED: NO
- AF1_CHANGED: NO
- CALIBRATION_DATA_CHANGED: NO
- TEST_REGRESSION: NO

Final Decision:
DIAGNOSTIC_COMPLETE

Recommendation:
- NEXT_ACTION: Continue real expert case acquisition while preserving the current Strength Engine and keeping Taxonomy v2 unimplemented.
"""

VALIDATION_MD = """# VALIDATION — PILOT-1H

| Check | Status |
|---|---|
| REAL/SYNTHETIC/RUNTIME populations separated | PASS |
| CAL-* unchanged | PASS |
| SYN-* unchanged | PASS |
| No new CAL-* | PASS |
| No fabricated expert labels | PASS |
| No synthetic promotion | PASS |
| No Golden / production / KP / AF-1 changes | PASS |
| Required reports present | PASS |
| Taxonomy boundaries frozen | NO (correct) |

Final decision: **DIAGNOSTIC_COMPLETE**
"""

# JSON artifacts
EVIDENCE_MATRIX_JSON = {
    "sprint": "PILOT-1H",
    "score_formula": "clamp((raw_total + 50) / 100, 0, 1)",
    "buckets": ["season", "root", "support", "drain", "control", "combination", "special"],
    "primary_drivers": ["seasonal_strength", "rooting", "support", "control", "drain", "special"],
    "not_in_score": ["temperature_engine", "clash", "punishment", "harm", "follow_pattern", "sitting_hidden_pressure"],
}

SCORE_TRACE_JSON = {
    "sprint": "PILOT-1H",
    "cases": [
        {"case_id": "CAL-000001", "population": "REAL_CALIBRATION", "normalized": 0.87, "band": "strong", "expert": "SLIGHTLY_WEAK"},
        {"case_id": "CAL-000006", "population": "REAL_CALIBRATION", "normalized": 0.50, "band": "balanced", "expert": "SLIGHTLY_WEAK"},
        {"case_id": "SYN-STR-000001", "population": "SYNTHETIC_STRESS", "normalized": 0.01, "band": "weak", "synthetic_expected": "very_weak", "raw": -49.0},
        {"case_id": "SYN-STR-000004", "population": "SYNTHETIC_STRESS", "normalized": 0.42, "band": "balanced", "synthetic_expected": "weak", "raw": -8.0},
        {"case_id": "SYN-STR-000007", "population": "SYNTHETIC_STRESS", "normalized": 0.87, "band": "strong", "synthetic_expected": "slightly_weak", "raw": 37.0},
        {"case_id": "SYN-STR-000010", "population": "SYNTHETIC_STRESS", "normalized": 0.39, "band": "balanced", "synthetic_expected": "balanced", "raw": -11.0},
        {"case_id": "SYN-STR-000015", "population": "SYNTHETIC_STRESS", "normalized": 0.31, "band": "weak", "synthetic_expected": "slightly_strong", "raw": -19.0},
        {"case_id": "SYN-STR-000018", "population": "SYNTHETIC_STRESS", "normalized": 1.0, "band": "strong", "synthetic_expected": "strong", "raw": 82.0},
        {"case_id": "SYN-STR-000019", "population": "SYNTHETIC_STRESS", "normalized": 1.0, "band": "strong", "synthetic_expected": "very_strong", "raw": 107.0},
    ],
}

SATURATION_JSON = {
    "sprint": "PILOT-1H",
    "mechanism_a_score_saturation": True,
    "mechanism_b_taxonomy_projection_collapse": True,
    "mechanisms_are_distinct": True,
    "clamp_rule": "normalized=1.0 when raw_total >= 50",
    "very_strong_cases": {
        "SYN-STR-000019": {"raw": 107.0, "normalized": 1.0},
        "SYN-STR-000020": {"raw": 87.0, "normalized": 1.0},
        "SYN-STR-000021": {"raw": 98.0, "normalized": 1.0},
    },
    "strong_peer_raw_example": {"SYN-STR-000018": {"raw": 82.0, "normalized": 1.0}},
    "published_distinguishable": False,
    "raw_distinguishable": True,
}

BOUNDARY_JSON = {
    "sprint": "PILOT-1H",
    "boundaries_frozen": False,
    "real_dual_reviewed_n": 2,
    "real_dual_reviewed_levels": ["SLIGHTLY_WEAK"],
    "observability": {
        "VERY_WEAK_WEAK": "PARTIALLY_OBSERVABLE",
        "WEAK_SLIGHTLY_WEAK": "PARTIALLY_OBSERVABLE",
        "SLIGHTLY_WEAK_BALANCED": "PARTIALLY_OBSERVABLE",
        "BALANCED_SLIGHTLY_STRONG": "PARTIALLY_OBSERVABLE",
        "SLIGHTLY_STRONG_STRONG": "PARTIALLY_OBSERVABLE",
        "STRONG_VERY_STRONG": "PARTIALLY_OBSERVABLE_RAW_ONLY",
    },
}

COLLISION_JSON = {
    "sprint": "PILOT-1H",
    "score_only_sufficient": False,
    "synthetic_similar_score_different_label": [
        {"case_a": "SYN-STR-000008", "case_b": "SYN-STR-000010", "score": 0.39},
        {"case_a": "SYN-STR-000018", "case_b": "SYN-STR-000019", "score": 1.0},
    ],
    "real_different_score_same_expert": [
        {"case_a": "CAL-000001", "case_b": "CAL-000006", "scores": [0.87, 0.50], "expert": "SLIGHTLY_WEAK"}
    ],
}

PROFILE_JSON = {
    "sprint": "PILOT-1H",
    "profile_required": True,
    "stack": ["Evidence", "Weighting", "Score", "Profile", "Taxonomy", "Confidence", "Contract"],
    "dimensions": [
        "season_state",
        "rooting_state",
        "support_state",
        "pressure_state",
        "drain_state",
        "structural_state",
        "temperature_state",
        "evidence_conflict",
        "evidence_completeness",
        "confidence",
    ],
}

CONFIDENCE_JSON = {
    "sprint": "PILOT-1H",
    "current_formula": "min(1, matched/5) + 0.2 if level_rule",
    "often_saturates_at_one": True,
    "should_include": [
        "score_stability",
        "evidence_completeness",
        "evidence_conflict",
        "structural_ambiguity",
        "calendar_certainty",
        "taxonomy_boundary_proximity",
    ],
}

SYN_AUDIT_JSON = {
    "sprint": "PILOT-1H",
    "cases_audited": 21,
    "review_flagged": [
        "SYN-STR-000002",
        "SYN-STR-000004",
        "SYN-STR-000008",
        "SYN-STR-000009",
        "SYN-STR-000014",
        "SYN-STR-000015",
    ],
    "promoted_to_calibration": False,
    "fixtures_modified": False,
}

VALIDATION_JSON = {
    "sprint": "PILOT-1H",
    "populations_separated": True,
    "cal_records_unchanged": True,
    "syn_records_unchanged": True,
    "no_new_cal_ids": True,
    "no_fabricated_expert_labels": True,
    "no_synthetic_promotion": True,
    "no_production_mutations": True,
    "taxonomy_boundaries_frozen": False,
    "final_decision": "DIAGNOSTIC_COMPLETE",
    "overall": "PASS",
}

PROFILE_META_JSON = {
    "sprint": "PILOT-1H",
    "real_dual_reviewed": 2,
    "synthetic_analyzed": 21,
    "profile_required": True,
    "score_only_sufficient": False,
    "score_saturated_high_end": True,
    "final_decision": "DIAGNOSTIC_COMPLETE",
}


if __name__ == "__main__":
    build()
