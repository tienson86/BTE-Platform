# G2-01R — Canonical result binding repair report

**Status: G2-01R: CANONICAL RESULT BINDING REPAIRED — READY FOR G2-02**

Gate-1 Frozen Truth was not modified. Ten G1-FINAL control cases vs live orchestrator: **0 analytical diffs**.

This repair is routing, identity, ResultStore precedence, customer contract binding, empty state, legacy isolation, and runtime/version protection only.

---

## Acceptance

- [x] empty `/result` has no mock fixture
- [x] one canonical analysis identity
- [x] request/API identity not dropped
- [x] ResultStore current identity matches payload
- [x] fresh current > implicit history
- [x] History requires explicit context (`?from=history&id=...`)
- [x] legacy route isolated (`?legacy=1` is EXPLICIT LEGACY ONLY)
- [x] no latent old Dụng/Hỷ fallback on structured Gate-1 result
- [x] `@1.5` contract guarded
- [x] new History has version metadata
- [x] old History not silently reinterpreted
- [x] Result/Report share analysis ID
- [x] Print uses the selected analysis (`data-analysis-id`)
- [x] ten control cases = 0 analytical diffs
- [x] no Gate-1 analytical files changed by this repair
- [x] live Dũng/Tuyền Analyze identity + Frozen fields match

Do **not** start G2-02 automatically.

---

## What was repaired

1. Production empty `/result` renders the empty gate. Mock fixture remains only for `?preview=1` or explicit `previewFallback`.
2. HTTP Analyze stamps `data.analysis_id = data.request_id = request_id`. Portal persists that ID. Frontend does not mint `bte-<birth>-<timestamp>` when a server ID exists.
3. ResultStore current (`bte_last_result` + `bte_current_analysis_id`) is the default. History view requires matching `id`. `loadForView()` is legacy-only.
4. Customer Useful God binds from `analysis_result.UsefulGodView@1.5` (`useful_display`, `favorable_display`, `short_reason`, Điều hậu). Missing `@1.5` does **not** fall back to `pattern.dung_than` / `pattern.hy_than`.
5. Incompatible / unversioned stored payloads show a reanalyze message. They are not reinterpreted.

---

## Changed files by category

### Routing
- `applications/customer_portal/app.py`
- `applications/customer_portal/src/entries/resultApp.tsx`
- `applications/customer_portal/src/entries/resultBoot.ts`
- `applications/customer_portal/src/resultState/currentResult.ts`
- `applications/customer_portal/static/js/history.js`
- `applications/customer_portal/static/js/dashboard.js`
- `applications/customer_portal/static/js/reports.js`

### ResultStore
- `applications/customer_portal/static/js/result_store.js`
- `applications/customer_portal/static/js/analyze.js`

### Contract binding
- `applications/api/services/result_identity.py` (new)
- `applications/api/routes/v1.py` (stamp after Analyze; no engine change)
- `applications/customer_portal/src/resultState/customerContract.ts` (new)
- `applications/customer_portal/src/adapters/canonicalUsefulGod.ts`
- `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts`
- `applications/customer_portal/src/adapters/baziResultAdapter.ts`
- `applications/customer_portal/src/report/fullReportViewModel.ts`
- `applications/customer_portal/src/entries/reportComposer.ts`

### Empty state
- `applications/customer_portal/src/hooks/useCanonicalDesktopResult.ts`
- `applications/customer_portal/src/screens/canonical_desktop/PortalPage.tsx`
- `applications/customer_portal/src/screens/result/ResultPageStatusGate.tsx`
- `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts` (`createCanonicalDesktopGateViewModel` clears fake chart id)

### Metadata
- `applications/customer_portal/src/models/dto.ts` (`analysis_id`, `result_meta`, `useful_god_source`)
- History row fields in `result_store.js` (`created_at`, `customer_contract`, `gate_core_freeze`, `month_pillar_standard`, `release_label`)

### Legacy isolation
- `applications/customer_portal/templates/result_legacy.html` (explicit banner)
- `result_store.js` `loadForView()` documented EXPLICIT LEGACY ONLY

### Tests
- `applications/customer_portal/tests/js/g2_01r_canonical_binding.test.tsx` (new, A–L)
- `applications/api/tests/test_result_identity.py` (new)
- Repairs: `result_app_boot.test.ts`, `canonical_result_routing.test.ts`, `canonical_desktop.test.tsx`, `canonical_desktop_adapter.test.tsx`, `full_report_composition.test.ts`, `result_store_flow.js`

### Docs / probes
- `release/gate_02/G2_01R_*.md` (this set)
- `release/gate_02/_g2_01r_live_probe.py`

### Analytical engine / rule files changed by this repair

**0**

---

## Live verification

- Orchestrator ten-case probe (`release/gate_02/_g2_01_binding_probe.py`): `mismatch_count = 0`.
- HTTP TestClient Analyze Dũng / Tuyền: `data.analysis_id === request_id`; Frozen pillars / Strength / Pattern / Dụng / Hỷ / Điều hậu match Gate-1.
- Portal rebuilt: `npm run build:result`.
- History precedence: ResultStore harness + Vitest explicit `?from=history&id=...`.

Browser click-through of History → `/result` → refresh was not driven as a headed UI session. The same precedence is enforced in `resolveForDisplay` / `resolveResultBoot`.

---

## G2-04 notes (not repaired here)

- Customer Print (`window.print` / Report Center HTML print) is **not** Report V1 PDF. Do not unify in G2-01R.
- No customer DOCX. Internal/report DOCX may remain.
