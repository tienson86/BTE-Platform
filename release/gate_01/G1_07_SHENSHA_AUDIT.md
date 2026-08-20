# G1-07 — Thần sát / ShenSha Truth & Evidence Audit

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-07 |
| **Document** | `release/gate_01/G1_07_SHENSHA_AUDIT.md` |
| **Phase** | 1 — Audit only |
| **Date** | 2026-08-20 |
| **Status** | AUDIT PASS / G1-07 NOT READY — REPAIR REQUIRED |
| **Scope** | Production ShenSha detection, maps, CASE-0001, Portal/Report binding |
| **Out of scope** | Engine repair; rule merge; Calendar/BaZi/Ten Gods/Strength/Temperature/Pattern/Useful God; Deep ShenSha interpretation |

Live CASE-0001 was executed read-only through:

```text
CalendarEngine → BaziEngine.build
  → ShenShaService.calculate
  → BaziChart.shensha (list[str])
  → build_bazi_view → data.bazi.shensha
  → ReportInputV1Adapter._build_shensha
  → Portal adapters (copy names)
```

No Engine, CSV, or adapter was modified for this audit.

---

# Verdict

| # | Question | Answer |
|---|----------|--------|
| 1 | Production ShenSha Engine? | **`engines.bazi_engine.shensha.service.ShenShaService`**, called from **`BaziEngine.build`**. Not `analysis_engine.shensha_engine`. Not CSV `08_than_sat`. |
| 2 | Canonical rule database? | **Hardcoded maps** in `engines/rule_contract/signal_maps.py`. Production **loads zero ShenSha CSV**. |
| 3 | How is each star determined? | `if` lookup: Day Stem / Year Branch / Day Branch / Month Branch → target in visible stems/branches. |
| 4 | Source pillars? | Nhật can, Niên chi, Nhật chi, Nguyệt chi. **Not** Niên can. **Not** Tàng can. |
| 5 | Target? | Visible **Địa chi** (most stars) or visible **Thiên can or Địa chi** (Thiên Đức) or visible **Thiên can** (Nguyệt Đức). |
| 6 | Position stored? | **No.** Match is boolean over the four pillars; result is a **name string**. |
| 7 | Multiple pillars? | Collapsed to **one name** via `dict.fromkeys`. Positions discarded. |
| 8 | Alias? | Production **appends both names** for four pairs. Narrative later maps aliases; Portal/Report **do not**. |
| 9 | Duplicate logical stars? | **Yes on CASE-0001:** four alias pairs published as eight independent items. Hồng Loan / Thiên Hỷ also share **one formula** that does not match the unused Thiên Hỷ table. |
| 10 | CASE-0001 list? | Thiên Ất Quý Nhân, Thiên Ất, Hồng Loan, Thiên Hỷ, Thiên Đức, Thiên Đức Quý Nhân, Nguyệt Đức, Nguyệt Đức Quý Nhân |
| 11 | Same across surfaces? | **Names yes** (API = Report = Portal copy of `bazi.shensha`). Evidence/positions **nowhere**. |
| 12 | Renderer drops evidence? | Production never stores evidence. Report `evidence = name`. Portal S07 lists names and **invents Cát/Hung buckets**. |

---

# PHASE 1 STATUS

**G1-07 PHASE 1: AUDIT PASS / G1-07 NOT READY — REPAIR REQUIRED**

Do not start repair in this phase. Product Owner must choose alias Option A vs B for the three Quý Nhân pairs. Hồng Loan vs Thiên Hỷ is **not** a clean alias question: production uses one formula; unused CSV has two.

---

## 1. Canonical production implementation

**Canonical module:** `engines/bazi_engine/shensha/service.py`

| Piece | Path | Production? |
|-------|------|-------------|
| Public entry | `BaziEngine.build` → `ShenShaService.calculate` | **yes** |
| Context | Pillar stems/branches passed as arguments (no `ShenShaContext` type) | **yes** |
| Rule loader | none on this path | no |
| Registry | `SHEN_SHA_KEYS` in interpretation `entity_types.py` (closed name list) | downstream only |
| Matcher | inline `if` in `ShenShaService` + duplicate copy in `RuleContextBuilder._detect_shensha_stars` | **yes** / fallback |
| Maps | `engines/rule_contract/signal_maps.py` | **yes** |
| Output | `list[str]` on `BaziChart.shensha` | **yes** |
| Evidence model | **absent** | — |
| Version | no engine version string; maps unlabeled | — |

