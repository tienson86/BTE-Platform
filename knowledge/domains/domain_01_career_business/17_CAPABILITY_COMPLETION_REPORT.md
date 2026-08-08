# 17 — Capability Completion Report · Career Selection Assessment

Version: 1.0  
Status: **DOMAIN 01 · SPRINT C — CAP-D1-CA-SEL COMPLETE**  
Date: 2026-08-08  
Capability: **Career Selection Assessment** (`CAP-D1-CA-SEL`)  
Depends on: Sprint A/A.5/B frozen · Wave 1.1 frozen  
Scope: Complete **one** capability only — Domain 01 CSV authoring; **no runtime**  

---

## 1. Summary

Career Selection Assessment is content-complete: when evidence supports (useful god present), the Domain 01 corpus can answer the ten consulting questions as one advisory service — not isolated fragments.

| Item | Result |
|------|--------|
| Capability | CAP-D1-CA-SEL only |
| SEL Knowledge Units | **11** (2 revised + 9 new) |
| Other capabilities authored | **None** (LE/BU P0 rows retained unchanged) |
| Wave 1.1 modified | **No** |
| Runtime / Narrative / Portal / API | **No** |
| Golden Cases (SEL) | **3/3 Accept** (offline allow-list eval) |

---

## 2. Ten questions → units

| # | Consulting question | Unit |
|---|---------------------|------|
| 1 | Career families / direction | KU-CN-CA-000001 (v1.1.0) |
| 2 | Preferred environment | KU-CN-CA-000010 |
| 3 | Preferred organizational role | KU-CN-CA-000011 |
| 4 | Leadership or specialist? | KU-CN-CA-000012 (SEL-scoped) |
| 5 | Employment or entrepreneurship? | KU-CN-CA-000013 (SEL-scoped) |
| 6 | Natural competitive advantages | KU-CN-CA-000014 (+ Wave 1.1 ST) |
| 7 | Primary career risks | KU-RK-CA-000010 |
| 8 | Mitigation | KU-MT-CA-000010 |
| 9 | Development priorities | KU-CN-CA-000015 |
| 9b | Decision timing (if supported) | KU-CN-CA-000016 |
| 10 | 90-day action plan | KU-AC-CA-000001 (v1.1.0) |

---

## 3. File update

`database/20_knowledge/22_domain01_career_business.csv`

- Wave tag for SEL pack: `W-D01-C-SEL`  
- All SEL units: `capability_id=CAP-D1-CA-SEL`  
- Unique `evidence_kind` per unit (coexist under current one-kind dedupe)  
- KU-CN-LE-000001 / KU-AC-BU-000001 left as prior P0 (other capabilities) — **not expanded**

---

## 4. Quality

| Standard | Applied |
|----------|---------|
| Golden Knowledge Standard | Yes |
| Commercial / consultant tone | Yes |
| No technical leakage | Yes (validated) |
| Risk → Mitigation pair | Yes (RK+MT) |
| No job-title / income guarantees | Yes |
| Traceability columns | Yes |

---

## 5. Production caveat

Default Adapter still loads Wave 1.1 allow-list + `21_*.csv` only.  
SEL is **production-ready as content**; live integration still needs Product-approved wiring (see `19`).

---

## 6. Stop line

Capability complete for Product Review.  
**Do not start Promotion Readiness.**

---

END
