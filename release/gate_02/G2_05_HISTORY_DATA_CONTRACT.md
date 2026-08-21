# G2-05 — History data contract

## Persistence inventory

| Store | Purpose | Data format | Identity field | Version metadata | Write condition | Read condition | Retention | Customer-visible? |
|-------|---------|-------------|----------------|------------------|-----------------|----------------|-----------|-------------------|
| `bte_last_result` | Current Analyze snapshot | JSON `{input, data}` | `data.analysis_id` + `bte_current_analysis_id` | Copied inside `data.result_meta` / `useful_god_source` | Successful Analyze only | Default `/result`, exports with `source=current` | Until next Analyze or explicit clear of last result | Indirect (Result UI) |
| `bte_current_analysis_id` | Canonical current id | JSON string | itself | none | Successful Analyze | Result identity | Same as current | No (technical) |
| `bte_history` | Append-only History index + snapshots | JSON array of History rows | `analysis_id` / `id` | `customer_contract`, `narrative_contract`, `gate_core_freeze`, `month_pillar_standard`, `release_label`, `created_at` | Successful Analyze (one row per declared id) | History page, History open, refresh of History URL | Newest 30 rows; older dropped | Yes (list + open) |
| `bte_view_result` | Transient History pointer | JSON `{input, data}` | paired `bte_view_analysis_id` | none | Open History / older report | Explicit History URL only | Session only | No |
| `bte_view_analysis_id` | Viewed History id | JSON string | itself | none | With view pointer | Explicit History URL | Session only | No |
| `sessionStorage` | Same keys, preferred read | same | same | same | Same writes (view is session-only) | Read before `localStorage` | Tab session | No |
| `localStorage` | Durable current + History | same | same | same | Current + History (not view) | Fallback if session empty | Browser profile | No |
| Legacy `bte_portal_last_result` / `bte_portal_history` | Migration bridge | JSON | varies | none | **Read-only** | If current keys empty | Until overwritten/cleared | No |
| Server / database History | none in V1.0 | — | — | — | — | — | — | — |

Pages must not touch Web Storage directly. Owner: `applications/customer_portal/static/js/result_store.js`.

## Canonical V1.0 History record

A new saved analysis stores:

| Field | Source | Notes |
|-------|--------|--------|
| `analysis_id` / `id` | Server Analyze `analysis_id` / `request_id` | Canonical customer identity |
| `request_id` | `data.request_id` | Same as analysis id when stamped |
| `created_at` | `data.result_meta.created_at` | Analysis creation time |
| `saved_at` | Same as `created_at` | Not last viewed / last export |
| `input` | Birth form posted to Analyze | Name, date/time, timezone, place |
| `data` | Full structured Analyze snapshot | Analytical truth. Not invented |
| `customer_contract` | `useful_god_source.contract` or `result_meta.customer_contract` | New saves: `analysis_result.UsefulGodView@1.5` |
| `narrative_contract` | `narrative_result.contract` | New saves: `pack05_narrative_result_v1` when present |
| `gate_core_freeze` | `result_meta.gate_core_freeze` | `G1` when stamped |
| `month_pillar_standard` | `result_meta.month_pillar_standard` | `BTE-MONTH-PILLAR-LUNAR-V1.0` |
| `release_label` | `result_meta.release_label` | `BTE V1.0 — Gate 1 Core Engine` |
| `summary` | Interpretation summary if already in payload | Display hint only |

Do **not** invent analytical values. Do **not** backfill these fields onto old rows.

## Immutability

Once stored, a History row is not updated when:

- current result changes
- Portal contract/bundle changes
- user opens report
- user exports PDF/DOCX/Print
- backend restarts

`saveHistory` skips prepend when the same declared `analysis_id` already exists. It does not mutate the existing snapshot.

## Presentation vs analytics

If History stores canonical `AnalysisResult` and not a prebuilt `PresentedReport`:

- **Allowed:** format the stored blob with the current G2-04 presentation builder (`build_customer_report_input` → `PresentedReportV1`).
- **Forbidden:** re-run Calendar / BaZi / Strength / Pattern / Useful God / Luck / Score / Composer.

## Storage limit

`HISTORY_LIMIT = 30`. Newest first (`unshift`). Rows beyond 30 are dropped from the end (oldest). Approximate localStorage quota is the browser limit (~5MB typical); oversized writes fail quietly and must not undo a successful current-result write.

## Delete / clear

- No per-row delete in V1.0. Do not add one here.
- “Xóa lịch sử” clears `bte_history` only. It does **not** clear `bte_last_result`.
- No confirmation dialog (existing behavior, not redesigned).
- No new “set as current” action.
