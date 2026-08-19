# G1-01 — Ten Gods Truth & Evidence Audit

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-01 |
| **Document** | `release/gate_01/G1_01_TEN_GODS_AUDIT.md` |
| **Phase** | 1 — Audit only |
| **Date** | 2026-08-19 |
| **Status** | READY FOR PRODUCT OWNER REVIEW |
| **Scope** | Calculation Truth → Evidence → Presentation |
| **Out of scope** | Narrative personality / career / wealth / marriage / luck; engine repair; Portal repair; contract break |

This report does not modify Engine, Portal, Report, or public contract.

No new Ten Gods engine is proposed. Canonical implementation already exists.

---

# Verdict

| Question | Result |
|----------|--------|
| Canonical calculator exists? | **Yes** — `engines/ten_gods_engine` wrapping `engines.bazi_engine.ten_god.ten_god_name` |
| New engine required? | **No** |
| 10×10 = 100 mapping test exists? | **No** — only Giáp × 10 is tested |
| Algorithm vs 100-row CSV | **96/100 match**; **4 CSV rows contradict STEM polarity** |
| Golden CASE visible | **PASS** |
| Golden CASE hidden | **PASS** in TenGodsEngine |
| Hidden Ten Gods exist in engine result? | **Yes** — 11 mapped occurrences on CASE-0001 |
| Why summary shows only 4 gods? | **Presentation / adapter bind visible stems only** |
| G1-01 PASS today? | **No** |

---

# 1. Canonical implementation hiện tại

## 1.1 Production owner (frozen)

`beta/BETA0_ANALYTICAL_TRUTH_LOCK.md` assigns Ten Gods to:

```text
TenGodsEngine
    engines/ten_gods_engine
```

Production callers:

| Caller | Function |
|--------|----------|
| `applications/api/services/orchestrator.py` | `TenGodsEngine.calculate(day_master, pillars)` |
| `applications/production/engine_runner.py` | same |

Day Master is **not recomputed** by Ten Gods Engine.

It is copied from BaZi:

```text
CalendarEngine.build
        ↓
BaziEngine.build  →  day_pillar.stem = Nhật Chủ
        ↓
BaziView.day_master
        ↓
TenGodsEngine.calculate(day_master=..., pillars=...)
```

Engine validates `pillars["day"].stem == day_master`.

## 1.2 Single mapper

| Layer | Path | Role |
|-------|------|------|
| Mapping function | `engines/bazi_engine/ten_god.py` → `ten_god_name(day_master, other_stem)` | Stem → Ten God label |
| Chart overlay | `engines/ten_gods_engine/mapper.py` → `map_stem_to_ten_god` | Same mapper; if `stem == day_master` → **Nhật Chủ** |
| Hidden stems | `engines/ten_gods_engine/loader.py` | `database/09_hidden_stems/hidden_stems.csv` |
| Aggregation | `engines/ten_gods_engine/calculator.py` | Visible + hidden layers, weights, distribution |

Do **not** treat these as canonical production calculation:

| Module | Why not production SSOT |
|--------|-------------------------|
| `engines/analysis_engine/ten_gods_engine` | Analysis Runtime stage 05. Knowledge-driven presence. Skips day pillar. **Not called** by production Orchestrator / EngineRunner. |
| `engines/bazi_engine/ten_gods/calculator.py` | Legacy CSV calculator. Imports `bazi_engine.core` (non-`engines.` path). `database/10_ten_gods/ten_gods.csv` is **absent**. |
| `engines/bazi_engine/ten_gods/service.py` | Stub returning Tỷ Kiên. |
| `engines/score_engine/.../ten_god_score.py` | Score, not Analytical Truth. |

`BaziEngine.build()` **also** writes `BaziChart.ten_gods` via the same `ten_god_name`. That is a second publication of visible labels, not a second algorithm.

