# Evidence Builder Validation Report — Epic 03 Milestone 05

## Summary

- Samples validated: **4**
- Total evidence items: **47**
- Duplicates removed across builds: **0**
- Categories supported: **BaZi, Five Elements, Ten Gods, Useful God, Pattern, Strength, Temperature, ShenSha**

## Evidence item contract

- `rule`
- `reason`
- `confidence`
- `source`

## Dedup policy

- Key: `category|rule|source` (case-insensitive)
- Repeated identical facts are kept once

## Sample digest

```json
[
  {
    "sample": "rich",
    "item_count": 37,
    "categories_present": [
      "bazi",
      "five_elements",
      "ten_gods",
      "useful_god",
      "pattern",
      "strength",
      "temperature",
      "shensha"
    ],
    "duplicate_removed": 0,
    "sample_rules": [
      "day_master=Bính",
      "day_master_element=Hỏa",
      "day_master_yin_yang=Dương",
      "year_pillar=Canh Ngọ",
      "month_pillar=Ất Tỵ",
      "day_pillar=Bính Ngọ",
      "hour_pillar=Quý Tỵ",
      "season=summer"
    ]
  },
  {
    "sample": "minimal_officer",
    "item_count": 3,
    "categories_present": [
      "ten_gods",
      "pattern",
      "strength"
    ],
    "duplicate_removed": 0,
    "sample_rules": [
      "present=Chính Quan",
      "main_pattern=chinh_quan",
      "level=strong"
    ]
  },
  {
    "sample": "weak_water",
    "item_count": 7,
    "categories_present": [
      "bazi",
      "useful_god",
      "strength",
      "temperature",
      "shensha"
    ],
    "duplicate_removed": 0,
    "sample_rules": [
      "day_master_element=Thủy",
      "status=ok",
      "element=Thổ",
      "level=weak",
      "status=cold",
      "cold_score=0.8",
      "present=Cô Thần"
    ]
  },
  {
    "sample": "empty",
    "item_count": 0,
    "categories_present": [],
    "duplicate_removed": 0,
    "sample_rules": []
  }
]
```

## Compatibility

- Input: RuleContext only
- No calculation engine changes
- No UI changes
