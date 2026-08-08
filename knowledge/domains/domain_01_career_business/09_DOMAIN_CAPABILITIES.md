# 09 — Domain Capabilities · Career & Business

Version: 1.0  
Status: **DOMAIN 01 · SPRINT A.5 — Capability Model**  
Date: 2026-08-08  
Depends on: Sprint A (`01`–`08`) frozen · Wave 1.1 frozen  
Scope: Documentation only — no units, no runtime  

---

## 1. Purpose

Define every **business capability** in Domain 01.

A **Capability** is a complete consulting service customers can consume.  
It is **not** an Engine, **not** a Knowledge Unit, and **not** Narrative.

```
Capability (business service)
    ↓ orchestrates
Knowledge + Decision Models + Narrative + Golden Cases
    ↓ delivers
Customer advisory outcome
```

---

## 2. Capability catalog (official)

| Capability id | Commercial name | Subdomain(s) | Phase |
|---------------|-----------------|--------------|-------|
| **CAP-D1-CA-SEL** | Career Selection Assessment | CA-SEL | P0 |
| **CAP-D1-CA-CHG** | Career Transition Planning | CA-CHG | P1 |
| **CAP-D1-CA-PRO** | Promotion Readiness Assessment | CA-PRO | P1 |
| **CAP-D1-CA-LED** | Leadership Assessment | CA-LED | P0 light → P1 deep |
| **CAP-D1-CA-MGT** | Management Capability Assessment | CA-MGT | P1 |
| **CAP-D1-BU-ENP** | Entrepreneurship Assessment | BU-ENP | P0 light → P1 deep |
| **CAP-D1-BU-PTR** | Business Partnership Assessment | BU-PTR | P1 |
| **CAP-D1-CA-DEV** | Professional Development Planning | CA-DEV | P0 |
| **CAP-D1-TM-DEC** | Decision Timing Assessment | CK-LU soft + Domain decisions | P1/P2 |
| **CAP-D1-BU-TEM** | Team Management Assessment | BU-TEM | P2 |

Ten capabilities cover Domain 01 service surface. Team Management is P2; Timing is cross-cutting.

---

## 3. Capability definitions

### 3.1 CAP-D1-CA-SEL — Career Selection Assessment

| Field | Definition |
|-------|------------|
| **Purpose** | Assess which work directions / role families fit the chart |
| **Business value** | Highest-frequency paid career entry; converts calculator users to consult |
| **Customer questions** | Q-01, Q-13, Q-15, Q-19 |
| **Expected outputs** | Work-direction themes; prefer/avoid environments; exploration next step |
| **Required decisions** | D-CA-SEL |
| **Required Narrative** | Exec work line; Reasoning fit; Recommendation exploration; Conclusion theme |
| **Golden Cases** | D1-GC-STRONG-EMP, D1-GC-WEAK-EMP, D1-GC-MIXED-EMP |
| **Out of scope** | Single job-title prophecy; salary guarantees |

### 3.2 CAP-D1-CA-CHG — Career Transition Planning

| Field | Definition |
|-------|------------|
| **Purpose** | Plan stay / switch / staged transition with buffers |
| **Business value** | High-intent decision product; reduces reckless quit advice |
| **Customer questions** | Q-02, Q-11, Q-12, Q-14 |
| **Expected outputs** | Go / stage / defer posture; transition action; reckless risk + mitigation |
| **Required decisions** | D-CA-CHG (DS-CC) |
| **Required Narrative** | Recommendation; Warning; Mitigation tone; Conclusion posture |
| **Golden Cases** | D1-GC-CHANGE-GO, D1-GC-CHANGE-HOLD |
| **Out of scope** | Legal resignation process; HR negotiation scripts |

### 3.3 CAP-D1-CA-PRO — Promotion Readiness Assessment

| Field | Definition |
|-------|------------|
| **Purpose** | Assess advance / prepare / defer for promotion |
| **Business value** | Upsell after selection; timing-sensitive paid scenario |
| **Customer questions** | Q-08 |
| **Expected outputs** | Readiness posture; opportunity language when valid; overreach warning |
| **Required decisions** | D-CA-PRO (DS-PR) |
| **Required Narrative** | Recommendation; Opportunity (conditional); Warning (conditional); Exec posture |
| **Golden Cases** | D1-GC-PROMOTE |
| **Out of scope** | Guaranteed promotion; internal politics playbooks |

### 3.4 CAP-D1-CA-LED — Leadership Assessment

| Field | Definition |
|-------|------------|
| **Purpose** | Clarify leadership style and authority strain conditions |
| **Business value** | Differentiates BTE from generic “career tips” |
| **Customer questions** | Q-05 |
| **Expected outputs** | Leadership style notes; strain risks; mitigation habits |
| **Required decisions** | D-CA-LED |
| **Required Narrative** | Exec; Impact; Warning; Recommendation habits |
| **Golden Cases** | D1-GC-STRONG-MGR, D1-GC-WEAK-MGR (shared with MGT) |
| **Out of scope** | Corporate competency frameworks; 360 HR tools |

