# 00 — Knowledge Model Index

Version: 1.2  
Status: **SPRINT A–B FROZEN · SPRINT C — Knowledge Unit Model**  
Date: 2026-08-08  
Epic: Knowledge Model (EPIC 2)  
Sprint: A–B (frozen) + C (atomic unit architecture)  
Scope: Documentation only — no records, no CSV/JSON population, no runtime  

---

## 1. Purpose

This index is the entry point for the **official Commercial Knowledge Model**.

Epic 1 (Coverage Audit) showed that BTE’s bottleneck is not calculation, not frozen architecture, and not Narrative runtime — it is the **commercial knowledge model**: how advisory meaning is organized so Analysis becomes professional consultation.

Sprint A defines that model. It does **not** author knowledge records.

---

## 2. Reading order

| Order | File | Read when |
|------:|------|-----------|
| 0 | `00_KNOWLEDGE_MODEL_INDEX.md` | Always first |
| 1 | `01_CONSULTATION_KNOWLEDGE_MODEL.md` | How a consultant thinks (domains & questions) |
| 2 | `02_COMMERCIAL_KNOWLEDGE_MODEL.md` | How commercial knowledge is organized (layers & kinds) |
| 3 | `03_NARRATIVE_KNOWLEDGE_MODEL.md` | How Narrative consumes knowledge (traceability) |
| 4 | `04_KNOWLEDGE_RELATIONSHIP_MAP.md` | Cross-system dependency diagrams |
| 5 | `05_KNOWLEDGE_EXPANSION_GUIDELINES.md` | Rules for future population |
| 6 | `06_CONSULTATION_SCENARIOS.md` | Customer scenario taxonomy (Sprint B) |
| 7 | `07_SCENARIO_RELATIONSHIP_MODEL.md` | Scenario → knowledge → narrative bindings |
| 8 | `08_DECISION_SUPPORT_MODEL.md` | Decision-support scenarios |
| 9 | `09_KNOWLEDGE_RETRIEVAL_MODEL.md` | Retrieval / ranking / fallback (design) |
| 10 | `10_SCENARIO_EXPANSION_GUIDE.md` | How to add future scenarios |
| 11 | `11_KNOWLEDGE_UNIT_MODEL.md` | Atomic Knowledge Unit definition (Sprint C) |
| 12 | `12_KNOWLEDGE_UNIT_SCHEMA.md` | Logical schema (no JSON/CSV) |
| 13 | `13_KNOWLEDGE_COMPOSITION_MODEL.md` | How units compose into consultation |
| 14 | `14_KNOWLEDGE_LIFECYCLE.md` | Draft → Published → Deprecated |
| 15 | `15_KNOWLEDGE_AUTHORING_STANDARD.md` | Authoring / naming / maintenance |

**Suggested path for reviewers (Sprint A):** 00 → 01 → 02 → 03 → 04 → 05.  
**Suggested path for reviewers (Sprint B):** 00 → 06 → 07 → 08 → 09 → 10 (with A as prerequisite).  
**Suggested path for reviewers (Sprint C):** 00 → 11 → 12 → 13 → 14 → 15 (with A–B as prerequisite).  
**Suggested path for content authors (after approval):** 00 → 15 → 14 → 12 → 11 → 05 → 10 → 06.

---

## 3. Dependency graph

```
Epic 1 Audit (knowledge/knowledge_enhancement/01–07)
        ↓
Sprint A Commercial Knowledge Model (this folder)
        ↓ (after architecture review)
Future content epics (records / CSV / evidence units)
        ↓ (separate implementation epics only when approved)
Loaders / Interpretation commercial evidence / Narrative fill
        ↓
Portal Result Page / future Report consumers
```

Internal document dependencies:

```
01 Consultation Knowledge Model
        ↓ defines domains & questions
02 Commercial Knowledge Model
        ↓ defines knowledge kinds & organization
03 Narrative Knowledge Model
        ↓ binds kinds → evidence → Pack 05 components
04 Knowledge Relationship Map
        ↓ places model in system topology
05 Knowledge Expansion Guidelines
        ↓ governs all future authoring
06 Consultation Scenarios          (Sprint B)
        ↓ customer intent entry points
07 Scenario Relationship Model
        ↓ required/optional/conditional bindings
08 Decision Support Model
        ↓ decision-centric specialization
09 Knowledge Retrieval Model
        ↓ how Narrative selects knowledge (design)
10 Scenario Expansion Guide
        ↓ governs future scenarios
11 Knowledge Unit Model            (Sprint C)
        ↓ atomic advisory building block
12 Knowledge Unit Schema
        ↓ logical fields
13 Knowledge Composition Model
        ↓ multi-unit assembly
14 Knowledge Lifecycle
        ↓ draft → published → deprecated
15 Knowledge Authoring Standard
        ↓ how authors write units
```

---

## 4. Architectural thesis (locked for Sprint A)

