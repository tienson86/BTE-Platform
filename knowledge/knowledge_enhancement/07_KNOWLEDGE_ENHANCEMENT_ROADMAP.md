# 07 — Knowledge Enhancement Roadmap

Version: 1.0  
Status: **OFFICIAL ROADMAP DRAFT — Awaiting review**  
Date: 2026-08-08  
Epic: Knowledge Coverage Audit (EPIC 1)  
Authority: Follows V1 Architecture Freeze; does not alter frozen layers  

---

## 1. Mission

Improve **knowledge quality** so BTE delivers commercial-grade BaZi consultation.

In scope:

- Explainable knowledge corpus  
- Commercial evidence for Narrative  
- Rule–knowledge alignment and orphan triage  
- Canon / citation integrity  

Out of scope (until separately approved):

- Architecture changes  
- Runtime / engine redesign  
- Foundation / Design System edits  
- Narrative Engine / Score Engine / Interpretation Engine modifications  
- UI polish  
- Report Engine redesign  

---

## 2. Current state (audit baseline)

| Area | State |
|------|-------|
| V1 Architecture | Frozen |
| Foundation | Frozen |
| Narrative Engine structure | Production-ready |
| Product Integration | Complete |
| Operational structural rules | Strong |
| Explainable corpus (`20_knowledge`) | 0% content |
| Commercial Narrative depth | Not consultant-grade (G6) |
| Composite commercial knowledge readiness | **~35%** |

Sources: `01_KNOWLEDGE_COVERAGE_AUDIT.md` … `06_PRIORITY_EXPANSION_PLAN.md`.

---

## 3. Roadmap phases

### Phase 0 — Audit & Gate (this epic)

| Deliverable | Status |
|-------------|--------|
| Coverage audit | Done |
| Gap analysis | Done |
| Rule coverage | Done |
| Evidence coverage | Done |
| Narrative support | Done |
| Priority plan | Done |
| This roadmap | Done |

**Gate:** Human review approval before any knowledge row expansion.

---

### Phase 1 — Commercial Evidence Foundation (P0)

**Goal:** Make Pack 05 Narrative commercially useful on structural charts.

| Workstream | Outputs |
|------------|---------|
| Evidence authoring | Commercial units: identity, strength, weakness, action, risk, implication |
| Useful God guidance | Practical do/avoid/prioritize language |
| Strength / Pattern explanations | Non-technical consultant prose |
| Warning pairs | Risk + mitigation |
| `20_knowledge` seed | FE, Ten Gods, Useful God, Strength, Patterns |

**Exit criteria:**

- Representative chart suite shows fewer `partial_insufficient` outcomes  
- Executive Summary / Recommendation / Warning meet Content Quality bar more often  
- All new rows cite REF-* / pass governance draft review  

**Implementation note:** Wiring into loaders/interpreters is a **follow-on implementation epic** after content approval; this roadmap authorizes *what* to write, not silent code change.

---

### Phase 2 — Life Domain Enablement (P1)

**Goal:** Unlock career, wealth, luck depth without architecture change.

| Workstream | Outputs |
|------------|---------|
| Orphan triage | Wire / migrate / archive decision for `08_hon_nhan`, `09_tu_tuc`, `10_tai_van`, orphan `interpretation_rules` |
| Luck guidance | Timing language for đại vận / lưu niên |
| Career + Wealth seeds | Explainable KB + commercial evidence |
| Temperature / Season guidance | Balance advice |
| Shensha curated caution set | Top stars only |
| Canon + REF remap | Fix Wood; expand stems/branches/ten gods |

**Exit criteria:**

- Documented SSOT for each life-domain rule pack  
- Career/wealth consultation themes available to commercial path (per approved wiring epic)  
- Citation IDs consistent with V1.0 SSOT  

---

### Phase 3 — Sensitive & Complete Catalog (P2)

**Goal:** Full consultation catalog with ethics.

| Workstream | Outputs |
|------------|---------|
| Marriage / Children | Ethics-first knowledge + approved caution language |
| Health | Non-medical lifestyle hints only |
| Parents / Education | Greenfield modules |
| Personality pack | Explicit module or documented ten-gods coverage |
| Transformations | Doctrine + rule alignment |
| Academic depth | BaZi JSON records, classic chapters, terminology expansion |
| Library hygiene | Sentence Library ↔ Pack 04 consolidation |

**Exit criteria:**

