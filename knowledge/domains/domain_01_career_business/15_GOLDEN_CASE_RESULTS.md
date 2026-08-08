# 15 — Golden Case Results · Domain 01 P0

Version: 1.0  
Status: **DOMAIN 01 · SPRINT B VALIDATION**  
Date: 2026-08-08  
Method: Offline merged corpus (Wave 1.1 + Domain 01 P0) via RetrievalService allow-list — **eval only**  
Cases: D1-GC-STRONG-EMP · WEAK-EMP · MIXED-EMP · INDEPENDENT · STRONG-MGR  

---

## 1. Suite verdict

| Check | Result |
|-------|--------|
| Cases run | **5 / 5** P0-first Golden profiles |
| Domain P0 units selectable | **4 / 4** on every profile with useful god |
| Technical token leak | **None** (`vuong`/`nhuoc`) |
| Career Rec specialization | **Yes** (KU-AC-CA-000001 replaces generic KU-RC action when both eligible) |
| Leadership / business posture present | **Yes** (section/bundle evidence) |
| Wave 1.1 structural spine retained | **Yes** (ID / ST|WK / UG) |

---

## 2. Before → After (STRONG-EMP)

| Surface | Wave 1.1 only | Wave 1.1 + Domain 01 P0 |
|---------|---------------|-------------------------|
| Selected | ID, RC, UG, ST | ID, ST, UG, **CN-CA, AC-CA, CN-LE, AC-BU** (RC displaced by career action) |
| Recommendation | Generic giữ mực → nuôi Dụng thần | **Hành động nghề nghiệp** — việc cụ thể / kỹ năng / trách nhiệm gắn Dụng thần |
| Career direction | Absent | Present (`Về công việc:…`) |
| Leadership light | Absent | Present |
| Business posture | Absent | Present (employment vs independent) |

---

## 3. Per-case notes

| Case | Domain units | Exec / Rec / Decision Support | Commercial usefulness |
|------|--------------|-------------------------------|------------------------|
| D1-GC-STRONG-EMP | All 4 | Career next step clear; direction + leadership color | **Lift** vs generic RC |
| D1-GC-WEAK-EMP | All 4 | Career action leads with giữ mực if thin/overloaded; WK retained | **Lift** with caution |
| D1-GC-MIXED-EMP | All 4 | ST+WK+career direction; avoid kỵ via UG frame | **Lift** |
| D1-GC-INDEPENDENT | All 4 | Business posture + career action both available | **Lift** for Q-03/Q-06 |
| D1-GC-STRONG-MGR | All 4 | Leadership style light + career action | **Partial** (manager-vs-IC is P1) |

---

## 4. Surface evaluation summary

| Surface | Finding |
|---------|---------|
| Executive Summary | Structural identity/strength unchanged quality; career/leadership added via commercial sections |
| Recommendation | Materially more career-specific |
| Decision Support | SEL/DEV/ENP-light postures present; CHG/PRO deep decisions still P1 |
| Commercial usefulness | First domain differentiation beyond Wave 1.1 core |

---

## 5. Production caveat

These results assume Domain 01 ids are allow-listed and `22_domain01_career_business.csv` is loaded.  
**Default production Adapter does not yet load Domain 01** (sprint forbid runtime change). See `16`.

---

## 6. Stop line

Validation recorded for Product Review.

---

END