| Statement | Meaning |
|-----------|---------|
| Commercial Knowledge is **not** Rule Database | Rules calculate / match; knowledge advises |
| Commercial Knowledge is **not** Narrative | Narrative composes; knowledge supplies meaning |
| Commercial Knowledge **bridges** Analysis → Advisory | Transforms technical outputs into consultant capability |
| Every Narrative component must be **traceable** to Knowledge | No invented commercial claims in UI or composer |
| V1 layer direction remains frozen | Knowledge → Analysis → Interpretation → Narrative → API → Portal |

---

## 5. Relationship to frozen / adjacent systems

### 5.1 Foundation (UI / brand / experience)

| Concern | Owner | Commercial Knowledge role |
|---------|-------|---------------------------|
| Product Manifesto, Experience, Brand, Visual, Design System | Foundation (frozen) | Must obey consultant voice; does not redefine layout/tokens |
| Trust → understanding → action | Experience Principles | Knowledge supplies understanding & action content |

Commercial Knowledge **does not** modify Foundation documents.

### 5.2 Interpretation (Pack 04)

| Concern | Owner | Commercial Knowledge role |
|---------|-------|---------------------------|
| InterpretationResult, evidence collection, sentence matching | Interpretation Engine | Consumes commercial knowledge as explainable / selectable evidence units |
| Technical rule prose | Must be filtered | Commercial Knowledge must be authored as **non-technical** advisory units |

Sprint A does **not** change Interpretation Engine code.

### 5.3 Narrative (Pack 05)

| Concern | Owner | Commercial Knowledge role |
|---------|-------|---------------------------|
| NarrativeTree, Composer, NarrativeResult (7 sections) | Narrative Engine | Consumes evidence kinds; does not invent analysis |
| Content Quality Release B | Prose bar | Commercial Knowledge must be sufficient to meet Exec / Rec / Warning standards |

Sprint A does **not** change Narrative Engine code.

### 5.4 Report

| Concern | Owner | Commercial Knowledge role |
|---------|-------|---------------------------|
| Delivery markdown / Report Engine | Report path (not redesigned) | Future Report must consume NarrativeResult, not scrape ad-hoc knowledge |
| Print / long-form consultation | Future | Same knowledge SSOT as Portal narrative |

### 5.5 Future Knowledge Packs

| Pack type | Role relative to this model |
|-----------|-----------------------------|
| Structural analytical packs (strength, pattern, …) | Feed **Analytical Knowledge** inputs; not commercial SSOT |
| Life-topic packs (career, marriage, …) | Populate **Consultation Domains** under this model |
| `database/20_knowledge` (future population) | Primary **explainable commercial corpus** candidate |
| BaZi blueprint modules | Academic / domain authoring aligned to Consultation Domains |
| Knowledge Canon / References | Citation & terminology SSOT — linked, not duplicated |

Future packs must declare which **Commercial Knowledge Kind** and **Consultation Domain** they serve (see `02`, `05`).

---

## 6. What Sprint A deliberately excludes

- Knowledge records (JSON / CSV / markdown academic bodies)  
- Database population  
- Runtime / loaders / engine edits  
- Portal / Report implementation  
- Golden Dataset / snapshot changes  

---

## 7. Success criteria (Sprint A)

| Criterion | Met when |
|-----------|----------|
| Model fully defined | Files 01–05 approved (Sprint A — done) |
| Scenario taxonomy defined | Files 06–10 approved (Sprint B — done) |
| Knowledge Unit defined | Files 11–15 complete (Sprint C) |
| Layer responsibilities clear | Rule ≠ Unit ≠ Evidence ≠ Narrative ≠ Scenario |
| Expansion blueprint ready | Files 05 + 10 + 15 |
| Traceability defined | Files 03 + 07 + 09 + 11–13 |
| Advisory SSOT declared | Commercial Knowledge = composed Knowledge Units; Scenario is entry point only |

---

## 8. Stop line

Sprint A–B are **frozen**.  
Sprint C ends at architecture review.  
**Do not create Knowledge Units / records. Do not populate database/20_knowledge. Do not implement runtime.**

---

## 9. Related Epic 1 inputs

| File | Use in Sprint A |
|------|-----------------|
| `../01_KNOWLEDGE_COVERAGE_AUDIT.md` | Domain inventory & readiness baseline |
| `../02_KNOWLEDGE_GAP_ANALYSIS.md` | Gap taxonomy feeding model kinds |
| `../03_RULE_COVERAGE_REPORT.md` | Rule vs knowledge separation |
| `../04_EVIDENCE_COVERAGE_REPORT.md` | Evidence kinds Narrative needs |
| `../05_NARRATIVE_SUPPORT_REPORT.md` | Component dependency |
| `../06_PRIORITY_EXPANSION_PLAN.md` | P0–P2 aligned to model later |
| `../07_KNOWLEDGE_ENHANCEMENT_ROADMAP.md` | Phase sequencing |

---

END
