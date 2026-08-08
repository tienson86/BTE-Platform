# 08 — Decision Support Model

Version: 1.0  
Status: **SPRINT B — Consultation Scenario Model**  
Date: 2026-08-08  
Depends on: `06`, `07`, Sprint A `02`  

---

## 1. Purpose

Design how BTE supports **decisions** — not only descriptions.

Decision support is a specialization of scenarios where the customer needs a **choice frame**:

```
Understand → Weigh risk/opportunity → Act / Wait / Prepare → Mitigate
```

Commercial Knowledge kinds **Action, Risk, Mitigation, Opportunity, Life Strategy** are mandatory design inputs.  
Rule Database supplies signals; it does not decide for the customer.

---

## 2. Official decision catalog

| ID | Decision | Linked scenario(s) |
|----|----------|--------------------|
| DS-CC | Career Change | CS-CC |
| DS-PR | Promotion | CS-PR |
| DS-IV | Investment | CS-IV |
| DS-MA | Marriage | CS-MA |
| DS-RL | Relocation | CS-RL |
| DS-BP | Business Partnership | CS-BU (+ partnership focus) |
| DS-HI | Health Improvement | CS-HE (lifestyle only) |
| DS-LA | Lifestyle Adjustment | CS-LS |
| DS-ST | Startup Launch | CS-ST |
| DS-PP | Property Commitment | CS-PP |
| DS-MD | Generic Major Decision | CS-MD |

Additional decisions must follow `10_SCENARIO_EXPANSION_GUIDE.md`.

---

## 3. Decision definition template

| Field | Meaning |
|-------|---------|
| Decision context | What choice is on the table |
| Required evidence | Evidence kinds that must exist |
| Risk factors | What Analysis/knowledge may elevate caution |
| Opportunity factors | What may support leaning in |
| Mitigation knowledge | How to reduce downside |
| Action knowledge | Concrete next steps (including wait/prepare) |
| Success indicators | How customer/product judge a good consultation outcome |

**Outputs never include:** guaranteed outcomes, medical treatment, legal/financial fiduciary advice beyond chart-informed posture.

---

## 4. Decision definitions

### 4.1 Career Change (DS-CC)

| Field | Content |
|-------|---------|
| **Decision context** | Stay vs leave vs prepare transition |
| **Required evidence** | identity, action, risk, implication |
| **Risk factors** | Hostile luck to useful god; weak strength during change; clash on career-related branches; enemy-god dominance |
| **Opportunity factors** | Favorable luck to useful god; output/resource support; pattern aligned with new path |
| **Mitigation knowledge** | Staged transition; skill buffer; timing deferral; lifestyle recovery |
| **Action knowledge** | Go / wait / prepare + one next employment action |
| **Success indicators** | Clear posture; named risk+mitigation; no reckless “resign now” without support |

### 4.2 Promotion (DS-PR)

| Field | Content |
|-------|---------|
| **Decision context** | Accept expanded authority vs consolidate |
| **Required evidence** | action, strength, implication; risk if strain |
| **Risk factors** | Officer overload; strength deficit; clash on authority stars; burnout lifestyle signals |
| **Opportunity factors** | Officer support; favorable luck; leadership-compatible pattern |
| **Mitigation knowledge** | Scope control; delegation habits; recovery pacing |
| **Action knowledge** | Accept / negotiate scope / defer |
| **Success indicators** | Advancement advice paired with capacity caution |

### 4.3 Investment (DS-IV)

| Field | Content |
|-------|---------|
| **Decision context** | Increase exposure vs conserve vs wait |
| **Required evidence** | risk, action, implication |
| **Risk factors** | Wealth clash; hostile period; speculative over-extension patterns |
| **Opportunity factors** | Wealth support; favorable luck; stable useful-god wealth path |
| **Mitigation knowledge** | Position sizing; diversify timing; avoid all-in language |
| **Action knowledge** | Conserve / selective / wait — never return promises |
| **Success indicators** | Risk-first framing; ethical money language |

### 4.4 Marriage (DS-MA)

| Field | Content |
|-------|---------|
| **Decision context** | Commit / slow down / strengthen foundations (not “destiny decree”) |
| **Required evidence** | implication, action; risk+mitigation when cautions exist |
| **Risk factors** | Clash/harm on spouse palace; hostile relation luck; extreme imbalance |
| **Opportunity factors** | Harmonizing combines; supportive luck; mature communication patterns |
| **Mitigation knowledge** | Pacing; counseling-oriented habits; boundary care |
| **Action knowledge** | Relationship practices — not ultimatums about third parties |
| **Success indicators** | Non-fatalistic tone; ethics flags respected |

### 4.5 Relocation (DS-RL)

| Field | Content |
|-------|---------|
| **Decision context** | Move / stay / prepare move |
| **Required evidence** | action, risk, implication, identity |
| **Risk factors** | Unfavorable luck for displacement; career/finance instability; environment mismatch |
| **Opportunity factors** | Useful-god supportive region themes; favorable period; career pull |
| **Mitigation knowledge** | Trial period; financial buffer; dual-location transition |
| **Action knowledge** | Relocate / defer / prepare checklist |
| **Success indicators** | Multi-domain (work+money+place) covered |

### 4.6 Business Partnership (DS-BP)

