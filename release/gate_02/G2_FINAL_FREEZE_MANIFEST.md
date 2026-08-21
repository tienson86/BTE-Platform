# G2-FINAL — Freeze manifest

**Release name:** BTE V1.0 — Gate 2 Customer Output Layer  
**Freeze date:** 2026-08-21  
**Entry:** G2-06: END-TO-END CUSTOMER ACCEPTANCE PASS — READY FOR G2-FINAL  
**G2-FINAL production source edits:** none

---

## Repo

| Item | Value |
|------|-------|
| Branch | `release/v1.0-final` |
| HEAD | `2d83ee3e209051ab840c17f6aad8ae4fd3ba017b` |
| HEAD message | Strip rule IDs from pattern evidence and add tests |
| Gate-1 freeze HEAD | `ed6dba05fd7683ed686c1d0035767ede6b5532f3` |
| G2-FINAL analytical / UI / export / persistence edits | **none** |

---

## Gate-1 dependency

| Item | Status |
|------|--------|
| G1-FINAL | PASS — Core Engine frozen |
| `G1_PREFINAL_101_TRUTH.json` SHA256 | `46386BC955119F5DFE9482E7D620767BFB8BB74003A0968A17A6F82017FFA5CC` — **match** |
| Ten named controls vs `G1_PREFINAL_CONTROL_CASES.json` | **0 diffs** |

---

## Customer contracts

| Contract | Frozen value |
|----------|----------------|
| Useful God customer | `analysis_result.UsefulGodView@1.5` |
| Narrative consumer | `pack05_narrative_result_v1` |
| Report model | `ReportInputV1` → `PresentedReportV1` |
| Official PDF | Report V1 + Playwright |
| DOCX | `DocxExporterV1` / python-docx |
| Gate core label | `G1` |
| Month pillar | `BTE-MONTH-PILLAR-LUNAR-V1.0` |

### HK-R1H (customer)

- Dụng = Overall `useful_display`
- Căn cứ chọn Dụng = `short_reason` (visible)
- Customer Hỷ = `favorable_display` only (`favorable_gods` is internal)
- Unsupported Hỷ → `Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng`
- No exact Dụng duplication as customer Hỷ
- Kỵ = current V1.0 `unfavorable_display`
- Điều hậu separate from Overall

---

## Canonical customer flow

```
Analyze → /result → Luận giải → Full Report
  → Tải PDF → Tải DOCX → History
  → reopen History → export again → return current result
```

No alternative customer analytical route may silently take precedence. Legacy `/result?legacy=1` remains explicit legacy only.

---

## Analysis identity

Successful Analyze: HTTP `request_id` = `data.analysis_id` = ResultStore / Report / PDF / DOCX / History id.

No frontend synthetic replacement ID when the server ID exists.

---

## ResultStore precedence

1. Fresh current Analyze  
2. Explicit History `?from=history&id=<analysis_id>` (snapshot in view pointer **or** History list)  
3. Empty gate  

Normal `/result` never silently loads History.

---

## History policy

- Immutable stored snapshot (`input` + `data`)
- Opening History does not re-run Analyze
- Re-analyze creates a **new** analysis; old row unchanged
- Browser-local `localStorage` / `sessionStorage`, maximum **30** rows
- No server History database in V1.0
- New rows store version metadata; old rows are not backfilled
- Incompatible contract → version / re-analyze notice (no silent migration)

---

## Control cases

Ten G1-FINAL named cases. Analytical diff: **0**. Primary G2-06 journeys (Sơn, Tuyền, Dũng, Trường) remain the E2E baseline. Values are not hand-edited. See `G2_FINAL_CONTROL_CASES.md` and `G2_FINAL_PROBE.json`.

---

## Test results (G2-FINAL rerun)

| Suite | Result |
|-------|--------|
| Vitest G2-01R / 02 / 03 / 04 / 05 / 06 | **48 passed** |
| Pytest G2-03 / 04 / 05 / 06 | **22 passed** |
| ResultStore flow harness | **61 passed / 0 failed** |
| Ten-control live probe | **mismatch_count 0** |

Exact commands are in `G2_FINAL_COMPLETION_REPORT.md`.

---

## Known limitations / Gate 3

See `G2_FINAL_KNOWN_LIMITATIONS.md` and `G2_FINAL_GATE3_HANDOFF.md`.

Gate 3 may package and operate the frozen product. It must not change Gate-1 analytical truth or Gate-2 customer semantics.

---

## Gate-2 baseline documents (present)

G2-01 / G2-01R, G2-02, G2-03, G2-04, G2-05, G2-06 freeze reports and checklists under `release/gate_02/` were verified present before this freeze. This pack does not replace them.