Ownership conflict: lock says TenGodsEngine owns Ten Gods; Portal/Report currently read the BaZi copy.

## 1.3 Ngũ hành sinh–khắc

Hard-coded in `engines/bazi_engine/ten_god.py`:

```text
GENERATES: Mộc→Hỏa→Thổ→Kim→Thủy→Mộc
CONTROLS:  Mộc→Thổ, Hỏa→Kim, Thổ→Thủy, Kim→Mộc, Thủy→Hỏa
```

Stem metadata:

```text
Giáp Mộc Dương · Ất Mộc Âm
Bính Hỏa Dương · Đinh Hỏa Âm
Mậu Thổ Dương · Kỷ Thổ Âm
Canh Kim Dương · Tân Kim Âm
Nhâm Thủy Dương · Quý Thủy Âm
```

Normative rule document (matches algorithm):

`database/02_quan_he/thap_than/quy_tac.md`

| Quan hệ Ngũ Hành | Cùng Âm Dương | Khác Âm Dương |
|------------------|---------------|---------------|
| Đồng hành | Tỷ Kiên | Kiếp Tài |
| Nhật Chủ sinh | Thực Thần | Thương Quan |
| Đối tượng sinh Nhật Chủ | Thiên Ấn | Chính Ấn |
| Nhật Chủ khắc | Thiên Tài | Chính Tài |
| Đối tượng khắc Nhật Chủ | Thất Sát | Chính Quan |

Địa Chi không tham gia mapping. Địa Chi chỉ cung cấp Tàng Can.

## 1.4 Nhật can

| Situation | `ten_god_name` | `map_stem_to_ten_god` / chart |
|-----------|----------------|-------------------------------|
| Day pillar visible stem | Tỷ Kiên | **Nhật Chủ** |
| Any other stem equal to Day Master (including hidden) | Tỷ Kiên | **Nhật Chủ** |

Nhật Chủ is a chart overlay, not a row in the 100-stem matrix.

## 1.5 Lộ can (visible)

For each of year / month / day / hour:

1. Read pillar heavenly stem.
2. Map via `map_stem_to_ten_god`.
3. Weight = `1.0`.
4. Evidence string: `visible:{pillar}:{stem}`.

## 1.6 Tàng can (hidden)

For each pillar branch, load ordered slots from `hidden_stems.csv`:

| Branch | Hidden stems | Weights |
|--------|----------------|---------|
| Dần | Giáp, Bính, Mậu | 0.6 / 0.3 / 0.1 |
| Sửu | Kỷ, Quý, Tân | 0.6 / 0.3 / 0.1 |
| Ngọ | Đinh, Kỷ | 0.7 / 0.3 |

Each hidden stem is mapped with the **same** `map_stem_to_ten_god`.

BaziEngine `HIDDEN` dict lists the same stems for these branches, but **does not map them to Ten Gods**.

## 1.7 Data contract hiện tại

### Canonical engine result — `TenGodsResult.to_dict()`

Already contains structured visible and hidden entries.

Visible entry fields:

`pillar, stem, ten_god, god_id, visibility, evidence`

Hidden entry fields:

`pillar, branch, hidden_stem, hidden_position, position_name, weight, ten_god, god_id, evidence`

Day Master block:

`stem, element, yin_yang`

**Missing on each occurrence (required by G1-01 evidence):**

- element of source stem
- element relation to Day Master
- polarity relation to Day Master

These values are derivable from `STEM_META` + `day_master` without a new engine.

`TenGodPositionFact.relation_to_day_master` currently copies the **Ten God label**, not the ngũ hành relation. That field is misnamed relative to G1-01.

### Compact BaZi contract — `BaziView`

| Field | Content |
|-------|---------|
| `bazi.ten_gods` | 4 visible labels only |
| `year/month/day/hour_pillar.ten_god` | same 4 labels |
| `pillar.hidden_stems` | stem **names**, not Ten Gods |
| `bazi.hidden_stems` | flat stem **names** |

