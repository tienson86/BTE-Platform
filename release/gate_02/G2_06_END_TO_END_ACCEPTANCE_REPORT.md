# G2-06 — End-to-end customer acceptance report

**Status: G2-06: END-TO-END CUSTOMER ACCEPTANCE PASS — READY FOR G2-FINAL**

Date: 2026-08-21  
Entry: G2-05 save / History / reload frozen  
Do **not** start G2-FINAL from this report.

Invariant:

```
INPUT → ANALYZE → RESULT → INTERPRETATION → REPORT → PDF → DOCX → HISTORY → REOPEN → EXPORT AGAIN
```

must preserve one coherent frozen analysis.

## Hard freeze

Gate-1 engines and rules were not changed. G2-01R routing/identity, G2-02 Result UI, G2-03 Narrative, G2-04 Report/PDF/DOCX, and G2-05 History remain frozen.

Ten G1-FINAL control cases vs Frozen Truth: **0 analytical diffs**.

If an analytical mismatch had appeared, this gate would have **stopped**.

## Method

Customer journey was executed through the same path the portal uses:

1. `POST /api/v1/analyze` (real orchestrator + identity stamp)
2. Stored snapshot → Result / Luận giải (same payload, no second Analyze)
3. `prepare_customer_report_input` → Presented Report V1 HTML
4. Official Playwright PDF + python-docx DOCX from that stored snapshot
5. History export of selected snapshot A while current is B
6. Re-analyze of A → new id C; snapshot A unchanged

Full live Chromium click-through of `/analyze` was not required; the spec allows a test-harness equivalent of the normal UI path. Portal UI gates (empty, missing, corrupt, contract, labels, isolation) were run in vitest against Canonical Desktop.

## Allowed repairs (non-analytical)

| Defect | Repair |
|--------|--------|
| Double Analyze from overlapping form click/submit | `analyzing` guard in `analyze.js` — one in-flight request |
| Pattern evidence leaked `pat_ca_01` into customer Report HTML/DOCX | Strip internal rule tokens in `customer_report_input._pattern` using the existing customer-facing helper |

Analytical engine/rule files changed: **0**.

## Primary four journeys

| Case | Analyze | Result / Report | PDF | DOCX | Identity |
|------|---------|-----------------|-----|------|----------|
| Nguyễn Tiến Sơn | PASS | Hỏa · Đinh · Chính Quan / CHẾ | file + MIME | Unicode tables | `g2-06-0` |
| Vũ Thị Thanh Tuyền | PASS | Mộc · Ất · Chính Quan / CHẾ — not Tòng Tài, not Nhâm Overall | file + MIME | Unicode tables | `g2-06-4` |
| Ngô Đắc Dũng | PASS | Thủy · Nhâm · Thực Thần / TIẾT / LEVEL-1 Giá Sắc, override false — not Thổ/Mậu/Thiên Ấn | file + MIME | Unicode tables | `g2-06-9` |
| Cao Xuân Trường | PASS | Kim · Tân · Chính Ấn / SINH/TRỢ / weak Nhâm | file + MIME | Unicode tables | `g2-06-5` |

## Ten-control analytical probe

**10/10 MATCH.** API payload, Result fingerprint, and Report model Dụng/Hỷ agree for every G1-FINAL case. See `G2_06_E2E_PROBE.json`.

## Workflow checks

| Check | Result |
|-------|--------|
| Birth labels Nam / Nữ | PASS (`analyze.gender_male` / `gender_female`) |
| One in-flight Analyze | PASS (button disable + `analyzing` flag) |
| Invalid Analyze 422, no stack, no fake result | PASS |
| Failed Analyze does not write History | PASS (save only after success) |
| Empty `/result` gate + Analyze CTA | PASS |
| Missing History → Không tìm thấy hồ sơ | PASS (G2-05 + G2-06 vitest) |
| Corrupt History safe | PASS |
| Old contract → reanalyze notice, no `pattern.dung_than` fallback | PASS |
| Current Tuyền / History Dũng isolated | PASS |
| History PDF/DOCX = Dũng only | PASS |
| Re-analyze Dũng → `g2-06-reanalyze-dung`, old `g2-06-9` unchanged | PASS |
| File A does not contain B | PASS |
| Print labeled **In**, distinct from **Tải PDF** | PASS |
| Export buttons reachable (roles + `aria-label="Xuất báo cáo"`) | PASS |

## Known frozen baseline (not a G2-06 redesign)

Official PDF is Playwright Report V1 (G2-04). Naive Unicode byte-search of the PDF file remains unreliable because of CID fonts. HTML source + DOCX paragraphs/tables are the searchable text artifacts. G2-04 already recorded `pdf_searchable: false`.

Browser persistence remains **localStorage / sessionStorage**. This gate did not add a History database.

Analyze form default gender option is **Nam** (valid customer label, not an English enum). Unspecified remains available.

## Tests

```
python release/gate_02/_g2_06_e2e_probe.py
python -m pytest applications/api/tests/test_g2_06_e2e.py -q
npx vitest run tests/js/g2_06_customer_e2e.test.tsx
```

(from `applications/customer_portal` for vitest)

- Probe: **PASS** (`ten_match`, four primary journeys, history, cross-file, 422)
- API pytest: **4 passed**
- Portal vitest: **5 passed**

## Diff audit

Analytical engine / rule files changed: **0**.

## Final status

**G2-06: END-TO-END CUSTOMER ACCEPTANCE PASS — READY FOR G2-FINAL**

Stop. Do not start G2-FINAL automatically.
