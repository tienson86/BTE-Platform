# 00 — Consulting Quality Index

Version: 1.0  
Status: **EPIC 5 · SPRINT A — Consulting Quality Framework**  
Date: 2026-08-08  
Depends on: V1 Architecture Freeze · Foundation · Narrative Engine · Knowledge Model · EPIC 4 Sprint B · Wave 1.1  
Scope: **Documentation only** — no runtime, no Knowledge Units, no engine/UI changes  

---

## 1. Purpose

Define the official **Consulting Quality Framework**: how BTE evaluates consultant-quality output **before commercial release**.

Commercial Knowledge is integrated (EPIC 4 Sprint B). Wave 1.1 is the only approved knowledge source.  
This epic answers: *Is the consultation good enough for a paying customer?*

This sprint does **not** implement scoring tooling, create Knowledge Units, or modify engines.

---

## 2. Reading order

| Order | File | Content |
|------:|------|---------|
| 0 | `00_CONSULTING_QUALITY_INDEX.md` | This index |
| 1 | `01_CONSULTING_QUALITY_FRAMEWORK.md` | Quality dimensions |
| 2 | `02_CONSULTANT_REVIEW_GUIDE.md` | How humans review Exec / Rec / Warning / Narrative |
| 3 | `03_CASE_REVIEW_WORKFLOW.md` | Case → Narrative → Review → Revision → Approval |
| 4 | `04_CONSULTING_SCORECARD.md` | Official 0–10 scorecard + overall ratings |
| 5 | `05_ACCEPTANCE_CRITERIA.md` | Minimum bar for commercial release |

**Reviewers:** 00 → 01 → 02 → 03 → 04 → 05.

---

## 3. Position in the V1 stack

```
AnalysisResult          (analytical truth — frozen engines)
        ↓
Interpretation          (unchanged)
        ↓
Commercial Knowledge    (Wave 1.1 allow-list only)
        ↓
NarrativeResult         (customer-facing consultation)
        ↓
Consulting Quality      ← THIS FRAMEWORK (human evaluation)
        ↓
Commercial release gate
```

Consulting Quality evaluates the **customer-facing consultation**, not calculation correctness alone.  
Calculation may be correct while consulting quality still fails commercial release.

---

## 4. Relationship to adjacent systems

| System | Relationship |
|--------|--------------|
| **Product Manifesto** | Consultant, not calculator; trust → understanding → action |
| **Golden Knowledge Standard (EPIC 3)** | Unit-level quality; this framework is **case/output-level** |
| **Knowledge Integration (EPIC 4)** | Wave 1.1 may enrich Exec/Rec; quality judges the merged Narrative |
| **Narrative Engine** | Frozen; review consumes NarrativeResult as-is |
| **Foundation / Design System / Portal** | Untouched; no UI redesign in this epic |
| **Wave 1.1** | Sole approved commercial knowledge source for cases under review |

---

## 5. Non-goals (Sprint A)

- Runtime quality scoring  
- Automated CI gates beyond existing module tests  
- New Knowledge Units or Wave 1.2  
- Engine / Foundation / Narrative / Portal / UI / Design System changes  
- Replacing Product or Legal review for ethics claims  

---

## 6. Success criteria (Sprint A)

| Criterion | Met by |
|-----------|--------|
| Official Consulting Quality Framework defined | `01` |
| Human review workflow defined | `02`, `03` |
| Scorecard completed | `04` |
| Commercial acceptance criteria completed | `05` |

---

## 7. Stop line

Sprint A ends at Product review.  
**No implementation. No Wave 1.2. No runtime changes.**

---

END