### 3.5 CAP-D1-CA-MGT — Management Capability Assessment

| Field | Definition |
|-------|------------|
| **Purpose** | Assess manager vs individual-contributor fit and sustainability |
| **Business value** | Answers a frequent Vietnamese professional dilemma |
| **Customer questions** | Q-04, Q-16 |
| **Expected outputs** | Manager/IC posture; load conditions; next habit |
| **Required decisions** | D-CA-MGT |
| **Required Narrative** | Recommendation; Warning overload; Conclusion |
| **Golden Cases** | D1-GC-STRONG-MGR, D1-GC-WEAK-MGR |
| **Out of scope** | Performance-review templates |

### 3.6 CAP-D1-BU-ENP — Entrepreneurship Assessment

| Field | Definition |
|-------|------------|
| **Purpose** | Assess founding / independent path vs employment |
| **Business value** | Premium scenario; strong commercial intent |
| **Customer questions** | Q-03, Q-06, Q-14 |
| **Expected outputs** | Founder posture; pilot/defer/launch framing; premature-launch risk + runway mitigation |
| **Required decisions** | D-BU-ENP |
| **Required Narrative** | Recommendation; Warning; Opportunity (conditional); Conclusion |
| **Golden Cases** | D1-GC-FOUNDER-READY, D1-GC-FOUNDER-RISK, D1-GC-INDEPENDENT |
| **Out of scope** | Fundraising term sheets; guaranteed startup success |

### 3.7 CAP-D1-BU-PTR — Business Partnership Assessment

| Field | Definition |
|-------|------------|
| **Purpose** | Assess solo vs partner and trust/role clarity |
| **Business value** | High-stakes decision; ethics-sensitive paid consult |
| **Customer questions** | Q-09, Q-17 |
| **Expected outputs** | Solo/partner posture; clash/trust risk; role-clarity mitigation |
| **Required decisions** | D-BU-PTR (DS-BP) |
| **Required Narrative** | Recommendation; Warning; Mitigation; Conclusion |
| **Golden Cases** | D1-GC-PARTNER |
| **Out of scope** | Legal shareholder agreements |

### 3.8 CAP-D1-CA-DEV — Professional Development Planning

| Field | Definition |
|-------|------------|
| **Purpose** | Plan skill/capability bets aligned to Dụng thần |
| **Business value** | Retention / follow-up product; soft entry after selection |
| **Customer questions** | Q-07, Q-18 |
| **Expected outputs** | Learning priorities; 2–4 week capability next step |
| **Required decisions** | D-CA-DEV |
| **Required Narrative** | Recommendation; Reasoning; soft Exec line |
| **Golden Cases** | D1-GC-STRONG-EMP (dev slice), shared with SEL |
| **Out of scope** | Full curriculum design; course marketplace |

### 3.9 CAP-D1-TM-DEC — Decision Timing Assessment

| Field | Definition |
|-------|------------|
| **Purpose** | Assess when to move on work/business decisions (prepare / advance / defer) |
| **Business value** | Cross-cuts change, promote, found; increases decision confidence |
| **Customer questions** | Timing facets of Q-02, Q-03, Q-08, Q-14 |
| **Expected outputs** | Timing posture; window language when luck evidence exists |
| **Required decisions** | Overlay on D-CA-CHG / D-CA-PRO / D-BU-ENP |
| **Required Narrative** | Impact; Recommendation timing clause; Opportunity (conditional) |
| **Golden Cases** | Shared with CHANGE / PROMOTE / FOUNDER sets |
| **Out of scope** | Full Đại vận product (CK-LU domain ownership); fortune-telling calendars |

### 3.10 CAP-D1-BU-TEM — Team Management Assessment

| Field | Definition |
|-------|------------|
| **Purpose** | Advise delegation, pace, and team conflict posture |
| **Business value** | Completes leadership/business suite for managers/founders |
| **Customer questions** | Q-10, Q-20 |
| **Expected outputs** | Team habits; conflict/overdrive caution |
| **Required decisions** | D-BU-TEM |
| **Required Narrative** | Recommendation; Warning; Impact |
| **Golden Cases** | Extend MGR / FOUNDER cases (P2) |
| **Out of scope** | Org-design consulting |

---

## 4. Capability principles

1. One capability = one primary customer job-to-be-done.  
2. Capabilities compose Wave 1.1 + Domain Knowledge — they do not recompute Analysis.  
3. Mitigate-first when Wave 1.1 Weakness is active.  
4. Missing domain Knowledge → capability may degrade gracefully to Wave 1.1 structural advice.  
5. Future APIs expose **capabilities**, not raw Knowledge Units.

---

## 5. Stop line

Capability catalog defined. Mapping → `10`.

---

END
