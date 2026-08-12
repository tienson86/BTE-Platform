# CASE-0001 — TEN GODS SYSTEM AUDIT
## PART 02 — ENGINEERING REPORT (Regenerated)

| Field | Value |
|-------|-------|
| Case | CASE-0001 |
| Subject | Nguyễn Tiến Sơn |
| Birth | 1987-01-21 04:30 |
| Pillars | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| Day Master | Canh (Kim, Dương) |
| Engine | Ten Gods Core Engine V1.0 |
| Source | `TenGodsResult` only — `engines.ten_gods_engine.run_case_0001()` |
| Report type | Engineering audit — not interpretation |

---

## Source contract

| Item | Value |
|------|-------|
| Engine | `engines/ten_gods_engine/` |
| Version | `1.0.0` |
| Mapper | `engines/bazi_engine/ten_god.ten_god_name` |
| Hidden weights | `database/09_hidden_stems/hidden_stems.csv` |
| Runtime | `engines/ten_gods_engine/runtime/case_0001.py` |

---

# SECTION 1 — Inventory

## 1.1 Visible heavenly stems

| Pillar | Stem | Ten God | god_id | Weight |
|--------|------|---------|--------|--------|
| Year | Bính | Thất Sát | qi_sha | 1.0 |
| Month | Tân | Kiếp Tài | jie_cai | 1.0 |
| Day | Canh | Nhật Chủ | day_master | 1.0 |
| Hour | Mậu | Thiên Ấn | pian_yin | 1.0 |

## 1.2 Hidden stems (weighted)

| Pillar | Branch | Position | Stem | Ten God | god_id | Weight |
|--------|--------|----------|------|---------|--------|--------|
| Year | Dần | primary | Giáp | Thiên Tài | pian_cai | 0.6 |
| Year | Dần | secondary | Bính | Thất Sát | qi_sha | 0.3 |
| Year | Dần | tertiary | Mậu | Thiên Ấn | pian_yin | 0.1 |
| Month | Sửu | primary | Kỷ | Chính Ấn | zheng_yin | 0.6 |
| Month | Sửu | secondary | Quý | Thương Quan | shang_guan | 0.3 |
| Month | Sửu | tertiary | Tân | Kiếp Tài | jie_cai | 0.1 |
| Day | Ngọ | primary | Đinh | Chính Quan | zheng_guan | 0.7 |
| Day | Ngọ | secondary | Kỷ | Chính Ấn | zheng_yin | 0.3 |
| Hour | Dần | primary | Giáp | Thiên Tài | pian_cai | 0.6 |
| Hour | Dần | secondary | Bính | Thất Sát | qi_sha | 0.3 |
| Hour | Dần | tertiary | Mậu | Thiên Ấn | pian_yin | 0.1 |

**Total slots:** 4 visible + 11 hidden = 15 mapped occurrences.

## 1.3 Taxonomy coverage

| Ten God | Present |
|---------|---------|
| Tỷ Kiên | No |
| Kiếp Tài | Yes |
| Thực Thần | No |
| Thương Quan | Yes |
| Thiên Tài | Yes |
| Chính Tài | No |
| Thất Sát | Yes |
| Chính Quan | Yes |
| Thiên Ấn | Yes |
| Chính Ấn | Yes |
| Nhật Chủ | Yes (Day Master) |

**8 of 10** standard Ten Gods present. **Tỷ Kiên, Thực Thần, Chính Tài** = DORMANT.

---

# SECTION 2 — Dominance

| Field | Value |
|-------|-------|
| Status | **DETERMINED** |
| Primary | **Thất Sát** (`qi_sha`) |
| Policy | `weighted_contribution_with_margin_0.05_exclude_day_master` |

## Weighted totals (excludes Nhật Chủ)

| Ten God | god_id | Weighted total |
|---------|--------|----------------|
| Thất Sát | qi_sha | **1.6** |
| Thiên Tài | pian_cai | 1.2 |
| Thiên Ấn | pian_yin | 1.2 |
| Kiếp Tài | jie_cai | 1.1 |
| Chính Ấn | zheng_yin | 0.9 |
| Chính Quan | zheng_guan | 0.7 |
| Thương Quan | shang_guan | 0.3 |
| Tỷ Kiên / Thực Thần / Chính Tài | — | 0.0 |

**Why:** Thất Sát leads by margin ≥ 0.05 (1.6 vs 1.2). Dominance uses weighted contribution, not raw occurrence count alone (Thất Sát and Thiên Ấn both have occurrence_count = 3).

---

# SECTION 3 — Distribution

## 3.1 Occurrence count (unweighted slots)

| Ten God | Visible | Hidden | Total occurrences |
|---------|---------|--------|-------------------|
| Thất Sát | 1 | 2 | 3 |
| Thiên Ấn | 1 | 2 | 3 |
| Kiếp Tài | 1 | 1 | 2 |
| Thiên Tài | 0 | 2 | 2 |
| Chính Ấn | 0 | 2 | 2 |
| Chính Quan | 0 | 1 | 1 |
| Thương Quan | 0 | 1 | 1 |
| Nhật Chủ | 1 | 0 | 1 |

## 3.2 Weighted contribution (separate field)

| Ten God | visible_count | hidden_weight | weighted_contribution |
|---------|---------------|---------------|----------------------|
| Thất Sát | 1 | 0.6 | 1.6 |
| Thiên Tài | 0 | 1.2 | 1.2 |
| Thiên Ấn | 1 | 0.2 | 1.2 |
| Kiếp Tài | 1 | 0.1 | 1.1 |
| Chính Ấn | 0 | 0.9 | 0.9 |
| Chính Quan | 0 | 0.7 | 0.7 |
| Thương Quan | 0 | 0.3 | 0.3 |