### Public API after Score stage

```text
payload["ten_gods"] = {
    visible: bazi.ten_gods,          # 4 labels
    hidden:  bazi.hidden_stems,      # stem names, NOT ten gods
    summary: join(bazi.ten_gods)
}
```

`TenGodsResult` is passed into Interpretation Foundation. It is **not** the public `payload["ten_gods"]` object.

### Report contract — `ReportTenGodsV1`

```text
visible: list[str]
hidden:  list[str]
summary: str
```

Adapter fills `hidden` from `bazi.hidden_stems` (stems), same type error.

---

# 2. Truth table hiện tại

## 2.1 Canonical 100-row table

`database/02_quan_he/thap_than/du_lieu.csv`

| Check | Value |
|-------|-------|
| Rows | 100 |
| Day Masters | 10 |
| Target stems | 10 |
| Unique pairs | 100 |
| Columns | `nhat_chu, doi_tuong, quan_he_ngu_hanh, quan_he_am_duong, thap_than` |
| Self-mapping | 10 rows, all **Tỷ Kiên** |

This table is the intended 10×10 evidence matrix.

Production does **not** load this CSV. Production uses the algorithm in `ten_god.py`.

## 2.2 Algorithm vs CSV

Live comparison of `ten_god_name` against all 100 CSV rows:

| Result | Count |
|--------|------:|
| Match | 96 |
| Mismatch | **4** |
| Empty algorithm cells | 0 |

Mismatches (Fire Day Master × Wood stems):

| Nhật chủ | Đối tượng | Actual polarity (STEM_META) | CSV polarity | CSV Ten God | Algorithm Ten God |
|----------|-----------|-----------------------------|--------------|-------------|-------------------|
| Bính (Hỏa Dương) | Giáp (Mộc Dương) | Cùng | Khác âm dương | Chính Ấn | Thiên Ấn |
| Bính (Hỏa Dương) | Ất (Mộc Âm) | Khác | Cùng âm dương | Thiên Ấn | Chính Ấn |
| Đinh (Hỏa Âm) | Giáp (Mộc Dương) | Khác | Cùng âm dương | Thiên Ấn | Chính Ấn |
| Đinh (Hỏa Âm) | Ất (Mộc Âm) | Cùng | Khác âm dương | Chính Ấn | Thiên Ấn |

CSV polarity on these four rows contradicts `STEM_META`.

`quy_tac.md` agrees with the algorithm: same polarity + đối tượng sinh → Thiên Ấn.

**Audit classification:** CSV data defect, not a live calculator bug, unless Product Owner declares CSV as SSOT over `quy_tac.md` + `STEM_META`.

Recommended SSOT for G1-01 calculation: **algorithm + `quy_tac.md` + `STEM_META`**. Repair the four CSV rows in Phase 2.

CASE-0001 uses Nhật chủ Canh. These four rows do not affect the golden case.

---

# 3. 100-mapping test status

| Item | Status |
|------|--------|
| Required matrix | 10 Day Masters × 10 stems = 100 |
| Must assert | element relation, yin/yang relation, Ten God result |
| Must not | hard-code only CASE-0001 |

Existing test: `tests/ten_gods_engine/test_core_ten_gods.py` → `test_all_ten_gods_mapping`

It parametrizes **Giáp × 10 stems only**.

It does not:

- iterate all 10 Day Masters
- assert ngũ hành relation
- assert âm dương relation
- load `du_lieu.csv`

Polarity test `test_yin_yang_polarity_mapping` only checks Giáp/Giáp and Giáp/Ất.

**Status: FAIL (missing test), not FAIL (wrong calculator).**

---

# 4. Golden CASE status — Nguyễn Tiến Sơn

Canonical pillars:

```text
Năm   Bính Dần
Tháng Tân Sửu
Ngày  Canh Ngọ
Giờ   Mậu Dần
Nhật chủ Canh Kim
```

