# D2 — Golden Validation

Version: 1.0

Status: COMPLETE — Sprint D2

Pack: 05 (Narrative Engine)

---

# 1. Policy

Sprint D2 golden validation uses a **structural golden fixture** owned by Narrative Engine tests.

It does **not** modify `knowledge/golden_dataset`.

It does **not** freeze free-form commercial prose (which must remain source-traced).

---

# 2. Fixture

Path:

`tests/narrative_engine/golden/d2_narrative_result_structure.json`

Validates:

| Check | Expected |
|-------|----------|
| Section count | 7 |
| Section ids / order | Official Sprint B order |
| Summary keys | Five commercial answers + confidence/flags |
| Insufficient text | `Chưa đủ dữ liệu để đưa ra kết luận.` |
| Filled paragraphs | Must carry evidence or interpretation refs |

Test:

`tests/narrative_engine/test_composer_d2.py::test_golden_structure_validation`

---

# 3. Source-support validation

Additional test asserts filled paragraph text is supported by Analysis/Interpretation source pool (no invented tokens).

---

# 4. Result

**PASS** with current Sprint D2 implementation and tests.

---

END
