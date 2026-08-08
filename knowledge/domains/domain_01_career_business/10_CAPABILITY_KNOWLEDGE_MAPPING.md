# 10 — Capability Knowledge Mapping · Career & Business

Version: 1.0  
Status: **OFFICIAL — Capability → Knowledge → Narrative → Portal → API**  
Date: 2026-08-08  
Depends on: `09`, `03`, `04`, Retrieval Contract, Pack 05  
Scope: Documentation only  

---

## 1. Purpose

Map each capability through the full advisory chain:

```
Capability
    ↓
Decision Models
    ↓
Knowledge Requirements
    ↓
Knowledge Units
    ↓
Commercial Bundle
    ↓
Narrative Components
    ↓
Portal Sections
    ↓
Future APIs
```

Relationship types: **required** · **optional** · **conditional**.

---

## 2. Shared spine (all Domain 01 capabilities)

| Layer | Items | Relationship |
|-------|-------|--------------|
| Knowledge Units | KU-ID-001, KU-UG-001 | **Required** (when signals exist) |
| Knowledge Units | KU-ST-001 | **Conditional** on favorable strength |
| Knowledge Units | KU-WK-001 | **Conditional** on weakness/enemy |
| Knowledge Units | KU-RC-001 | **Optional** baseline until domain AC specializes |
| Commercial Bundle | identity, useful_god, strengths/weaknesses, recommendations | **Required** fields when selected |
| Narrative | executive_summary, recommendation, conclusion | **Required** |
| Narrative | warning | **Conditional** on RK / WK |
| Portal | Result Exec / Rec / Warning / Conclusion | **Required** surfaces |
| Future API | capability response embeds NarrativeResult + bundle | **Required** contract (`12`) |

---

## 3. Per-capability mapping

### 3.1 CAP-D1-CA-SEL

| Layer | Mapping |
|-------|---------|
| Decisions | D-CA-SEL **required** |
| Knowledge req | P0 CN/AC career direction **required** |
| Knowledge Units | KU-CN-CA-000001, KU-AC-CA-000001 **required**; theme packs 000002/3 **optional** (P1) |
| Bundle | recommendations + identity/useful_god **required** |
| Narrative | Exec, Reasoning, Recommendation, Conclusion **required** |
| Portal | Exec + Rec **required** |
| Future API | `career.selection.assess` |

### 3.2 CAP-D1-CA-CHG

| Layer | Mapping |
|-------|---------|
| Decisions | D-CA-CHG / DS-CC **required** |
| Knowledge req | AC Go + staged **required** (P1); RK+MT change pair **conditional** on hostile/rush signals |
| Knowledge Units | KU-AC-CA-000002/000003 **required**; KU-RK-CA-000001 + KU-MT-CA-000001 **conditional** |
| Bundle | recommendations **required**; warnings **conditional** |
| Narrative | Recommendation, Warning, Conclusion **required**; Opportunity **optional** |
| Portal | Rec + Warning **required** when risk fires |
| Future API | `career.transition.plan` |

### 3.3 CAP-D1-CA-PRO

| Layer | Mapping |
|-------|---------|
| Decisions | D-CA-PRO / DS-PR **required** |
| Knowledge req | Promotion OP **conditional**; prepare/defer via AC **required** |
| Knowledge Units | KU-OP-CA-000001 **conditional**; Wave 1.1 ST/UG **required** |
| Bundle | opportunities **conditional**; recommendations **required** |
| Narrative | Recommendation **required**; Opportunity **conditional**; Warning **conditional** |
| Portal | Rec (+ Opportunity card if Product surfaces) |
| Future API | `career.promotion.assess` |

### 3.4 CAP-D1-CA-LED

| Layer | Mapping |
|-------|---------|
| Decisions | D-CA-LED **required** |
| Knowledge req | CN leadership light **required** (P0); RK+MT strain **conditional** (P1) |
| Knowledge Units | KU-CN-LE-000001 **required**; KU-RK-LE-000001 + KU-MT-LE-000001 **conditional** |
| Bundle | identity + recommendations + warnings **conditional** |
| Narrative | Exec, Impact, Recommendation **required**; Warning **conditional** |
| Portal | Exec + Rec |
| Future API | `career.leadership.assess` |

