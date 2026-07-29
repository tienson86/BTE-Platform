# BTE Platform — Changelog

All notable changes to BTE Platform are documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/).  
Versioning follows [VERSION_POLICY.md](VERSION_POLICY.md).

---

## [1.0.0] — 2026-07-27

**Release name:** Production Stable  
**Architecture:** V1.0 Frozen

### Summary

First official production release. Implements a locked linear pipeline with Single Source of Truth per engine slice, central `AnalysisResult` object, frozen API and Portal contracts, production certification, stabilization with 105-case smoke validation, and complete release documentation.

### Added

- **Production pipeline:** Calendar → Bazi → Pattern → Score → Interpretation → Report → AnalysisResult → API → Portal
- **AnalysisResult** with authoritative views: `BaziView`, `PatternView`, `ScoreView`, `InterpretationView`, `ReportView`, `NarrativeView`
- **Truth modules:** `bazi_truth`, `pattern_truth`, `score_truth`, `interpretation_truth`, `report_truth`
- **Report Engine terminal path:** `ReportEngine.render_from_analysis()` — sole producer of portal report/narrative JSON
- **Interpretation portal serialization:** `engines/interpretation_engine/portal_view.py`
- **API endpoints:** `/api/v1/calendar` through `/api/v1/analyze` with unified `BirthRequest` / `APIResponse`
- **Customer Portal:** analyze → ResultStore → result tabs (no re-POST on result page)
- **Production smoke suite:** 105 real-world cases (`validation/production_smoke_runner.py`)
- **Release documentation:** `docs/releases/` (architecture freeze, API contract, AnalysisResult contract, RC1, release notes)
- **Project governance:** `docs/project/` (roadmap, versioning, contributing, standards, workflow)
- **Certification & stabilization docs:** `docs/production_*.md`
- **Phase regression tests:** unified truth tests for Bazi, Pattern, Score, Interpretation, Report (API module)

### Changed

- Orchestrator wires SSOT slices only; removed `_shape_interpretation` and `_shape_report_like` from production path
- Narrative produced inside Report Engine ( `NarrativeEngine` not on production orchestrator path)
- API serializes `analysis.*_dict()` without engine reshaping for interpretation/report

### Improved

- RuleContext built once in Pattern Engine; Score appends score slice only
- Portal presenters consume commercial JSON only (no internal engine fields on wire)
- Production readiness tests for portal-facing payload hygiene
- Bazi calendar regression coverage (Li Chun, critical 1987-01-21 case)

### Deprecated

- Production use of `NarrativeEngine.compose()` in orchestrator (module retained for legacy/audit)
- Production use of `ReportEngine.render(interpretation)` for API path (retained for tests)
- Orchestrator shaping of interpretation/report (superseded by engine portal views)

### Removed

- Nothing from public API or Portal contracts (backward compatibility preserved)

### Known issues

| ID | Severity | Summary |
|----|----------|---------|
| BUG-PROD-001 | Medium | `timezone` parameter not applied |
| BUG-PROD-002 | Medium | Golden dataset requires `jsonschema` |
| BUG-PROD-003 | Medium | Cold-start analyze latency ~2s |
| BUG-PROD-004–009 | Low/Info | Docstring drift, narrative=report, legacy tests, Portal fallbacks |

Full list: `docs/production_bug_tracker.md`

### Milestones (development history)

| Milestone | Date | Phase |
|-----------|------|-------|
| Architecture Lock | 2026-07 | Phase 1 — contract definition |
| Unified Bazi Truth | 2026-07 | Phase 2 |
| Unified Pattern Truth | 2026-07 | Phase 3 |
| Unified Score Truth | 2026-07 | Phase 4 |
| Unified Interpretation Truth | 2026-07 | Phase 5 |
| Unified Report Truth | 2026-07 | Phase 6 |
| Production Architecture Certification | 2026-07-27 | Phase 7 — Conditional PASS |
| Production Stabilization | 2026-07-27 | Smoke 105/105, bug tracker |
| Release Candidate RC1 | 2026-07-27 | Go decision |
| Official Release 1.0.0 | 2026-07-27 | Production Stable |

---

## [Unreleased]

Planned work tracked in `docs/project/PRODUCT_ROADMAP.md`:

- V1.0.x — maintenance, performance, knowledge expansion
- V1.1 — Legacy cleanup, Calendar SSOT, Golden Dataset
- V1.2 — Narrative / sentence quality
- V1.3 — PDF export
- V1.4 — CRM / case management
- V2.0 — Architecture review

---

## Version links

| Version | Documentation |
|---------|---------------|
| 1.0.0 | [Release notes](../releases/release_notes_v1.0.0.md) · [Version doc](../releases/version_1_0_0.md) |

---

**Maintainers:** Update this file on every release. One section per version. No source code in changelog entries.