## 3.3 Pattern summary

```text
Visible:     4 distinct labels on stems
Hidden:      11 weighted slots across 4 branches
Repeated:    Thất Sát ×3, Thiên Ấn ×3 (occurrence); Thiên Tài hidden-only ×2
Missing:     Tỷ Kiên, Thực Thần, Chính Tài
```

---

# SECTION 4 — Hierarchy

| Tier | Ten Gods | Weighted contribution |
|------|----------|----------------------|
| **PRIMARY** | Thất Sát | 1.6 |
| **SECONDARY** | Thiên Tài, Thiên Ấn, Kiếp Tài, Chính Ấn | 1.2, 1.2, 1.1, 0.9 |
| **SUPPORTING** | Chính Quan, Thương Quan | 0.7, 0.3 |
| **DORMANT** | Tỷ Kiên, Thực Thần, Chính Tài | 0.0 |

Nhật Chủ is mapped in visible/distribution but excluded from dominance hierarchy tiers.

---

# SECTION 5 — Relationship graph

Structural family relations only (no luck, pattern, useful god, or auspiciousness).

**Edge types:** `generation` (生) · `restriction` (克) · `support` (same family)

## Key edges involving PRIMARY (Thất Sát)

| From | To | Relation |
|------|-----|----------|
| qi_sha | jie_cai | restriction |
| qi_sha | pian_yin | generation |
| qi_sha | zheng_yin | generation |
| qi_sha | zheng_guan | support |
| shang_guan | qi_sha | restriction |
| pian_cai | qi_sha | generation |

**Total published edges:** 23

---

# SECTION 6 — Interaction matrix

**Present gods in matrix:** jie_cai, pian_cai, pian_yin, qi_sha, shang_guan, zheng_guan, zheng_yin (7×7 = 49 cells)

## Semantics

| State | Meaning |
|-------|---------|
| SUPPORT | Row family generates Column family |
| CONTROL | Row family controls Column family |
| DRAIN | Column family generates Row family (Row loses energy) |
| SAME | Same god_id or same structural family |
| INDIRECT | One-hop mixed generate/control between families |
| NONE | No direct structural relation |
| UNKNOWN | God not in chart |

## Sample — Row = Thất Sát (qi_sha)

| Column | State |
|--------|-------|
| Kiếp Tài | CONTROL |
| Thiên Tài | DRAIN |
| Thiên Ấn | SUPPORT |
| Thất Sát | SAME |
| Thương Quan | INDIRECT |
| Chính Quan | SAME |
| Chính Ấn | SUPPORT |

Full matrix available in `TenGodsResult.interaction_matrix`.

---

# SECTION 7 — Evidence

Every conclusion derives from `TenGodsResult` fields:

| Conclusion | Evidence field |
|------------|----------------|
| Visible inventory | `visible[]` |
| Hidden inventory + weights | `hidden[]`, `weights[]` |
| Occurrence vs weight separation | `distribution[].occurrence_count` vs `weighted_contribution` |
| Dominance | `dominant.status`, `dominant.primary_god_ids`, `dominant.weighted_totals` |
| Hierarchy tiers | `hierarchy[]` |
| Structural relationships | `relationships[]` |
| Pairwise interactions | `interaction_matrix[]` |
| Mapping provenance | each `evidence` string on visible/hidden entries |

---

# SECTION 8 — Missing runtime data

| Field | Status |
|-------|--------|
| Ten Gods Core Engine output | **PUBLISHED** (this report) |
| Hidden stem Ten Gods | **PUBLISHED** |
| Weighted distribution | **PUBLISHED** |
| Dominance / hierarchy / matrix | **PUBLISHED** |
| Orchestrator pipeline registration | **NOT WIRED** — engine runs via direct API |
| Analysis Runtime `ten_gods` stage bridge | **NOT WIRED** to core engine |
| PACK-02 knowledge catalog / NarrativePlan | **NOT PUBLISHED** |
| Luck × Ten Gods overlay | **NOT IN SCOPE** |
| Pattern / Useful God cross-inference | **EXCLUDED** by engine design |

`TenGodsResult.missing_data`: **[]** (empty — no blockers inside core engine run).

---

# SECTION 9 — Risks (interpretation layer)

Conclusions that **still must not** be inferred without separate packs:

| # | Blocked without additional publish |
|---|-------------------------------------|
| 1 | Personality / career / marriage customer prose |
| 2 | Auspicious vs inauspicious favorability |
| 3 | Pattern-derived Ten God roles |
| 4 | Useful-God-adjusted favorability |
| 5 | Luck-period modulation |
| 6 | Expert calibration vs engine dominance |

---

# SECTION 10 — MASTER INTERPRETATION READINESS

## Can Part 02 Master Interpretation be written?

**PARTIAL — engineering foundation YES; commercial Part 02 NO**

## Ready

- Complete visible + hidden Ten Gods inventory
- Deterministic dominance (Thất Sát PRIMARY)
- Hierarchy, relationship graph, interaction matrix
- Evidence strings per occurrence

## Remaining blockers for commercial Part 02

1. Orchestrator / API publish path not wired
2. No PACK-02 frozen golden NarrativePlan for CASE-0001
3. No Ten Gods knowledge catalog QA / unit selection
4. Interpretation composer not connected to `TenGodsResult`

## Minimum gate before customer Part 02

```text
1. Wire Ten Gods Core Engine into orchestrator public payload
2. Freeze CASE-0001 Ten Gods golden NarrativePlan
3. Connect Interpretation Engine V2 Ten Gods selector to TenGodsResult facts
```

---

END — Engineering report only. No interpretation.
