# BTE Platform — Product Roadmap

| Field | Value |
|-------|-------|
| **Current version** | BTE Platform 1.0.0 |
| **Status** | Production Stable |
| **Architecture** | Frozen (V1.0) |
| **Last updated** | 2026-07-27 |

---

## Current version

**BTE Platform 1.0.0** is the baseline production release.

- Locked pipeline: Calendar → Bazi → Pattern → Score → Interpretation → Report → AnalysisResult → API → Portal
- Single Source of Truth per engine slice
- Customer Portal renders API JSON without recalculating engine logic
- 105-case production smoke suite green

See `docs/releases/` for frozen contracts and release notes.

---

## Roadmap overview

| Version | Theme | Architecture impact |
|---------|-------|---------------------|
| **V1.0.x** | Production maintenance | None (frozen) |
| **V1.1** | Legacy cleanup & SSOT completion | Additive only |
| **V1.2** | AI rewrite & narrative quality | Within Report / Interpretation boundaries |
| **V1.3** | PDF export & branding | New export surface; API additive |
| **V1.4** | CRM & case history | Applications layer extension |
| **V2.0** | Architecture review & scale | Major — new architecture version |

---

## V1.0.x — Production maintenance

**Goal:** Keep Production Stable release reliable without breaking frozen contracts.

| Area | Scope |
|------|-------|
| **Bug fixes** | Critical/High production defects; Medium/Low per `VERSION_POLICY.md` |
| **Performance** | Cold-start warm-up, loader cache (no pipeline change) |
| **Knowledge expansion** | New rules/phrases in `database/` and `knowledge_base/` — no schema break |
| **Smoke expansion** | Additional validation cases in `validation/production_smoke_runner.py` |
| **Documentation** | Governance, runbooks, knowledge guides |

**Out of scope:** Pipeline reorder, new producers, breaking API/Portal fields, architecture refactor.

---

## V1.1 — Legacy cleanup & platform hardening

**Goal:** Remove dead code paths and complete SSOT gaps without changing user-visible contracts.

| Initiative | Description |
|------------|-------------|
| **Legacy cleanup** | Remove or quarantine `NarrativeEngine` production confusion, obsolete root tests, duplicate builders |
| **Calendar SSOT** | Introduce `CalendarView` + `calendar_truth`; reduce orchestrator `_shape_calendar` |
| **Golden dataset** | CI integration with `jsonschema`; restore full golden regression |
| **Dependency cleanup** | Align dev/QA requirements; document optional packages |
| **Code cleanup** | Legacy modules marked deprecated; no public API removal without wrapper |

**Deferred from 1.0.0:** BUG-PROD-001 (timezone), BUG-PROD-002 (golden dataset), BUG-PROD-006 (legacy tests).

---

## V1.2 — AI rewrite & narrative quality

**Goal:** Improve commercial prose quality while respecting frozen pipeline and Report Engine terminal role.

| Initiative | Description |
|------------|-------------|
| **Narrative enhancement** | Distinct narrative prose inside Report Engine (not orchestrator duplication) |
| **Sentence optimization** | Phrase library tuning, redundancy reduction, tone control |
| **Report quality** | Section ordering, transitions, commercial readability |
| **AI rewrite** | Optional rewrite layer on **formatted** output only — no new inference in engines |

**Constraint:** Interpretation rules remain database-driven; AI assists formatting, not rule substitution.

---

## V1.3 — PDF report & export

**Goal:** Deliver branded customer-facing PDF and export formats.

| Initiative | Description |
|------------|-------------|
| **Export engine** | Formalize PDF/HTML export from `ReportView` (extend Report Engine export path) |
| **Customer report** | Branded layout, cover page, customer metadata from `data.customer` |
| **Branding** | Templates, logos, configurable themes |

**API:** Additive endpoints or fields; existing `report.markdown` / `report.html` unchanged.

---

## V1.4 — CRM & customer history

**Goal:** Persist analyses and support customer relationship workflows.

| Initiative | Description |
|------------|-------------|
| **Customer history** | Link `customer_id` to stored analyze results |
| **Case management** | Extend `applications/case_management` and Portal history |
| **Search & retrieval** | List, filter, re-open past reports |

**Constraint:** Analyze pipeline remains stateless; persistence is Applications layer only.

---

## V2.0 — Architecture review & future platform

**Goal:** Evaluate major architectural evolution for scale and multi-tenant operation.

| Theme | Considerations |
|-------|----------------|
| **Architecture review** | Formal V2.0 proposal; migration from V1.0 frozen contracts |
| **Scalability** | Async jobs, queue-based analyze, horizontal API scale |
| **Distributed services** | Optional engine microservices vs monolith orchestrator |
| **Future platform** | Multi-region, tenancy, plugin engines, external integrations |

**Requires:** Explicit architecture approval, new major version, contract migration plan.

---

## How roadmap items enter development

1. Issue / proposal in planning
2. Alignment with `docs/project/VERSION_POLICY.md`
3. Architecture review if touching frozen pipeline
4. Feature branch → regression + smoke → review → release

See `docs/project/DEVELOPMENT_WORKFLOW.md`.

---

## Related documents

| Document | Purpose |
|----------|---------|
| `docs/releases/version_1_0_0.md` | 1.0.0 milestones and deferred work |
| `docs/project/VERSION_POLICY.md` | Version numbering rules |
| `docs/project/CHANGELOG.md` | Released changes |
| `docs/production_known_issues.md` | Current limitations |

---

**BTE Platform Product Roadmap — V1.0.0 baseline — 2026-07-27**
