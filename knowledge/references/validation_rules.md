# Reference Library Validation Rules

**Module:** `knowledge/references`  
**Version:** V1.0.0  

---

## 1. Identifier rules

1. `reference_id` MUST match `^REF-[0-9]{6}$`
2. No duplicated `reference_id` values
3. IDs MUST be unique across the entire library

---

## 2. Title rules

1. `title_english` MUST be unique (case-insensitive trim)
2. `title_original` MUST be non-empty
3. `title_english` MUST be non-empty

---

## 3. Category / enum rules

1. `category` MUST be one of: `classic`, `modern`, `paper`, `internal`
2. `source_type` MUST be one of: `classical_text`, `commentary`, `modern_book`, `journal_article`, `internal_document`
3. `canonical_status` MUST be one of: `draft`, `review`, `official`, `deprecated`, `placeholder`

---

## 4. Required metadata

Every record MUST include all fields defined in `REFERENCES_SPEC.md` §4, including `identifier`.

Empty arrays are allowed for:

- `chapter_support`
- `keywords` (discouraged)
- `related_modules` (discouraged)

`TODO_REVIEW` is allowed for uncertain bibliographic scalars.

---

## 5. Index consistency

1. Every `references.json` record MUST appear in `reference_index.json`
2. Every index entry MUST resolve to a record in `references.json`
3. Index `title` SHOULD equal record `title_english`

---

## 6. Execution

```bash
python knowledge/references/validate_references.py
```

Validation fails if any ERROR-severity rule is violated.