Runtime: `engines/ten_gods_engine/runtime/case_0001.py`  
Tests: `tests/ten_gods_engine/test_case_0001_core_integration.py`, `test_core_ten_gods.py`

## 4.1 Visible stems — PASS

| Pillar | Stem | Required | Engine |
|--------|------|----------|--------|
| Year | Bính | Thất Sát | Thất Sát |
| Month | Tân | Kiếp Tài | Kiếp Tài |
| Day | Canh | Nhật Chủ | Nhật Chủ |
| Hour | Mậu | Thiên Ấn | Thiên Ấn |

## 4.2 Hidden stems — PASS in TenGodsEngine

**Dần (year)**

| Stem | Required | Engine |
|------|----------|--------|
| Giáp | Thiên Tài | Thiên Tài |
| Bính | Thất Sát | Thất Sát |
| Mậu | Thiên Ấn | Thiên Ấn |

**Sửu (month)**

| Stem | Required | Engine |
|------|----------|--------|
| Kỷ | Chính Ấn | Chính Ấn |
| Quý | Thương Quan | Thương Quan |
| Tân | Kiếp Tài | Kiếp Tài |

**Ngọ (day)**

| Stem | Required | Engine |
|------|----------|--------|
| Đinh | Chính Quan | Chính Quan |
| Kỷ | Chính Ấn | Chính Ấn |

**Dần (hour)**

| Stem | Required | Engine |
|------|----------|--------|
| Giáp | Thiên Tài | Thiên Tài |
| Bính | Thất Sát | Thất Sát |
| Mậu | Thiên Ấn | Thiên Ấn |

Hidden count = 11. Weights match CSV.

## 4.3 Golden CASE in Portal / Report summary — visible only

The four-god string is correct **as a visible-stem summary**. It is incomplete as a full Ten Gods truth display.

---

# 5. Visible / hidden data status

| Layer | Visible Ten Gods | Hidden Ten Gods |
|-------|------------------|-----------------|
| `TenGodsResult` | 4 mapped labels + evidence | 11 mapped labels + branch + weight + evidence |
| Interpretation Foundation facts | Copied from `TenGodsResult` when engine is passed | Copied from `TenGodsResult` |
| `BaziView` / `BaziChart` | 4 labels | Stem **names** only |
| API `payload["ten_gods"]` | 4 labels | Stem **names** only |
| `ReportTenGodsV1` | 4 labels | Stem **names** only |
| Portal pillar table `thap_than` | 4 labels | Not mapped |
| Portal S06 checklist | Tokens from visible labels | Not included |
| Commercial PDF cover `ten_gods_summary` | join of 4 labels | Absent |
| Professional `sec-ten_gods` | Uses foundation visible + hidden for consultation copy | Hidden used only as location of selected roles, not as an evidence table |

**Conclusion:** Hidden Ten Gods **exist in canonical engine result**. They are **dropped or type-confused by adapters and presentation**, not missing from calculation.

---

# 6. Portal binding status

Sources:

- `applications/customer_portal/static/js/presenters/summary_builder.js`
- `applications/customer_portal/static/js/presenters/bazi.js`
- `applications/customer_portal/static/js/presenters/discussion.js`
- `applications/customer_portal/static/js/presenters/executive.js`

| Surface | Binds | Effect on CASE-0001 |
|---------|-------|---------------------|
| Pillar row Thập thần | `pillar.ten_god` or `bazi.ten_gods[i]` | Thất Sát · Kiếp Tài · Nhật Chủ · Thiên Ấn |
| Discussion chip | `bazi.ten_gods.join` | same four |
| S06 checklist `collectPresentGods` | visible pillar gods + `bazi.ten_gods` | same four; hidden gods such as Chính Quan / Thương Quan / Thiên Tài / Chính Ấn unmarked unless they also appear lộ |
| Tàng can row | `pillar.hidden_stems` stem names | Giáp, Bính, Mậu / … — **no Ten God** |
| Score ten-god bars | `score.ten_god_series` | Score, not Analytical Truth |

