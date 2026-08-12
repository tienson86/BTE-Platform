# Wave 01 Roadmap — Ten Gods

## Phase 1 — Engineering (CURRENT)

**Goal:** Verify Ten Gods Engine is complete. No redesign.

- Confirm public API: `TenGodsEngine.calculate` → `TenGodsResult`
- Confirm published fields: day_master, visible, hidden, distribution, weights, dominant, hierarchy, relationships, interaction_matrix, missing_data
- Confirm module tests PASS (`tests/ten_gods_engine`)
- Document any gap that blocks interpretation (missing publish fields only — no algorithm changes)
- Exit: Engineering verification report → Phase 1 PASS/FAIL

## Phase 2 — Knowledge

**Goal:** Author PACK_02 Interpretation Knowledge for Ten Gods. Reuse PACK-01 architecture.

Target layout (mirror PACK_01):

```
knowledge/interpretation_knowledge/PACK_02_TEN_GODS/
knowledge/knowledge_catalog/PACK_02_TEN_GODS/
knowledge/interpretation_standard/PACK_02_TEN_GODS/   # if required by PACK-01 pattern
```

Topics (system-first, not ten textbook definitions):

1. Operating structure / system meaning
2. Dominant & secondary roles
3. Pressure / support / competition relationships
4. Advantages
5. Challenges
6. Career contribution
7. Relationship contribution
8. Recommendations
9. Edge / missing-data restraint

Status on create: **Draft** until QA freeze.

## Phase 3 — Knowledge QA

**Goal:** Apply Knowledge QA Standard V1.0 topic-by-topic.

- Use `knowledge/knowledge_qa/STANDARD/`
- Create `knowledge/knowledge_qa/PACK_02_TEN_GODS/` reviews
- PASS / REVIEW / FAIL per topic
- Freeze only after review (FREEZE_POLICY)

## Phase 4 — Reasoning

**Goal:** Implement Ten Gods reasoning using frozen Reasoning model.

- Mirror `knowledge/reasoning_engine/PACK_01_STRENGTH/` → `PACK_02_TEN_GODS/`
- Implement runtime under `engines/interpretation_engine_v2/ten_gods/` (or equivalent) reusing selector / evidence gate / reasoner / planner / composer contracts
- Input: `TenGodsPublishedFacts` from canonical `TenGodsResult`
- No Reasoning redesign

## Phase 5 — Master Interpretation

**Goal:** CASE-0001 PART_02 commercial master.

- Existing: `knowledge/master_interpretations/CASE_0001/PART_02_TEN_GODS_MASTER_INTERPRETATION.md`
- Review against frozen knowledge + reasoning output
- Update only if commercial gaps found; keep immutable once Wave freeze declared

## Phase 6 — Commercial Review

**Goal:** Commercial Acceptance Review for Part 02.

- Produce `knowledge/customer_review/CASE_0001/` Part 02 review (or equivalent)
- Score commercial tone, actionability, no overclaim, system-not-definitions
- PASS required before production freeze

## Phase 7 — Production

**Goal:** Wire generic Ten Gods interpretation into production pipeline.

- Replace Sprint 4 pilot fact composer with catalog-driven V2 path
- Orchestrator remains generic — no CASE branching
- Customer Mode hides diagnostics / DRAFT labels until Frozen
- Regression: CASE-0001 + SYNTHETIC_REQUEST_B
- Exit: Wave 01 COMPLETE

---

## Estimated schedule

| Phase | Effort (relative) |
|-------|-------------------|
| 1 Engineering | 0.5 day |
| 2 Knowledge authoring | 2–3 days |
| 3 Knowledge QA | 1–2 days |
| 4 Reasoning + runtime | 2–3 days |
| 5 Master Interpretation | 0.5–1 day |
| 6 Commercial Review | 0.5 day |
| 7 Production wiring | 1 day |

**Wave estimate:** ~8–11 working days from start (sequential, one domain).
