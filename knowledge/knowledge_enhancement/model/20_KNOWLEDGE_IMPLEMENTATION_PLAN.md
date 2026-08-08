# 20 — Knowledge Implementation Plan

Version: 1.0  
Status: **SPRINT D — Knowledge Catalog Blueprint**  
Date: 2026-08-08  
Depends on: `16`–`19`, Epic 1 roadmap `07`, Sprint A–C  
Scope: Planning only — **no population in this sprint**  

---

## 1. Purpose

Estimate phased delivery of the Commercial Knowledge Catalog:

- Phase 1 / 2 / 3  
- Database population order  
- Commercial priority  
- Validation strategy  

Still **no CSV/JSON/runtime** here.

---

## 2. Commercial priority (unchanged thesis)

| Rank | Focus | Why |
|------|-------|-----|
| 1 | P0 Critical KUs | Kill G6 / enable Exec-Rec-Warning |
| 2 | P1 Career/Finance/Luck/Business | Highest paying consultation intents |
| 3 | P2 Sensitive + adjacent | Ethics-gated completeness |

Scenario is entry point; **Published KUs** remain advisory SSOT.

---

## 3. Phase plan

### Phase 1 — Narrative commercial foundation

| Attribute | Plan |
|-----------|------|
| **Goal** | Default Result Page reaches consultant-usable baseline |
| **Catalog scope** | All **P0** units (~42) — especially Minimum Narrative pack (`19` §7) |
| **Domains** | CK-ID, CK-DM, CK-LU, structural RK/MT, light CK-CA/LS |
| **Scenarios unlocked** | Default, CS-ID, CS-LT, CS-MD light, CS-CA light |
| **Exit criteria** | P0 Published; sample charts show material drop in `partial_insufficient`; Exec/Rec/Warning meet Content Quality bar more often |
| **Estimate** | Large content effort (authoring + 3-gate review); sizing set at kickoff |

### Phase 2 — Decision & life-domain depth

| Attribute | Plan |
|-----------|------|
| **Goal** | Career change, promotion, finance, investment, business, startup, luck depth |
| **Catalog scope** | **P1** units (~48) |
| **Domains** | CK-CA, CK-FI, CK-BU, CK-LE, CK-ED, CK-PG, CK-EN (relocation) |
| **Scenarios unlocked** | CS-CC, CS-PR, CS-FI, CS-IV, CS-BU, CS-ST, CS-ENP light, CS-ED, CS-PG, CS-RL |
| **Exit criteria** | Domain Required sets Published per `17`; decision postures used in DS-* samples |
| **Estimate** | Large; parallelizable by domain owners |

### Phase 3 — Sensitive & complete catalog

| Attribute | Plan |
|-----------|------|
| **Goal** | Ethics-complete relationship/health + adjacent scenarios |
| **Catalog scope** | **P2** units (~36) + Future backlog from `17` |
| **Domains** | CK-MA, CK-RE, CK-CH, CK-PA, CK-HE, CK-EN/TR/RT depth |
| **Scenarios unlocked** | CS-MA, CS-DT, CS-CH, CS-PA, CS-HE, CS-EN, CS-TR, CS-RT |
| **Exit criteria** | Ethics reviews passed; catalog ≥85% Published of planned 126; re-audit metrics |
| **Estimate** | Medium–Large; policy-bound |

---

## 4. Database population order

Logical order (physical store TBD — likely `database/20_knowledge` and/or evidence libraries):

```
1. Schema mapping: logical fields `12` → physical columns (additive)
2. Reserve all KU ids from `16` in a registry (still no advisory body required)
3. Author Phase 1 bodies (P0) → lifecycle to Published
4. Wire retrieval/composition (separate implementation epic after content gate)
5. Author Phase 2 (P1)
6. Author Phase 3 (P2)
7. Orphan rule triage (Epic 1) may feed new KU intents — additive only
```

**Population rules:**

| Rule | Detail |
|------|--------|
| Content before broad wiring | Prefer Published KUs exist before large runtime bets |
| Additive only | No Rule DB column renames |
| Pairs together | RK+MT always authored as pairs |
| No Golden Dataset mutation | To force Narrative pass |
| Format decision | CSV vs JSON vs Pack 04 library — choose in implementation epic; semantics from `12` |

---

## 5. Suggested authoring waves (Phase 1 detail)

| Wave | Units | Narrative unlock |
|------|-------|------------------|
| 1.1 | AN-ID-000001…000008, AN-XX-000001 | Identity / Observation / Conclusion |
| 1.2 | AC-DM-000001…000007 | Recommendation / postures |
| 1.3 | RK/MT-XX-000001…000004 | Warning pairs |
| 1.4 | CN-LU-000001, AC-LU-000001, OP-LU-000001, PG-XX-000001 | Luck + practical |
| 1.5 | CN-CA-000001, AC-CA-000001, CN-XX-000001, AN-XX-000002/3, CN-PE-000001, remaining P0 | Impact + career light |

---

## 6. Validation strategy

### 6.1 Unit-level

| Check | Method |
|-------|--------|
| Schema completeness | Checklist `15` / required fields `12` |
| No rule duplication | Technical Review |
| Analytical non-contradiction | Knowledge Review + sample Analysis signals |
| Ethics | Flagged domain reviews |
| Pair integrity | Every Published RK has Published MT |

### 6.2 Composition-level

| Check | Method |
|-------|--------|
| Scenario Required profile | Matrix `18` against Published set |
| Narrative component fill | Sample compositions per `13` |
| Dedup / conflict | Fixture scenarios with opposing Actions |

### 6.3 Product-level

| Check | Method |
|-------|--------|
| G6 insufficient rate | Fixed chart suite before/after Phase 1 |
| Content Quality bar | Exec/Rec/Warning guidelines |
| Traceability | Trace contains KU ids |
| Regression | No Foundation/Architecture/engine edits in content epics |

### 6.4 What not to do

- Do not weaken asserts or edit snapshots to fake richness  
- Do not invent KU bodies that ignore Analysis  
- Do not ship Draft units to production  

---

## 7. Dependencies on other epics

| Epic | Relationship |
|------|--------------|
| Architecture Freeze | Must not break |
| Content Quality B | Defines prose bar Phase 1 must meet |
| Retrieval implementation | After enough Published KUs |
| Report Engine redesign | Consumes NarrativeResult backed by KUs |
| Orphan rule triage | May add catalog rows later (amend `16`) |

---

## 8. Success metrics (planning)

| Metric | Baseline | Phase 1 | Phase 2 | Phase 3 |
|--------|----------|---------|---------|---------|
| Planned KUs Published | 0 / 126 | ~42 | ~90 | ~126 |
| Default Narrative commercial readiness | ~40% | ~60%+ | ~75% | ~85%+ |
| Critical CV units live | 0 | All C in P0 | + P1 C/H | Complete |
| Open GAP-N1 | Open | Closed | — | — |

---

## 9. Risks

| Risk | Mitigation |
|------|------------|
| Authoring bottleneck | Wave parallelization by kind (AN vs AC vs RK/MT) |
| Ethics delay on P2 | Keep P2 off critical path for default Result |
| Store format bikeshedding | Freeze logical schema; pick store in impl epic |
| Scope creep into engines | Content-only epics; wrappers if API additive later |

---

## 10. Stop line

Implementation plan complete.

**Sprint D complete.**  
Do **not** populate database.  
Do **not** create Knowledge Records.  
Wait for architecture review.

---

END
