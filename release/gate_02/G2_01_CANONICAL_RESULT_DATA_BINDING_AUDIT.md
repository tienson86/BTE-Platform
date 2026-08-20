# G2-01 — Canonical Result & Data Binding Audit

**Mode:** AUDIT ONLY. No production repair. No Gate-1 engine change.  
**Date:** 2026-08-20  
**Upstream:** G1-FINAL PASS · HEAD `ed6dba05fd7683ed686c1d0035767ede6b5532f3`  
**Frozen dump:** `release/gate_01/G1_PREFINAL_101_TRUTH.json` SHA256 `46386BC955119F5DFE9482E7D620767BFB8BB74003A0968A17A6F82017FFA5CC`  
**Customer contract:** `analysis_result.UsefulGodView@1.5`

**Final status:** G2-01: CUSTOMER DATA BINDING DEFECTS FOUND — REPAIR REQUIRED

Gate-1 analytical truth **matches** live API on all ten control cases (0 diffs). Defects are **routing / empty-state / identity / latent fallback / versioning**, not Frozen Truth mismatches. **No unfreeze.**

---

## 1. Executive status

Production customer result is the HTML Portal (`/analyze` → ResultStore → `/result` Desktop V2). After a **successful fresh Analyze**, Canonical Desktop, Luận giải (same page), and structured Báo cáo copy one stored `data` blob. Adapters format Gate-1 fields; they do not retune engines.

Binding is **not** fully canonical because:

1. Empty `/result` renders a **complete mock fixture** as if it were a live analysis.
2. API `request_id` is dropped; Portal IDs are synthetic; payload has no `analysis_id`.
3. History rows have **no** engine/contract/Gate version.
4. Latent Hỷ/Dụng fallbacks to `pattern.hy_than` / `pattern.dung_than`.
5. `/result?legacy=1` still uses different precedence (`loadForView`).
6. Portal does not detect UsefulGodView `@1.5` vs stale API/bundle.
7. Customer PDF is browser Print, not Report V1 PDF. Customer DOCX does not exist.

Happy-path Analyze of Dũng / Tuyền would show Frozen Dụng, HK-R1H Hỷ, separate Điều hậu, LEVEL-1 without override — **if** the stored payload is the fresh Analyze `data`.

---

## 2. Canonical Analyze flow

```
GET /analyze  (analyze.html + analyze.js)
  → BtePortal.post("/api/v1/analyze") via /backend proxy
  → applications.api.routes.v1.analyze_endpoint
  → OrchestratorService.analyze
  → attach_presentation_metadata + useful_god_source @1.5
  → APIResponse { success, data, request_id }
  → saveLastResult({ input, data })     // request_id not saved
  → verify ResultStore.load().data
  → location.assign("/result")
```

| Item | Value |
|------|--------|
| Endpoint | `POST /api/v1/analyze` (portal: `/backend/api/v1/analyze`) |
| Service | `OrchestratorService.analyze` |
| Result object | API `data` dict (AnalysisResult-shaped public payload) |
| Analysis ID creation | ResultStore `makeAnalysisId` after save |
| Storage writes | `bte_last_result`, `bte_current_analysis_id`, `bte_history`; clears view; removes `bte_portal_last_result` |
| Redirect | `/result` (no query) |

Successful Analyze writes the intended current blob to `bte_last_result`.

Parallel **non-production** path: `PortalApp.startAnalysis` keeps `analysisSession` in React memory and navigates `#/result`. Not mounted by `customer_portal.app`.

---

## 3. Analysis ID chain

See `G2_01_ANALYSIS_ID_FLOW.md`.

De facto current id: **`bte_current_analysis_id`**.  
API UUID `request_id` is **not** the Portal chain. Orchestrator `data.analysis_id` is **null** on all ten probes.

---

## 4. ResultStore precedence

