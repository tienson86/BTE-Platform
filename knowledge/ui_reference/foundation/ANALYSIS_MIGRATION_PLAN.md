# ANALYSIS_MIGRATION_PLAN.md

Version: 1.0  
Date: 2026-08-07  
Epic: Analysis Experience Unification  
Status: **PLAN ONLY** — no code migration in this epic

---

## 1. Goal

Migrate all analysis viewing to the official flow:

```
/analyze → ResultStore → /result → PortalPage → ResultPageBody
```

Preserve:

- Result Page architecture freeze
- Visual Language V2
- Foundation V1.0
- Analyze API contracts

---

## 2. Official Analysis Flow (Target)

| Step | Owner | Action |
|------|-------|--------|
| 1 | User | Opens `/analyze`, submits birth data |
| 2 | Portal JS | Persists payload via ResultStore |
| 3 | Portal | Redirects / navigates to `/result` |
| 4 | `resultApp.tsx` | Boots `PortalPage` with request or stored data |
| 5 | Service | `getCanonicalDesktopViewModel` |
| 6 | UI | Zones render `ResultPageViewModel` |

**Single SSOT UI:** `applications/customer_portal/src/screens/result/`  
**Single SSOT host:** `PortalPage`  
**Single SSOT adapter chain:** `canonicalDesktopAdapter` → `resultPresentationAdapter`

---

## 3. Migration Waves

### Wave U0 — Policy (docs / process) ✅ this epic

- Inventory + deprecation list + this plan
- Declare Result Page the only Analysis Experience in docs
- Block new feature work on deprecated stacks (review policy)

### Wave U1 — Traffic & entry consolidation (P0)

| Task | Description | Effort | Risk |
|------|-------------|--------|------|
| U1.1 | Ensure all product links use `/result` (not legacy) | S | Low |
| U1.2 | Soft-deprecate `/result?legacy=1` (banner or docs-only first) | S | Low |
| U1.3 | Confirm `/analyze` always lands on official `/result` | S | Low |
| U1.4 | Document “no new mounts” for BaZi/WP screens | S | Low |

**Do not delete code in U1.**

### Wave U2 — Adapter / hook consolidation (P1)

| Task | Description | Effort | Risk |
|------|-------------|--------|------|
| U2.1 | Prefer `useCanonicalDesktopResult` for all analysis consumers | M | Med |
| U2.2 | Mark `getBaZiResultViewModel` / `useBaZiResult` deprecated in code comments / docs | S | Low |
| U2.3 | Stop extending `adaptAnalysisToBaZiResult` mappings | S | Low |
| U2.4 | Keep wrappers if tests still need BaZi VM (compatibility) | M | Med |

### Wave U3 — UI stack retirement (P1–P2)

| Task | Description | Effort | Risk |
|------|-------------|--------|------|
| U3.1 | Quarantine `screens/bazi/**` as legacy (no new features) | S | Low |
| U3.2 | Quarantine WP screens + `ConsultationReportScreen` | S | Low |
| U3.3 | Quarantine `canonical_desktop/sections` + `rows` | S | Low |
| U3.4 | Quarantine `screens/s00` | S | Low |
| U3.5 | Redirect or remove legacy HTML presenters after U1 soak | M | Med |
| U3.6 | Eventually remove dead mounts/tests in a dedicated cleanup epic | L | Med |

**Deletion is a later epic.** This plan only schedules quarantine then cleanup.

### Wave U4 — Presentation dedupe (P2)

| Task | Description | Effort | Risk |
|------|-------------|--------|------|
| U4.1 | Route all truncation through PACK_04 presentation helpers | M | Low |
| U4.2 | Avoid reimplementing preview/expand in business components | M | Low |
| U4.3 | Align remaining business components used outside analysis (if any) | M | Med |

### Wave U5 — Verification (continuous)

| Gate | Criteria |
|------|----------|
| Build / tsc | Pass |
| Result module tests | Pass |
| Manual `/result` | Reading flow Context→…→Knowledge |
| No production link to legacy | Verified |
| Foundation checklist | Pass for touched modules |

---

## 4. Suggested Order

```
U0 Policy (done)
→ U1 Traffic consolidation
→ U2 Adapter preference
→ U3 Quarantine UI stacks
→ U4 Presentation dedupe
→ Later: Cleanup epic (delete unused)
```

---

## 5. Mapping — Legacy Concern → Official Zone

| Legacy / WP concern | Official Result target |
|---------------------|------------------------|
| Context / chart meta | ContextZone |
| Executive summary / indicators / direction | SummaryZone (LP-001) |
| Elements / strength / ten gods | AnalysisZone (LP-003) |
| Radar / timeline | VisualizationZone (LP-004) |
| Actions / recommendations | RecommendationZone (LP-005) |
| Narrative / explainable blocks | InterpretationZone (LP-006) |
| Glossary / refs / appendix meta | KnowledgeZone (LP-007) |
| Portal chrome | `shell/PortalChrome` (keep) |

Do **not** invent new zones during migration.

---

## 6. Compatibility Strategy

| Phase | Strategy |
|-------|----------|
| Now | Official path live; legacy code remains for tests / escape hatch |
| Soft deprecation | Docs + Cursor rules + optional UI banner on legacy |
| Hard deprecation | Remove public legacy route; keep code behind tests only |
| Cleanup epic | Delete unused modules after usage = 0 |

Backward compatibility: prefer wrappers over breaking AnalyzeService public methods until cleanup epic.

---

## 7. Out of Scope

- Redesigning Result Page zones / patterns
- Changing Engine / Score / Rule Database
- Migrating Dashboard Brand/Visual (Foundation Wave 3)
- Deleting code in this documentation epic

---

## 8. Exit Criteria

| Criterion | Done when |
|-----------|-----------|
| Single user-facing analysis UI | Only `/result` official path |
| Single adapter chain documented & preferred | Canonical → Result |
| Deprecated list enforced in review | PRs blocked from extending legacy |
| Cleanup scheduled | Separate epic ticket exists |

---

END
