# G2-01R — Regression report

## Ten G1-FINAL control cases

Probe: `python release/gate_02/_g2_01_binding_probe.py`  
Frozen: `release/gate_01/G1_PREFINAL_CONTROL_CASES.json`

**Analytical diff vs Gate-1 Frozen Truth: 0**

No GATE-1 FROZEN TRUTH MISMATCH.

## Live Dũng / Tuyền (HTTP Analyze)

Probe: `python release/gate_02/_g2_01r_live_probe.py`

| Case | Pillars | Strength | Pattern | Dụng | Hỷ | Điều hậu preference |
|------|---------|----------|---------|------|----|---------------------|
| Ngô Đắc Dũng | Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn | 1.00 strong | gia_sac LEVEL-1, override false | Thủy · Nhâm · Thực Thần | insufficient (HK-R1H customer copy) | Điều hậu ưu tiên Hỏa |
| Vũ Thị Thanh Tuyền | Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi | 0.66 strong | Kiếp Tài | Mộc · Ất · Chính Quan | insufficient | Điều hậu ưu tiên Thủy |

`data.analysis_id === request_id` on both. Contract `analysis_result.UsefulGodView@1.5`.

## Module tests

| Suite | Result |
|-------|--------|
| `applications/api/tests/test_result_identity.py` | 2 passed |
| `applications/customer_portal/tests/test_result_store.py` | 13 passed (15 total with identity) |
| Vitest G2-01R A–L + boot/routing/adapter/G1-06/full report | passed |
| `npm run build:result` | passed |

## Binding tests A–L

| Id | Coverage | Result |
|----|----------|--------|
| A | empty `/result` no mock | PASS |
| B | server canonical ID persists | PASS |
| C | fresh current beats history | PASS |
| D | explicit history isolated | PASS |
| E | normal `/result` never implicit history | PASS |
| F | `@1.5` mismatch does not use legacy Dụng/Hỷ | PASS |
| G | `legacy=1` cannot affect Desktop boot | PASS |
| H | Dũng frozen fields preserved on bind | PASS |
| I | Tuyền frozen fields preserved on bind | PASS |
| J | Report uses same analysis ID | PASS |
| K | Print HTML uses selected analysis id | PASS |
| L | no field mixing | PASS |

## Frontend recomputation

Portal adapters **copy** published Strength / Pattern / Useful God / Luck / ShenSha fields. They do not re-run engines. Pattern Dụng/Hỷ is no longer a customer fallback.

## Print vs Report V1 PDF

Customer Print = current surface HTML (`window.print` on `/result`, or Report Center `printReport(selected)`).  
Report V1 PDF = server `report_engine` export (internal). **Not unified.** Recorded for G2-04.

Customer Print binds `data-analysis-id` of the selected blob. Report V1 PDF is out of Portal customer controls; G2-01R did not add a new export path.

## DOCX

No customer DOCX. G2-04 scope.

## Legacy fallback inventory (reclassified)

| Path | Classification |
|------|----------------|
| Desktop `/result` + `resultBoot` + `resolveForDisplay` | **ACTIVE CANONICAL** |
| `/interpretation` (same Desktop template) | **ACTIVE CANONICAL** |
| `/reports` structured `BteFullReport` when contract `ok` | **ACTIVE CANONICAL** |
| `?preview=1` / screenshot `previewFallback` | **EXPLICIT LEGACY ONLY** (dev/preview) |
| `/result?legacy=1` + `result.js` + `loadForView` | **EXPLICIT LEGACY ONLY** |
| `static/js/presenters/*` on legacy result | **EXPLICIT LEGACY ONLY** |
| `bte_portal_last_result` read | **EXPLICIT LEGACY ONLY** (migration read) |
| `templates/result.html` | **DEAD** |
| `BaZiResultScreen` on production `/result` | **DEAD** |
| Pattern `dung_than`/`hy_than` as customer Dụng/Hỷ on Desktop | **REMOVED** |
| Empty-store mock fixture on production `/result` | **REMOVED** |
| Implicit `bte_view_result` on normal `/result` | **REMOVED** |
| Unstructured `/reports` HTML when no structured data | **EXPLICIT LEGACY ONLY** |
| React `PortalApp` hash SPA | **EXPLICIT LEGACY ONLY** (not served by `app.py`) |

No **AMBIGUOUS FALLBACK** remains for normal fresh customer result.
