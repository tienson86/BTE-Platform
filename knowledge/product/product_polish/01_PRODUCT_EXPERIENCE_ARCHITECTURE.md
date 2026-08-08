# 01 — Product Experience Architecture

Version: 1.0.0  
Status: **OFFICIAL — Design Reference**  
Date: 2026-08-08  
Sprint: Product Polish V1 · Sprint A  
Scope: Architecture only — no implementation  

---

## 1. Mission

Define the Product Experience layer so the Result Page behaves as a **commercial consulting experience**, not a data dump of Engine outputs.

Commercial V1 context: **RC1**. Engines, Foundation, Knowledge, Narrative, and Portal architecture remain frozen.

---

## 2. Layer stack

```
Product Layer
        ↓
Presentation Layer
        ↓
Narrative Layer
        ↓
Knowledge Layer
        ↓
Engine Layer
```

Each layer has one job. Lower layers never decide customer journey. Upper layers never recalculate BaZi truth.

---

## 3. Layer responsibilities

### 3.1 Product Layer

| Aspect | Definition |
|--------|------------|
| **Owns** | Customer outcome, Capability framing, reading journey, CTA strategy, commercial priority |
| **Decides** | What the customer should understand first; which Capability is primary vs secondary; when to upsell |
| **Does not** | Compute scores, author Knowledge Units, invent Design System tokens, add Portal routes |
| **Artifacts** | This pack · Capability Registry · Release Management · consulting acceptance |

### 3.2 Presentation Layer

| Aspect | Definition |
|--------|------------|
| **Owns** | How Product intent appears inside frozen Result zones/rows/cards |
| **Decides** | Density, hierarchy emphasis, progressive disclosure, card copy framing, CTA placement *within existing slots* |
| **Does not** | Change PACK_06 zone order; redesign layout patterns; invent spacing/type scales |
| **Depends on** | Design System · Visual Language · Foundation (frozen) |

### 3.3 Narrative Layer

| Aspect | Definition |
|--------|------------|
| **Owns** | Composed consulting prose (NarrativeResult), executive composition, recommendation structure |
| **Decides** | Sentence selection/merge within enrich-only rules |
| **Does not** | Replace Interpretation facts; invent Capability truth; own Portal layout |
| **Status this sprint** | **Frozen** — Product Experience designs *how* Narrative is consumed, not Narrative Engine changes |

### 3.4 Knowledge Layer

| Aspect | Definition |
|--------|------------|
| **Owns** | Knowledge Units, Domain Capability content, commercial retrieval allow-lists |
| **Decides** | What consulting content exists for a Capability |
| **Does not** | Control Result reading order or visual hierarchy |
| **Status this sprint** | **Frozen** |

### 3.5 Engine Layer

| Aspect | Definition |
|--------|------------|
| **Owns** | Calendar → Bazi → Score → Pattern → Interpretation → Report pipeline truth |
| **Decides** | Analytical results and evidence |
| **Does not** | Speak as the commercial product voice; own CTAs |
| **Status this sprint** | **Frozen** |

---

## 4. Boundaries (hard rules)

| From → To | Allowed | Forbidden |
|-----------|---------|-----------|
| Product → Presentation | Experience requirements, hierarchy, CTA intent | Token invention, new routes |
| Presentation → Narrative | Consume NarrativeResult / adapters | Rewrite Engine truth |
| Narrative → Knowledge | Enrich from approved KUs | Hard-code rules replacing KU data |
| Knowledge → Engine | Read Engine results as context | Write Engine state |
| Any upper → Engine | Read-only via public APIs | Cross-import / reverse dependency |

```
Capability Released  ≠  Experience polished
Commercial RC1       ≠  Product Experience complete
```

---

## 5. Experience contract (Result Page)

The Result Page must deliver, in order of product obligation:

1. **Trust** — identity + clear consulting posture  
2. **Understanding** — who I am, strengths, challenges  
3. **Direction** — career (and secondary milestones)  
4. **Action** — primary recommendation with clear next steps  
5. **Evidence** — why the advice is grounded  
6. **Detail** — charts, tables, technical depth on demand  

Aligned with Experience Principles: trust → understanding → action.

---

## 6. Success criteria

| ID | Criterion | Pass signal |
|----|-----------|-------------|
| PE-01 | Customer can state the main advice in ≤30 seconds | Exec + primary Rec answer without scrolling to charts |
| PE-02 | One primary commercial question owns the page | Career Strategy primary; Promotion secondary (Commercial V1) |
| PE-03 | Every visible card answers one question | Per `06_CARD_RESPONSIBILITY.md` |
| PE-04 | Technical data never outranks advice | Priority model `02` / `04` respected |
| PE-05 | CTAs exist without new routes | Per `07_CALL_TO_ACTION_STRATEGY.md` |
| PE-06 | No frozen-layer mutations | Engines / Foundation / Knowledge / Narrative / Portal routes unchanged |

---

## 7. Non-goals (Sprint A)

- UI implementation  
- Design System / PACK_06 redesign  
- Narrative Engine or KU edits  
- New Portal routes or Result zones  
- Declaring Commercial V1 Released  

---

## 8. Stop line

Product Experience Architecture defined.  

Use this document as the **official design reference** for Product Polish V1.

---

END
