# BaZi Blueprint — Future Development Roadmap

**Sprint:** BaZi Knowledge Blueprint V1.0  
**Date:** 2026-07-31  
**Status:** Awaiting Architecture Review  

---

## Phase 0 — Complete (this sprint)

- Scaffold `knowledge/bazi/` with 14 modules
- Authoring docs + templates + empty record directories
- Blueprint reports

---

## Phase 1 — Architecture Review (next)

1. Confirm module boundaries and dependency graph
2. Confirm ID allocation ranges for BaZi Knowledge Records
3. Decide relationship to Knowledge Canon (link vs duplicate policy)
4. Approve first content modules to populate

---

## Phase 2 — Pilot content (authorized modules only)

Suggested pilot order (subject to Architecture Review):

1. `01_fundamental_knowledge`
2. `06_ten_gods_knowledge`
3. `02_strength_knowledge`
4. `03_temperature_knowledge`
5. `05_useful_god_knowledge`

Rules:

- No invented references/terminology
- Use Foundation `REF-*` / `TERM-*`
- Keep uncertain fields as `TODO_REVIEW`
- Do not modify Foundation / Canon / schemas unless authorized

---

## Phase 3 — Structural + topic expansion

1. `04_pattern_knowledge`
2. `07_combination_knowledge`
3. `08_shensha_knowledge`
4. `09_luck_knowledge`

---

## Phase 4 — Life-topic modules

1. `10_marriage_knowledge`
2. `11_career_knowledge`
3. `12_wealth_knowledge`
4. `13_health_knowledge`
5. `14_children_knowledge`

These SHOULD consume earlier structural modules rather than redefine core theory.

---

## Phase 5 — Integration (separate authorization)

- Rule Database mapping
- Interpretation / Report consumption
- Automated citation + relationship CI checks

---

## Non-goals until authorized

- Academic record population in this blueprint tree (done only after review)
- Engine / scoring / interpretation logic
- Foundation or Canon edits
