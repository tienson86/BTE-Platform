# B1_P0_001U_USEFUL_GOD_TYPE_DISPLAY_REPAIR_REPORT

| Field | Value |
|-------|-------|
| Issue | B1-P0-001U Useful God Type and Customer Display Repair |
| Date | 2026-08-17 |
| Edition | Professional |

---

## 1. Status

**COMPLETE — READY_FOR_ARTIFACT_REVIEW**

Canonical K2.1 entity types (`stem` / `role` / `element`) are preserved from Useful God facts through explanation, narrative, published narrative, and the Professional report.

Customer display no longer appends Day Master element to a role-type Useful God.

---

## 2. Root cause

Useful God explainer formatted the selected value as a stem:

```text
selected_el = STEM_ELEMENT.get(facts.selected, facts.day_master_element)
"Dụng thần chính: {selected} ({selected_el})"
```

`STEM_ELEMENT` maps heavenly stems only.

`Thực Thần` missed lookup.

Fallback returned Day Master element `Kim`.

Therefore role-type Useful God rendered as `Thực Thần (Kim)`.

---

## 3. Type preservation

K2.1 `entity_type` is copied from Knowledge lookup. It is not guessed from the label.

| Layer | Where type lives |
|-------|------------------|
| Useful God facts | `selected_entity_type`, `favorable_entity_types`, `unfavorable_entity_types` |
| Explanation | `Decision.selected_entity_type` |
| Knowledge | existing `coverage.selected_entity_type` and entity `entity_type` |
| Narrative | `ChartFocus.selected_entity_type` / Hỷ / Kỵ type tuples |
| Published + Professional | formatted customer labels copied from explanation meaning |

`Decision.selected_type` remains the engine **rule group** (season / strength / …). Entity type is a separate field.

---

## 4. Customer display contract

| `entity_type` | Display |
|---------------|---------|
| `stem` | `Đinh (Hỏa)` — canonical stem→element only |
| `role` | `Thực Thần` — no Day Master element, no derived element |
| `element` | canonical element label only |
| missing type | value only — **no new fallback** |

---

## 5. Sơn before / after

| | Before | After |
|--|--------|-------|
| Engine selected | Thực Thần | Thực Thần |
| Knowledge type | role | role |
| Customer line | `Dụng thần chính: Thực Thần (Kim)` | `Dụng thần chính: Thực Thần` |

Hỷ: Thực Thần, Thương Quan — both `role`.

Kỵ: Tỷ Kiên, Kiếp Tài — both `role`.

---

## 6. Huỳnh regression

| | Result |
|--|--------|
| Engine selected | Đinh |
| Type | stem |
| Customer line | `Dụng thần chính: Đinh (Hỏa)` — unchanged and valid |
| Hỷ | Đinh, Bính, Ất — all `stem` |
| Kỵ | Canh, Tân — all `stem` |

---

## 7. Tân regression

| | Result |
|--|--------|
| Engine selected | Canh |
| Type | stem |
| Customer line | `Dụng thần chính: Canh (Kim)` — unchanged and valid |
| Hỷ | Canh, Tân, Nhâm — all `stem` |
| Kỵ | Giáp, Ất — all `stem` |

---

## 8. Hỷ / Kỵ type verification

Role values are not forced into stem display.

| Chart | Hỷ types | Kỵ types |
|-------|----------|----------|
| Sơn | role, role | role, role |
| Huỳnh | stem, stem, stem | stem, stem |
| Tân | stem, stem, stem | stem, stem |

---

## 9. Files changed

- `engines/interpretation_engine/foundation/facts/useful_god.py`
- `engines/interpretation_engine/foundation/builders/interpretation_facts_builder.py`
- `engines/interpretation_engine/foundation/explanation/models.py`
- `engines/interpretation_engine/foundation/interpreters/useful_god/templates.py`
- `engines/interpretation_engine/foundation/interpreters/useful_god/explainer.py`
- `engines/interpretation_engine/foundation/narrative/input.py`
- `engines/interpretation_engine/foundation/narrative/adapters.py`
- `knowledge/editorial_validation/b1_p0_001u_product_test.py`
- `knowledge/editorial_validation/exports/b1_p0_001u/`
- `knowledge/editorial_validation/B1_P0_001U_USEFUL_GOD_TYPE_DISPLAY_REPAIR_REPORT.md`

---

## 10. Engine changes

**NONE**

UsefulGodEngine ranking and selected values were not modified.

Winners remain:

- Sơn: Thực Thần
- Huỳnh: Đinh
- Tân: Canh

---

## 11. Architecture changes

**NONE**

No Knowledge content change.

No Narrative architecture change (additive type fields only).

No Da Yun change.

---

## 12. Tests

`pytest tests/interpretation_engine/foundation tests/interpretation_engine/knowledge/test_useful_god_knowledge_k2.py tests/interpretation_engine/knowledge/test_useful_god_role_knowledge_k2_1.py tests/interpretation_engine/narrative -q`

**164 passed.** Tests were not modified.

Product check `b1_p0_001u_product_test.py`: **pass**.

---

## 13. Artifacts

`knowledge/editorial_validation/exports/b1_p0_001u/professional/`

| Chart | Pages | PDF |
|-------|------:|-----|
| Nguyễn Tiến Sơn | 11 | `BTE_CASE-0001_Production_E2E.pdf` |
| Lương Ngọc Huỳnh | 11 | `BTE_HUYNH_Production_E2E.pdf` |
| Ngô Đặng Minh Tân | 11 | `BTE_TAN_Production_E2E.pdf` |

Metrics: `knowledge/editorial_validation/exports/b1_p0_001u/_metrics.json`

---

## 14. Final verdict

**READY_FOR_ARTIFACT_REVIEW**

STOP.
