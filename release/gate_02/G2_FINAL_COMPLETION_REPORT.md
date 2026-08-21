# G2-FINAL — Completion report

**Date:** 2026-08-21  
**Final status:** G2-FINAL: PASS — BTE V1.0 CUSTOMER OUTPUT LAYER FROZEN

G2-FINAL was a freeze / release documentation phase. No analytical engines, Result UI, narrative, export path, or History persistence code was modified.

---

## What is frozen

Customer flow:

Analyze → `/result` → Luận giải → Full Report → Tải PDF → Tải DOCX → History → reopen → export again → current result.

Contracts: `analysis_result.UsefulGodView@1.5`, `pack05_narrative_result_v1`, `ReportInputV1` / `PresentedReportV1`. Official PDF = Report V1 Playwright. History = immutable browser-local snapshot (max 30). Identity: `request_id` = `data.analysis_id`.

Baseline packs G2-01R through G2-06 remain authoritative. This freeze does not rewrite their expected values.

---

## Tests (exact totals)

```
npx vitest run tests/js/g2_01r_canonical_binding.test.tsx tests/js/g2_02_customer_result_ui.test.tsx tests/js/g2_03_narrative_freeze.test.ts tests/js/g2_04_customer_export.test.tsx tests/js/g2_05_history_reload.test.tsx tests/js/g2_06_customer_e2e.test.tsx
```

(from `applications/customer_portal`) — **6 files, 48 passed**

```
python -m pytest applications/api/tests/test_g2_04_customer_export.py applications/api/tests/test_g2_04_export_parity.py applications/api/tests/test_g2_05_history_snapshot.py applications/customer_portal/tests/test_g2_05_history.py applications/api/tests/test_g2_06_e2e.py tests/commercial_knowledge/test_g2_03_signal_projection.py -q
```

— **22 passed**

```
node applications/customer_portal/tests/js/result_store_flow.js
```

— **61 passed / 0 failed**

Ten-control live fingerprint vs `G1_PREFINAL_CONTROL_CASES.json`: **mismatch_count 0** (`G2_FINAL_PROBE.json`).

`G1_PREFINAL_101_TRUTH.json` SHA256 re-verified against G1-FINAL.

---

## Control cases / exports / History

Ten named G1-FINAL cases: 0 analytical diffs. Primary G2-06 journeys Sơn / Tuyền / Dũng / Trường remain PASS. Official PDF/DOCX artifacts were not regenerated. History isolation and re-analyze-new-row behavior remain as G2-05 / G2-06.

---

## Known limitations

See `G2_FINAL_KNOWN_LIMITATIONS.md` (local History, Print vs official PDF, CID-font PDF grep, concise narrative, Hỷ/Kỵ V1.1).

Gate-1 V1.1 backlog remains: `release/gate_01/G1_FINAL_V1_1_BACKLOG.md`. Gate-2 later items (server History, account sync, richer narrative/PDF, accessibility/mobile polish) are not V1.0 blockers.

---

## Next gate

Gate 3: packaging, environment, deployment, proxy, TLS, backup, monitoring, release automation.

Gate 3 must not change Gate-1 analytical truth or Gate-2 customer semantics.

**Do not start Gate 3 automatically.**