Production call:

```text
pillars + day_master
  → ShenShaService.calculate(day_master, year/month/day/hour branches, stems, branches)
  → list[str] unique by name
  → build_bazi_view copies chart.shensha
  → data.bazi.shensha
```

### Other implementations

| Implementation | Class | Role |
|----------------|-------|------|
| `ShenShaService` | **canonical production** | Orchestrator / Report / Portal |
| `RuleContextBuilder._detect_shensha_stars` | **helper / fallback** | Same maps; used only if `bazi.shensha` missing |
| `engines/bazi_engine/shensha/calculator.py` + `rule_loader.py` | **legacy / unused** | Expects `database/08_than_sat/*.csv` — **folder does not exist** |
| `engines/analysis_engine/shensha_engine` | **unused** on Orchestrator | Knowledge-session analyzer; has IDs/presence; **not** `data.bazi.shensha` |
| `engines/analysis_engine/analyzers/shensha` | **unused** | Older analyzer package |
| `database/05_phan_tich/07_than_sat/` | **unused** by production | 20 catalog rows + lookup CSVs |
| `database/15_score_engine/07_shensha/` | **Score Engine** | Quality scoring, not natal detection |
| `database/01_du_lieu_goc/09_calendar/06_jdn_can_chi_ngay.csv` | **Calendar** | Has `khong_vong` per sexagenary day; **not read by ShenShaService** |
| Interpretation `build_shensha_facts` | **copy-only** | Copies names; evidence usually empty |
| Narrative `SHENSHA_CANONICAL_OVER_ALIAS` | **presentation helper** | Dedups aliases for narrative only |
| Portal S07 / Report §08 | **presentation-only** | Copy names; S07 adds Cát/Hung |

---

## 2. Rule inventory

Production **does not load** ShenSha CSV.

| Category | On disk | Loaded by production | Reachable | Disabled | Invalid |
|----------|--------:|---------------------:|----------:|---------:|--------:|
| Hardcoded detectors in `ShenShaService` | 8 branches | 8 | 8 | 0 | 0 |
| Display names those detectors can emit | 12 | 12 | 12 | 0 | 0 |
| `database/08_than_sat/*.csv` | **0** (path missing) | 0 | 0 | — | loader would fail if used |
| `05_phan_tich/07_than_sat/01_than_sat.csv` | 20 entities | 0 | 0 | — | unused |
| `02_rule_kich_hoat.csv` | 20 rows | 0 | 0 | 4 PENDING | unused |
| Lookup CSVs in that folder | 16 files | 0 | 0 | 4 rules point at missing files | unused |
| Score `15_score_engine/07_shensha` | present | Score only | n/a | — | not natal detection |

**Canonical production ShenSha count:** 12 **display names**, 8 **detectors**.

One detector can emit **two names** (alias double-append). There are **no CSV rule IDs** on the production path. Identity is the **display string**.

Duplicate rule IDs: n/a (no loaded CSV). Duplicate names: four intentional alias pairs. Fallback: `RuleContextBuilder._detect_shensha_stars` if chart list empty (same maps).

---

## 3. Canonical identity model

Production identity = **display label** (`"Thiên Ất Quý Nhân"`).

There is **no** ShenSha ID, **no** rule ID, **no** normalized key on `BaziChart.shensha`.

Report synthesizes `id = shensha_{n}` by list order.

Interpretation closed list `SHEN_SHA_KEYS` matches the 12 production names.

| Pair | Production | Case |
|------|------------|------|
| Thiên Ất vs Thiên Ất Quý Nhân | Same detector `TIAN_YI_BRANCHES`; both appended | **B** same formula / alias candidate (published as two entities) |
| Thiên Đức vs Thiên Đức Quý Nhân | Same `TIAN_DE_BRANCH` check; both appended | **B** |
| Nguyệt Đức vs Nguyệt Đức Quý Nhân | Same `YUE_DE_STEM` check; both appended | **B** |
| Hồng Loan vs Thiên Hỷ | Same `HONG_LUAN_OPPOSITE` check; both appended | **Not clean B.** Unused CSV has **different** Thiên Hỷ targets. Narrative treats Thiên Hỷ as alias of Hồng Loan. |

