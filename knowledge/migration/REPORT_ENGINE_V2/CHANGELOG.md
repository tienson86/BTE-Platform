# CHANGELOG — Report Engine V2

Date: 2026-08-13

---

## Files changed

### New

| File | Reason |
|------|--------|
| `engines/report_engine/commercial/__init__.py` | Public commercial path |
| `engines/report_engine/commercial/models.py` | Feature-only report models |
| `engines/report_engine/commercial/theme_catalog.py` | Runtime projection of Theme Library V1.0 |
| `engines/report_engine/commercial/theme_hook.py` | Select operating theme + overlays + variant |
| `engines/report_engine/commercial/leak_filter.py` | Customer leak gate |
| `engines/report_engine/commercial/builder.py` | Cover → Identity → Career → Executive |
| `engines/report_engine/commercial/html_renderer.py` | Commercial HTML |
| `engines/report_engine/commercial/pdf_exporter.py` | Commercial PDF |
| `knowledge/migration/REPORT_ENGINE_V2/*` | This migration pack |

### Modified

| File | Reason |
|------|--------|
| `applications/production/orchestrator.py` | Production PDF uses Commercial Report Builder |
| `engines/report_engine/services/__init__.py` | Export commercial builder (wrapper, no API break) |

### Not modified (frozen / out of scope)

Calendar, BaZi, Strength, Pattern, Useful God, Ten Gods, Knowledge packs, CDR, CLL writer/service, Theme Library markdown catalog, Golden Dataset, Quality Gates, Product Context engine, Product Backlog, tests, snapshots, expected outputs.

---

## Tests executed

| Suite | Result |
|-------|--------|
| `py -3.14 -m pytest tests/production -q` | **78 passed** |
| `py -3.14 -m pytest tests/report_engine -q` | **98 passed** |
| `py -3.14 -m pytest tests/golden_dataset -q` | 101 cases PASS; 2 scanner artifacts (see below) |

---

## Golden Dataset

All golden **cases** `case_0001` … `case_0101`: **PASS**.

`test_golden_dataset` also flags two non-case JSON files under `tests/golden_dataset/report_v1/CASE-0001/`:

- `expected_report_input`
- `input`

Schema: “Cannot detect schema.” Pre-existing directory scan — **not** produced by this migration. Tests and Golden Dataset were not edited.

---

## RC2

No RC2 pytest module. RC2 remains a quality-gate score (CASE_0002 commercial floor + CASE_0003 packaging decision). This migration does not change engines or Golden cases. CASE_0003 customer PDF now applies Parent Context (packaging live). CASE_0001/0002 customer PDFs now print the commercial features that RC2 already scored in payload form.

---

## Remaining blockers

1. **Golden dataset scanner** still fails pytest on two Report V1 fixture filenames. Out of scope (do not edit tests / golden files).
2. **CLL residual phrases** (“miền”, “luận vận trình”) can still appear in Executive close. Frozen Commercial Language — not changed here.
3. **Legacy Report V1 presenter** remains for existing `tests/report_engine` HTML/PDF contracts. Customer production path no longer uses it.
4. **Advisor appendix** is implemented but not exercised by CASE_0001–0003 (correct — those are customer PDFs).

None of these block Report Engine V2 customer cutover.

---

## Impact

| Area | Impact |
|------|--------|
| Customer PDF | Now Identity + Career + Executive only |
| Production JSON deliverable | Unchanged (tests still compare feature bodies) |
| Engines | None |
| Public ReportExportServiceV1 | Unchanged |
| Theme Library | Wired at report compose time |

END
