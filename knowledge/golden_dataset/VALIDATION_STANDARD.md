# Golden Dataset Validation Standard

**Document:** VALIDATION_STANDARD  
**Module:** knowledge/golden_dataset  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define validation requirements for Golden Dataset framework cases before Official publication and before regression use.

---

## Validation Layers

| Layer | Checks |
|-------|--------|
| L1 Identity | ID format, uniqueness, domain placement |
| L2 Schema | Mandatory fields present |
| L3 Links | Knowledge / Rules / Sentences / References resolve when listed |
| L4 Determinism | Expected Output complete for Official status |
| L5 Review | Review gate recorded |

Framework V1.0.0 validates scaffolding completeness only (no case payloads).

---

## Input Validation Rules

- Input MUST be present for Official cases.
- Input SHOULD be self-contained (no undeclared external state).
- Birth / chart fixtures MUST declare required identity fields when used later.

---

## Expected Output Validation Rules

- Expected Output MUST be present for Official cases.
- Default tolerance is `Exact`.
- Non-exact tolerance MUST be versioned and justified in Evidence/Review notes.
- Silent edits to Official Expected Output are prohibited.

---

## Link Validation Rules

- Prefer empty lists over fake IDs.
- `KNO-*`, `RUL-*`, `SEN-*`, `REF-*` MUST use allocated formats when present.
- Broken links are Major defects.

---

## Score Validation Rules

- If Score is in scope for the case, Expected Output or Score section MUST declare the scored fields.
- Score expectations MUST align with linked Knowledge/Rules when those links exist.

---

## Pass / Fail Semantics (Future Content Phase)

| Result | Meaning |
|--------|---------|
| Pass | Actual matches Expected under Tolerance Policy |
| Fail | Deterministic mismatch |
| Skip | Missing actual / not executable |
| Error | Execution or schema failure |

---

## Non-Goals

This standard does not run engines and does not modify `tests/golden_dataset/`.
