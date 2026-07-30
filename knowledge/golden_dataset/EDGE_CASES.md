# Golden Dataset Edge Cases

**Document:** EDGE_CASES  
**Module:** knowledge/golden_dataset  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Document recurring edge cases for golden case identity, tolerance, and coexistence with operational fixtures.

---

## 1. Framework vs `tests/golden_dataset/`

**Rule:** This module is documentary scaffolding. Do not modify operational fixtures unless a later explicit migration task authorizes it.

---

## 2. CASE vs Legacy `case_0001` Naming

**Rule:** Framework catalog uses `CASE-000001`. Legacy test names may differ; mapping is a future alignment concern, not a silent rename.

---

## 3. Non-Exact Tolerance

**Rule:** Allowed only with versioned Tolerance Policy and Review justification.

---

## 4. Cross-Domain Cases

**Rule:** Place by primary validation concern; link secondary assets explicitly.

---

## 5. Missing Sentence Links

**Rule:** Allowed when case validates Knowledge/Rules only.

---

## 6. Score-Only Cases

**Rule:** Score section MUST declare expected score fields; still prefer Knowledge/Rule links.

---

## 7. Special Cases Overflow

**Rule:** Use `10_special_cases/` only when no primary domain fits; graduate later when stable.

---

## 8. Official Expected Output Change

**Rule:** Bump Version, re-enter Review, record Revision History. Never silent-edit Official outputs.

---

## Resolution Log Template

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Dataset ID | CASE-NNNNNN |
| Edge Case | section title |
| Decision | short statement |
| Follow-up | index / registry updates |