Do not merge in Phase 1. Product Owner must choose Option A vs B for the three Quý Nhân pairs. Hồng Loan / Thiên Hỷ needs a formula decision, not only a label decision.

---

## 4. Alias / duplicate candidates

| ID A (detector) | Name A | ID B | Name B | Same formula in production? | Candidate alias? |
|-----------------|--------|------|--------|----------------------------:|------------------|
| `tian_yi` | Thiên Ất Quý Nhân | `tian_yi` | Thiên Ất | **yes** | **yes — Option A/B** |
| `tian_de` | Thiên Đức | `tian_de` | Thiên Đức Quý Nhân | **yes** | **yes — Option A/B** |
| `yue_de` | Nguyệt Đức | `yue_de` | Nguyệt Đức Quý Nhân | **yes** | **yes — Option A/B** |
| `hong_luan` | Hồng Loan | `tian_xi` (same `if`) | Thiên Hỷ | **yes in code** | **No as classical alias.** Unused `bang_thien_hy.csv` ≠ Hồng Loan table. Production false-publishes Thiên Hỷ whenever Hồng Loan hits. |
| `wen_chang` | Văn Xương | Score map Văn Khúc | Văn Khúc | Score approximates Văn Khúc → Văn Xương | Score-only; not natal emit |

Unicode / case / whitespace variants: not observed in production maps (fixed Vietnamese strings).

---

## 5. Source types (production)

| Detector | Source | Target test |
|----------|--------|-------------|
| Thiên Ất / Thiên Ất Quý Nhân | **Nhật can** | any of 4 **Địa chi** in noble pair |
| Văn Xương | Nhật can | that **Địa chi** present |
| Lộc Thần | Nhật can | that **Địa chi** present |
| Dương Nhẫn | Nhật can (yang stems only) | that **Địa chi** present |
| Hồng Loan / Thiên Hỷ | **Niên chi** | mapped **Địa chi** present |
| Hoa Cái | **Nhật chi** | day branch ∈ {Thìn, Tuất, Sửu, Mùi} |
| Thiên Đức / Thiên Đức Quý Nhân | **Nguyệt chi** | mapped token in **stems or branches** |
| Nguyệt Đức / Nguyệt Đức Quý Nhân | **Nguyệt chi** | mapped **stem** in visible stems |

Not used: Niên can, Nguyệt can, giờ as source (hour is only a **search location**), Tàng can, Thập thần, ngũ hành.

---

## 6. Match target

| Kind | Used? |
|------|------:|
| Visible earthly branches | **yes** (primary) |
| Visible heavenly stems | **yes** (Thiên Đức token; Nguyệt Đức stem) |
| Pillar object | no (flattened lists) |
| Hidden stems | **no** |
| Combination / tam hợp | **no** in production (unused CSV Hoa Cái/Đào Hoa/Dịch Mã use tam hợp) |
| Element / Ten God | no |

Renderer does not recompute targets. It also **cannot show** targets because they were never stored.

---

## 7. Position / pillar provenance

`ShenShaService` answers only: **is the name present?**

It cannot answer “ở trụ nào?” without re-running the lookup in the auditor’s head.

Not stored: year/month/day/hour, stem vs branch, matched character, source character.

Report `ReportShenShaItemV1.evidence` is set to **the name**. Interpretation items have empty `position` / `rule_id` and `evidence_status = UNAVAILABLE`.

---

## 8. Multiple-occurrence behavior

Exact code: `return list(dict.fromkeys(stars))`.

- Two pillars with the same target → **one name**.
- That is **not** two logical ShenSha; it is **lost multi-position evidence**.
- Alias double-append is the opposite problem: **one match → two names**.

CASE-0001 does not exercise two-position (Thiên Ất target Sửu only at **month**). The contract still cannot represent Year+Hour of the same star.

---

## 9. CASE-0001 full trace