| Field | Content |
|-------|---------|
| **Decision context** | Partner / solo / renegotiate terms |
| **Required evidence** | risk, action, implication |
| **Risk factors** | Clash between partnership indicators; wealth drain patterns; trust/officer strain |
| **Opportunity factors** | Combine/harmony support; complementary ten-god structure; favorable luck |
| **Mitigation knowledge** | Clear contracts (as practical advice theme); role clarity; exit clauses mindset |
| **Action knowledge** | Partner carefully / solo / wait for timing |
| **Success indicators** | Partnership risk not ignored |

### 4.7 Health Improvement (DS-HI)

| Field | Content |
|-------|---------|
| **Decision context** | Lifestyle adjustments to improve balance — **not treatment choice** |
| **Required evidence** | risk, action, implication |
| **Risk factors** | Extreme temperature/element imbalance; overwork strength drain; selected caution stars |
| **Opportunity factors** | Useful-god lifestyle alignment; seasonal balance opportunities |
| **Mitigation knowledge** | Rest, pacing, elemental lifestyle hints |
| **Action knowledge** | Habit changes; seek professional medical care when symptoms exist (disclaimer) |
| **Success indicators** | Explicit non-medical framing present |

### 4.8 Lifestyle Adjustment (DS-LA)

| Field | Content |
|-------|---------|
| **Decision context** | Change daily rhythm / habits |
| **Required evidence** | action, implication |
| **Risk factors** | Unsustainable pace vs strength; sleep/recovery neglect signals |
| **Opportunity factors** | Useful-god habits; seasonal alignment |
| **Mitigation knowledge** | Gradual habit change; recovery buffers |
| **Action knowledge** | 1–3 concrete habit actions |
| **Success indicators** | Specific, sustainable actions |

### 4.9 Startup Launch (DS-ST)

| Field | Content |
|-------|---------|
| **Decision context** | Launch now / validate / defer |
| **Required evidence** | action, risk, implication, strength |
| **Risk factors** | Hostile luck; capital clash; pattern instability; partnership risk |
| **Opportunity factors** | Favorable period; output support; founder-compatible structure |
| **Mitigation knowledge** | MVP scope; runway; co-founder fit checks |
| **Action knowledge** | Launch / pilot / defer |
| **Success indicators** | Timing + downside both explicit |

### 4.10 Property Commitment (DS-PP)

| Field | Content |
|-------|---------|
| **Decision context** | Buy/commit vs wait vs rent/flex |
| **Required evidence** | action, risk, implication |
| **Risk factors** | Wealth lock-up in hostile period; relocation conflict; over-leverage themes |
| **Opportunity factors** | Stable wealth luck; supportive environment themes |
| **Mitigation knowledge** | Liquidity reserve; timing windows; avoid forced buy |
| **Action knowledge** | Commit / wait / prepare financing carefully |
| **Success indicators** | No guaranteed appreciation language |

### 4.11 Generic Major Decision (DS-MD)

| Field | Content |
|-------|---------|
| **Decision context** | Any high-stakes binary/multi-option choice |
| **Required evidence** | identity, action, risk, implication |
| **Risk factors** | Context-domain risks + current luck hostility |
| **Opportunity factors** | Context strengths + favorable luck |
| **Mitigation knowledge** | Wait option; information-gathering; reversible steps |
| **Action knowledge** | Decide / wait / prepare — with criteria checklist |
| **Success indicators** | Criteria explicit; wait is a first-class action |

---

## 5. Decision outcome vocabulary (standard)

All decision consultations should resolve to one primary posture:

| Posture | Meaning |
|---------|---------|
| **Advance** | Conditions support moving forward |
| **Prepare** | Direction OK; readiness/timing incomplete |
| **Wait** | Timing or risk dominates |
| **Protect** | Prioritize mitigation / conservation |
| **Reassess** | Evidence insufficient — honest incomplete |

Narrative Recommendation must name the posture.  
Insufficient evidence → Reassess / approved insufficient — never fake Advance.

---

## 6. Evidence pack for decisions (minimum)

| Layer | Minimum |
|-------|---------|
| Analytical substrate | Strength / useful god / luck facts as applicable |
| Opportunity | ≥0 (optional) but required to claim Advance |
| Risk | ≥1 if any hostile signal; else explicit “no major caution found” only if knowledge supports |
| Mitigation | Required whenever Risk ≥1 |
| Action | ≥1 including possible Wait/Prepare |
| Implication | ≥1 tying decision to life impact |

---

## 7. Success indicators (product-level)

A decision-support NarrativeResult is successful when:

1. Customer question is reflected in Exec / Impact.  
2. Posture is explicit.  
3. Risk and mitigation co-appear when cautions exist.  
4. Actions are specific and chart-bound.  
5. Trace links to Commercial Knowledge / evidence.  
6. Ethics constraints for MA/HI satisfied.  
7. No contradiction with AnalysisResult.

---

## 8. Relationship to scenarios

```
Decision (DS-*)
    ↓ specializes
Scenario (CS-*)
    ↓ uses profile from
07 Scenario Relationship Model
    ↓ fills
Narrative Recommendation + Warning (+ Exec)
```

Not every scenario is a decision (e.g. pure Identity).  
Every decision maps to ≥1 scenario.

---

## 9. Stop line

Decision Support Model complete.  
No decision engine implementation in this sprint.

---

END
