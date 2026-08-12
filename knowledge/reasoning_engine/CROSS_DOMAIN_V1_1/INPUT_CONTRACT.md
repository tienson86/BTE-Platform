# INPUT_CONTRACT — CrossDomainReasoningInput

Canonical input. Prefer typed fields over arbitrary dicts.

| Field | Type | Notes |
|-------|------|-------|
| strength_level | str | e.g. balanced, strong |
| strength_score | float | evidence weight |
| pattern_key | str | engine key |
| pattern_label | str | Vietnamese label |
| pattern_than_vuong_nhuoc | str | body intensity from pattern |
| tong_cach | str | follow / special pattern label |
| ten_gods_primary | list[str] | labels |
| ten_gods_secondary | list[str] | labels |
| ten_gods_families | list[str] | companion / output / officer / … |
| useful_god | str | balance pivot |
| useful_reasoning | str | published reasoning |
| favorable / unfavorable | list[str] | balance lists |
| domain_conclusions | dict[str,str] | composer conclusions by domain |
| missing_domains | list[str] | insufficient / unavailable |
| question_context | QuestionContext | GENERAL / IDENTITY / CAREER |
| versions | dict[str,str] | engine/composer versions |

Builder: `cross_domain/input_builder.build_reasoning_input`.
