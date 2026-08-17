# BETA0 Architecture Lock

| Field | Value |
|-------|-------|
| Document | BETA0_ARCHITECTURE_LOCK |
| Date | 2026-08-17 |
| Status | **FROZEN** |
| Owner | Architecture Board + Product Owner |
| Prior freeze | `knowledge/docs/platform/ARCHITECTURE_FREEZE.md` (AF-1, 2026-08-09) |

---

## 1. Final architecture

BTE V1.0 commercial path:

```
Presentation
  Portal · Result Page · ViewModels · Adapters
        ↓
Application
  API · ProductionEndToEndOrchestrator · Auth / Cases
        ↓
Publishing
  Published Narrative Builder · Professional Report Publisher
        ↓
Narrative
  Narrative Composer V2 → NarrativeResult
        ↓
Interpretation
  Interpretation Engine / foundation interpreters
        ↓
Analysis / Decision / Luck
  Score · Pattern · Strength · Useful God · Temperature · Luck
        ↓
Chart
  Calendar Engine · BaZi Engine · Ten Gods · Shen Sha facts
        ↓
Knowledge
  Rule Database (CSV-first) · Knowledge packages · Concept / Canon
```

Higher layers consume lower layers through Public APIs and Result objects only.

Reverse imports are forbidden.

---

## 2. Canonical pipelines (already frozen)

| Pipeline | Order |
|----------|-------|
| Analysis | calendar → four pillars → seasonal → strength → temperature → pattern → pattern evaluation → useful god |
| Decision | useful god foundation → priority → override |
| Luck | timeline → analysis → decision |
| Interpretation | foundation → knowledge selection → composition |
| Narrative | Decision → State → Relationship → Knowledge → Composer → Published Narrative → Professional Publisher |
| Report | commercial builder → HTML → PDF |

These pipelines are the only supported execution models for Beta.

---

## 3. Engine principle

One Engine · One Responsibility.

An engine may calculate, decide, or format.
It may not take a second engine’s job.

---

## 4. Explicit prohibition

During Beta, **no additional** of the following may be introduced without Product Owner approval:

- Engine
- Framework
- Matrix
- Publisher
- Composer
- Canon
- Layer
- Runtime component

Existing surfaces remain. New ones require signoff.

In particular, do **not** start:

- Story Engine
- Case Identity Engine
- Luck Domain rewrite
- Temperature Domain rewrite
- a second Narrative Composer
- a second Professional Publisher
- a new knowledge canon beside Editorial Standard V1

---

## 5. What may still happen

Inside frozen boundaries:

- Bug fixes
- Editorial filtering improvements
- Knowledge record improvements
- Engine correctness inside the existing owner
- Product consultation quality

Those are not architecture changes.

---

## 6. Architecture Change

Any change that:

- adds a subsystem
- changes pipeline order
- changes public engine identity
- splits or merges frozen ownership
- introduces a new consumer contract

is an **Architecture Change**.

It requires Product Owner approval before work starts.

---

## 7. Official status

**Architecture is frozen for Beta 0.**
