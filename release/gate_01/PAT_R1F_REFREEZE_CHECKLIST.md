# PAT-R1F — Refreeze checklist

**Date:** 2026-08-20  
**Gate:** Special-pattern Overall override safety (conservative V1.0)

---

## Freeze decision

- [x] LEVEL-1 chuyên remain **detected**
- [x] LEVEL-1 chuyên **do not** enter `spc_*` Overall
- [x] G1-X01 follow still may invoke `spc_001` / `spc_002` / `spc_003`
- [x] No new chuyên / phá / Wealth-break theory
- [x] Strength / `str_*` / Flow / Điều hậu / priorities unchanged
- [x] Golden Dataset **not** updated
- [x] G1-FINAL **not** started

---

## PAT-V1.1-DEEP-QUALIFICATION (backlog)

Do **not** implement in V1.0. Author when Product Owner opens V1.1:

- Visible Wealth break conditions for chuyên
- Visible Officer / Killings break conditions (especially Giá Sắc vs siblings)
- Hidden Output significance (visible-only `output_elements` today)
- Root / support requirements
- Element-specific specialized structures (Metal output-empty vs others officer-empty)
- phá cách / tạp khí as identification (today knowledge-only)
- Giá Sắc semantic review (`gia_sac` vs generic strong Metal)
- Qualification levels beyond V1.0 LEVEL 1 vs LEVEL 2 follow
- Special-pattern-specific Useful God theory (`spc_004` Ấn vs ordinary Chế/Tiết)

See also `release/gate_01/PAT_V1.1_DEEP_QUALIFICATION.md`.

---

## Live Dũng

Reconstruct: `1985-09-18 08:00` male → Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn.

- [x] Strength 1.00 strong
- [x] Pattern token `gia_sac`
- [x] Display not absolute “established chuyên” (`Cấu trúc đặc biệt được nhận diện: Giá Sắc`)
- [x] `spc_004` absent from Overall
- [x] Overall `str_004` Thủy · Nhâm · Thực Thần
- [x] Narrative reasoning = `Than vượng cần tiết khí`
- [x] Hỷ/Kỵ from `str_004`, not stale `spc_004`
- [x] Điều hậu remains `sea_004` (climate)
- [x] API restarted; fresh Analyze (not ResultStore)
- [x] POST `/api/v1/analyze` + `/report` + `/narrative` agree on Overall `str_004`
- [x] Report V1 HTML + DOCX: detected Giá Sắc; Dụng/Hỷ/Kỵ from `str_004`; no `spc_004` / `Chuyên cách ưu tiên Ấn`
- [x] PDF exported from the same ReportInputV1 (~154 KB)

---

## Tests

```
pytest tests/useful_god tests/pattern -q
59 passed
```

- [x] New PAT-R1F gate tests
- [x] G1-X01 follow tests

---

## Remaining before G1-FINAL

- HK-R1 Hỷ/Kỵ reconciliation
- Golden update only when Product Owner authorizes
- V1.1 deep chuyên qualification (backlog)

**PAT-R1F: UNDER-QUALIFIED SPECIAL OVERRIDE DISABLED — PATTERN V1.0 REFREEZE READY**
