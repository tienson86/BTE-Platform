# Rule Database Edge Cases

**Document:** EDGE_CASES  
**Module:** knowledge/rule_database  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Document recurring edge cases for rule identity, priority conflicts, and coexistence with operational packs.

---

## 1. Framework Domains vs Existing `*_rules/` Packs

**Case:** `01_strength/` framework domain coexists with `01_strength_rules/`.

**Rule:** Do not modify operational packs in this phase. Treat framework domains as scaffolding for future aligned content.

---

## 2. Governance RID vs Framework RUL

**Rule:** Catalog primary key is `RUL-NNNNNN`. Optional governance alias may be noted later without editing Governance.

---

## 3. Conflicting Official Rules

**Rule:** Require Priority; document Related Rules; prefer higher Priority or earlier Official ID per Mapping Standard.

---

## 4. Cross-Domain Rules

**Rule:** Place by primary decision domain; link secondary domains via Related Rules / Knowledge Links.

---

## 5. Missing Knowledge Link

**Rule:** Allowed in Draft. Block Official for doctrinal rules without Knowledge (or explicit Evidence justification).

---

## 6. Special Cases Overflow

**Rule:** Use `12_special_cases/` only when no primary domain fits; graduate later when stable.

---

## 7. Empty Sentence Links

**Rule:** Valid until sentence consumers exist.

---

## 8. Duplicate Extraction Risk

**Rule:** Search domain INDEX, registry, and existing operational indexes before creating new framework rules in later phases.

---

## Resolution Log Template

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Rule ID | RUL-NNNNNN |
| Edge Case | section title |
| Decision | short statement |
| Follow-up | index / registry updates |
