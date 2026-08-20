# UG-R2 — Refreeze checklist

**Date:** 2026-08-20  
**Status to freeze against:** architecture split is done; **knowledge coverage is not closed.**

Do **not** start G1-FINAL until Product Owner accepts the knowledge-gap list (or explicitly defers it).

---

## Freeze what is repaired

- [x] Điều hậu (`sea_*` / `tmp_*`) is a separate layer from Overall Dụng thần.
- [x] Climate candidate cannot automatically win Overall.
- [x] No silent fallback from season/temperature when Overall is empty.
- [x] Incomplete Overall copy: `Chưa đủ căn cứ xác định Dụng thần tổng thể`.
- [x] Strength / Pattern / G1-X01 / G1-05 counts unchanged.
- [x] Hỷ/Kỵ copied from Overall winner only.
- [x] Customer Dụng/Hỷ/Kỵ vs Điều hậu presentation split (Portal, Report, PDF, DOCX).
- [x] Five Elements disclaimer under G1-05 distribution.
- [x] API `UsefulGodView@1.2` additive climate fields; `useful_god` remains Overall.
- [x] 101-case Overall groups: `strength` + `special` only (season/temperature = 0).

---

## Do not freeze as complete theory

- [ ] Strong Day Master wealth path (none in CSV).
- [ ] Strong control via Thất Sát / Mộc for Earth (Tuyền).
- [ ] Pattern-main / combination Useful God rules (`kiep_tai`, `chinh_an`, …).
- [ ] Follow gaps: `tong_vuong`, `tong_nhi`, `tong_an`.
- [ ] Special gap: `jia_wang` not in `spc_004`.
- [ ] Flow unique-max occurrence as Overall excess (explicitly not promoted).
- [ ] Wiring `knowledge/packages/useful_god` (`bz_07`) into production.

Marked: **`V1.0 KNOWLEDGE GAP — PRODUCT OWNER DECISION REQUIRED`**.

---

## Regression commands (module only)

```
python -m pytest tests/useful_god tests/temperature/test_g1_04_temperature_binding.py tests/report_engine/test_g1_06_useful_god_binding.py tests/report_engine/test_g1_04_temperature_binding.py tests/report_engine/test_g1_05_five_elements_binding.py tests/report_engine/test_case_0001_report_input.py -q
```

Portal:

```
npx vitest run tests/js/g1_06_useful_god_binding.test.ts tests/js/g1_05_five_elements_binding.test.ts tests/js/g1_04_temperature_binding.test.ts
```

Golden Dataset / snapshots / expected JSON: **not edited.** CASE-0001 report-input snapshot compares everything except `useful_god` + `interpretation` (those now follow structural Overall).

---

## Product Owner sign-off

| Question | Options |
|----------|---------|
| Accept Tuyền Overall = Kim · Canh · Thực Thần (`str_004`) with Điều hậu Thủy separate? | Yes / No |
| Author a later knowledge task for Mộc / Thất Sát control / Pattern-UG rules? | Defer / Author |
| Allow G1-FINAL? | **Not until this checklist’s knowledge items are decided.** |