| Key | Purpose | Write | Read | Precedence | Overwrite |
|-----|---------|-------|------|------------|-----------|
| `bte_last_result` | last Analyze blob `{input,data}` | `save()` only | `load` / `loadCurrent` | current | each Analyze |
| `bte_history` | last 30 rows with full `data` | `save` / `saveHistory` | `loadHistory` | append-only | cap 30 |
| `bte_view_result` | explicit older selection | `selectForView` session-only | `peekView` | history only if `?from=history` on Desktop | cleared on Analyze |
| `bte_current_analysis_id` | current id | `save` | `getCurrentAnalysisId` | current | each Analyze |
| `bte_view_analysis_id` | view id | `selectForView` session | history display | with view | cleared on Analyze |
| `bte_portal_last_result` | pre-refactor | deleted on save | `load()` fallback | behind current key | migration |
| URL `?from=history` | Desktop history mode | History/Reports/Dashboard | `isHistoryViewSearch` | required for view | — |
| URL `?preview=1` | fixture | — | resultBoot | overrides store | — |
| URL `?legacy=1` | old result page | — | app.py | separate renderer | — |
| Server session | none for results | — | — | — | — |

**Current-result precedence (Desktop V2):**  
`from=history` + view → history; else last_result; else TS may treat leftover view as `legacy`; else mock preview.

---

## 5. Surface / source matrix

See `G2_01_SURFACE_SOURCE_MATRIX.md`.

---

## 6. Canonical Desktop bindings (S00–S11)

| Section | Canonical field(s) | Adapter | Fallback | Legacy if any |
|---------|--------------------|---------|----------|----------------|
| S00 Technical | customer, calendar lunar, request birth, **chartId = analysis id** | `mapS00` | fixture name/date/chartId | **analyzedAt = `new Date()` (clock, not stored)** |
| S01 summary | day master, strength label/score, pattern line, Điều hậu (`temperature` + `climate_preference_label`), luck | `mapS01` | NarrativeResult then interpretation sections | — |
| S02 overview | five_elements counts; strength class; **Dụng `useful_display`**; **Hỷ `favorable_display`**; Kỵ `unfavorable_display` | `mapS02` | Dụng → `useful_god` → `pattern.dung_than`; Hỷ → `pattern.hy_than` | compact Pattern names |
| S03 pillars | `bazi.*_pillar` + ten_gods hidden lines | `mapS03` | — | — |
| S04 Five Elements | `data.five_elements` counts | `canonicalFiveElementCounts` | empty rows | **not** `score.wuxing_*` |
| S05 Strength | `strength.strength_score` / `strength_level` | `canonicalStrength*` | — | **not** `score.strength_score` |
| S06 Ten Gods | `ten_gods` / `ten_gods_result` labels | prominence helper | `bazi.ten_gods` | display `score: "1"` is UI filler, not ScoreEngine |
| S07 ShenSha | shen sha adapter from analysis | `shenShaEntriesFromAnalysis` | unavailable copy | — |
| Useful God area | S02 + S01 Điều hậu | `canonicalUsefulGod.ts` | see S02 | **does not** copy `favorable_gods` into Hỷ |
| Luck | `data.luck` | formatLuck* | unavailable | — |
| S08 Narrative | `narrative_result` Pack 05 | `mapS08` | `data.interpretation` sections | **only if NarrativeResult absent** |
| S09–S11 | derived from S08 / bone-weight stub | `mapS10` empty | fixture leakage blocked for S10 | — |

---

## 7. Interpretation binding

`GET /interpretation` and `/result#interpretation` / `#luan-giai` load **the same** `result_desktop.html` + `result.js` boot. Same ResultStore, same `analysisId` on `ResultPageBody`.

Source A: same canonical current (or history if `?from=history`).  
Not B/C/D: no second Analyze, no separate interpretation store.  
E: NarrativeResult first; legacy interpretation HTML only if Pack 05 missing.

Invariant holds when both routes use the same query string (current vs history).

---

## 8. Report binding

`/reports` builds list from history + last_result. Structured rows use `window.BteFullReport` (`fullReportViewModel.ts`) — format only. Does not recompute Strength / Pattern / UG / Hỷ / Five Elements / Ten Gods / ShenSha / Luck.