Chart: **Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần**. Nhật Chủ **Canh**. Stems `Bính, Tân, Canh, Mậu`. Branches `Dần, Sửu, Ngọ, Dần`.

Production list (API = chart = Report):

1. Thiên Ất Quý Nhân  
2. Thiên Ất  
3. Hồng Loan  
4. Thiên Hỷ  
5. Thiên Đức  
6. Thiên Đức Quý Nhân  
7. Nguyệt Đức  
8. Nguyệt Đức Quý Nhân  

Not emitted: Văn Xương (need Hợi), Lộc Thần (need Thân), Dương Nhẫn (need Dậu), Hoa Cái (day Ngọ not earth-storage).

| ShenSha | Detector / “rule” | Source | Source value | Target | Matched position (reconstructed; **not stored**) | Result |
|---------|-------------------|--------|--------------|--------|--------------------------------------------------|--------|
| Thiên Ất Quý Nhân | `TIAN_YI_BRANCHES` | Nhật can | Canh | Sửu, Mùi | **Tháng chi Sửu** | published |
| Thiên Ất | same | Nhật can | Canh | Sửu, Mùi | **Tháng chi Sửu** | published (alias) |
| Hồng Loan | `HONG_LUAN_OPPOSITE` | Niên chi | Dần | Sửu | **Tháng chi Sửu** | published |
| Thiên Hỷ | **same `if` as Hồng Loan** | Niên chi | Dần | Sửu (wrong vs unused table Mùi) | **Tháng chi Sửu** | published |
| Thiên Đức | `TIAN_DE_BRANCH` | Nguyệt chi | Sửu | Canh | **Ngày can Canh** | published |
| Thiên Đức Quý Nhân | same | Nguyệt chi | Sửu | Canh | **Ngày can Canh** | published (alias) |
| Nguyệt Đức | `YUE_DE_STEM` | Nguyệt chi | Sửu | Canh | **Ngày can Canh** | published |
| Nguyệt Đức Quý Nhân | same | Nguyệt chi | Sửu | Canh | **Ngày can Canh** | published (alias) |

Unused CSV Thiên Hỷ for Dần → **Mùi**. Chart has no Mùi. A table-correct Thiên Hỷ would be **absent**. Production still prints Thiên Hỷ because Hồng Loan matched.

---

## 10. Item-by-item (visible CASE-0001 set)

### Thiên Ất Quý Nhân

1. Rule: hardcoded `TIAN_YI_BRANCHES["Canh"] = (Sửu, Mùi)` (甲戊庚牛羊).  
2. Identity: display name.  
3. Source: Nhật can Canh.  
4. Target: Sửu (present), Mùi (absent).  
5. Match: month branch Sửu.  
6. Pillar: month (not stored).  
7. Alias: pair with Thiên Ất.

Unused `bang_thien_at.csv` **Canh → Dần-Ngọ** (looks like 六辛 swapped onto Canh). Production does **not** use that row. CASE-0001 would still match Dần/Ngọ on that unused table (year/hour Dần, day Ngọ) — **different evidence**, same “present” bit. Do not treat unused CSV as production truth.

Production omits **Tân** from Thiên Ất (六辛逢马虎 missing). Not CASE-0001.

### Thiên Ất

Same formula, second published name. **ALIAS/DUPLICATE CANDIDATE.**

### Hồng Loan

Year Dần → Sửu. Matches unused `bang_hong_loan.csv` HL003. Present at month Sửu.

### Thiên Hỷ

Published from Hồng Loan `if`, not from `bang_thien_hy.csv` (Dần → Mùi). **False companion of Hồng Loan on CASE-0001.**

### Thiên Đức / Thiên Đức Quý Nhân

Month Sửu → Canh; Canh is day stem. Same formula, two names. Unused RKH016 is PENDING / missing lookup / wrongly labeled Nhật Chủ. Production month-branch Thiên Đức is the live formula.

### Nguyệt Đức / Nguyệt Đức Quý Nhân

Month Sửu → Canh stem; day stem Canh. Same formula, two names. Unused RKH017 PENDING.

---

## 11. Thiên Ất audit

