# G2-02 — Customer Result UI freeze report

**Status: G2-02: CUSTOMER RESULT UI FROZEN — READY FOR G2-03**

Date: 2026-08-20  
Entry: G2-01R canonical binding repaired  
Surface: `/result` Canonical Desktop V2 (PACK_07). No second Result UI.

## Hard freeze

Gate 1 analytical truth is unchanged. G2-01R identity/routing/`@1.5` is unchanged.

This phase changed layout, labels, card order, empty/history/version chrome, and customer-safe presentation only.

If a card had looked wrong because engine data was wrong, this gate would have **stopped**. Ten control cases remain **0 analytical diffs**.

## What was frozen

1. **Reading order (primary first):** Tứ trụ → Điểm thân + Cách cục → Dụng/Hỷ/Kỵ + Căn cứ chọn Dụng → Điều hậu → Ngũ hành + Thập thần → Thần sát.
2. **Dụng card** is only Dụng / Hỷ / Kỵ. Reason is a full-width line on that card. Điều hậu is its own card.
3. **Tứ trụ** binds live `s03` pillars (Thiên can / ngũ hành can / Thập thần / Địa chi / ngũ hành chi / Tàng can / Thập thần ẩn). Day pillar shows **Nhật Chủ** when that is the pillar identity.
4. **Điểm thân** shows `label · strength.strength_score` (example: `Thân vượng · 1.00`). Score Engine grade is not under Điểm thân.
5. **Phân bố Ngũ hành** keeps the structural title and the V1.0 disclaimer (counts, not vượng/suy, not Dụng).
6. **LEVEL-1** keeps detected wording (`Cấu trúc đặc biệt được nhận diện: Giá Sắc`). Override-false is not sold as tuyệt đối.
7. **Empty / mismatch / History** chrome: Analyze CTA; reanalyze notice without contract id; History banner without mutating current.
8. **Print:** `/result` hides chrome and unclips critical cards. PDF freeze remains G2-04.

## Acceptance

| Probe | Result |
|-------|--------|
| Dũng | Strength 1.00 strong → Thân vượng · 1.00; Giá Sắc LEVEL-1 detected; Dụng `Thủy · Nhâm · Thực Thần`; Hỷ insufficient; reason Tiết / cân bằng V1.0; Điều hậu Hỏa separate |
| Tuyền | 0.66 strong; Kiếp Tài; Dụng `Mộc · Ất · Chính Quan`; CHẾ; Hỷ insufficient; Điều hậu Thủy separate; no Tòng Tài |
| Ten control cases | Analytical MATCH 10/10 · UI PASS 10/10 |
| Empty / mismatch / History | Gate / notice / banner as specified |

## Tests

```
npx vitest run tests/js src/features/portal
```

- Files: 41 passed
- Tests: **277 passed / 0 failed**
- Added: `applications/customer_portal/tests/js/g2_02_customer_result_ui.test.tsx`
- Ten-case probe: `python release/gate_02/_g2_02_ui_probe.py`

Existing G1 / G2-01R Portal tests were **not** rewritten to weaken asserts.

## Diff audit (this phase)

Analytical engine / rule files changed: **0** (`engines/`, `knowledge/database` clean).

Allowed changes: Portal components, CSS, customer adapters, presentation bindings, Portal tests, release docs, Result bundle.

Working tree may still contain **G2-01R** identity files (`applications/api/routes/v1.py`, ResultStore JS, `result_identity.py`). Those are routing/identity, not Gate-1 analytics.

## Deliverables

- `release/gate_02/G2_02_CUSTOMER_RESULT_UI_FREEZE_REPORT.md` (this file)
- `release/gate_02/G2_02_SECTION_MATRIX.md`
- `release/gate_02/G2_02_CONTROL_CASE_UI_MATRIX.md`
- `release/gate_02/G2_02_VISUAL_ACCEPTANCE.md`
- `release/gate_02/G2_02_REFREEZE_CHECKLIST.md`
- `release/gate_02/screenshots/g2_02/`

## Next

Do **not** start G2-03 automatically. G2-03 begins only after Product Owner accepts this freeze.
