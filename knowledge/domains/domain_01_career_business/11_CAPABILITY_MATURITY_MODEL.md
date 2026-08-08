# 11 — Capability Maturity Model · Career & Business

Version: 1.0  
Status: **OFFICIAL — Capability Maturity Model**  
Date: 2026-08-08  
Depends on: `09`, `10`, Wave 1.1 production baseline  
Scope: Documentation only  

---

## 1. Purpose

Define maturity levels for Domain 01 capabilities and estimate **current vs target** state.

---

## 2. Maturity levels (official)

| Level | Name | Meaning |
|------:|------|---------|
| **1** | Basic advisory | Structural Wave 1.1 only; work questions get generic compass |
| **2** | Structured guidance | Domain CN/AC present; clear work themes + next step |
| **3** | Decision support | Go/stage/defer (or equivalent) with reasons; risks when due |
| **4** | Strategic consulting | Pairs RK+MT+OP; scenario-complete journeys; Golden Cases Acceptable+ |
| **5** | Professional advisory | Stable domain pack; scorecard Good+; API-ready; ethics proven |

Rules:

- Level N requires all lower-level criteria.  
- Wave 1.1 alone caps most work capabilities at **Level 1**.  
- Missing Narrative fill does not block Knowledge maturity but caps **customer-felt** maturity.

---

## 3. Current baseline (today)

| Fact | State |
|------|-------|
| Wave 1.1 | Production baseline (structural) |
| Domain 01 Knowledge Units | **None authored** |
| Domain capabilities as services | **Designed only** (this sprint) |
| Runtime capability API | **None** |

Therefore: all Domain 01 capabilities are effectively **Level 1** in production (Wave 1.1 fallback), except where Product already sells generic Result without domain label.

---

## 4. Per-capability maturity estimate

| Capability | Current | Target ( Dom 01 V1) | Missing Knowledge | Missing Narrative | Missing Golden Cases |
|------------|:-------:|:-------------------:|-------------------|-------------------|----------------------|
| CAP-D1-CA-SEL | 1 | **3** | P0 CN/AC; P1 themes optional for 4 | Work-line Exec specialization | D1-GC-* EMP trio |
| CAP-D1-CA-CHG | 1 | **4** | P1 AC Go/stage + RK/MT | Warning/Mitigation surfaces | CHANGE-GO / HOLD |
| CAP-D1-CA-PRO | 1 | **3** | P1 OP + posture AC | Opportunity component use | D1-GC-PROMOTE |
| CAP-D1-CA-LED | 1 | **3** | P0 CN light; P1 RK/MT | Impact + Warning | MGR cases |
| CAP-D1-CA-MGT | 1 | **3** | P1 manager-vs-IC CN | Rec specialization | MGR cases |
| CAP-D1-BU-ENP | 1 | **4** | P0 light AC; P1 CN/AC/RK/MT | Warning + Opportunity | FOUNDER + INDEPENDENT |
| CAP-D1-BU-PTR | 1 | **4** | P1 AC + RK/MT | Warning + Mitigation | D1-GC-PARTNER |
| CAP-D1-CA-DEV | 1 | **3** | P0 AC; P1 skill AC | Reasoning + Rec | SEL shared + skill slice |
| CAP-D1-TM-DEC | 1 | **3** | Luck OP conditional; posture hooks | Timing clauses in Rec/Impact | Shared CHG/PRO/ENP |
| CAP-D1-BU-TEM | 1 | **2→3** (later) | P2 team CN/AC | Team Rec/Warning | P2 extensions |

**Domain 01 V1 commercial bar:** Capabilities in Phase 1–2 roadmap reach targets above; TEM may lag at Level 2.

---

## 5. Maturity gates

| From → To | Gate |
|-----------|------|
| 1 → 2 | P0 domain KUs authored + allow-listed; SEL/DEV/LED-light/ENP-light live |
| 2 → 3 | Decision postures explicit; Golden P0 cases ≥ Acceptable (EPIC 5) |
| 3 → 4 | P1 RK+MT pairs; scenario journeys; P1 Golden Cases ≥ Acceptable |
| 4 → 5 | Scorecard Good+ on suite; capability API contract implemented; Publish policy clear |

---

## 6. Cross-cutting gaps (all capabilities)

| Gap type | Current issue |
|----------|---------------|
| Knowledge | Domain slots reserved in `04` — content not written |
| Narrative | Pack 05 section body fill / summary dedupe (EPIC 7 remaining) |
| Golden Cases | Planned in `05` — not yet executed with domain KUs |
| API | Contract only (`12`) — no implementation |
| Portal | No capability-specific UX (Foundation frozen; uses NarrativeResult) |

---

## 7. Stop line

Maturity model complete. API contract → `12`.

---

END
