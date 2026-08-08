# 13 — Capability Roadmap · Career & Business

Version: 1.0  
Status: **OFFICIAL — Domain 01 Capability Roadmap**  
Date: 2026-08-08  
Depends on: `09`–`12`, `04`, `05`  
Scope: Planning only — no authoring / no implementation this sprint  

---

## 1. Purpose

Plan how Domain 01 capabilities move from design → Knowledge → validated services.

```
Phase 1 — P0 Capabilities
        ↓
Phase 2 — P1 Capabilities
        ↓
Phase 3 — P2 Capabilities
```

---

## 2. Phase 1 — P0 Capabilities

**Goal:** First commercial Career & Business services above Wave 1.1.

| Capability | Priority | Commercial impact | Dependencies | Est. new KUs | Golden Cases |
|------------|:--------:|-------------------|--------------|-------------:|--------------|
| CAP-D1-CA-SEL | P0 | Highest entry conversion | Wave 1.1; CS-CA/default policy | 2 | STRONG/WEAK/MIXED-EMP |
| CAP-D1-CA-DEV | P0 | Retention / soft upsell | SEL P0 AC overlap | 0–1 (+ skill later) | Shared EMP |
| CAP-D1-CA-LED | P0 light | Differentiation | Wave 1.1 | 1 | MGR light optional |
| CAP-D1-BU-ENP | P0 light | Premium teaser | Wave 1.1 | 1 | INDEPENDENT |

**Phase 1 KU estimate:** **3–4** new units (per `04` P0).  
**Exit:** Maturity ≥ 2 (target 3 on SEL); EPIC 5 Acceptable on P0 Golden Cases; no Wave 1.1 edits.

**Not in Phase 1:** Capability HTTP API implementation (contract only); Portal redesign.

---

## 3. Phase 2 — P1 Capabilities

**Goal:** Decision-grade services (change / promote / found / partner / manage).

| Capability | Priority | Commercial impact | Dependencies | Est. new KUs | Golden Cases |
|------------|:--------:|-------------------|--------------|-------------:|--------------|
| CAP-D1-CA-CHG | P1 | High-intent paid | Phase 1 SEL; DS-CC | 4 (AC×2+RK+MT) | CHANGE-GO/HOLD |
| CAP-D1-CA-PRO | P1 | Upsell | Phase 1; luck optional | 1–2 | PROMOTE |
| CAP-D1-BU-ENP | P1 deep | Premium | Phase 1 light ENP | 4 (CN+AC+RK+MT) | FOUNDER-READY/RISK |
| CAP-D1-BU-PTR | P1 | High-stakes | ENP helpful | 3 (AC+RK+MT) | PARTNER |
| CAP-D1-CA-MGT | P1 | Professional segment | LED light | 1 | MGR duo |
| CAP-D1-CA-LED | P1 deep | Completes LED | Phase 1 CN | 2 (RK+MT) | MGR duo |
| CAP-D1-TM-DEC | P1 | Cross-cut confidence | CHG/PRO/ENP + CK-LU soft | 0–2 luck OP | Shared |
| CAP-D1-CA-SEL | P1 deepen | Better themes | Phase 1 | 2 theme CN | EMP refresh |
| CAP-D1-CA-DEV | P1 deepen | Skill bets | Phase 1 | 1 | EMP skill slice |

**Phase 2 KU estimate:** **~15–18** (per `04` P1).  
**Exit:** Target maturity 3–4 on decision capabilities; RK always paired with MT; Golden Cases Acceptable+.

---

## 4. Phase 3 — P2 Capabilities

**Goal:** Strategic depth and team/founder long-horizon.

| Capability | Priority | Commercial impact | Dependencies | Est. new KUs | Golden Cases |
|------------|:--------:|-------------------|--------------|-------------:|--------------|
| CAP-D1-BU-TEM | P2 | Completes suite | MGT/LED/ENP | 2 | MGR/FOUNDER extend |
| CAP-D1-BU-ENP | P2 deepen | Flagship advisory | Phase 2 | 3–4 ST/OP/RK/MT | Founder long-horizon |
| CAP-D1-TM-DEC | P2 deepen | Timing product link | CK-LU domain | 1–2 | Timing suite |
| Capability API | P2 eng | Externalization | Phases 1–2 content stable | 0 (eng) | Contract conformance |
| Maturity 5 push | P2 | Brand trust | Scorecard Good+ | — | Full D1 suite |

**Phase 3 KU estimate:** **~6–8** domain (+ luck cross-domain).  
**Exit:** Professional advisory bar on flagship capabilities; API optional go-live by Product.

---

## 5. Priority summary

| Order | Focus | Why |
|------:|-------|-----|
| 1 | SEL + DEV + LED-light + ENP-light | Open the domain commercially |
| 2 | CHG + ENP-deep + PTR | Highest decision value |
| 3 | PRO + MGT + LED-deep + TM | Complete decision surface |
| 4 | TEM + P2 depth + API | Strategic / platform |

---

## 6. Cross-phase constraints

| Constraint | Rule |
|------------|------|
| Wave 1.1 | Frozen — never modified to “make domain easier” |
| Quantity | Do not skip Phase 1 quality for Phase 2 volume |
| Narrative Engine | Frozen — capabilities consume NarrativeResult |
| Foundation / Portal UI | No redesign required for Phases 1–2 |
| Finance / Marriage | Separate domains — not sneak-authored here |

---

## 7. Suggested Product checkpoints

1. Approve Sprint A.5 capability model  
2. Authorize Phase 1 Knowledge authoring (still no API)  
3. Run D1 P0 Golden Cases + EPIC 5 scorecard  
4. Authorize Phase 2  
5. Decide Capability API engineering epic separately  

---

## 8. Success for Domain 01 consulting service model

Domain 01 is **complete as a consulting service model** when:

- Capabilities defined (`09`)  
- Mapped to Knowledge/Narrative/Portal/API (`10`)  
- Maturity understood (`11`)  
- Future API contracted (`12`)  
- Roadmap phased (`13`)  

Knowledge population and API build remain **later sprints**.

---

## 9. Stop line

Roadmap complete.  

**Stop after Sprint A.5. Do not author Knowledge Units. Wait for Product review.**

---

END
