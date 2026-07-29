# Pattern Rule Database — database/14_pattern/

Version: 2.0  
Last updated: 2026-07-29

## Overview

Production rule database cho Pattern Engine (Cách Cục nhận diện).  
Toàn bộ tri thức phân loại Cách Cục nằm trong các file CSV này.  
Engine code **không hard-code** bất kỳ rule nào.

---

## File Structure

| File | Purpose | Rules |
|---|---|---|
| `01_main_pattern.csv` | 10 cách cục cặn chính — dựa trên Lệnh Tháng | 10 |
| `02_special_pattern.csv` | Chuyên Cách (Khúc Trực, Viêm Thượng, Nhuận Hạ, Giá Sắc) | 4 |
| `03_follow_pattern.csv` | Tòng Cách override rules | 6 |
| `04_combination_pattern.csv` | Combination cách (Quan Ấn, Sát Ấn, Tài Quan...) | 5 |
| `05_priority_rules.csv` | Priority hierarchy documentation | 3 |
| `06_pattern_conditions.csv` | Condition reference library | 24 |
| `07_pattern_examples.csv` | Verified examples for testing | 16 |

---

## Rule Schema (01–04)

```
rule_id        — unique identifier
pattern        — pattern code (snake_case, matches labels.py)
priority       — integer, higher = wins over lower
conditions     — JSON array of condition objects
score          — float (0–100), tiebreaker when priority equal
description    — Vietnamese display text
enabled        — true/false
source         — filename or "follow_override"
```

### Condition Object Schema

```json
{
  "field": "month_branch_ten_god",
  "operator": "==",
  "value": "Chính Quan"
}
```

### Supported Operators

| Operator | Meaning |
|---|---|
| `==` | equals |
| `!=` | not equals |
| `>`, `>=`, `<`, `<=` | numeric comparison |
| `contains` | value in list field |
| `not_contains` | value not in list field |
| `in` | field value in list |
| `not_in` | field value not in list |

---

## PatternContext Fields Available for Conditions

| Field | Type | Description |
|---|---|---|
| `day_master` | str | Nhật chủ (e.g. "Giáp") |
| `month_branch` | str | Địa chi tháng (e.g. "Tý") |
| `month_stem` | str | Thiên can tháng (e.g. "Canh") |
| `month_stem_ten_god` | str | Thập thần của thiên can tháng |
| `month_branch_ten_god` | str | Thập thần của can chính Địa chi tháng (Lệnh Tháng) |
| `ten_gods_list` | list[str] | Toàn bộ thập thần trong chart |
| `hidden_stems_flat` | list[str] | Toàn bộ tàng can |
| `season` | str | Mùa: spring/summer/autumn/winter |
| `strength_level` | str | Thân vượng/nhược: strong/weak/balanced |

---

## Priority Hierarchy

```
Follow Cách (follow_override source) — priority ≥ 90
  ↓ overrides when FollowPatternCalculator detects follow type
Special Cách (02_special_pattern.csv) — priority = 95
Combination Cách (04_combination_pattern.csv) — priority 82–86
Main Cách (01_main_pattern.csv) — priority 60–80
```

---

## Key Design Principle: Lệnh Tháng (月令)

Main pattern is determined by **month branch main stem** → ten god relative to day master.

Example: Day Master = Giáp (Wood), Month Branch = Dậu
- Dậu main stem = Tân (Metal)
- Tân relative to Giáp = Chính Quan
- → Pattern = Chính Quan Cách

This is classical Ziping Bazi (子平命理) methodology.

---

## Adding New Rules

1. Add row to appropriate CSV file
2. Assign `rule_id` with prefix matching file (e.g. `pat_`, `spe_`, `fol_`, `com_`)
3. Set `conditions` as JSON array using fields from PatternContext
4. Set `priority` appropriate to rule type (see hierarchy above)
5. Set `enabled = true`
6. Run validation: `python validation/pattern_db_validate.py`