- Domain checklist complete for product-defined consultation scope  
- Composite readiness target ≥ 85% for in-scope domains  

---

### Phase 4 — Continuous Knowledge Ops (ongoing)

| Practice | Description |
|----------|-------------|
| Governance | Draft → Review → Official per existing policies |
| Validation | Duplicate id, missing fields, REF integrity |
| Golden consultation samples | Curated NarrativeResult exemplars (do not mutate Golden Dataset calculation fixtures without approval) |
| Coverage refresh | Re-run this audit pack on each major knowledge release |
| Compatibility | Additive CSV rows only; no column renames |

---

## 4. Official sequencing

```
Phase 0 Audit (DONE — wait for review)
        ↓ approval
Phase 1 P0 Commercial Evidence Foundation
        ↓
Phase 2 P1 Life Domain Enablement
        ↓
Phase 3 P2 Sensitive & Complete Catalog
        ↓
Phase 4 Continuous Knowledge Ops
```

Parallel allowed only when:

- Content owners differ, and  
- No conflicting SSOT decisions (especially orphan triage vs new seeds).

---

## 5. Success metrics

| Metric | Baseline | Phase 1 target | Phase 2 target |
|--------|----------|----------------|----------------|
| Commercial knowledge readiness | ~35% | ~55–60% | ~70–75% |
| `20_knowledge` content rows | 0 | Seed set populated | Career/wealth/luck added |
| Pack 05 insufficient rate (sample suite) | High (G6) | Materially reduced | Further reduced |
| Orphan life-domain rule packs | Untriaged | Triage plan approved | Executed |
| Canon domains with Official content | ~1 (Wood draft issues) | Remap + expand plan | Multiple domains Official |

Exact numeric SLAs set at Phase kickoff.

---

## 6. Risks and controls

| Risk | Control |
|------|---------|
| Invented classical quotations | Require REF-* / Academic Review |
| Medical / marital overclaim | Ethics templates; P2 only |
| Duplicating rules across CSV/JSON | Mapping policy before authoring |
| Quiet engine changes under “knowledge” banner | Strict: content first; code only in approved implementation epics |
| Editing Golden Dataset / snapshots to force pass | Forbidden |
| Scope creep into UI / Report Engine | Separate epics after content gate |

---

## 7. Relationship to other freezes / releases

| Document | Relationship |
|----------|--------------|
| `knowledge/releases/v1/01_V1_ARCHITECTURE_FREEZE.md` | Must not violate |
| Content Quality Release B | Defines prose bar this roadmap feeds |
| Product Integration G6 | Primary commercial symptom this roadmap addresses |
| BaZi Blueprint roadmap | Scholarly module population aligns under Phase 2–3 |
| Foundation freeze | References/terminology extend additively |

---

## 8. Decision log (open)

| Decision | Options | Needed before |
|----------|---------|---------------|
| SSOT for commercial sentences | Pack 04 library vs `sentence_library` vs `20_knowledge` retrieval | Phase 1 kickoff |
| Orphan packs | Wire vs migrate vs archive | Phase 2 |
| Feng Shui in core product | In / out / hint-only | Phase 2–3 |
| Life domains as Narrative sections vs thematic evidence only | Product choice | Phase 2 |

---

## 9. Immediate next step

1. Review this `knowledge/knowledge_enhancement/` package.  
2. Approve or amend P0 list.  
3. Authorize Phase 1 content authoring epic.  
4. **Do not expand knowledge until that authorization.**

---

## 10. Package index

| File | Title |
|------|-------|
| `01_KNOWLEDGE_COVERAGE_AUDIT.md` | Domain inventory & coverage % |
| `02_KNOWLEDGE_GAP_ANALYSIS.md` | Missing rules / mappings / explanations / edges / examples / guidance |
| `03_RULE_COVERAGE_REPORT.md` | Implemented / partial / missing / orphan |
| `04_EVIDENCE_COVERAGE_REPORT.md` | Evidence sufficiency for Exec / Rec / Warning / Narrative |
| `05_NARRATIVE_SUPPORT_REPORT.md` | Pack 05 component support map |
| `06_PRIORITY_EXPANSION_PLAN.md` | P0 / P1 / P2 |
| `07_KNOWLEDGE_ENHANCEMENT_ROADMAP.md` | This roadmap |

---

## 11. Stop line

**EPIC 1 complete.**  
Await review before expanding knowledge.

---

END
