# BTE V1.0 — Final Presentation Polish Report

**Status:** PASS  
**Scope:** Customer-facing Result / Full Report / HTML / Print / PDF / DOCX  
**Date:** 2026-08-20  
**G1-FINAL:** not started

Presentation only. Strength, Pattern, Temperature, Useful God, Ten Gods mapping, ShenSha calculation, Luck, Score, and Golden analytical truth were not changed in this polish.

---

## 1. Customer rule IDs

Internal tokens such as `rule cli_001`, `rule com_san_01`, `pat_*`, `str_*`, `sea_*`, `tmp_*`, `flo_*` remain on engine / canonical payloads (`evidence_compact`, `winning_rule_id`, diagnostics).

Customer surfaces strip them:

- Portal Result (`canonicalDesktopAdapter` + Result cards)
- Full Report HTML (`fullReportViewModel`)
- Report V1 HTML / PDF / DOCX (`display_text` + `report_sections_v1`)

Technical / diagnostic views may still show compact evidence with scores and rule IDs.

---

## 2. Nhật chủ / Thân / Cách cục card

Duplicated headings removed from customer copy:

- Căn cứ chính
- Căn cứ (pattern)
- Căn cứ khí hậu

Customer layout:

| Field | Source |
|---|---|
| Nhật chủ | canonical day master |
| Thân | Strength classification + score |
| Yếu tố chính | natural-language Strength evidence |
| Cách cục | canonical Pattern + short stripped evidence |
| Điều hậu | climate + balancing need + short climate evidence |

Luck still has its own `Căn cứ` row (G1-08). That is not one of the three identity-card duplicates.

---

## 3. Strength customer summary

Raw contributions (`+10 / -20 / …`) are no longer the customer card body.

Summary is generated from canonical `evidence_compact` reasons plus month branch. It is not hard-coded to any CASE.

Đặng Thị Dung live example:

`Vô căn · sinh tháng Tỵ · Thực Thương tiết khí mạnh · Quan Sát gây áp lực · có sinh trợ nhưng không đủ cân lại`

Canonical compact evidence is unchanged and still contains signed scores.

---

## 4–8. Ten Gods prominence (presentation)

G1-01 mapping is unchanged. Full visible / hidden / stem / pillar / provenance data remains on the technical payload and in the Full Report Lộ can / Tàng can lines.

Customer heuristic (deterministic, no cát/hung rank):

1. visible stem occurrence
2. repeated hidden occurrences
3. total occurrence count
4. pillar spread

Labels: `Lộ rõ` · `Ẩn nổi bật` · `Có ẩn` · `Không hiện`

Day Stem is never counted as Tỷ Kiên. Nhật Chủ is excluded from the prominence list.

Customer card title: **Thập thần nổi bật** (top 3–5) then `Các thần khác: …`

### Đặng Thị Dung live prominence (not hard-coded)

| Thần | Class | Evidence |
|---|---|---|
| Thất Sát | Lộ rõ | Tân lộ trụ Giờ, đồng thời có tàng |
| Chính Ấn | Lộ rõ | Nhâm lộ trụ Năm |
| Tỷ Kiên | Lộ rõ | Ất xuất hiện ngoài Nhật can |
| Chính Tài | Ẩn nổi bật | Mậu xuất hiện lặp trong tàng can (Năm · Tháng · Ngày · Giờ) |
| Chính Quan | Ẩn nổi bật | Canh xuất hiện tại 3 chi Tỵ |

`Thương Quan` is also `Ẩn nổi bật` (Bính in three Tỵ) and appears under **Các thần khác** because the featured slot cap is 5. Three Tỵ is still visible via Chính Quan.

---

## 9–10. ShenSha prominence

G1-07 calculation is unchanged. No Hoa Cái / Cô Thần / Đào Hoa / Dịch Mã were added.

Multiple occurrences get `Nổi bật` plus positions, e.g. Hồng Loan: `Có tại trụ Tháng · Ngày · Giờ`.

Single occurrence stays `Có` plus one pillar, e.g. Thiên Đức Quý Nhân: `Có tại trụ Giờ`.

---

## 11–12. Pattern / Temperature copy

Pattern customer evidence is the canonical identification line with `rule com_san_01` / `pat_*` removed. No extra Deep Pattern qualification is invented.

Temperature customer evidence is climate-only, not Overall Useful God:

Đặng Thị Dung: `Sinh tháng Tỵ, khí mùa Hạ thiên nhiệt.`  
Nguyễn Tiến Sơn: `Sinh tháng Sửu, khí mùa Đông thiên hàn.`

Canonical `evidence_compact` still includes `rule cli_*`.

---

## 13. Cross-surface

Same presentation helpers feed:

- `/result` (Canonical Desktop → Result adapter)
- Full Report HTML / print
- Report V1 HTML / PDF / DOCX (`build_presented_report`)

