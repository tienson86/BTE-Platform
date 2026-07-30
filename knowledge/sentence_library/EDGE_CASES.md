# Sentence Library Edge Cases

**Document:** EDGE_CASES  
**Module:** knowledge/sentence_library  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Document recurring edge cases for sentence identity, templates, tone, and cross-links.

---

## 1. Same Condition, Multiple Tones

**Rule:** Separate `SEN-*` IDs; declare Tone/Style explicitly; link Related sentences in notes if needed.

---

## 2. Multilingual Variants

**Rule:** Prefer separate IDs per Language, or one bilingual template with explicit Variables. Do not mix undeclared languages.

---

## 3. Variable Drift

**Case:** Template uses `{day_master}` but Variables omit it.

**Rule:** Treat as Major defect; block Official.

---

## 4. Rule Without Knowledge

**Rule:** Allowed if Rule Link is present and Evidence justifies. Prefer both Knowledge and Rule links for doctrinal sentences.

---

## 5. Cross-Domain Wording

**Rule:** Place by primary communicative domain; link secondary Knowledge/Rules explicitly.

---

## 6. Special Cases Overflow

**Rule:** Use `12_special_cases/` only when no primary domain fits; graduate later when stable.

---

## 7. Governance SEN Padding

**Case:** Governance examples use `SEN-00412`.

**Rule:** Framework catalog uses zero-padded `SEN-000412` equivalents for new IDs. Do not edit Governance files.

---

## 8. Empty Reference Links

**Rule:** Valid when Knowledge/Rule grounding is sufficient; still prefer References for high-stakes claims.

---

## Resolution Log Template

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Sentence ID | SEN-NNNNNN |
| Edge Case | section title |
| Decision | short statement |
| Follow-up | index / registry updates |