| | Production | Unused CSV |
|--|------------|------------|
| Formula | Day stem → 2 noble branches; any of 4 branches | Same idea, **different Canh/Tân rows** |
| Source | Nhật can only (not niên can) | `Nhat_Chu` |
| Canh | Sửu, Mùi | Dần, Ngọ |
| Tân | **missing** | Dần, Ngọ |
| Output | two strings | unused |
| IDs | none | TA001–TA010 unused |

**ALIAS/DUPLICATE CANDIDATE** for the two published names. Formula itself is a standard 甲戊庚牛羊 table.

---

## 12. Thiên Đức audit

Production: **month branch → token**; token may be a stem **or** a branch (`TIAN_DE_BRANCH`). CASE-0001 Sửu → Canh, hit on day stem.

Thiên Đức vs Thiên Đức Quý Nhân: **identical match**. No separate evidence. **Option A/B.**

Do not assume they are the same only because names are close — in *this* engine they are the same **because the code appends both after one check**.

---

## 13. Nguyệt Đức audit

Production: **month branch → stem only** (`YUE_DE_STEM`). CASE-0001 Sửu → Canh.

Pair is same-check double publish. **Option A/B.**

---

## 14. Hồng Loan / Thiên Hỷ

| | Hồng Loan | Thiên Hỷ (classical / unused CSV) | Production |
|--|-----------|-----------------------------------|------------|
| Source | Niên chi | Niên chi | Niên chi |
| Dần → | Sửu | **Mùi** | Sửu for **both names** |
| CASE-0001 | hit month Sửu | would **miss** (no Mùi) | both published |

G1-07 fact only: **Có Hồng Loan** because niên chi Dần → Sửu at tháng. **Thiên Hỷ is published without a distinct hit.** No marriage reading.

---

## 15. Other important ShenSha

| Name | Production? | CASE-0001 | Notes |
|------|-------------|-----------|-------|
| Văn Xương | yes | no (need Hợi) | map matches unused `bang_van_xuong.csv` |
| Lộc Thần | yes | no (need Thân) | matches unused `bang_loc_than.csv` |
| Dương Nhẫn | yes (yang DM only) | no (need Dậu) | |
| Hoa Cái | yes | no | **Formula ≠ unused tam hợp table** (see §17) |
| Đào Hoa | no | — | unused CSV: Dần-Ngọ-Tuất → Mão (absent) |
| Dịch Mã | no | — | unused: → Thân (absent) |
| Quốc Ấn | no | — | unused Canh → Thìn (absent) |
| Học Đường | no | — | |
| Kim Dư | no | — | |
| Không Vong | **no natal emit** | — | Calendar CSV has tuần không; Score has a star; ShenShaService ignores |
| Cô Thần | no | — | unused year Dần group → Tỵ (absent) |
| Quả Tú | no | — | unused lookup |
| Tướng Tinh | no | — | |
| Kiếp Sát / Bạch Hổ / Hàm Trì / Thiên Khốc / Thiên Hư | no | — | unused lookups |
| Văn Khúc | no natal | — | Score aliases to Văn Xương |

Coverage is a **closed 8-detector / 12-name** catalog, not the 20-row analysis CSV.

---

## 16. Không Vong

- **ShenShaService:** does not compute Không Vong. Not a CASE-0001 published star.  
- **Calendar canonical table:** `database/01_du_lieu_goc/09_calendar/06_jdn_can_chi_ngay.csv` column `khong_vong`. Canh Ngọ = tuần Giáp Tý → **Tuất-Hợi**. Chart branches are Dần/Sửu/Ngọ/Dần — **no empty branch on the four chi** even if natal Không Vong were applied.  
- **CalendarEngine Python:** no `khong_vong` consumer found.  
- BLOCKER 8 (wrong sexagenary formula) is **not triggered** because production does not emit Không Vong. Gap: natal star not wired; Calendar table exists unused.

---

## 17. Hidden-stem matching

Production searches **visible** `stems` and `branches` only. Hidden stems of Sửu (Kỷ, Quý, Tân) are **not** used.

**Semantic risk is the opposite of hidden over-match:** unused Hoa Cái is tam hợp (Dần-Ngọ-Tuất → Tuất); production Hoa Cái is “day branch is a storage chi”. CASE-0001 both miss. Other charts can diverge.

---

## 18. Source priority

