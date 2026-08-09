# Package Dependency Graph

Edges are taken only from `DEPENDENCIES.json` (`required` + `optional`). All current edges are **optional**.

## Graph

```mermaid
flowchart TB
  bz01[bz_01_strength_core]
  bz02[bz_02_seasonal_core]
  bz03[bz_03_temperature_core]
  bz04[bz_04_pattern_core]
  bz05[bz_05_pattern_evaluation]
  bz06[bz_06_useful_god_foundation]
  bz07[bz_07_useful_god_priority]
  bz08[bz_08_useful_god_override]
  bz09[bz_09_luck_foundation]
  bz10[bz_10_follow_pattern_core]
  bz11[bz_11_transformation_core]
  bz12[bz_12_combination_clash_core]
  bz13[bz_13_ten_gods_advanced]
  bz14[bz_14_twelve_growth_advanced]
  bz15[bz_15_hidden_stems_advanced]

  bz02 --> bz01
  bz03 --> bz02
  bz03 --> bz01
  bz04 --> bz01
  bz04 --> bz02
  bz04 --> bz03
  bz05 --> bz04
  bz05 --> bz01
  bz05 --> bz02
  bz05 --> bz03
  bz06 --> bz01
  bz06 --> bz02
  bz06 --> bz03
  bz06 --> bz05
  bz07 --> bz01
  bz07 --> bz02
  bz07 --> bz03
  bz07 --> bz05
  bz07 --> bz06
  bz08 --> bz01
  bz08 --> bz02
  bz08 --> bz03
  bz08 --> bz05
  bz08 --> bz07
  bz10 --> bz01
  bz10 --> bz02
  bz10 --> bz03
  bz10 --> bz04
  bz10 --> bz05
  bz10 --> bz06
  bz10 --> bz07
  bz11 --> bz01
  bz11 --> bz02
  bz11 --> bz03
  bz11 --> bz05
  bz11 --> bz07
  bz11 --> bz10
  bz12 --> bz01
  bz12 --> bz02
  bz12 --> bz03
  bz12 --> bz05
  bz12 --> bz07
  bz12 --> bz10
  bz12 --> bz11
  bz13 --> bz01
  bz13 --> bz02
  bz13 --> bz03
  bz13 --> bz05
  bz13 --> bz07
  bz13 --> bz10
  bz13 --> bz11
  bz13 --> bz12
  bz14 --> bz01
  bz14 --> bz02
  bz14 --> bz03
  bz14 --> bz05
  bz14 --> bz07
  bz14 --> bz10
  bz14 --> bz11
  bz14 --> bz12
  bz14 --> bz13
  bz15 --> bz01
  bz15 --> bz02
  bz15 --> bz03
  bz15 --> bz05
  bz15 --> bz07
  bz15 --> bz10
  bz15 --> bz11
  bz15 --> bz12
  bz15 --> bz13
  bz15 --> bz14
```

Arrow `A --> B` means **A optionally depends on B** (A consumes B’s published outputs).

## Cyclic dependency

**None.** DFS over the optional graph found 0 back-edges.

## Missing / dangling edges

**None.** Every `package_id` referenced in `DEPENDENCIES.json` exists in the released set.

## Orphan / unreachable

| Class | Packages | Notes |
| --- | --- | --- |
| No outbound deps (roots) | bz_01_strength_core, bz_09_luck_foundation | bz_01 is a healthy producer root. bz_09 declares no deps. |
| No inbound deps (leaves / isolated) | bz_08_useful_god_override, bz_15_hidden_stems_advanced, bz_09_luck_foundation | bz_08 / bz_15 are intended leaves until Interpretation. bz_09 is isolated from the analytical spine. |
| Unreachable from bz_01 spine | bz_09_luck_foundation | Parallel reference package; not consumed by bz_02–bz_15. |

## Required vs optional

| Kind | Count |
| --- | --- |
| Required dependencies | 0 |
| Optional dependencies | all declared edges |
| Conflicts | 0 |

Independently deployable policy is consistent: no hard required coupling.

## Consumer / producer relationships

See [PACKAGE_CONSUMER_MATRIX.md](PACKAGE_CONSUMER_MATRIX.md) and [PACKAGE_PRODUCER_MATRIX.md](PACKAGE_PRODUCER_MATRIX.md).
