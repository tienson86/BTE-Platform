# 07 — Golden Case Comparison (Before → After P0)

Version: 1.0  
Status: **EPIC 7 · SPRINT B**  
Date: 2026-08-08  
Method: 12 Golden Case profiles · `scenario_id=default` · Wave 1.1 Adapter on  
Before baseline: EPIC 6 Sprint A evaluation (`knowledge/real_case_validation/03`)  

---

## 1. Suite result

| Metric | Before (EPIC 6) | After (Sprint B) |
|--------|-----------------|------------------|
| Cases run | 5 structural + coverage notes | **12 / 12** |
| Technical band tokens (`vuong`/`nhuoc`) | Present | **None observed** |
| Enemy label duplication (`Hỏa; Hỏa`) | Present | **None** |
| Mixed “mỏng” on strong+enemy | Present | **Fixed (Frame B)** |
| Mitigation-first recommendation | Trailing clause only | **Leads Action** when Rec present |
| Unit count | 5 | **5** (unchanged) |

---

## 2. Structural cases

### GC-STRONG-FOLLOW

| Surface | Before | After |
|---------|--------|-------|
| Identity | Consultant OK but `thân vuong` | `Ở mức thân được nâng đỡ` |
| Strength | Embedded band token | Strength-only beat; commercial label |
| Weakness | Insufficient (correct) | Insufficient (correct) |
| Rec | Expand-first UG | **Giữ mực trước → nuôi Dụng thần Thủy** |

### GC-WEAK-ENEMY

| Surface | Before | After |
|---------|--------|-------|
| Weakness | `Hỏa; Hỏa; mức thân nhuoc` + duplicate para risk | Unique `Hỏa; thân đang mỏng lực` + full arc in bundle |
| Rec | Expand UG; reduce-load trailing | **Mitigation-first** then Mộc |
| Frame | Always “mỏng” template | Frame A appropriate |

### GC-FOLLOW-PATTERN

| Before | After |
|--------|-------|
| Treated like strong core | Same core quality; still no follow-specific KU (expected) |
| Tokens possible | Commercial labels clean |

### GC-SPECIAL-PATTERN

| Before | After |
|--------|-------|
| `thân can` leakage | `đang cân bằng` |
| No special-pattern counsel | Unchanged gap (P1) — no regression |

### GC-MIXED

| Before | After |
|--------|-------|
| WK said cấu trúc mỏng while thân vượng | **Frame B:** “không phải vì bạn thiếu nền… phần dễ kéo lệch: Thủy” |
| `Thủy; Thủy` | Single `Thủy` |
| ST + WK tension | Consistent strength + opposed caution |

---

## 3. Intent cases (core only — no domain KU)

Evaluated on **default** Result path (Wave 1.1 scenarios include `default`).

| Case | After core quality | Domain advice |
|------|--------------------|---------------|
| GC-BUSINESS | ID/ST/UG/RC OK; mitigation-first | **Missing** business pack (P1/P2) |
| GC-CAREER | Same | **Missing** career pack |
| GC-MARRIAGE | ID/ST/WK/UG/RC; Frame B on Kim | **Missing** relationship pack |
| GC-HEALTH | ID/WK/UG/RC; Frame A | **Missing** health lifestyle pack (ethics intact) |
| GC-WEALTH | ID/ST/UG/RC OK | **Missing** wealth pack |

No regression: system does **not** invent domain claims.

---

## 4. Control cases

| Case | Before | After |
|------|--------|-------|
| GC-NO-USEFUL-GOD | ID+ST; Rec insufficient | Same honest thin Rec; labels clean |
| GC-THIN-EVIDENCE | Thin / empty commercial | Bundle empty (day master alone without pattern/strength) — honest |

---

## 5. Surface checklist (12/12)

| Surface | Pass intent after P0 |
|---------|----------------------|
| Executive Summary | Improved labels, rhythm of ID vs ST in **bundle**; summary still may merge beats (see `08`) |
| Recommendation | Mitigation-first + next step clearer |
| Warning / Weakness | Arc present in WK bundle; summary may still double-print (Narrative aggregation) |
| Narrative | Pack 05 bodies still often empty (P1) |
| Commercial Quality | Core structural consulting **Good**; domain intents still **Needs Improvement** by coverage |

---

## 6. Regressions

| Item | Severity | Notes |
|------|----------|-------|
| Mitigation-first on pure strong charts | Minor | Slightly heavier prepare tone; acceptable for P0 ethics |
| Summary weakness paragraph doubled | Known | Bundle text once; summary aggregation duplicates — **not introduced by KU**, still open |
| Identity+strength merged in summary.identity | Known | Composition; ST bundle text itself no longer reopens identity |

No accuracy/ethics regressions observed on the 12-case set.

---

## 7. Stop line

Comparison complete. Remaining gaps → `08`.

---

END
