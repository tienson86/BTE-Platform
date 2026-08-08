# 07 — Scenario Relationship Model

Version: 1.0  
Status: **SPRINT B — Consultation Scenario Model**  
Date: 2026-08-08  
Depends on: `06_CONSULTATION_SCENARIOS.md`, Sprint A `01`–`03`  

---

## 1. Purpose

Model relationships from customer **Scenario** through knowledge and delivery layers.

Official chain:

```
Scenario
    ↓
Knowledge Domains (CK-*)
    ↓
Evidence (typed)
    ↓
Interpretation
    ↓
Commercial Knowledge (kinds)     ← SSOT for advisory text
    ↓
Narrative Components
    ↓
Narrative Result
```

**Note on order:** Domains and commercial kinds jointly constrain what may be retrieved. Evidence is the typed runtime form of selected Commercial Knowledge (plus allowed Analysis substrate). Interpretation binds; Narrative composes. Commercial Knowledge remains SSOT even when drawn mid-chain.

Normalized selection flow (implementation-facing design):

```
Scenario intent
    ↓
Required/optional/conditional domain + kind profile
    ↓
Commercial Knowledge units matching signals
    ↓
Evidence units
    ↓
InterpretationResult refs
    ↓
Narrative components → NarrativeResult
```

---

## 2. Cardinality vocabulary

| Label | Meaning |
|-------|---------|
| **Required** | Must be present for scenario to claim commercial completeness |
| **Optional** | Improves depth; absence → shorter but valid partial |
| **Conditional** | Required only when Analysis signals fire (e.g. clash → Risk) |

Missing **Required** commercial evidence → `partial_insufficient` (or scoped insufficient slots) — honesty over filler.

---

## 3. Master relationship diagram

```
                    ┌─────────────┐
                    │  Scenario   │  customer intent (CS-*)
                    └──────┬──────┘
                           │ selects profile
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
     CK Domains      Commercial      Analytical
     (required/      Kinds           signals
      optional)      (req/opt/cond)  (from Rule DB)
           │               │               │
           └───────────────┼───────────────┘
                           ▼
                    Knowledge match
                           ▼
                      Evidence
                           ▼
                   Interpretation
                           ▼
              Narrative Components (Pack 05)
                           ▼
                   NarrativeResult
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
           Portal                    Report
```

---

## 4. Scenario → Domain relationships

| Scenario | Required domains | Optional | Conditional |
|----------|------------------|----------|-------------|
| CS-ID | CK-ID | CK-PE | — |
| CS-CA | CK-CA, CK-DM | CK-LU, CK-LE | CK-FI if wealth-work blended |
| CS-CC | CK-CA, CK-DM, CK-LU | CK-PG | CK-FI if money-driven change |
| CS-PR | CK-CA, CK-LE, CK-DM | CK-LU | CK-PE if style central |
| CS-BU | CK-BU, CK-DM | CK-FI, CK-LE | CK-LU always recommended |
| CS-ST | CK-BU, CK-FI, CK-LU, CK-DM | CK-LE | CK-EN if location-bound |
| CS-LE | CK-LE, CK-PE | CK-CA | CK-LU if timing asked |
| CS-IV | CK-FI, CK-DM, CK-LU | — | CK-BU if business investment |
| CS-FI | CK-FI | CK-LS, CK-LU | — |
| CS-PP | CK-FI, CK-DM, CK-EN | CK-LU | CK-RL overlap if moving |
| CS-MA | CK-MA | CK-RE, CK-LU | ethics always on |
| CS-DT | CK-RE, CK-PE | CK-MA | — |
| CS-CH | CK-CH | CK-RE | ethics always on |
| CS-PA | CK-PA | CK-RE | — |
| CS-HE | CK-HE, CK-LS | — | non-medical always on |
| CS-LS | CK-LS | CK-PG, CK-HE | — |
| CS-ED | CK-ED, CK-PG | CK-LU | — |
| CS-PG | CK-PG, CK-ID | CK-DM | — |
| CS-LT | CK-LU, CK-DM | — | context domain if user named one |
| CS-MD | CK-DM, CK-LU | — | **Required conditional:** context domain of the decision |
| CS-EN | CK-EN | CK-LS | — |
| CS-TR | CK-EN, CK-LU | CK-LS | — |
| CS-RL | CK-EN, CK-DM, CK-LU | CK-CA, CK-FI | both CA/FI if work+money move |
| CS-ENP | CK-BU, CK-LE, CK-FI | CK-PG, CK-LU | — |
| CS-RT | CK-PG, CK-FI, CK-LS | CK-LU | — |

---

## 5. Scenario → Commercial Knowledge kinds