Portal rebuilt: `applications/customer_portal` `npm run build:result`.  
API restarted so Report V1 Python presentation is live.

Product Owner must **Analyze again** after this rebuild (`bte_last_result` is browser-local).

---

## 14. Tests

Added:

- `applications/customer_portal/tests/js/v1_final_presentation_polish.test.ts`
- `tests/report/test_v1_final_presentation_polish.py`

Updated heading/HTML assertions (presentation contract only):

- `g1_03_pattern_binding.test.ts`
- `g1_04_temperature_binding.test.ts`
- `g1_06_useful_god_binding.test.ts`
- `tests/report_engine/test_g1_04_temperature_binding.py` (HTML looks for `Sinh tháng Sửu`, not `Nguyệt lệnh Sửu`; canonical ReportInput still has Nguyệt lệnh)

Golden Dataset / snapshots / expected analytical JSON: not modified.

Results:

| Suite | Result |
|---|---|
| Portal G1-02 / G1-03 / G1-04 / G1-06 + polish | 18 passed |
| `pytest tests/report -q` | 52 passed |
| `pytest tests/report_engine` after heading fix | 126 passed + 2 fixed, then re-checked G1-01 / polish PASS |

---

## 15. Live validation

Live `POST http://127.0.0.1:8000/api/v1/analyze`.

### Nguyễn Tiến Sơn — 1987-01-21 04:30 male Asia/Bangkok

| Check | Result |
|---|---|
| Analytical truth | Strength **0.87 strong**, Pattern **Chính Ấn** — unchanged |
| Canonical climate | still contains `rule cli_*` |
| Customer climate | `Sinh tháng Sửu, khí mùa Đông thiên hàn.` — no rule ID |
| Strength summary | readable season/root/support/officer/Ấn mùa lạnh language, not `+25 / -10` |
| Ten Gods | Lộ rõ: Thiên Ấn, Thất Sát, Kiếp Tài; Ẩn nổi bật: Chính Ấn, Thiên Tài |
| ShenSha | only canonical live stars (Thiên Ất / Hồng Loan / Thiên Đức / Nguyệt Đức) |

### Đặng Thị Dung — 1982-05-22 09:30 female Asia/Bangkok

| Check | Result |
|---|---|
| Pillars | Nhâm Tuất / Ất Tỵ / Ất Tỵ / Tân Tỵ, Nhật chủ Ất |
| Thân | **0.24 weak / Thân nhược** (current canonical after G1-02R) |
| Pattern | `Sát Ấn tương sinh — Thất Sát chế bởi Chính Ấn` (`com_san_01` stays on engine, stripped in customer copy) |
| No customer rule IDs | PASS |
| Three Tỵ | Chính Quan `Canh xuất hiện tại 3 chi Tỵ`; Thương Quan also Ẩn nổi bật |
| Thất Sát | Lộ rõ, visible hour + tàng |
| Hồng Loan | `Nổi bật` · `Có tại trụ Tháng · Ngày · Giờ` |
| Unsupported stars | not present |

---

## Files changed (this polish)

Presentation / tests only:

- `applications/customer_portal/src/adapters/customerFacingPresentation.ts` *(new)*
- `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts`
- `applications/customer_portal/src/adapters/canonicalShenSha.ts`
- `applications/customer_portal/src/adapters/tenGodsDisplay.ts`
- `applications/customer_portal/src/adapters/baziResultAdapter.ts`
- `applications/customer_portal/src/report/fullReportViewModel.ts`
- `applications/customer_portal/src/screens/result/**`
- `applications/customer_portal/src/screens/canonical_desktop/sections/S07ShenSha.tsx`
- `applications/customer_portal/src/styles/result-page.css`
- `engines/report_engine/rendering/customer_facing.py` *(new)*
- `engines/report_engine/rendering/report_sections_v1.py`
- `engines/report_engine/localization/display.py`
- presentation tests listed above

Portal production bundle rebuilt under `applications/customer_portal/static/dist/`.

**Not part of this polish:** uncommitted G1-02R Strength engine files and G1-02R reports already in the working tree.

---

## Acceptance

| Criterion | Status |
|---|---|
| Customer report contains no internal rule IDs | PASS |
| Duplicated Căn cứ headings removed | PASS |
| Strength evidence reads as customer explanation | PASS |
| Ten Gods has a clear prominence hierarchy | PASS |
| ShenSha multiple occurrences are visually meaningful | PASS |
| No analytical engine changed in this polish | PASS |
| PDF/DOCX/Result share the same presentation helpers | PASS |
| Live Sơn + Dung | PASS |

---

## Remaining

Do **not** start G1-FINAL until Product Owner re-Analyzes both cases on the rebuilt `/result` (port 8081) and confirms the printed Full Report.

END
