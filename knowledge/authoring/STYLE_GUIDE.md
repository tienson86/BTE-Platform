# Style Guide

**Document:** STYLE_GUIDE  
**Version:** 1.0.0  
**Status:** Specification

---

## 1. Voice

- Precise, academic, neutral.
- Prefer short declarative sentences for definitions.
- Avoid marketing language and unverifiable absolute claims (“always”, “never fails”).
- Vietnamese primary authoring language is allowed when the record’s `language` field says so; keep Canonical Name stable in the agreed romanization/English form used by the index.

---

## 2. Structure

1. Follow the template section order (Identity → … → Release).
2. Use tables for identity, sources, relationships, and review fields.
3. Use blockquotes for the canonical definition.
4. Keep hierarchy trees in fenced `text` blocks.
5. Do not reorder Parts in a way that breaks compiler mapping hints.

---

## 3. Placeholders

- Templates use `{{PLACEHOLDER}}`.
- Finished drafts MUST contain zero unresolved `{{...}}` tokens (except when documenting the template system itself).
- Prefer explicit `TODO_REVIEW: …` over leaving placeholders.

---

## 4. Citations & sources

- Cite bibliography as `SRC-NNNNNN`, not free-form book titles alone.
- When quoting, keep quotes short and attribute the source ID.
- Conflict between sources → record under conflict notes; do not silently pick a side without governance.

---

## 5. Emphasis & formatting

- **Bold** sparingly for field labels or true emphasis.
- Code spans for IDs: `KR-000001`, `SRC-000001`, `FOUNDATIONAL_FOR`.
- No emoji in official records.
- No screenshots as substitutes for definitions.

---

## 6. Uncertainty

Mark uncertainty inline:

```text
TODO_REVIEW: Classical attribution of X to Y is contested; pending Academic Review.
```

Do not convert uncertainty into false confidence to pass review.

---

## 7. Length

- Prefer completeness over verbosity.
- Split a second concept into a new `KR-*` rather than expanding one record until it owns two concepts.

---

## 8. Language consistency

| Element | Convention |
|---------|------------|
| Canonical Name | Stable official form used in indexes |
| Vietnamese Name | Diacritics correct when known |
| Chinese | Traditional or simplified — state which if mixed packs require it |
| Pinyin | Tone marks preferred when known |

---

## 9. Cross-links

Link related records by ID (`KR-000002`), not by fragile relative paths alone. Paths in `record_index` are publication concerns.
