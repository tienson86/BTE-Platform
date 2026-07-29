# BTE Platform V1.0 — Production Known Issues

**Architecture:** FROZEN (V1.0)  
**Last updated:** 2026-07-27  
**Stabilization status:** Smoke 105/105 PASS; no Critical/High open bugs

This document lists accepted limitations, queued defects, and non-production paths. It does not authorize architectural changes.

---

## Production path status

| Layer | Status | Notes |
|-------|--------|-------|
| Pipeline order | LOCKED | Calendar → Bazi → Pattern → Score → Interpretation → Report → API |
| AnalysisResult schema | LOCKED | View slices per Phase 2–6 |
| API contract | STABLE | `BirthRequest` + `APIResponse` envelope |
| Portal binding | STABLE | Reads API JSON; no engine rebuild |
| Smoke suite | GREEN | 105 cases |

---

## Open issues (queued)

See `production_bug_tracker.md` for full repro and fix recommendations.

| ID | Severity | Summary |
|----|----------|---------|
| BUG-PROD-001 | Medium | `timezone` accepted but not applied |
| BUG-PROD-002 | Medium | Golden dataset needs `jsonschema` |
| BUG-PROD-003 | Medium | Cold-start analyze ~2s |
| BUG-PROD-004 | Low | `/narrative` docstring mentions NarrativeEngine |
| BUG-PROD-005 | Low | Narrative JSON equals report JSON |
| BUG-PROD-006 | Low | 5 legacy root pytest failures |
| BUG-PROD-007 | Low | Score.js `details.*` fallback |
| BUG-PROD-008 | Low | Portal Bazi hidden-stem display fallback |
| BUG-PROD-009 | Info | No `AnalysisResult.calendar` slice |

**None are Critical or High.** No immediate production code changes applied.

---

## Accepted design limitations (V1.0)

| Topic | Description | Portal impact |
|-------|-------------|---------------|
| Narrative = Report content | Phase 6: same markdown/html from interpretation sections | Narrative tab shows same prose as report; renders correctly |
| NarrativeEngine unused | WP7 engine exists but not wired | None — Portal uses API narrative slice |
| Calendar shaping in API layer | `_shape_calendar` in orchestrator, not CalendarEngine portal_view | Portal receives enriched `year_can_chi`, feng keys |
| Feng Shui parallel | `FengShuiEngine` enriches calendar; not on AnalysisResult | `chart_info` / calendar tab show cung_phi when gender valid |
| Missing gender | Feng block omitted; Bazi/pattern/score continue | Portal shows `--` for feng fields |
| Double serialization layer | Engine `to_portal_dict` → `*View.to_dict` | Tests verify equality; no duplicate logic |

---

## Legacy / non-production (do not use for Portal)

| Component | Location | Risk if used |
|-----------|----------|--------------|
| NarrativeEngine | `engines/narrative_engine/` | Alternate report composition |
| ReportService.build | `engines/report_engine/service.py` | Template ReportModel with internal metadata |
| IntegrationOrchestrator | `engines/integration/orchestrator.py` | Wrong pipeline order |
| InterpretationEngine.calculate | Stub text response | Not full interpretation |
| interpretation_engine/builders | Legacy builders | Not on `run()` path |
| rc1_audit_runner | Uses NarrativeEngine + old report path | Audit only |
| Root tests/test_*.py (4 files) | Obsolete imports | CI noise |

**Production orchestrator does not import these.**

---

## QA / CI exclusions

| Item | Status | Workaround |
|------|--------|------------|
| Golden dataset pytest | Blocked (`jsonschema`) | Install dep or skip in CI |
| Legacy root tests | 5 failures | Exclude in CI until Legacy Cleanup V1 |
| Portal Playwright audit | Optional | `validation/portal_qa_audit.py` needs Playwright |
| ResultStore Node test | Conditional skip | Requires Node for harness |

---

## Portal UI notes

| Area | Status | Detail |
|------|--------|--------|
| Home / Dashboard | OK | Route 200 |
| Input (Analyze) | OK | Requires full_name + birth_place client-side |
| Result tabs | OK | No re-POST; ResultStore only |
| Loading UX | OK | Button disabled + progress messages |
| Error UX | OK | Flash messages on validation/API errors |
| Executive summary | OK | `summary_builder.js` aggregates API slices |
| Reports history | OK | Reads stored `report` / `narrative` |
| Responsive layout | Manual | CSS present; visual QA on devices recommended |

**Portal does not recalculate** Bazi, score, or interpretation. Display fallbacks (`STEM_META`, `details.*`) are cosmetic only.

---

## API notes

| Topic | Behavior |
|-------|----------|
| Null gender | 200; feng_shui may be null |
| Invalid body | 422 from Pydantic |
| Stage endpoints | Partial pipeline; same orchestrator |
| `customer` block | Presentation only; not passed to engines |
| `bat_trach` echo | Only if client sent in `metadata`; never computed |
| Internal fields | Stripped from score/interpretation/report on wire |

---

## Performance expectations

| Scenario | Typical latency |
|----------|-----------------|
| Warm analyze | 150–450 ms |
| Cold first analyze | up to ~2 s |
| Stage calendar | < 100 ms |
| Stage score | 200–350 ms |

Not a correctness issue; see BUG-PROD-003.

---

## Before Legacy Cleanup V1

Stabilization should reach:

- [x] 100+ smoke cases PASS
- [x] API + Portal pytest PASS
- [x] Bug tracker populated
- [x] No Critical/High production bugs
- [ ] Golden dataset runnable (optional QA)
- [ ] Legacy root tests excluded or fixed in cleanup phase
- [ ] Timezone behavior documented for users OR implemented (product decision)

---

## Document index

| File | Purpose |
|------|---------|
| `production_architecture_certification.md` | Phase 7 architecture sign-off |
| `production_bug_tracker.md` | Active defect register |
| `production_validation_cases.md` | Case library |
| `production_smoke_report.md` | Latest smoke run |
| `production_known_issues.md` | This file |

---

## Stabilization verdict

**Production V1.0 is stable** for the frozen architecture. Remaining items are Medium/Low/Info and queued. Legacy Cleanup V1 may proceed after stakeholder sign-off on this stabilization report.
