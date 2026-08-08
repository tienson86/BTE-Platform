# 00 — Integration Index

Version: 1.1  
Status: **EPIC 4 · SPRINT A FROZEN · SPRINT B COMPLETE — awaiting Product Review**  
Date: 2026-08-08  
Depends on: V1 Architecture Freeze · EPIC 2 Knowledge Model · EPIC 3 Population/Golden · Wave 1.1 units  
Scope: Sprint A = contract docs; Sprint B = Wave 1.1 production integration runtime  

---

## 1. Purpose

Define how **Commercial Knowledge** (approved Knowledge Units) enters the production consultation pipeline so Narrative can consume them **without changing analytical meaning**.

Wave 1.1 units exist as Golden Baseline content but are **not yet used** by production Narrative.  
This sprint specifies the **Retrieval Contract** and integration design for Phase B implementation.

---

## 2. Reading order

| Order | File | Content |
|------:|------|---------|
| 0 | `00_INTEGRATION_INDEX.md` | This index |
| 1 | `01_RETRIEVAL_CONTRACT.md` | Official retrieval I/O contract |
| 2 | `02_PIPELINE_INTEGRATION.md` | Stage-by-stage pipeline |
| 3 | `03_COMMERCIAL_KNOWLEDGE_ADAPTER.md` | Adapter responsibilities |
| 4 | `04_NARRATIVE_INTEGRATION_SPEC.md` | How Narrative consumes CK |
| 5 | `05_EXECUTIVE_SUMMARY_MAPPING.md` | Wave 1.1 → Exec mapping |
| 6 | `06_RECOMMENDATION_MAPPING.md` | Wave 1.1 → Rec mapping |
| 7 | `07_INTEGRATION_VALIDATION.md` | Validation gates |
| 8 | `08_EPIC4_SPRINTA_FINAL_REPORT.md` | Gaps + Phase B plan |
| 9 | `09_SPRINT_B_IMPLEMENTATION_REPORT.md` | Sprint B runtime implementation |
| 10 | `10_SPRINT_B_VALIDATION_REPORT.md` | Validation gates + test results |
| 11 | `11_BEFORE_AFTER_COMPARISON.md` | Exec / Rec before vs after Wave 1.1 |

**Reviewers (Sprint A):** 00 → 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08.  
**Reviewers (Sprint B):** 09 → 10 → 11.

---

## 3. Architecture position (frozen V1)

```
Rule Database / Analysis engines     (unchanged)
        ↓
AnalysisResult                       (facts — SSOT for truth)
        ↓
Interpretation Engine                (unchanged — not modified this epic)
        ↓
Commercial Knowledge Adapter         ← NEW (spec now; impl Phase B)
  reads: Analysis + scenario + Published/Approved KUs
  emits: Commercial Knowledge Bundle → Narrative-ready evidence payload
        ↓
Narrative Runtime → Composer         (unchanged grammar; consumes enriched evidence)
        ↓
NarrativeResult
        ↓
Portal / future Report
```

**Invariant:** Adapter must not invent analytical facts.  
It only selects and shapes **advisory** Knowledge Units whose `condition` matches Analysis signals.

---

## 4. Relationship to adjacent systems

| System | Relationship |
|--------|--------------|
| **Knowledge Model (EPIC 2)** | Domains, kinds, scenarios, KU schema, retrieval model design |
| **Population / Golden (EPIC 3)** | Wave 1.1 units; Publish still HOLD until Product; integration may target `approved`/`published` allow-list |
| **Narrative Engine** | Consumes typed evidence; **no redesign** of Pack 05 sections |
| **Interpretation Engine** | **Not modified**; remains analytical/interpretive path; Adapter is additive beside it |
| **Portal** | Continues to prefer `narrative_result`; no UI change this epic |
| **Report** | Future consumer of same NarrativeResult; no Report redesign here |
| **Foundation / Design System** | Untouched |

---

## 5. Wave 1.1 integration scope (Sprint A)

| Unit | Primary integration target |
|------|----------------------------|
| KU-ID-001 | Executive Summary — identity |
| KU-ST-001 | Executive Summary — strengths |
| KU-WK-001 | Executive Summary — weaknesses (+ Warning soft) |
| KU-UG-001 | Executive Summary / Reasoning support + Rec reason |
| KU-RC-001 | Recommendation — action / next step |

No new units. No CSV edits. No Publish in this sprint.

---

## 6. Non-goals (Sprint A)

- Runtime retrieval code  
- Publishing Wave 1.1  
- Interpretation Engine changes  
- Narrative Engine redesign  
- Portal / Foundation / Rule Database edits  

---

## 7. Success criteria (Sprint A)

| Criterion | Met by |
|-----------|--------|
| Retrieval Contract defined | `01` |
| Adapter specified | `03` |
| Pipeline documented | `02` |
| Exec mapping completed | `05` |
| Recommendation mapping completed | `06` |
| Validation defined | `07` |
| Ready for implementation | `08` Phase B plan |

---

## 8. Sprint B status

Wave 1.1 production integration is implemented under `engines/commercial_knowledge/` and wired through `narrative_result_truth`.  
See `09`–`11` for implementation, validation, and before/after.

## 9. Stop line

Sprint B complete.  
**Wait for Product Review. Do not start Wave 1.2. Do not publish additional Knowledge Units.**

---

END