Opening `source: "last"` → `/result` (clears view). Opening history → `/result?from=history`.

---

## 9. PDF paths

| PDF path | Source | Renderer | Analysis ID | Canonical? | Customer? | Legacy? |
|----------|--------|----------|-------------|------------|-----------|---------|
| Browser Print on `/result` (`#xuat` → `window.print`) | Full Report HTML from stored `data` | browser | Portal id | presentation of stored truth | **Yes** | not Report V1 |
| Browser Print on `/reports` | `composeHtmlDocument` | popup print | report id | if structured + BteFullReport | **Yes** | executive HTML if unstructured |
| Report V1 PDF | `ReportExportServiceV1` | server PDF | ReportInput metadata | Gate-1 export path | **No** | different pipeline |
| `data.report.pdf` URL in history | rare stored link | iframe/link | — | only if Analyze stored a URL | if present | usually absent |

G1-09 finding stands: **Print ≠ Report V1 PDF.**

---

## 10. DOCX path

No customer Portal action / endpoint downloads DOCX.

Ops path: `ReportExportServiceV1.export_docx(ReportInputV1)` (G1-PREFINAL smoke). Same presentation semantics as ReportInput, **not** wired to ResultStore.

**Gap:** customer DOCX is missing, not a dual-truth mix.

---

## 11. History behavior

Stored row: `{ id, analysis_id, saved_at, input, summary, data }` with **full `data` snapshot**.

Reopen: **renders stored historical truth**. Does **not** re-run engines.

`selectForView` does **not** mutate `bte_last_result`.

---

## 12. History versioning

| Metadata | Stored? |
|----------|---------|
| analysis ID | yes (synthetic) |
| analysis timestamp | `saved_at` |
| engine version | **no** |
| UsefulGodView contract | **no** (only inside `data.useful_god_source` if that payload was saved) |
| calendar/month standard | **no** explicit; implied by stored pillars |
| Gate/release version | **no** |

V1.1 re-analyze of an old birth would create a **new** history row; old row still shows V1.0 snapshot **if** UI keeps using stored `data`. Risk: a future “refresh analysis” feature could reinterpret silently. **Class E.**

---

## 13. Reload behavior

Fresh Analyze → `/result` → F5: **same-tab sessionStorage + localStorage keep `bte_last_result`**. Current remains. No implicit History B.

Close tab: session keys gone; **localStorage last_result still loads** on a new tab (writeRaw is not session-only for last). View key is session-only, so history context does **not** survive a new tab.

---

## 14. Stale ResultStore / runtime

`save()` overwrites `bte_last_result` and deletes `bte_portal_last_result`. Fresh Analyze **replaces** stale analytical payload.

Restart backend + new Portal bundle: next Analyze writes new `@1.5` `data`. Old localStorage until overwritten can still show previous Analyze (correct for that historical run). Empty store + new bundle still hits **mock fixture** (defect).

Portal does not compare `useful_god_source.contract` to a pinned `@1.5`.

---

## 15. UsefulGodView@1.5 binding

| Surface | Dụng | short_reason | customer Hỷ | Kỵ | Điều hậu |
|---------|------|--------------|-------------|-----|----------|
| Canonical Desktop S02/S01 | `useful_display` | `dungReason` | `favorable_display` (**not** `favorable_gods`) | `unfavorable_display` or list | climate label + temperature line |
| Full Report / print HTML | same | `usefulGodReason` | `canonicalFavorableDisplay` | same | climate fields |
| `/reports` structured | same composer | same | same | same | same |
| Legacy presenters | pattern/useful mixed keys | often absent | `hy_than` / `favorable_god` | mixed | mixed |
| PortalApp Result V2 | presentation envelope | unknown mix | **no `favorable_display` usage found** | — | temperature helpers |

Internal `favorable_gods` still includes Dụng token (`internal_gods_include_dung: true`). Customer Hỷ is distinct on all ten probes.

