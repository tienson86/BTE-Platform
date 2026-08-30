# N-IMP-10 PORTAL SHADOW INTEGRATION REPORT

Sprint: N-IMP-10
Module: Customer Portal + Analyze orchestrator (shadow only)
Mode: Shadow Mode (`portal_connection = true_shadow`, `replaces_pack05 = false`)
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

NarrativeV2Presentation `bte.presentation.v2.1` is wired into Customer Portal in **SHADOW MODE only**. Pack05 remains the production Narrative. Default `/result` is unchanged. Narrative V2 is reachable only through `/result?narrative=v2-shadow` (and internal `/result?narrative=v2-compare`). Analyze still succeeds if the V2 runtime fails.

---

## 2. Portal integration architecture

```
Analyze
  → Canonical Analysis (unchanged)
  → Pack05 production narrative (unchanged)
  → Narrative V2 shadow runtime (isolated try/except)
  → serialize_customer(NarrativeV2Presentation v2.1)
  → payload.narrative_v2_shadow
  → ResultStore (layer beside narrative_result)
  → /result                 → CommercialDashboardPage (Pack05)
  → /result?narrative=v2-shadow   → NarrativeV2ShadowPage (Presentation only)
  → /result?narrative=v2-compare  → internal side-by-side review
```

Portal reads **only** `NarrativeV2Presentation` inside `narrative_v2_shadow`. Adapter copies overview / interpretation / action_plan. It does not read Evidence, Reasoning, Knowledge, Rewrite, traces, rule ids, or knowledge ids.

Runtime boolean `portal_connected` stays `False` (N-IMP-09 compatibility). Shadow connection is the separate metadata string `portal_connection = "true_shadow"`.

---

## 3. Production route behavior

`GET /result` with no `narrative` query mounts `CommercialDashboardPage`.

- `data-narrative-surface="production"`
- Pack05 / current customer dashboard (Identity, Tứ Trụ, Overview, Interpretation, Action Plan)
- No Narrative V2 banner
- No `data-narrative-v2-shadow`

Verified live with CASE-0001: production dashboard rendered Nguyễn Tiến Sơn / Pack05 cards. Screenshot `01_production_result_unchanged.png`.

---

## 4. Shadow route/flag

Explicit, not default:

| Query | Surface |
| --- | --- |
| *(none)* | production |
| `?preview=1` | production (preview is not a V2 switch) |
| `?narrative=v2-shadow` | Narrative V2 — Shadow Review |
| `?narrative=v2-compare` | CURRENT PRODUCTION vs NARRATIVE V2 SHADOW |

Resolver: `applications/customer_portal/src/resultState/narrativeV2Shadow.ts`.

Shadow banner copy: **Narrative V2 — Shadow Review** / “Xem Presentation v2.1 (không phải luồng khách hàng)”.

---

## 5. ResultStore strategy

`normalizeResult` keeps both layers:

- `data.narrative_result` — Pack05 / current production
- `data.narrative_v2_shadow` — isolated envelope `{status, portal_connection, replaces_pack05, presentation, error}`

`loadNarrativeV2Shadow()` reads the shadow envelope from current (or raw `load()` fallback). It never overwrites Pack05 fields.

Conceptual store shape:

```
current analysis
pack05 / current narrative   → narrative_result
narrative_v2_shadow          → narrative_v2_shadow
```

Backward compatible: payloads without `narrative_v2_shadow` still load.

---

## 6. Presentation version handling

Accepted: `bte.presentation.v2.1` (`metadata.version`).

Rejected cleanly: any other version, including `bte.presentation.v2`.

Error: `incompatible_presentation_version`. No silent fallback composition. Shadow page shows diagnostic error; production `/result` is untouched.

API attach also rejects a serialized payload whose version is not `PRESENTATION_VERSION`.

---

## 7. Overview rendering

Copy-only from `presentation.overview`:

- `headline`
- `summary`
- `identity` / `balance` / `conclusion` — omitted values are **not invented**

CASE-0001: headline + summary render exactly. `identity`, `balance`, `conclusion` are null and show the diagnostic placeholder “Không có trong Presentation”.

---

## 8. Interpretation rendering

Primary customer-reading field on the shadow surface: `consulting_flow`.

Structured Interpretation is **not** concatenated into that paragraph. Structured fields live under expandable diagnostic detail.

---

## 9. Consulting flow rendering

Rendered unchanged from `presentation.interpretation.consulting_flow`.

CASE-0001 (exact):

> Điểm nổi bật ở đây là bạn thường làm việc tốt hơn khi có chỗ dựa ổn định và khi công việc cần xây từ nền tảng. Điều này cho thấy bạn thường duy trì được sự ổn định tốt khi theo đuổi những việc cần thời gian và sự bền bỉ. Ở mặt tích cực, bạn cũng phù hợp với việc học có hệ thống và cần thời gian để ngấm dần. Điều đáng chú ý là điều này hữu ích khi bạn có lối để thể hiện năng lực và khi giới hạn được giữ rõ.

