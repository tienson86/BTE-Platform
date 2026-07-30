# Validation — Career Knowledge

**Module:** `knowledge/bazi/11_career_knowledge`  
**Version:** V1.0.0  
**Status:** Draft (Blueprint)

---

## 1. Required fields

Future Knowledge Records MUST include base Knowledge Record sections:

- `identity`
- `classification`
- `definition`
- `characteristics`
- `relationships`
- `references`
- `metadata`
- `validation`
- `revision_history`

Module-specific required slots will be defined when a module schema overlay is authorized (schemas are locked in this sprint).

---

## 2. Schema validation

- Validate against Foundation base schema when content exists
- Module overlay schemas are out of scope for this blueprint sprint
- Blueprint templates are not asserted schema-valid Official content

---

## 3. Reference validation

- Every `references[].reference_id` MUST exist in `knowledge/references/references.json`
- Empty `references` array allowed only for non-Official draft placeholders
- Invented `REF-*` IDs are errors

---

## 4. Relationship validation

- Related `KNO-*` IDs MUST exist before Official status
- Cross-module relationships documented in MODULE_SPEC
- Broken links are errors for Official promotion

---

## 5. Terminology validation

- Canonical labels SHOULD match Foundation glossary where applicable
- Unknown terms require Terminology registration before Official use

---

## 6. Blueprint-phase validation

For this sprint, validation means:

1. Required module files exist
2. `knowledge_records/` contains no academic JSON records
3. Example/template files are placeholders only