Detectors are independent `if`s. Results are a **union of names**, insertion order fixed by source code.

- Thiên Ất does **not** also use niên can.  
- Hồng Loan does **not** also use nhật chi as source.  
- No Day-vs-Year overwrite.  
- Alias pairs are not two evidence records; they are two strings from one `if`.

Deterministic: same pillars → same `list[str]`.

---

## 19. ShenShaResult contract (production)

There is **no** `ShenShaResult` on the Orchestrator path.

Stored:

| Field | Present? |
|-------|----------|
| canonical ID | no (`shensha_1` only in Report) |
| name | **yes** |
| rule ID | no |
| source type / character | no |
| target character | no |
| pillar / location | no |
| alias flag | no |
| evidence | no (Report copies name) |

Rich models exist on **unused** `bazi_engine.shensha.shensha.ShenShaResult` / analysis-engine `ShenShaPresence`. Not bound.

---

## 20. Portal / Report / PDF / DOCX binding

```text
data.bazi.shensha: list[str]
  → Canonical Desktop mapS07: names → Cát vs Hung via hardcoded HUNG_SHENSHA set
  → baziResultAdapter mapShenSha: names only (tone Trung, note = name)
  → fullReportViewModel: bullet names
  → ReportShenShaItemV1: name + evidence=name + present=true
  → HTML/PDF/DOCX section 08: Tên / Loại / Hiện diện / Bằng chứng(=tên)
```

| Surface | Names | Positions | Dedup | Recalc? |
|---------|------:|----------:|-------|---------|
| API | 8 | no | name `dict.fromkeys` in engine | no |
| Report / PDF / DOCX | same 8 | no | none extra | no |
| Portal S07 | same 8, split Cát/Hung | no | none extra | **no stars**; **yes polarity** |
| Narrative | may collapse aliases via `SHENSHA_CANONICAL_OVER_ALIAS` (maps Thiên Hỷ → Hồng Loan) | no | alias collapse | no |

Portal does **not** invent extra star names. It **does** invent Cát/Hung (CASE-0001 all eight go to Cát because none match the hung set).

API list equals Report names (live check).

---

## 21. Test coverage vs required matrix

| Case | Covered on production path? |
|------|----------------------------|
| Day-stem star | only trivial `tests/bazi/test_shensha.py` (type/len) |
| Year-branch / day-branch / month | no dedicated G1 tests |
| Multiple occurrences | **no** |
| Alias double publish | **no assert** (golden currently **locks 8 names**) |
| No-match | weak |
| Duplicate rule | n/a |
| Không Vong natal | **no** |
| Same target Year+Hour | **no** |
| Day vs Year collision | **no** |
| `analysis_engine.shensha_engine` tests | **other engine**, not production |

Golden CASE-0001 ReportInput currently expects the eight names. That snapshot **freezes the alias double-publish**.

---

## 22. Alias / duplicate candidates (summary)

Must not `set(name)` as a universal fix.

| Kind | CASE-0001 |
|------|-----------|
| Duplicate logical entity (alias pair) | Thiên Ất ×2, Thiên Đức ×2, Nguyệt Đức ×2 |
| Multiple occurrence | none stored; Thiên Ất/Hồng Loan only **month Sửu** |
| Separate rules, similar names | Hồng Loan vs Thiên Hỷ **should be** this; production treats as one `if` |
| Name dedup losing positions | contract yes; this chart no second pillar |

---

## 23. Blockers

| # | Condition | Status |
|---|-----------|--------|
| 1 | CASE-0001 star not traceable to a rule | **Partial.** Traceable to `signal_maps` constants, **not** to a rule ID/CSV. |
| 2 | Portal recalculates ShenSha | **No** for names. Polarity Cát/Hung is renderer-invented. |
| 3 | Same logical star twice via alias | **YES** (four pairs) |
| 4 | Multi-position lost to name dedup | **Contract YES** (not exercised by CASE-0001) |
| 5 | Thiên Ất / Thiên Ất Quý Nhân same formula, two entities | **YES** |
| 6 | Thiên Đức aliases double publish | **YES** |
| 7 | Nguyệt Đức aliases double publish | **YES** |
| 8 | Không Vong contradicts Calendar | **N/A** (not emitted). Calendar table unused. |
| 9 | Wrong source pillar | Hồng Loan source OK. **Thiên Hỷ target/table wrong.** Hoa Cái source/formula ≠ unused tam hợp. |
| 10 | Hidden stems matched against intent | **No** (not matched) |
| 11 | API ≠ Report list | **No** (same 8 names) |
| 12 | Nondeterministic | **No** |
| 13 | Published star has no evidence | **YES** (name-only; Report evidence = name) |
| 14 | Legacy override of canonical | **No** (legacy calculator unused) |