### 3.5 CAP-D1-CA-MGT

| Layer | Mapping |
|-------|---------|
| Decisions | D-CA-MGT **required** |
| Knowledge req | Manager vs IC CN **required** (P1); WK load **conditional** |
| Knowledge Units | KU-CN-LE-000002 **required** |
| Bundle | recommendations **required**; warnings **conditional** |
| Narrative | Recommendation, Warning, Conclusion |
| Portal | Rec + Warning |
| Future API | `career.management.assess` |

### 3.6 CAP-D1-BU-ENP

| Layer | Mapping |
|-------|---------|
| Decisions | D-BU-ENP **required** |
| Knowledge req | P0 independence posture **required**; P1 enterprise CN + launch AC + RK/MT **required** for full maturity |
| Knowledge Units | KU-AC-BU-000001 **required** (light); KU-CN-BU-000001, KU-AC-BU-000002, RK/MT-BU-000002 **required** at P1 |
| Bundle | recommendations **required**; warnings/opportunities **conditional** |
| Narrative | Recommendation, Warning, Conclusion; Opportunity **conditional** |
| Portal | Rec + Warning |
| Future API | `business.entrepreneurship.assess` |

### 3.7 CAP-D1-BU-PTR

| Layer | Mapping |
|-------|---------|
| Decisions | D-BU-PTR / DS-BP **required** |
| Knowledge req | RK+MT partnership **required**; solo/partner AC **required** |
| Knowledge Units | KU-AC-BU-000001, KU-RK-BU-000001, KU-MT-BU-000001 **required** (P1) |
| Bundle | recommendations + warnings **required** when assessing partner |
| Narrative | Recommendation, Warning, Conclusion |
| Portal | Rec + Warning |
| Future API | `business.partnership.assess` |

### 3.8 CAP-D1-CA-DEV

| Layer | Mapping |
|-------|---------|
| Decisions | D-CA-DEV **required** |
| Knowledge req | Role-fit AC **required** (P0); skill AC-000004 **optional→required** at P1 |
| Knowledge Units | KU-AC-CA-000001 **required**; KU-AC-CA-000004 **optional** (P1) |
| Bundle | recommendations **required** |
| Narrative | Recommendation, Reasoning |
| Portal | Rec |
| Future API | `career.development.plan` |

### 3.9 CAP-D1-TM-DEC

| Layer | Mapping |
|-------|---------|
| Decisions | Overlay on CHG/PRO/ENP **required** when timing asked |
| Knowledge req | Luck OP units **conditional**; Domain postures **required** |
| Knowledge Units | KU-OP-LU-* **conditional** (CK-LU); domain AC posture **required** |
| Bundle | opportunities **conditional** |
| Narrative | Impact + Rec timing clause **required**; Opportunity **conditional** |
| Portal | Rec (+ timing callout) |
| Future API | `decision.timing.assess` (domain-scoped param) |

### 3.10 CAP-D1-BU-TEM

| Layer | Mapping |
|-------|---------|
| Decisions | D-BU-TEM **required** |
| Knowledge req | Team CN/AC **required** (P2) |
| Knowledge Units | KU-CN-TEM-000001, KU-AC-TEM-000001 **required** at P2 |
| Bundle | recommendations **required**; warnings **conditional** |
| Narrative | Recommendation, Warning, Impact |
| Portal | Rec |
| Future API | `business.team.assess` |

---

## 4. Relationship legend

| Type | Meaning |
|------|---------|
| **Required** | Capability cannot claim full service without it (may still run degraded) |
| **Optional** | Improves quality; not blocking |
| **Conditional** | Included only when Analysis signals / scenario match |

---

## 5. Bundle field ownership (Domain 01)

| Bundle field | Typical capability owners |
|--------------|---------------------------|
| identity | All (via Wave 1.1) |
| strengths / weaknesses | All; gate Advance |
| useful_god | SEL, DEV, ENP, CHG, PRO |
| recommendations | All |
| warnings | CHG, ENP, PTR, LED, MGT, TEM |
| opportunities | PRO, ENP, TM-DEC |

Narrative consumes Bundle only — never raw KUs (frozen Integration rule).

---

## 6. Stop line

Mapping complete. Maturity → `11`.

---

END
