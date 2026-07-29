# BTE Platform — Release Candidate RC1

| Field | Value |
|-------|-------|
| **Version** | 1.0.0-rc1 → 1.0.0 |
| **Release name** | Production Stable |
| **Date** | 2026-07-27 |
| **Architecture** | V1.0 Frozen |

---

## Current status

| Area | Status |
|------|--------|
| **Production** | Stable |
| **Architecture** | Frozen (V1.0) |
| **Pipeline** | Locked |
| **Critical bugs** | 0 open |
| **High bugs** | 0 open |
| **Certification** | Conditional PASS (Phase 7) |
| **Stabilization** | Complete |

---

## Smoke test

| Metric | Result |
|--------|--------|
| Harness | `validation/production_smoke_runner.py` |
| Cases | 105 |
| PASS | 105 |
| FAIL | 0 |
| Pass rate | 100% |

**Coverage:** Li Chun before/after, leap year/month, solar-term boundaries, Zi hour, midnight, missing gender, invalid input (422), RC1 20 cases, bazi regression, hour sweep, decade grid.

**Raw output:** `validation/production_smoke_raw.json`

---

## Regression

| Suite | Result |
|-------|--------|
| API + Portal pytest | 76 / 76 PASS |
| Report module | 47 / 47 PASS |
| Production-clean (excl. legacy root tests) | 380 / 380 PASS |
| Full repo (excl. golden dataset) | 392 passed, 5 failed (legacy) |

**Legacy failures (not production path):** `tests/test_builder.py`, `tests/test_pipeline.py`, `tests/test_sentence_generator.py`, `tests/integration/test_pipeline.py`

---

## Certification

| Document | Verdict |
|----------|---------|
| `docs/production_architecture_certification.md` | **Conditional PASS** |

**Conditions met for release:**

- Single producer per engine slice on production path
- No duplicate API shaping (report/interpretation)
- Portal reads API only
- Legacy isolated from orchestrator imports

**Accepted exceptions documented:** calendar shaping in API layer, narrative = report content, golden dataset tooling.

---

## Known issues

See `docs/production_known_issues.md` and `docs/production_bug_tracker.md`.

### Open medium bugs

| ID | Summary |
|----|---------|
| BUG-PROD-001 | `timezone` parameter accepted but not applied |
| BUG-PROD-002 | Golden dataset blocked (`jsonschema` missing) |
| BUG-PROD-003 | Cold-start analyze latency ~2s |

### Open low bugs

| ID | Summary |
|----|---------|
| BUG-PROD-004 | `/narrative` route docstring mentions NarrativeEngine |
| BUG-PROD-005 | Narrative JSON identical to report JSON |
| BUG-PROD-006 | 5 legacy root pytest failures |
| BUG-PROD-007 | Score.js `details.*` fallback |
| BUG-PROD-008 | Portal Bazi hidden-stem display fallback |
| BUG-PROD-009 | No `AnalysisResult.calendar` slice (info) |

**None block production release.**

---

## Golden dataset status

| Item | Status |
|------|--------|
| `tests/golden_dataset/test_golden_dataset.py` | **Cannot collect** — `jsonschema` not installed |
| `validation/real_cases/` (20 cases) | PASS via smoke runner (`rc1_*` cases) |
| Golden Dataset files | Not modified (policy) |

**Recommendation:** Add `jsonschema` to QA/dev requirements for CI; optional gate post-1.0.0.

---

## Performance

| Scenario | Typical latency |
|----------|-----------------|
| Warm `/api/v1/analyze` | 150–450 ms |
| Cold first analyze | up to ~2 s |
| Smoke average | 252.6 ms |
| Stage `calendar` | < 100 ms |

**Bottleneck:** First-request loader initialization (score, interpretation, templates). Not a correctness defect.

---

## Release risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Timezone ignored | Medium | Document for users; fix in 1.1 |
| Cold-start latency | Low | Warm-up or accept first-request delay |
| Narrative = report | Low | Product expectation set in release notes |
| Legacy CI noise | Low | Exclude legacy tests in CI until cleanup |
| Golden dataset unavailable | Low | Smoke suite covers 105 cases |

**No Critical or High release risks identified.**

---

## Deployment checklist

### Pre-deploy

- [ ] Tag `v1.0.0` on approved commit
- [ ] Verify `py -3.13 validation/production_smoke_runner.py` → 105 PASS
- [ ] Verify `pytest applications/api/tests applications/customer_portal/tests -q` → all PASS
- [ ] Confirm API health: `GET /api/v1/health` → 200
- [ ] Confirm Portal routes: dashboard, analyze, result, reports → 200
- [ ] Review `docs/releases/` release notes for ops team

### Deploy

- [ ] Deploy API application (`applications/api`)
- [ ] Deploy Customer Portal (`applications/customer_portal`)
- [ ] Configure reverse proxy: Portal → API `/api/v1/*`
- [ ] Set production `timezone` default documentation (Asia/Ho_Chi_Minh)
- [ ] Enable request logging (`X-Request-ID`, `X-Elapsed-Ms`)

### Post-deploy smoke

- [ ] POST `/api/v1/analyze` with critical case 1987-01-21 03:30 male
- [ ] Verify pillars: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần
- [ ] Portal: full analyze → result tabs render
- [ ] Verify no internal fields in JSON (`details`, `templates_used`)

---

## Rollback strategy

| Step | Action |
|------|--------|
| 1 | Revert to previous deployment artifact (API + Portal) |
| 2 | Clear Portal sessionStorage if schema mismatch (user instruction) |
| 3 | Verify `/api/v1/health` and one analyze request |
| 4 | No database migration rollback required (stateless analyze pipeline) |

**Data:** Analyze results stored client-side in `ResultStore`; server rollback does not affect persisted customer cases unless separately deployed.

---

## Go / No-Go decision

| Criterion | Required | Actual | Go? |
|-----------|----------|--------|-----|
| Architecture frozen | Yes | Yes | ✅ |
| Production smoke PASS | 100% | 105/105 | ✅ |
| API + Portal tests PASS | Yes | 76/76 | ✅ |
| Critical bugs | 0 | 0 | ✅ |
| High bugs | 0 | 0 | ✅ |
| Certification | PASS/Conditional | Conditional PASS | ✅ |
| Release docs complete | Yes | Yes | ✅ |

### Decision: **GO**

BTE Platform **1.0.0** is approved for production release as **Production Stable** under Architecture V1.0 Frozen.

**Sign-off roles:** Product, Engineering, QA (documentation complete; formal signatures external to this repo).

---

## References

- `docs/releases/architecture_v1_frozen.md`
- `docs/releases/version_1_0_0.md`
- `docs/releases/release_notes_v1.0.0.md`
- `docs/production_smoke_report.md`