---

## 10. Structured interpretation rendering

Expandable `<details>` (“3. Structured Interpretation details”), each field copied independently:

`overview` · `observation` · `reasoning` · `meaning` · `impact` · `recommendation` · `closing`

Portal does not join these strings. Empty fields are omitted from the detail list.

---

## 11. Action rendering

Copy-only from `presentation.action_plan`:

- `top_priority` (title + description)
- `actions[]` (title + description)
- `warnings[]`
- `current_period`

No UI-12 legacy copy. No rewrite.

CASE-0001: top priority “Ưu tiên giữ nền tảng hiện tại”; three practice actions; one warning. `current_period` is null → diagnostic placeholder only.

---

## 12. Commercial handling

`commercial` is always treated as null on the Portal shadow surface. Diagnostic card: “Chưa có (Commercial Builder chưa triển khai)”. No local commercial copy is generated.

---

## 13. Failure isolation

`attach_narrative_v2_shadow()` never raises.

If `NarrativeRuntime.run` fails:

- envelope `{status: "error", presentation: null, error: "shadow_runtime_failed", replaces_pack05: false}`
- Pack05 `narrative_result` is still written
- Analyze HTTP path still returns 200-class success for the production payload
- `/result` still mounts production dashboard from Pack05
- Shadow page shows “Không tải được Narrative V2” without mounting production as V2

Orchestrator wrapper `_attach_narrative_v2_shadow` is monkeypatchable so tests can inject failure without touching astrology engines.

---

## 14. Public/private boundary

Portal adapter / DOM do not include:

- `evidence.*`
- `NR-REL-*`
- `knowledge.*`
- `source_unit_ids`
- `pipeline_trace`
- `runtime_metrics`
- debug JSON
- rule ids / knowledge ids

Customer-safe serializer is `serialize_customer` on the API side. Shadow UI copies Presentation fields only.

---

## 15. Files created

- `applications/api/services/narrative_v2_shadow.py`
- `applications/api/tests/test_narrative_v2_shadow.py`
- `applications/customer_portal/src/resultState/narrativeV2Shadow.ts`
- `applications/customer_portal/src/adapters/narrativeV2PresentationAdapter.ts`
- `applications/customer_portal/src/screens/narrative_v2_shadow/NarrativeV2ShadowPage.tsx`
- `applications/customer_portal/src/screens/narrative_v2_shadow/narrative-v2-shadow.css`
- `applications/customer_portal/src/screens/narrative_v2_shadow/index.ts`
- `applications/customer_portal/tests/js/narrative_v2_shadow.test.tsx`
- `applications/customer_portal/scripts/capture_n_imp_10_screenshots.py`
- `implementation/narrative_v2/n_imp_10/01_production_result_unchanged.png`
- `implementation/narrative_v2/n_imp_10/02_narrative_v2_shadow_full.png`
- `implementation/narrative_v2/n_imp_10/03_narrative_v2_shadow_overview.png`
- `implementation/narrative_v2/n_imp_10/04_narrative_v2_shadow_interpretation.png`
- `implementation/narrative_v2/n_imp_10/05_narrative_v2_shadow_action.png`
- `implementation/narrative_v2/n_imp_10/06_production_vs_v2_comparison.png`
- `implementation/narrative_v2/n_imp_10/07_mobile_shadow.png`
- `implementation/narrative_v2/N_IMP_10_REPORT.md`

---

## 16. Files modified

- `applications/api/services/orchestrator.py` — attach shadow envelope after Pack05
- `engines/narrative_v2/runtime/narrative_runtime.py` — `portal_connection="true_shadow"` (boolean `portal_connected` remains False)
- `applications/customer_portal/static/js/result_store.js` — preserve `narrative_v2_shadow`; `loadNarrativeV2Shadow()`
- `applications/customer_portal/src/models/dto.ts` — `NarrativeV2ShadowEnvelopeDto`
- `applications/customer_portal/src/models/index.ts` — export envelope type
- `applications/customer_portal/src/entries/resultApp.tsx` — mount shadow only on explicit flag
- `applications/customer_portal/src/screens/commercial_dashboard/CommercialDashboardPage.tsx` — `data-narrative-surface="production"`
- `applications/customer_portal/tests/js/result_store_flow.js` — PS15 independence + G1-10C on existing harness calendars so `loadCurrent` still runs
- `applications/customer_portal/static/dist/result.js` / `result.css` — Vite production rebuild

Not modified: astrology engines, Pack05 `engines.narrative_engine`, PDF/DOCX export, Golden Dataset, snapshots, expected outputs.

---

## 17. Tests

