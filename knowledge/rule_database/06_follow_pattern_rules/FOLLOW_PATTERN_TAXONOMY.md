# FOLLOW_PATTERN_TAXONOMY.md — Follow Pattern Rule Taxonomy

> Module: 06_follow_pattern_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the complete taxonomy for Follow Pattern (Tòng Cách) classification in the BTE Knowledge Base.

---

# 2. Follow Types

| Code | Vietnamese | Condition |
|------|------------|-----------|
| tong_vuong | Tòng Vượng | Support ratio ≥ 0.70, no Quan/Sát/Tài |
| tong_tai | Tòng Tài | Weak body, wealth dominant |
| tong_sat | Tòng Sát | Weak body, killing dominant |
| tong_quan | Tòng Quan | Weak body, officer dominant |
| tong_nhi | Tòng Nhi | Weak body, output dominant |
| tong_an | Tòng Ấn | Weak body, resource dominant |

---

# 3. Categories

| Category | Family | Description |
|----------|--------|-------------|
| true_follow | true_follow | Verified follow patterns from CSV |
| pseudo_follow | pseudo_follow | Incomplete or false follow conditions |
| eligibility | follow_eligibility | Gates before follow matching |
| maintenance | follow_maintenance | Conditions that sustain follow |
| break | follow_break | Conditions that break follow |
| conversion | follow_conversion | Weak/strong body conversion rules |
| seasonal | season_confirmation | Season validates follow type |
| threshold | strength_threshold | Support ratio and count thresholds |
| special_interaction | special_case_interaction | Special case module interaction |
| priority | priority_ordering | Execution and conflict resolution |
| fallback | fallback_behavior | Default when no follow detected |

---

# 4. Detection Thresholds

| Parameter | Value | Source |
|-----------|-------|--------|
| weak_support_ratio | 0.25 | FollowPatternCalculator |
| strong_support_ratio | 0.70 | FollowPatternCalculator |
| dominant_ratio | 0.50 | FollowPatternCalculator |
| dominant_count_min | 2 | FollowPatternCalculator |

---

# 5. Priority Hierarchy

```
Follow beats Main Pattern     (order 200)
  ↓
Tòng Vượng check first        (order 195)
  ↓
Tòng Nhược family             (order 190)
  ↓
True follow rules             (order 90)
  ↓
Eligibility gates             (order 60–73)
  ↓
Fallback                      (order 1–5)
```

---

# 6. References

- `database/14_pattern/03_follow_pattern.csv`
- `engines/pattern_engine/calculators/follow_pattern.py`
- `FOLLOW_PATTERN_DECISION_TREE.md`
