# Report Template Edge Cases

**Document:** EDGE_CASES  
**Module:** knowledge/report_templates  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Document recurring edge cases for report template identity, audience, and cross-domain reuse.

---

## 1. Same Structure, Multiple Audiences

**Rule:** Separate `RPT-*` IDs; declare Audience explicitly.

---

## 2. Multilingual Templates

**Rule:** Prefer separate IDs per Language, or one bilingual structure with explicit Language = Bilingual.

---

## 3. Custom Domain Overflow

**Rule:** Use `10_custom/` only when no thematic domain fits; graduate later when stable.

---

## 4. Missing Sentence Links

**Rule:** Allowed in Draft. Official client-facing templates SHOULD include Sentence Links.

---

## 5. Engine Theme vs Knowledge Template

**Case:** Runtime report themes (Classic/Modern/etc.) may exist in engines.

**Rule:** This framework is Knowledge Infrastructure documentation. Do not modify engine theme code from this module.

---

## 6. Cross-Domain Sections

**Rule:** Place template by primary audience/theme; link secondary Knowledge/Sentences explicitly.

---

## 7. Empty Reference Links

**Rule:** Valid when Sentence/Knowledge grounding is sufficient.

---

## Resolution Log Template

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Report Template ID | RPT-NNNNNN |
| Edge Case | section title |
| Decision | short statement |
| Follow-up | index / registry updates |
