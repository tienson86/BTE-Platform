# 18 — Acceptance Test Results · Career Selection Assessment

Version: 1.0  
Status: **PASS (offline corpus evaluation)**  
Date: 2026-08-08  
Capability: CAP-D1-CA-SEL  
Method: Merged Wave 1.1 + Domain 01 CSV · Retrieval allow-list includes SEL ids · **no production runtime change**  

---

## 1. Cases run

| Case | Profile | Result |
|------|---------|--------|
| D1-GC-STRONG-EMP | Strong + UG | **PASS** · 11/11 SEL units |
| D1-GC-WEAK-EMP | Weak + enemy + UG | **PASS** · 11/11 SEL units |
| D1-GC-MIXED-EMP | Strong + enemy + UG | **PASS** · 11/11 SEL units |

---

## 2. Acceptance checklist (all cases)

| Criterion | Strong | Weak | Mixed |
|-----------|:------:|:----:|:-----:|
| Career direction clear | ✓ | ✓ | ✓ |
| Environment recommended | ✓ | ✓ | ✓ |
| Role recommended | ✓ | ✓ | ✓ |
| Leadership posture explained | ✓ | ✓ | ✓ |
| Employment/Business posture explained | ✓ | ✓ | ✓ |
| Strengths explained | ✓ | ✓ | ✓ |
| Risks explained | ✓ | ✓ | ✓ |
| Mitigation included | ✓ | ✓ | ✓ |
| Development plan included | ✓ | ✓ | ✓ |
| 90-day actions included | ✓ | ✓ | ✓ |
| Timing guidance (supported) | ✓ | ✓ | ✓ |
| No technical token leak | ✓ | ✓ | ✓ |

**Capability acceptance: PASS** (content + offline compose).

---

## 3. Sample Rec lift (STRONG-EMP)

Recommendation uses KU-AC-CA-000001 90-day plan (priority specializes over generic KU-RC), e.g. Tháng 1–3 structure with Dụng thần bind + mitigate-first if thin.

---

## 4. Ten consulting questions coverage

| Question | Covered in selected commercial text |
|----------|-------------------------------------|
| 1 Career families | Yes — KU-CN-CA-000001 |
| 2 Environment | Yes — KU-CN-CA-000010 |
| 3 Org role | Yes — KU-CN-CA-000011 |
| 4 Lead vs specialist | Yes — KU-CN-CA-000012 |
| 5 Employ vs enterprise | Yes — KU-CN-CA-000013 |
| 6 Advantages | Yes — KU-CN-CA-000014 |
| 7 Risks | Yes — KU-RK-CA-000010 |
| 8 Development | Yes — KU-CN-CA-000015 |
| 9 Timing | Yes — KU-CN-CA-000016 |
| 10 90-day plan | Yes — KU-AC-CA-000001 |

---

## 5. Caveat

PASS is for **authored capability completeness** under offline allow-list.  
Default production path without Domain wiring will **not** yet serve this capability live.

---

## 6. Stop line

Acceptance recorded. Remaining → `19`.

---

END
