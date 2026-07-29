# FOLLOW_PATTERN_DECISION_TREE.md — Follow Pattern Decision Tree

> Module: 06_follow_pattern_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Documents the decision flow for Follow Pattern detection, validation, and override resolution.

---

# 2. Pipeline Position

```
Season → Strength → Temperature → Pattern → Special Case → Follow Pattern → Combination
```

---

# 3. Decision Tree

```
START
  │
  ├─► Load upstream signals
  │     (strength_level, season, primary_pattern, special_case_flag)
  │
  ├─► Phase 1: Eligibility Gates
  │     ├─ Pattern confirmed? ──NO──► fallback_no_follow
  │     ├─ Strength weak/strong? ──► continue
  │     └─ Support ratio check (0.25 / 0.70)
  │
  ├─► Phase 2: Follow Detection (FollowPatternCalculator)
  │     ├─ support_ratio ≥ 0.70 ──► Tòng Vượng (fol_tv_01)
  │     ├─ support_ratio > 0.25 ──► no follow (balanced)
  │     └─ support_ratio ≤ 0.25 ──► match dominant family
  │           ├─ wealth ──► Tòng Tài
  │           ├─ officer ──► Tòng Quan
  │           ├─ killing ──► Tòng Sát
  │           ├─ output ──► Tòng Nhi
  │           └─ resource ──► Tòng Ấn
  │
  ├─► Phase 3: Special Case Check
  │     ├─ FALSE_FOLLOW? ──► pseudo_follow_false (block)
  │     └─ special_case_flag? ──► apply interaction rules
  │
  ├─► Phase 4: Break / Maintenance
  │     ├─ Break conditions met? ──► downgrade or reject follow
  │     └─ Maintenance conditions? ──► boost confidence
  │
  ├─► Phase 5: Season Confirmation
  │     └─ Season aligns with follow type? ──► confirm (+weight)
  │
  ├─► Phase 6: Priority Resolution
  │     ├─ Follow beats main pattern (pri_follow_beats_main)
  │     ├─ Score tiebreak
  │     └─ First match
  │
  └─► OUTPUT: follow_pattern_match
        ├─ follow_type
        ├─ is_true_follow / is_pseudo_follow
        ├─ confidence
        └─ matched_rules[]
```

---

# 4. Break Conditions

| Rule | Trigger | Effect |
|------|---------|--------|
| break_officer_clash | Stem clash + Tòng Quan | Follow broken |
| break_seal_attack | Thương Quan + Tòng Ấn | Follow broken |
| break_wealth_rob | Kiếp Tài + Tòng Tài | Follow broken |
| break_strength_recovery | Support ratio > 0.40 | Follow invalidated |
| break_special_case | FALSE_FOLLOW flag | Follow blocked |

---

# 5. Fallback

| Rule | Condition | Action |
|------|-----------|--------|
| fallback_no_follow | No follow detected | Use primary_pattern |
| fallback_ambiguous_follow | confidence < 0.65 | Conservative handling |

---

# 6. References

- `FOLLOW_PATTERN_TAXONOMY.md`
- `DEPENDENCIES.json`
- `knowledge/rule_database/05_special_case_rules/SPECIAL_CASE_DECISION_TREE.md`