| Scenario | Required kinds | Optional | Conditional |
|----------|----------------|----------|-------------|
| CS-ID | Analytical | Consultation | Risk if weak structure |
| CS-CA | Consultation, Action, Analytical | Opportunity, Strategy | Risk+Mitigation if hostile signals |
| CS-CC | Action, Risk, Mitigation, Consultation, Opportunity | Strategy | — |
| CS-PR | Opportunity, Action, Consultation | Strategy | Risk+Mitigation if officer strain |
| CS-BU | Consultation, Action, Risk, Mitigation | Strategy, Opportunity | — |
| CS-ST | Opportunity, Risk, Mitigation, Action, Strategy | Practical Guidance | — |
| CS-LE | Analytical, Consultation, Practical Guidance | Action | Risk+Mitigation if strain |
| CS-IV | Risk, Mitigation, Action, Consultation | Opportunity | — |
| CS-FI | Consultation, Practical Guidance, Action | Risk, Mitigation, Opportunity | — |
| CS-PP | Action, Risk, Mitigation, Consultation | Opportunity | — |
| CS-MA | Consultation, Risk, Mitigation, Action | — | ethics templates required |
| CS-DT | Consultation, Practical Guidance | Risk, Mitigation | — |
| CS-CH | Consultation, Practical Guidance | Risk | ethics templates required |
| CS-PA | Consultation, Action | Mitigation | — |
| CS-HE | Practical Guidance, Action, Risk, Mitigation | — | non-medical flag required |
| CS-LS | Practical Guidance, Action | Analytical | — |
| CS-ED | Consultation, Opportunity, Action | Practical Guidance | — |
| CS-PG | Life Strategy, Analytical, Action | Opportunity | — |
| CS-LT | Consultation, Action, Opportunity | Risk, Mitigation | Risk+Mitigation if clash period |
| CS-MD | Action, Risk, Mitigation, Opportunity | Strategy | — |
| CS-EN | Practical Guidance, Consultation | Action | — |
| CS-TR | Practical Guidance, Opportunity | Risk, Mitigation | — |
| CS-RL | Action, Risk, Mitigation, Opportunity, Strategy, Consultation | — | — |
| CS-ENP | Strategy, Consultation, Action, Risk, Mitigation | Opportunity | — |
| CS-RT | Strategy, Practical Guidance, Action | Risk, Mitigation | — |

---

## 6. Scenario → Evidence relationships

| Evidence kind | Typical scenarios requiring it | Cardinality pattern |
|---------------|--------------------------------|---------------------|
| identity | CS-ID, CS-PG, CS-MD, CS-RL, defaults | Required for identity-led; optional elsewhere |
| strength | CS-ID, CS-PR, CS-ST, CS-ED | Optional→Required when opportunity claimed |
| weakness | CS-ID, warnings | Conditional on analytical weakness |
| risk | CS-CC, CS-IV, CS-ST, CS-MA, CS-HE, CS-MD… | Conditional on hostile signals; Required for decision scenarios once signal fires |
| action | Most T0/T1 scenarios | Required for decision & recommendation-led |
| grade | CS-ID, general Result | Optional |
| explanation | CS-ID, CS-PG, CS-LE | Required for Reasoning depth |
| implication | Life scenarios (CA, FI, MA, …) | Required for Impact |

---

## 7. Scenario → Interpretation focus

Interpretation remains structural (Pack 04 sections). Scenarios **weight** which sections must be commercially usable:

| Scenario group | Interpretation emphasis (required) | Optional |
|----------------|------------------------------------|----------|
| Identity / Growth | strength, pattern, summary | ten_gods |
| Career / Leadership / Promo | useful_god, ten_gods, pattern | luck, scoring |
| Business / Startup / Invest | useful_god, luck, combination/conflict | pattern |
| Finance / Property | useful_god, luck | ten_gods wealth |
| Relationship family | relation-oriented outputs when available | luck |
| Health / Lifestyle | temperature, five_elements, strength | shensha |
| Luck Timing / Major Decisions | luck, useful_god, strength | conflict |
| Environment / Travel / Relocation | useful_god, luck, temperature | — |

If interpretation only emits technical prose, scenario completeness fails → Narrative insufficient (known G6), not a Scenario model defect.

---

## 8. Scenario → Narrative components

| Component | Required for which scenario classes | Optional | Conditional |
|-----------|-------------------------------------|----------|-------------|
| Executive Summary | All T0; all decision scenarios | Adjacent | — |
| Observation | Identity-led; default Result | Others | — |
| Reasoning | Identity, Growth, Leadership, Entrepreneurship | Short scenarios | When customer asks “why” |
| Impact | All life scenarios | Pure identity | — |
| Recommendation | All decision & action scenarios | Pure observation | — |
| Warning | — | Soft scenarios | **Required** when Risk evidence present |
| Conclusion | All T0/T1 | T3 short | — |

**Hard rule:** If Risk evidence is selected for a scenario, Warning becomes **Required**, and Mitigation action should be present (`02` / CQ-5).

---

## 9. Scenario → NarrativeResult

| NarrativeResult field | Relationship |
|-----------------------|--------------|
| `sections[]` / components | Filled per §8 |
| `summary` slots | identity/strengths/weaknesses/priority/next_action themed by scenario |
| `recommendations[]` | From Action Knowledge for scenario |
| `status` | `complete` only if Required profile satisfied; else `partial_insufficient` |
| `trace` | Must include knowledge/evidence ids used for scenario |

Portal and Report consume NarrativeResult — they do not redefine scenario relationships.

---

## 10. Multi-scenario sessions

| Case | Rule |
|------|------|
| Single explicit scenario | Use that profile |
| Default Result Page | CS-ID + CS-LT light + CS-MD light |
| Two scenarios (e.g. Career + Marriage) | Union of Required; Conflict handling per `09` |
| Contradictory actions | Priority: safety/ethics > Risk mitigation > scenario-specific Action > generic Action |

---

## 11. Forbidden relationships

| From | To | Forbidden |
|------|----|-----------|
| Scenario | Rule Database | Scenario must not author rules |
| Scenario | Narrative grammar | Scenario must not add sections |
| Portal | Scenario advice strings | UI must not own advisory SSOT |
| Scenario | Analysis invention | Scenario cannot invent signals |

---

## 12. Stop line

Scenario relationships documented.  
No runtime wiring in this sprint.

---

END