Portal does not read `TenGodsResult.hidden`.

S06 blueprint (`knowledge/ui_blueprints/02_SCREEN_BLUEPRINTS/S06_TEN_GODS.md`) asks for presence / prominence / missing roles **without** luck or career interpretation. Current UI cannot show hidden presence because the API compact contract does not deliver hidden Ten God labels.

---

# 7. Report / PDF / DOCX binding status

| Artifact | Binding | CASE-0001 effect |
|----------|---------|------------------|
| Report V1 adapter | `visible = bazi.ten_gods`; `hidden = bazi.hidden_stems` | Visible = 4 gods; “Ẩn can” = stem names |
| Report V1 HTML section `05. Thập thần` | prints those three fields | Summary = four visible gods |
| DOCX exporter V1 | same `build_presented_report` | same |
| Commercial PDF cover | `ten_gods_summary = join(bazi.ten_gods)` | `Thất Sát, Kiếp Tài, Nhật Chủ, Thiên Ấn` |
| Professional PDF `sec-ten_gods` | `stamp_ten_gods_consultation` from Foundation facts | Has hidden positions internally; publishes consultation prose, not a truth/evidence table |

G1-01 does not require expanding Professional consultation copy.

It does require Report/PDF/DOCX **truth presentation** to stop treating hidden stem names as hidden Ten Gods.

---

# 8. Lỗi / gap phát hiện

1. No 10×10 = 100 mapping test with element + polarity + result.
2. CSV truth table has 4 polarity/label errors vs `STEM_META` / `quy_tac.md` / algorithm.
3. Dual publication: BaZi compact list vs TenGodsEngine result; adapters prefer BaZi.
4. `payload["ten_gods"].hidden` and `ReportTenGodsV1.hidden` are stem names, not Ten Gods.
5. Portal summary / S06 / commercial cover show visible stems only, so hidden gods disappear from the synthesis line.
6. Occurrence evidence lacks element, element relation, polarity relation.
7. `relation_to_day_master` is a duplicate of the Ten God label.
8. `map_stem_to_ten_god` overlays Nhật Chủ on **any** stem equal to Day Master, including hidden; classical 100-table uses Tỷ Kiên. CASE-0001 does not hit this.
9. `engines/analysis_engine/ten_gods_engine` remains a second Ten Gods implementation (not production), risking future dual calculation.
10. Legacy `bazi_engine/ten_gods` calculator references a missing CSV.

---

# 9. Phân loại gap

| ID | Gap | Class |
|----|-----|-------|
| G-01 | Missing 100-mapping test | **contract / test** (not calculator) |
| G-02 | 4 CSV rows wrong polarity + Ten God | **calculation / data** |
| G-03 | Adapters bind BaZi compact list instead of `TenGodsResult` | **adapter** |
| G-04 | `hidden` field typed as stem names | **adapter / contract misuse** (schema already allows `list[str]` but semantics are wrong) |
| G-05 | Portal synthesis = visible only | **presentation** (blocked by G-03/G-04) |
| G-06 | Report/PDF/DOCX synthesis = visible only; Ẩn can = stems | **presentation** + **adapter** |
| G-07 | Evidence fields element / relations not published on each result | **contract** (additive; data already derivable) |
| G-08 | Hidden same-stem labeled Nhật Chủ | **calculation** (policy; not hit by golden CASE) |
| G-09 | Second Ten Gods engine in Analysis Runtime | **architecture risk** — do not wire into production |
| G-10 | `relation_to_day_master` misused | **contract** |

No gap requires a new engine.

No gap requires expanding Interpretation.

---

# 10. Minimal changes for G1-01 PASS

Phase 2 only. Do not implement until Product Owner approves.