---

## 16. Ten-control-case probes

See `G2_01_CONTROL_CASE_BINDING_MATRIX.md` and `G2_01_BINDING_PROBE.json`.

Frozen JSON vs live API: **10/10 MATCH**. Class G: **none**.

---

## 17. Dũng live trace (binding)

Expected Frozen / live API:

- Pillars: Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn  
- Strength: 1.00 strong  
- Pattern: `gia_sac` LEVEL-1, override **false**  
- Overall: Thủy · Nhâm · Thực Thần (Tiết chain; no `str_` in `short_reason`)  
- Customer Hỷ: `Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng` (internal still Nhâm+Quý)  
- Điều hậu: Hỏa · Đinh · Chính Quan / Cần ôn ấm — separate from Overall  

Stale paths that **would** show old Thổ/Mậu/Thiên Ấn, Hỷ Nhâm+Quý, or override: empty **mock fixture**; `/result?legacy=1` presenters if they bind internal gods; PortalApp **demo** report; unstructured `report.html`. Production Desktop adapter copies Frozen fields when `data` is the Analyze payload.

---

## 18. Tuyền live trace

- 0.66 strong · Kiếp Tài · Overall Mộc · Ất · Chính Quan · CHẾ  
- Customer Hỷ insufficient (internal still includes Thực Thần sibling)  
- Điều hậu Thủy · Nhâm · Thiên Tài / ưu tiên Thủy  

Old UG-R2 climate-as-Overall would appear only from a **stale stored blob** or mock/demo, not from current adapter mapping of a fresh payload.

---

## 19. History cross-case (code + store tests)

Scenario Dũng then Tuyền then open Dũng:

| Step | last | view | `/result` | `/result?from=history` | Reports default |
|------|------|------|-----------|------------------------|-----------------|
| Analyze Dũng | Dũng | cleared | Dũng | Dũng | Dũng first (unshift last) |
| Analyze Tuyền | Tuyền | cleared | Tuyền | Tuyền | Tuyền current |
| Open Dũng History | Tuyền | Dũng | **Tuyền** | **Dũng** | list still has both; preview follows selection |
| Refresh `/result` | Tuyền | Dũng session | Tuyền | Dũng if URL kept | — |

`result_store_flow.js` already asserts Analyze does not rewrite last when opening history, and new Analyze clears view.

Mixing Dũng pillars + Tuyền UG would require UI to read two blobs. Desktop boot uses **one** resolved record for adapter + fullReport. **No mix on that path.**

---

## 20. Field-mixing test

Fingerprint = `{id, pillars, strength, pattern, useful_god, luck current}` all from the same `data` object in ResultStore.

Desktop: one `payload.data` → both ViewModels.  
Forbidden mix is not produced by Canonical Desktop boot.

Risk: `/reports` `currentAnalysisId()` can fall back to **current** store id if a row lacks `id` (rows from `save()` do have ids).

Diagnostic fingerprint must not be shown in UI (not added).

---

## 21. Legacy inventory

See `G2_01_LEGACY_FALLBACK_INVENTORY.md`.

---

## 22. Fallback inventory

See same file, high-risk table. Dominant production defect: **empty store → mock analysis**.

---

## 23. Partial / empty-state

| State | Expected (product) | Actual |
|-------|--------------------|--------|
| No current result | empty / CTA to Analyze | **full mock Canonical Desktop** (`resultBoot` `previewFallback: true`) |
| Corrupt JSON | empty | `readValue` returns null → same mock |
| Partial legacy (html only) | not a complete analysis | `/reports` may show old HTML; Desktop `hasStructuredAnalysis` false may still fail boot into preview |
| Missing NarrativeResult | show structured facts; narrative unavailable | S08 falls back to interpretation sections |
| Missing ReportInput | n/a in Portal | server export only |
| Missing History row | empty list | empty copy |

Partial legacy can masquerade on **legacy result** and **reports HTML fallback**. Empty current masquerades as a **complete** fixture person.

