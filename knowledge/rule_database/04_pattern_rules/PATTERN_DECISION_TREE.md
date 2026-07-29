# PATTERN_DECISION_TREE.md — Pattern Recognition Decision Tree

> Module: 04_pattern_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Documents the decision flow for Pattern Engine rule matching and conflict resolution.

---

# 2. Pipeline Position

```
Calendar → Bazi → Season → Strength → Temperature → Pattern → Useful God
```

Pattern Engine receives:

- `BaziChart` (ten gods, elements, pillars)
- `strength_level` from 01_strength_rules
- `season` from 02_season_rules
- `temperature_type` from 03_temperature_rules

---

# 3. Decision Tree

```
START
  │
  ├─► Load all PAT rules from pattern_rules.json
  │
  ├─► Phase 1: Eligibility Gates
  │     ├─ month_branch_ten_god available? ──NO──► exceptional_no_month_command (PAT-000044)
  │     └─ YES ──► continue
  │
  ├─► Phase 2: Match All Rules
  │     ├─ Standard (main_pattern)     ──► 10 Lệnh Tháng rules
  │     ├─ Transformed (special_pattern) ──► 5 Chuyên Cách rules
  │     ├─ Follow (follow_pattern)     ──► 6 Tòng Cách rules
  │     ├─ Mixed (combination_pattern) ──► 5 combination rules
  │     ├─ Pseudo-follow               ──► 4 partial follow rules
  │     ├─ Broken                      ──► 5 broken pattern rules
  │     ├─ Mixed (mixed_pattern)       ──► 4 complex mix rules
  │     └─ Exceptional                 ──► 4 edge case rules
  │
  ├─► Phase 3: Follow Detection
  │     └─ FollowPatternCalculator.detect() ──► if follow_type set,
  │           apply follow_override rules (priority ≥ 90)
  │
  ├─► Phase 4: Conflict Resolution
  │     ├─ Apply priority hierarchy:
  │     │     Follow (200) > Special (195) > Combination (190) > Main (180)
  │     ├─ Same priority? ──► score_tiebreak (higher weight wins)
  │     ├─ Same priority + score? ──► first_match
  │     └─ Special vs Follow both match? ──► special_vs_follow (Special wins)
  │
  ├─► Phase 5: Quality Assessment
  │     ├─ Broken pattern detected? ──► downgrade pattern_quality
  │     ├─ Temperature extreme? ──► temperature_override adjustment
  │     └─ Calculate confidence score
  │
  └─► OUTPUT: PatternResult
        ├─ primary_pattern
        ├─ secondary_patterns
        ├─ follow_pattern (bool)
        ├─ special_pattern (bool)
        ├─ confidence
        ├─ matched_rules
        └─ rejected_rules
```

---

# 4. Conflict Resolution Rules

| Rule ID | Scenario | Resolution |
|---------|----------|------------|
| PAT-000028 | Follow vs Main | Follow wins |
| PAT-000029 | Special vs Main | Special wins |
| PAT-000030 | Combination vs Standard | Combination wins |
| PAT-000058 | Equal priority | Higher score wins |
| PAT-000059 | Equal priority + score | First match wins |
| PAT-000060 | Follow vs Combination | Follow wins |
| PAT-000061 | Special vs Follow | Special wins |

---

# 5. Group Priority Order

| Order | Group | Rule ID |
|-------|-------|---------|
| 200 | follow | PAT-000062 |
| 195 | special | PAT-000063 |
| 190 | combination | PAT-000064 |
| 180 | main | PAT-000065 |
| 170 | broken | PAT-000066 |
| 50 | eligibility | PAT-000067 |
| 45 | exceptional | PAT-000068 |

---

# 6. Fallback

When no rule matches:

1. `pat_fallback` (PAT-000001) — lowest priority, empty conditions
2. `exceptional_no_month_command` (PAT-000044) — when month command unknown

---

# 7. References

- `PATTERN_TAXONOMY.md`
- `MODULE_SPEC.md`
- `DEPENDENCIES.json`
- `database/14_pattern/05_priority_rules.csv`
