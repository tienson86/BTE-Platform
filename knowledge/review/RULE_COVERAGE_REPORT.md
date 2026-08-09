# Rule Coverage Report

## Totals

| Metric | Value |
| --- | --- |
| Production rules | **2 849** |
| Packages with rules | 14 / 15 |
| Packages with 0 rules | bz_09_luck_foundation |
| Prefixes | SKC SEC TEC PAT PEV UGD UGP UGO FPC TRC CBC TGA TGP HSA |

## Coverage by package

| Package | Prefix | Rules | Share |
| --- | --- | --- | --- |
| bz_01_strength_core | SKC | 110 | 3.9% |
| bz_02_seasonal_core | SEC | 110 | 3.9% |
| bz_03_temperature_core | TEC | 110 | 3.9% |
| bz_04_pattern_core | PAT | 110 | 3.9% |
| bz_05_pattern_evaluation | PEV | 110 | 3.9% |
| bz_06_useful_god_foundation | UGD | 109 | 3.8% |
| bz_07_useful_god_priority | UGP | 110 | 3.9% |
| bz_08_useful_god_override | UGO | 110 | 3.9% |
| bz_09_luck_foundation | — | 0 | 0% |
| bz_10_follow_pattern_core | FPC | 250 | 8.8% |
| bz_11_transformation_core | TRC | 280 | 9.8% |
| bz_12_combination_clash_core | CBC | 300 | 10.5% |
| bz_13_ten_gods_advanced | TGA | 400 | 14.0% |
| bz_14_twelve_growth_advanced | TGP | 360 | 12.6% |
| bz_15_hidden_stems_advanced | HSA | 380 | 13.3% |

## Coverage by domain (primary `domain_id`)

| Domain | Packages | Rules |
| --- | --- | --- |
| DOM-STRENGTH | bz_01 | 110 |
| DOM-SEASONAL | bz_02 | 110 |
| DOM-TEMPERATURE | bz_03 | 110 |
| DOM-PATTERN | bz_04, bz_05, bz_10 | 470 |
| DOM-USEFUL_GOD | bz_06, bz_07, bz_08 | 329 |
| DOM-LUCK_CYCLE | bz_09 | 0 |
| DOM-TRANSFORMATION | bz_11 | 280 |
| DOM-COMBINATION | bz_12 | 300 |
| DOM-TEN_GODS | bz_13 | 400 |
| DOM-TWELVE_GROWTH | bz_14 | 360 |
| DOM-HIDDEN_STEM | bz_15 | 380 |

DOM-CLASH / DOM-HARM / DOM-PUNISHMENT have **no primary package**; their rules live as categories inside bz_12.

## Heatmap (relative density)

```
STRENGTH     ██
SEASONAL     ██
TEMPERATURE  ██
PATTERN      █████████
USEFUL_GOD   ██████
LUCK         ·
TRANSFORM    █████
COMBINATION  ██████
TEN_GODS     ████████
GROWTH       ███████
HIDDEN       ███████
```

## Future expansion candidates

- Luck analytical rules (Da Yun / Liu Nian scoring) under DOM-LUCK_CYCLE / DOM-ANNUAL_LUCK / DOM-MONTHLY_LUCK
- Calendar + Four Pillars construction packages
- Shen Sha
- Dedicated Clash / Harm / Punishment packages if bz_12 should stay combination-primary
- Interpretation / Report knowledge (not analytical scores)
- Ten Gods / Growth / Hidden Stems **core** (currently advanced-only)

See [RULE_GAP_ANALYSIS.md](RULE_GAP_ANALYSIS.md).
