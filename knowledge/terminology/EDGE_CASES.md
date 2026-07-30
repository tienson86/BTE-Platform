# Terminology Edge Cases

**Document:** EDGE_CASES  
**Module:** knowledge/terminology  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Document recurring edge cases for terminology identity, multilingual labels, aliases, and cross-domain placement.

---

## 1. Same Concept, Multiple Spellings

**Rule:** One Official `TERM-*`; variants go in Aliases.

---

## 2. Traditional vs Simplified Divergence

**Rule:** Keep both fields. Prefer Traditional for classical doctrine notes when sources are classical; keep Simplified for modern accessibility.

---

## 3. Homographs

**Case:** Same Chinese characters, different meanings by domain.

**Rule:** Separate Terminology IDs; disambiguate in English and Definition; cross-link via Related Terms.

---

## 4. Cross-Domain Terms

**Case:** A term belongs to both Ten Gods and Patterns discussions.

**Rule:** Choose primary Domain by dominant Knowledge usage; list secondary domains in Usage notes; link Related Terms.

---

## 5. Deprecated Classical Synonyms

**Rule:** Deprecated term record may exist for citation continuity; must point to surviving Official ID.

---

## 6. Empty Reference Links

**Case:** Foundational term with no REF yet.

**Rule:** Allowed in Draft. For Official, require Reference or internal justification note.

---

## 7. Governance GLS vs TERM IDs

**Rule:** Framework primary key is `TERM-NNNNNN`. Do not edit Governance to force format changes. Optional dual labels may be noted later in metadata.

---

## 8. Vietnamese Missing

**Rule:** Use `N/A` temporarily; treat missing Vietnamese as Minor defect before broad product localization milestones.

---

## 9. School Conflict

**Case:** Term meaning differs by school.

**Rule:** Prefer school-qualified English labels or separate IDs; document School field explicitly.

---

## 10. Bucket Glossary Terms

**Case:** Cross-cutting vocabulary without clear technical domain.

**Rule:** Place in `glossary/` or `basic/`; avoid forcing into specialized domains.

---

## Resolution Log Template

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Term ID | TERM-NNNNNN |
| Edge Case | section title |
| Decision | short statement |
| Follow-up | index updates |
