# Package Consumer Matrix

Who declares consumption of which published (or implicit) signals.

| Signal | Consumers |
| --- | --- |
| strength_score | bz_06, bz_07, bz_08, bz_10, bz_11, bz_12, bz_13, bz_14, bz_15 |
| season_score | bz_06, bz_07, bz_08, bz_10, bz_11, bz_12, bz_13, bz_14, bz_15 |
| temperature_score | bz_06, bz_07, bz_08, bz_10, bz_11, bz_12, bz_13, bz_14, bz_15 |
| pattern_score | bz_06, bz_07, bz_08, bz_10, bz_11, bz_12, bz_13, bz_14, bz_15 |
| pattern_quality | bz_06, bz_07, bz_08, bz_10, bz_11, bz_12, bz_13, bz_14, bz_15 |
| pattern_confidence | bz_06, bz_07, bz_08, bz_10, bz_11, bz_12, bz_13, bz_14, bz_15 |
| pattern_integrity | bz_06, bz_07, bz_10, bz_11, bz_12, bz_13, bz_14, bz_15 |
| pattern_stability | bz_06, bz_07, bz_10, bz_11, bz_12, bz_13, bz_14, bz_15 |
| useful_god / favorable / unfavorable / decision_* | bz_07 |
| resolved_useful_god | bz_08, bz_10, bz_11, bz_12, bz_13, bz_14, bz_15 |
| decision_priority | bz_08, bz_10, bz_11, bz_12, bz_13, bz_14, bz_15 |
| resolution_confidence | bz_08, bz_10, bz_11, bz_12, bz_13, bz_14, bz_15 |
| resolution_reasoning / resolution_diagnostics | bz_08 |
| follow_pattern | bz_11, bz_12, bz_13, bz_14, bz_15 |
| follow_pattern_type | bz_11, bz_12 |
| follow_pattern_confidence | bz_11 |
| follow_pattern_score | bz_11, bz_12, bz_13, bz_14, bz_15 |
| transformation_detected | bz_11 consumers: bz_12; also bz_13 |
| transformation_type / transformation_strength | bz_12 |
| transformation_score | bz_12, bz_13, bz_14, bz_15 |
| interaction_score / interaction_confidence | bz_13, bz_14, bz_15 |
| ten_gods_profile / ten_gods_balance | bz_14, bz_15 |
| ten_gods_dominance | bz_14 |
| growth_profile / growth_score | bz_15 |
| year/month/day/hour pillar, gender, birth_* | bz_09 only |

bz_01–bz_05 do not declare `published_inputs.json` (chart-native / score producers).

## Fan-in summary

Later Wave 1 packages consume a **stable core** of season/strength/temperature/pattern + a **narrow slice** of the immediately upstream advanced contracts. They do not consume every diagnostic tail — by design.
