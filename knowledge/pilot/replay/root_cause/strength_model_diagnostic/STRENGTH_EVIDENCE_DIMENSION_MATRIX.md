# STRENGTH_EVIDENCE_DIMENSION_MATRIX

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
