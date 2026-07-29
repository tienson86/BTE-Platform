# PATTERN_TAXONOMY.md — Pattern Rule Taxonomy

> Module: 04_pattern_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the complete taxonomy for Pattern (Cách Cục) classification in the BTE Knowledge Base.

---

# 2. Pattern Categories

| Category | Family | Description | ID Prefix Range |
|----------|--------|-------------|-----------------|
| standard | main_pattern | 10 main patterns from Lệnh Tháng (月令) | PAT-000001–011 |
| transformed | special_pattern | Chuyên Cách (Khúc Trực, Viêm Thượng, etc.) | PAT-000012–016 |
| follow | follow_pattern | Tòng Cách override rules | PAT-000017–022 |
| mixed | combination_pattern | Multi-god combination patterns | PAT-000023–027 |
| priority | conflict_resolution | Priority hierarchy markers | PAT-000028–030 |
| pseudo_follow | pseudo_follow | Incomplete follow conditions | PAT-000031–034 |
| broken | broken_pattern | Pattern broken by clash or drain | PAT-000035–039 |
| mixed | mixed_pattern | Complex multi-structure patterns | PAT-000040–043 |
| exceptional | exceptional_pattern | Edge cases and tiebreaks | PAT-000044–047 |
| eligibility | eligibility_condition | Pattern matching gates | PAT-000048–057 |
| priority | conflict_resolution | Extended conflict resolution | PAT-000058–061 |
| priority | group_priority | Rule group execution order | PAT-000062–068 |

---

# 3. Main Patterns (Standard)

| Code | Vietnamese | Ten God (Lệnh Tháng) |
|------|------------|----------------------|
| chinh_quan | Chính Quan Cách | Chính Quan |
| that_sat | Thất Sát Cách | Thất Sát |
| chinh_tai | Chính Tài Cách | Chính Tài |
| thien_tai | Thiên Tài Cách | Thiên Tài |
| thuc_than | Thực Thần Cách | Thực Thần |
| thuong_quan | Thương Quan Cách | Thương Quan |
| chinh_an | Chính Ấn Cách | Chính Ấn |
| thien_an | Thiên Ấn Cách | Thiên Ấn |
| ty_kien | Kiến Lộc Cách | Tỷ Kiên |
| kiep_tai | Dương Nhẫn Cách | Kiếp Tài |

---

# 4. Transformed Patterns (Special)

| Code | Vietnamese | Element Condition |
|------|------------|-------------------|
| khuc_truc | Khúc Trực Cách | Wood DM + Wood month, no officer |
| viem_thuong | Viêm Thượng Cách | Fire DM + Fire month, no officer |
| nhuan_ha | Nhuận Hạ Cách | Water DM + Water month, no officer |
| gia_sac | Giá Sắc Cách | Metal DM + Metal month, no output |
| jia_wang | Giá Vượng Cách | Earth DM + Earth month, no officer |

---

# 5. Follow Patterns (Tòng Cách)

| Code | Vietnamese | Condition |
|------|------------|-----------|
| tong_vuong | Tòng Vượng Cách | No Quan/Sát/Tài in chart |
| tong_tai | Tòng Tài Cách | Contains Chính Tài |
| tong_sat | Tòng Sát Cách | Contains Thất Sát |
| tong_quan | Tòng Quan Cách | Contains Chính Quan |
| tong_nhi | Tòng Nhi Cách | Contains Thực Thần |
| tong_an | Tòng Ấn Cách | Contains Chính Ấn |

---

# 6. Priority Hierarchy

```
Follow Override     (priority ≥ 90, order 200)
  ↓
Special Pattern     (priority = 95, order 195)
  ↓
Combination Pattern (priority 82–86, order 190)
  ↓
Main Pattern        (priority 60–80, order 180)
  ↓
Broken Pattern      (priority 50–55, order 170)
  ↓
Eligibility Gates   (order 50)
  ↓
Exceptional/Fallback (order 1–45)
```

---

# 7. Condition Fields

| Field | Type | Source |
|-------|------|--------|
| month_branch_ten_god | str | Bazi Engine |
| ten_gods_list | list[str] | Bazi Engine |
| day_master_element | str | Bazi Engine |
| month_branch_element | str | Bazi Engine |
| officer_elements | list[str] | Pattern Context |
| output_elements | list[str] | Pattern Context |
| season | str | Season Module |
| strength_level | str | Strength Module |
| temperature_type | str | Temperature Module |

---

# 8. References

- `database/14_pattern/README.md`
- `MODULE_SPEC.md`
- `PATTERN_DECISION_TREE.md`
- `.specs/pattern_engine.md`