---

## 24. Gap classification

| Gap | Type |
|-----|------|
| Identity is display string; no ShenSha ID / rule ID | identity / contract |
| Alias pairs double-published | alias |
| Hồng Loan `if` also emits Thiên Hỷ | calculation |
| No positions / source / target on result | provenance / contract |
| Name `dict.fromkeys` drops multi-pillar | provenance |
| Hardcoded maps, CSV unused / `08_than_sat` missing | rule |
| Hoa Cái production ≠ tam hợp lookup | calculation |
| Tân missing from Thiên Ất | rule / coverage |
| Không Vong not natal-wired despite Calendar column | coverage |
| Portal Cát/Hung hardcoded | presentation |
| Report evidence = name | adapter / presentation |
| Golden snapshot locks 8 alias names | test |
| Production tests almost empty | test |
| Deep cát/hung/hôn nhân interpretation | out of V1.0 (do not add) |

---

## 25. Minimum changes required for G1-07 PASS

Do **not** implement in Phase 1.

1. **Identity:** one canonical ID per logical star; display name + alias list.  
2. **Product Owner Option A or B** for Thiên Ất, Thiên Đức, Nguyệt Đức pairs. If A: one published entity, aliases for compatibility, **stop appending twice**.  
3. **Hồng Loan vs Thiên Hỷ:** separate formulas (unused `bang_thien_hy` / 六冲 of Hồng Loan). Do not treat as Quý Nhân-style alias until formula is fixed. CASE-0001 would then show Hồng Loan **without** Thiên Hỷ.  
4. **Evidence:** store source type, source character, target, pillar slot(s) `positions[]`. One logical star + two pillars ≠ two stars.  
5. **Contract:** replace bare `list[str]` as canonical (keep wrapper for compatibility). Report/Portal **copy** evidence; do not derive Can/Chi; do not invent Cát/Hung.  
6. **Maps:** give detectors stable rule IDs; freeze or load from database — production currently ignores `05_phan_tich/07_than_sat`.  
7. **Tests:** CASE-0001 trace; alias; multi-position; Thiên Hỷ miss on Dần without Mùi; no hidden-stem match; API = Report.  
8. **Không Vong:** either bind Calendar sexagenary `khong_vong` or explicitly out-of-scope V1.0 — do not invent a third table.

Minimum V1.0 presentation (proposal only):

```text
Thiên Ất Quý Nhân
Có · tại trụ Tháng
Căn cứ: Nhật can Canh → gặp Sửu
```

No tốt/xấu, nghề, hôn nhân, tài vận, lời khuyên.

---

# PRODUCT OWNER DECISIONS REQUIRED

If audit is accepted that these pairs share one production formula:

- Thiên Ất / Thiên Ất Quý Nhân  
- Thiên Đức / Thiên Đức Quý Nhân  
- Nguyệt Đức / Nguyệt Đức Quý Nhân  

**Do not delete rules in Phase 1.** Choose:

### Option A
One canonical ShenSha; keep the other string as alias for compatibility.

### Option B
Keep two display entities only if a **distinct** formula/evidence is introduced. Today they do not have distinct evidence.

**Hồng Loan / Thiên Hỷ:** not the same decision. Production currently **mis-publishes** Thiên Hỷ. Multiple-position (same star, two trụ) is evidence, not a Product question to drop duplicates.

---

**G1-07 PHASE 1: AUDIT PASS / G1-07 NOT READY — REPAIR REQUIRED**

STOP. No engine, rule, Calendar, BaZi, Ten Gods, Strength, Temperature, Pattern, Useful God, Portal, or Report edits. No Deep ShenSha interpretation. Wait for Product Owner review before Phase 2.