---

## 24. Version-skew risk

| Pair | Detection |
|------|-----------|
| New Portal + old API | **none** — no check of `useful_god_source.contract` |
| Old Portal + new API | **none** — old adapters may bind `favorable_gods` if that build predates HK-R1H |
| Result V2 `contract_version` `2.0.0` | UI presentation contract, **not** UsefulGodView@1.5 |

G1-09 operational skew remains possible.

---

## 25. Frontend recomputation audit

No customer-side recalculation of Ten Gods mapping, Strength class thresholds, Pattern, Dụng winner, Luck, or ShenSha formulas.

Allowed presentation: label maps, meter percent from `strength_score`, five-element **percentage of published counts**, commercial snippet filters, `score: "1"` UI filler on god chips.

`useCanonicalDesktopResult` **can** POST Analyze again if invoked with `request` and no `initialData`. Production `/result` avoids this by injecting `initialData`.

---

## 26. Defect list

| ID | Class | Finding |
|----|-------|---------|
| G2-01-01 | **D** | Empty `/result` shows mock fixture as a complete analysis |
| G2-01-02 | **A** | API `request_id` dropped; `data.analysis_id` null; synthetic Portal ids |
| G2-01-03 | **A** | S02 Hỷ/Dụng latent fallback to `pattern.hy_than` / `dung_than` |
| G2-01-04 | **D** | `/result?legacy=1` uses `loadForView` (view without `from=history`) + old presenters |
| G2-01-05 | **D** | TS `resolveCurrentStoredResult`: leftover view used as `legacy` if current missing |
| G2-01-06 | **E** | History lacks engine/contract/Gate version fields |
| G2-01-07 | **C** | No Portal check of `UsefulGodView@1.5` vs running API/bundle |
| G2-01-08 | **F** | S00 `analyzedAt` is wall-clock, not Analyze time |
| G2-01-09 | **D** | PortalApp demo report if no id (non-prod host) |
| G2-01-10 | **E** | Customer DOCX absent; Print PDF ≠ Report V1 PDF (documented split) |

No Class **G**.

Existing tests (`canonical_result_routing.test.ts`, `result_store_flow.js`) lock happy-path fresh > stale and Hỷ ≠ `favorable_gods`. They do **not** fail empty-mock.

---

## 27. Minimum G2-01 repair (do not implement here)

1. Production `/result` with no store: **empty gate**, never `createCanonicalDesktopMockViewModel`.  
2. `analyze.js` save `{ input, data, analysis_id: envelope.request_id }`; persist on current + history.  
3. Remove S02 fallbacks to `pattern.hy_than` / `dung_than` once `useful_god` exists; keep Hỷ = `favorable_display` only.  
4. Isolate or remove `?legacy=1` from customer nav; Desktop-only `resolveForDisplay`.  
5. Stamp history with `useful_god_source.contract` + Gate/release id (no migration of old rows).  
6. Optional binding-only: if `data.useful_god_source.contract` ≠ `@1.5`, show error — do not render mock.  
7. Keep Print vs Report V1 PDF as two named exports; add customer DOCX later as a **copy** of Full Report / ReportInput, not a new engine.

Do **not** retune Gate-1 engines.

---

## 28. Gate-2 acceptance recommendation

**Do not treat G2-01 as binding-complete.** Happy-path Analyze→Desktop is aligned with Frozen Truth, but empty-state, identity, legacy route, and version skew are unresolved customer-output risks.

Next allowed phase: **G2-01 repair (binding/routing only)** when Product Owner starts it.  
**Do not start G2-02** from this audit.

---

## Satellites

- `G2_01_SURFACE_SOURCE_MATRIX.md`  
- `G2_01_ANALYSIS_ID_FLOW.md`  
- `G2_01_LEGACY_FALLBACK_INVENTORY.md`  
- `G2_01_CONTROL_CASE_BINDING_MATRIX.md`  
- `G2_01_BINDING_PROBE.json` (read-only probe)