Keep public compact `bazi.ten_gods` (4 visible labels). Do not break it.

Use existing `TenGodsResult.to_dict()` as the structured truth object.

## 10.1 Tests (required)

Add one parameterized test:

```text
10 Day Masters × 10 stems
```

For each pair assert:

1. element relation (đồng hành / nhật chủ sinh / đối tượng sinh / nhật chủ khắc / đối tượng khắc)
2. yin/yang relation (cùng / khác)
3. Ten God label from `ten_god_name`

Source of expected values: `STEM_META` + `quy_tac.md` (same rules as the calculator).

Do not hard-code CASE-0001 as the mapping matrix.

Keep CASE-0001 as a golden chart test (already present).

## 10.2 Data

Repair four rows in `database/02_quan_he/thap_than/du_lieu.csv` so polarity matches `STEM_META` and Ten God matches `quy_tac.md`.

Do not change `ten_god.py` for those four pairs unless Product Owner reverses SSOT.

## 10.3 Adapter (minimal)

In Orchestrator public payload and Report V1 adapter:

- `visible` ← TenGodsEngine visible labels (already equal to BaZi four)
- `hidden` ← TenGodsEngine hidden **Ten God labels** (or structured entries already in `to_dict()`), **not** `bazi.hidden_stems`
- `summary` ← keep visible four for backward cover line, **or** add a separate `hidden_summary` without removing `summary`

Prefer copying existing `TenGodsResult.to_dict()` under `payload["ten_gods"]` and keep `bazi.ten_gods` unchanged.

Do not invent a new schema if `visible[]` / `hidden[]` objects already carry stem, pillar, evidence.

## 10.4 Evidence (additive, no break)

On each visible/hidden occurrence, publish or derive:

| Required | Existing equivalent | Minimal action |
|----------|---------------------|----------------|
| source stem | `stem` / `hidden_stem` | keep |
| source position | `pillar` + `hidden_position` / `position_name` | keep |
| visible/hidden | `visibility` / layer | keep |
| element | from `STEM_META[stem]` | add optional field or derive in adapter |
| element relation | from GENERATES/CONTROLS vs Day Master | add optional field; stop stuffing it into `relation_to_day_master` |
| polarity relation | same/diff vs Day Master `yin_yang` | add optional field |
| Ten God result | `ten_god` | keep |

Additive keys only. Do not rename public `ten_god` / `visible` / `hidden`.

## 10.5 Presentation (after adapter)

Portal S06 / pillar evidence: mark hidden Ten Gods from engine hidden entries.

Report/PDF/DOCX section 05: print hidden **Ten Gods**, not raw stem names. Stem names stay on the pillar Ẩn can row.

Do not add personality, career, wealth, marriage, or cát/hung copy.

## 10.6 Explicit non-goals

- Do not create a new Ten Gods engine.
- Do not wire `engines/analysis_engine/ten_gods_engine` into production.
- Do not expand Interpretation / Professional consultation for this gate.
- Do not recalculate Day Master.
- Do not change Useful God, Pattern, Strength, or Luck.

---

# Suggested G1-01 pass criteria (for Phase 2)

1. 100/100 mapping test green (element + polarity + label).
2. CSV 100 rows consistent with `STEM_META` + `quy_tac.md`.
3. CASE-0001 visible and hidden Ten Gods match the tables in §4.
4. Public structured Ten Gods object exposes hidden Ten God **labels** with source stem and position.
5. Portal and Report synthesis can show hidden gods as evidence, not only `Thất Sát · Kiếp Tài · Nhật Chủ · Thiên Ấn`.
6. Each published occurrence can trace the seven evidence fields in §10.4.
7. No new engine. No interpretation expansion.

---

# STOP

Phase 1 complete.

No Engine change.
No Portal change.
No Report change.
No contract change.
No Interpretation expansion.

Await Product Owner review before Phase 2 — Repair & Validation.

---

END