| ID | Check | Result |
| --- | --- | --- |
| PS1 | Production `/result` unchanged by default | PASS |
| PS2 | V2 shadow loads only with explicit flag | PASS |
| PS3 | Portal reads Presentation v2.1 only | PASS |
| PS4 | `consulting_flow` renders unchanged | PASS |
| PS5 | Structured Interpretation renders unchanged | PASS |
| PS6 | Action Plan renders unchanged | PASS |
| PS7 | Portal does not compose Narrative | PASS |
| PS8 | Missing Summary fields not invented | PASS |
| PS9 | Commercial null handled safely | PASS |
| PS10 | Internal ids not exposed | PASS |
| PS11 | Pack05 remains production default | PASS |
| PS12 | V2 failure does not break Analyze | PASS |
| PS13 | V2 missing/failure does not break `/result` | PASS |
| PS14 | Presentation version validated | PASS |
| PS15 | ResultStore keeps production and shadow independently | PASS |
| PS16 | No astrology engine modified | PASS |
| PS17 | No PDF/DOCX modified | PASS |
| PS18 | Same Presentation → same shadow rendering | PASS |

Commands:

```
py -m pytest applications/api/tests/test_narrative_v2_shadow.py applications/customer_portal/tests/test_result_store.py -q
npx vitest run tests/js/narrative_v2_shadow.test.tsx
```

Summary: **19 passed** (pytest module) + **14 passed** (vitest). Remaining failures in this module: **none**.

---

## 18. Runtime validation

Live CASE-0001 via `/analyze` (1987-01-21 04:30 male, Nguyễn Tiến Sơn, Hà Tây):

1. Analyze completed.
2. Production `/result` showed Pack05 commercial dashboard (name, Tứ Trụ, Overview, Interpretation, Action Plan).
3. ResultStore persisted `narrative_v2_shadow.status === "ok"` with Presentation v2.1.
4. `/result?narrative=v2-shadow` rendered Overview, consulting_flow, structured details, Action Plan, empty Commercial.
5. `/result?narrative=v2-compare` showed Pack05 snippet vs V2 Presentation.
6. Mobile 390×844 shadow view rendered the same Presentation copy.

---

## 19. Screenshots

All under `implementation/narrative_v2/n_imp_10/`:

| File | Content |
| --- | --- |
| `01_production_result_unchanged.png` | Default `/result` Pack05 dashboard, CASE-0001 |
| `02_narrative_v2_shadow_full.png` | Full Shadow Review (`status: partial · version: bte.presentation.v2.1`) |
| `03_narrative_v2_shadow_overview.png` | Overview + missing identity/balance/conclusion placeholders |
| `04_narrative_v2_shadow_interpretation.png` | consulting_flow + structured fields |
| `05_narrative_v2_shadow_action.png` | Action Plan copy-only + current_period placeholder |
| `06_production_vs_v2_comparison.png` | CURRENT PRODUCTION vs NARRATIVE V2 SHADOW |
| `07_mobile_shadow.png` | Mobile shadow review |

---

## 20. Production regression

- Default `/result` still Pack05 Commercial Dashboard.
- No customer-visible routing change without the query flag.
- Pack05 `narrative_result.contract = pack05_narrative_result_v1` still present after Analyze.
- PDF/DOCX export route has no `narrative_v2` reference.
- Calendar / Bazi / Score engines are not imported by the shadow attach module.

---

## 21. CASE-0001 shadow review

Presentation status: **partial**. Version: **bte.presentation.v2.1**.

| Block | Shadow rendering |
| --- | --- |
| Overview headline/summary | Exact V2 copy (stability / foundation / systematic learning) |
| identity / balance / conclusion | Null → diagnostic placeholder, not invented |
| consulting_flow | Exact 07C wording (section 9) |
| Structured Interpretation | All seven fields copied; closing still repeats observation (upstream) |
| Action | “Ưu tiên giữ nền tảng hiện tại” + three practice actions + warning |
| current_period | Null → placeholder |
| Commercial | Empty |

Pack05 production Overview/Interpretation/Action on the same Analyze remain the current customer wording (“Người định khung”, “Thân vượng”, UI-12-style action cards). That difference is expected: shadow does not replace Pack05.

---

## 22. Contract gaps

Unchanged from N-IMP-09A (Portal does not repair them):

- Summary `identity` / `balance` / `conclusion` remain null
- `commercial` remains null (Commercial Builder not implemented)
- `current_period` remains null
- Interpretation `closing` still duplicates `observation`
- Production Pack05 wording and V2 Presentation wording are different systems

No new Portal-side composition was added to close these gaps.

---

## 23. Shadow mode verification

- `SHADOW_MODE=True`
- `replaces_pack05=false` on envelope and UI
- `portal_connected=False` (boolean, existing tests)
- `portal_connection="true_shadow"` (N-IMP-10 Portal attach)
- Pack05 `NarrativeEngine` still builds `narrative_result`
- Customer default route does not mount V2

---

## 24. Out-of-scope confirmation

Pack05 remains production default: **YES**

No production switch: **YES**

No PDF/DOCX integration: **YES**

No astrology engine modified: **YES**

No Portal-side Narrative composition: **YES**

No internal trace exposed: **YES**

N-IMP-11 not started.

---

## 25. Verdict

**READY FOR PRODUCT OWNER REVIEW**
