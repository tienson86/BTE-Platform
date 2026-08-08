# 03 — Decision Model · Career & Business

Version: 1.0  
Status: **OFFICIAL — Domain 01 Decision Model**  
Date: 2026-08-08  
Depends on: `01`, `02` · Decision Support Model (`DS-*`) · Retrieval Contract  
Scope: Documentation only  

---

## 1. Purpose

Map each major **customer decision** in Domain 01 to:

1. Required Evidence  
2. Required Interpretation focus  
3. Commercial Knowledge (kinds / slots)  
4. Narrative outputs  

No unit content is authored here.

---

## 2. Decision catalog (Domain 01)

| Decision id | Customer decision | Scenario | Official DS |
|-------------|-------------------|----------|-------------|
| D-CA-SEL | Choose / affirm work direction | CS-CA | — (selection) |
| D-CA-CHG | Change job / stay / stage | CS-CC | DS-CC |
| D-CA-PRO | Seek / accept promotion | CS-PR | DS-PR |
| D-CA-LED | Take / deepen leadership | CS-LE | — |
| D-CA-MGT | Become / remain manager | CS-LE / CS-CA | — |
| D-BU-ENP | Start / grow own business | CS-ENP / CS-ST | — |
| D-BU-PTR | Enter / reshape partnership | CS-BU | DS-BP |
| D-BU-TEM | Expand / restyle team leadership | CS-BU / CS-LE | — |
| D-CA-DEV | Invest in skills / development | CS-CA / CS-ED | — |

---

## 3. Decision maps

### 3.1 D-CA-SEL — Career selection

| Layer | Requirement |
|-------|-------------|
| **Required Evidence** | Day master identity; pattern; strength band; useful god; (optional) output/officer/wealth ten-god themes |
| **Required Interpretation** | Overview + useful_god + strength summary |
| **Commercial Knowledge** | Wave 1.1 ID/ST/WK/UG; Domain: career direction CN, role-fit AC (P0) |
| **Narrative outputs** | Exec work-direction line; Reasoning fit; Recommendation exploration step; Conclusion one theme |

### 3.2 D-CA-CHG — Career change

| Layer | Requirement |
|-------|-------------|
| **Required Evidence** | Useful god; strength/weakness; luck window if present; clash/enemy caution |
| **Required Interpretation** | Useful_god; summary; risk-relevant strength |
| **Commercial Knowledge** | Wave 1.1 WK/UG/RC; Domain: change Go/staged AC; reckless RK + MT pair (P1) |
| **Narrative outputs** | Rec stay/switch/stage; Warning if reckless; Mitigation buffer; Conclusion posture |

### 3.3 D-CA-PRO — Promotion

| Layer | Requirement |
|-------|-------------|
| **Required Evidence** | Strength favorable or readiness signals; useful god; optional luck opportunity |
| **Required Interpretation** | Strength; useful_god; summary |
| **Commercial Knowledge** | Wave 1.1 ST/UG; Domain: promotion OP + prepare/defer AC (P1) |
| **Narrative outputs** | Rec advance/prepare/defer; Opportunity when valid; Warning if overreach |

### 3.4 D-CA-LED — Leadership

| Layer | Requirement |
|-------|-------------|
| **Required Evidence** | Officer/kill-related structure if available; strength; pattern; useful god |
| **Required Interpretation** | Pattern; strength; useful_god |
| **Commercial Knowledge** | Wave 1.1 ID/ST/WK; Domain: leadership style CN; strain RK/MT (P1) |
| **Narrative outputs** | Exec leadership posture; Impact; Warning strain; Rec habits |

### 3.5 D-CA-MGT — Management vs IC

| Layer | Requirement |
|-------|-------------|
| **Required Evidence** | Same as leadership + weakness/load signals |
| **Required Interpretation** | Strength; useful_god |
| **Commercial Knowledge** | Domain: manager-vs-IC CN/AC; load MT with Wave 1.1 WK |
| **Narrative outputs** | Rec manager/IC posture; Warning overload; Conclusion |

### 3.6 D-BU-ENP — Entrepreneurship / startup

| Layer | Requirement |
|-------|-------------|
| **Required Evidence** | Useful god; strength/weakness; wealth/output themes if any; luck if present |
| **Required Interpretation** | Useful_god; summary; strength |
| **Commercial Knowledge** | Wave 1.1 UG/WK/RC; Domain: enterprise CN; launch/pilot/defer AC; premature RK+MT (P1) |
| **Narrative outputs** | Rec pilot/defer/launch framing; Warning premature; Opportunity window if valid |

### 3.7 D-BU-PTR — Business partnership

| Layer | Requirement |
|-------|-------------|
| **Required Evidence** | Clash/combine/enemy caution; useful god; pattern; strength |
| **Required Interpretation** | Useful_god; strength; summary |
| **Commercial Knowledge** | Wave 1.1 WK if caution; Domain: solo-vs-partner AC; partnership RK+MT (P1) |
| **Narrative outputs** | Rec solo/partner posture; Warning trust/clash; Mitigation role clarity |

### 3.8 D-BU-TEM — Team management

| Layer | Requirement |
|-------|-------------|
| **Required Evidence** | Leadership-related signals; weakness/load; useful god |
| **Required Interpretation** | Strength; useful_god |
| **Commercial Knowledge** | Domain: team/delegation CN/AC; ties CA-LED |
| **Narrative outputs** | Rec team habits; Warning conflict/overdrive |

### 3.9 D-CA-DEV — Professional development

| Layer | Requirement |
|-------|-------------|
| **Required Evidence** | Useful god; strength; optional education/luck |
| **Required Interpretation** | Useful_god; summary |
| **Commercial Knowledge** | Wave 1.1 UG/RC; Domain: skill-investment AC; practical PG bridge (P0/P1) |
| **Narrative outputs** | Rec skill bet; Reasoning why it serves Dụng thần |

---

## 4. Shared decision postures

| Posture | When |
|---------|------|
| **Prepare** | Default safe; signals mixed or weak load |
| **Advance** | Strength + useful god + (optional) opportunity aligned |
| **Stage / Pilot** | Change or found desired but risk present |
| **Defer** | Hostile timing or thin capacity |
| **Mitigate-first** | Wave 1.1 WK selected — Domain actions must honor this |

Domain 01 must never emit Advance that contradicts active structural weakness without Mitigation.

---

## 5. Evidence sufficiency rules

| Situation | Behavior |
|-----------|----------|
| No useful god | Domain Rec may thin; do not invent work compass |
| No strength/pattern | Limit to honest insufficient; no career oracle |
| Scenario CS-CA but only Wave 1.1 present | Deliver core structure + generic work line if P0 domain units missing |
| Finance-only ask | Hand off / cross-link CK-FI — not forced into Domain 01 |

---

## 6. Traceability chain (required)

```
Customer decision (D-*)
    ↓
Analysis evidence
    ↓
Interpretation focus
    ↓
Wave 1.1 + Domain Commercial Knowledge
    ↓
Narrative components
    ↓
Portal Result
```

Every future Domain 01 KU must declare decision ids it serves.

---

## 7. Stop line

Decision model complete. KU requirements → `04`.

---

END
