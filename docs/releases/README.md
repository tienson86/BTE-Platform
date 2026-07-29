# BTE Platform — Release Documentation

**Current release:** 1.0.0 (Production Stable)  
**Architecture:** V1.0 Frozen  
**Last updated:** 2026-07-27

This directory contains **official release references** for BTE Platform. All future development must comply with these documents unless a new major architecture version is approved.

---

## Quick links

| Document | Description |
|----------|-------------|
| [Architecture V1 Frozen](architecture_v1_frozen.md) | Official architecture freeze — pipeline, engines, SSOT, forbidden changes |
| [Release Candidate RC1](release_candidate_rc1.md) | Go/no-go, deployment checklist, rollback |
| [Version 1.0.0](version_1_0_0.md) | Version history, milestones, roadmap |
| [API Contract V1](api_contract_v1.md) | Frozen HTTP JSON contract |
| [AnalysisResult Contract V1](analysis_result_contract_v1.md) | Field-level SSOT matrix |
| [Release Notes 1.0.0](release_notes_v1.0.0.md) | User-facing release summary |

### Project governance

| Document | Description |
|----------|-------------|
| [Project governance index](../project/README.md) | Entry point for process and standards |
| [Product roadmap](../project/PRODUCT_ROADMAP.md) | Official roadmap V1.0.x → V2.0 |
| [Version policy](../project/VERSION_POLICY.md) | Semantic versioning rules |
| [Changelog](../project/CHANGELOG.md) | Official project changelog |
| [Contributing](../project/CONTRIBUTING.md) | Branches, PRs, commit conventions |
| [Coding standards](../project/CODING_STANDARDS.md) | Engineering standards and SSOT rules |
| [Development workflow](../project/DEVELOPMENT_WORKFLOW.md) | Feature, bug, hotfix workflows |

---

## Release documentation

### Version 1.0.0 — Production Stable

- **Date:** 2026-07-27
- **Status:** Current stable release
- **Architecture:** Frozen
- **Smoke:** 105 / 105 PASS
- **Certification:** Conditional PASS (Phase 7)

Start here: [release_notes_v1.0.0.md](release_notes_v1.0.0.md)

---

## Architecture documents

| Document | Location |
|----------|----------|
| Architecture freeze (official) | `docs/releases/architecture_v1_frozen.md` |
| Production certification | `docs/production_architecture_certification.md` |
| Pipeline dependency map | `docs/production_pipeline_dependency_map.md` |
| Pipeline contract audit | `docs/production_pipeline_contract_audit.md` |
| Legacy analysis result draft | `docs/analysis_result_contract.md` (superseded by `analysis_result_contract_v1.md`) |

### Official production pipeline

```
Calendar Engine → Bazi Engine → Pattern Engine → Score Engine
  → Interpretation Engine → Report Engine → AnalysisResult → API → Portal
```

---

## Contracts (frozen V1.0)

| Contract | Document | Code reference |
|----------|----------|----------------|
| API JSON | [api_contract_v1.md](api_contract_v1.md) | `applications/api/schemas/common.py`, routes `v1.py` |
| AnalysisResult | [analysis_result_contract_v1.md](analysis_result_contract_v1.md) | `applications/api/models/analysis_result.py` |
| Portal binding | [api_contract_v1.md](api_contract_v1.md#portal-binding-summary) | `applications/customer_portal/static/js/` |

**Policy:** Additive optional fields only in 1.0.x. No removal or rename of required Portal fields.

---

## Certification & validation

| Document | Purpose |
|----------|---------|
| [production_architecture_certification.md](../production_architecture_certification.md) | Phase 7 architecture audit |
| [production_smoke_report.md](../production_smoke_report.md) | 105-case smoke results |
| [production_validation_cases.md](../production_validation_cases.md) | Case library taxonomy |
| [production_bug_tracker.md](../production_bug_tracker.md) | Open defect register |
| [production_known_issues.md](../production_known_issues.md) | Accepted limitations |

**Smoke runner:** `validation/production_smoke_runner.py`  
**Raw results:** `validation/production_smoke_raw.json`

---

## Known issues (summary)

| Severity | Count | Release blocker? |
|----------|-------|------------------|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 3 | No |
| Low | 6 | No |

Details: [production_bug_tracker.md](../production_bug_tracker.md)

Notable: timezone not applied (Medium), golden dataset needs `jsonschema` (Medium), cold-start latency (Medium).

---

## Roadmap

### V1.0.x (maintenance)

- Bug fixes without contract breaks
- Smoke suite expansion
- Documentation updates

### V1.1 (planned)

- Legacy Cleanup V1
- Calendar SSOT (`CalendarView`)
- Golden Dataset in CI
- Performance optimization
- Timezone support
- Narrative enhancement (within Report Engine)

See [version_1_0_0.md](version_1_0_0.md#future-roadmap) for full roadmap.

---

## Version history

| Version | Name | Date | Notes |
|---------|------|------|-------|
| **1.0.0** | Production Stable | 2026-07-27 | Architecture freeze, SSOT pipeline, certification |
| 1.0.0-rc1 | Release Candidate | 2026-07-27 | RC1 go decision |

---

## For developers

### Before changing production code

1. Read [architecture_v1_frozen.md](architecture_v1_frozen.md) — what MUST NOT change
2. Read relevant contract (`api_contract_v1.md`, `analysis_result_contract_v1.md`)
3. Run smoke: `py -3.13 validation/production_smoke_runner.py`
4. Run tests: `py -3.13 -m pytest applications/api/tests applications/customer_portal/tests -q`

### Forbidden without architecture approval

- Pipeline reorder or parallel paths
- New producers for existing slices
- Orchestrator shaping for interpretation/report
- Breaking API or Portal JSON fields
- Portal engine recalculation

---

## Directory structure

```
docs/releases/
├── README.md                      ← this file
├── architecture_v1_frozen.md
├── release_candidate_rc1.md
├── version_1_0_0.md
├── api_contract_v1.md
├── analysis_result_contract_v1.md
└── release_notes_v1.0.0.md

docs/project/                      ← governance (see ../project/README.md)
```

---

**BTE Platform Release Documentation — Official Reference — V1.0.0**
