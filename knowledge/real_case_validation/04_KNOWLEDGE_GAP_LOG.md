# 04 — Knowledge Gap Log

Version: 1.0  
Status: **OFFICIAL — Knowledge Gap Log (Sprint A)**  
Date: 2026-08-08  
Depends on: `03_CASE_EVALUATION_REPORT.md` · Wave 1.1 · Knowledge Catalog (planned)  
Scope: Gap classification only — no unit authoring  

---

## 1. Purpose

Map every observed consulting weakness to a **primary root cause class**:

| Class | Definition |
|-------|------------|
| **Missing Knowledge** | Required advisory unit/domain not present in Wave 1.1 |
| **Weak Knowledge** | Unit exists but condition, bind labels, or prose is insufficient |
| **Missing Evidence** | Analysis/projection does not supply needed signal |
| **Weak Narrative** | Signals/units exist but composition/surfaces degrade quality |

Secondary classes may be noted; backlog uses the primary class.

---

## 2. Gap log

| Gap id | Symptom | Cases | Primary class | Secondary | Notes |
|--------|---------|-------|---------------|-----------|-------|
| **KG-001** | No business / venture counsel | GC-BUSINESS | Missing Knowledge | — | Need CS-BU / CK-BU units (catalog P0/P1) |
| **KG-002** | No career role / fit counsel | GC-CAREER | Missing Knowledge | — | Need CS-CA units |
| **KG-003** | No marriage / relationship counsel | GC-MARRIAGE | Missing Knowledge | — | Need CS-RL/MA; ethics bounds |
| **KG-004** | No health lifestyle counsel | GC-HEALTH | Missing Knowledge | — | Non-medical only |
| **KG-005** | No wealth / money posture | GC-WEALTH | Missing Knowledge | — | Need CS-FI/IV |
| **KG-006** | Special pattern not explained | GC-SPECIAL-PATTERN | Missing Knowledge | Weak Narrative | Pattern label only; no special-pattern KU |
| **KG-007** | Follow-pattern not distinct | GC-FOLLOW-PATTERN | Missing Knowledge | Weak Knowledge | May need follow-specific analytical KU |
| **KG-008** | Strength band tokens (`vuong`/`nhuoc`/`can`) in customer text | Strong, Weak, Special, Mixed | Weak Knowledge | Weak Narrative | `{strength_band_label}` bind quality |
| **KG-009** | Weakness signal label duplicates (`Hỏa; Hỏa`) | Weak, Mixed | Weak Narrative | Missing Evidence | Projection joins ky_than + unfavorable without dedupe |
| **KG-010** | Weakness paragraph duplicated in summary slot | Weak, Mixed | Weak Narrative | — | Composer/summary aggregation |
| **KG-011** | Strengths slot clones identity | Strong, Special, Mixed, No-UG | Weak Narrative | Weak Knowledge | Exec slot filling / component selection |
| **KG-012** | Priority == next_action identical | All UG-complete | Weak Knowledge | Weak Narrative | KU-RC-001 does not split priority vs next; Narrative mirrors |
| **KG-013** | Weak chart: expand-UG action without elevate reduce-load | GC-WEAK-ENEMY | Weak Knowledge | Weak Narrative | KU-RC pairs with WK but posture not conditional enough |
| **KG-014** | Mixed ST+WK “mỏng” vs thân vượng tension | GC-MIXED | Weak Knowledge | Weak Narrative | WK template assumes thin structure; enemy-on-strong needs distinct wording |
| **KG-015** | No UG → Rec insufficient | GC-NO-USEFUL-GOD | Missing Knowledge | Missing Evidence | Honest today; need non-UG action fallback KU later |
| **KG-016** | Pack 05 section bodies often empty | Multiple | Weak Narrative | — | Summary carries prose; section body fill weak |
| **KG-017** | Domain scenario_id unused commercially | Intent cases | Missing Knowledge | Weak Narrative | Retrieval scenario affinity unused beyond default |
| **KG-018** | Units still `awaiting_review` | All | Weak Knowledge | — | Product Publish policy (process gap) |

---

## 3. Class distribution (Sprint A)

| Class | Gap count | Customer impact theme |
|-------|----------:|------------------------|
| Missing Knowledge | 8 | Domain + special/follow + non-UG fallback |
| Weak Knowledge | 5 | Labels, RC split, WK/RC posture, publish |
| Weak Narrative | 4 (+ secondaries) | Dedupe, slot cloning, section bodies |
| Missing Evidence | 0 primary | (secondary on KG-009 only) |

---

## 4. Mapping rules (for future reviews)

1. If advice cannot exist without a new domain/unit → **Missing Knowledge**.  
2. If Wave 1.1 unit selected but text wrong/weak → **Weak Knowledge**.  
3. If Analysis lacks signal and system correctly thins → prefer **Missing Evidence** only when signal *should* exist for the profile.  
4. If unit+signal OK but Exec/Rec/Warning presentation fails → **Weak Narrative**.  
5. Never classify “needs Wave 1.2” as Weak Narrative alone.

---

## 5. Explicit non-gaps

| Observation | Why not a gap |
|-------------|---------------|
| Weaknesses insufficient on pure strong chart | Correct honesty |
| UG/RC omitted without useful god | Contract-correct |
| No medical diagnosis on health intent | Ethics — must remain absent |

---

## 6. Stop line

Gap log frozen for Sprint A Product review. Remediation via `05` only after authorization.

---

END
