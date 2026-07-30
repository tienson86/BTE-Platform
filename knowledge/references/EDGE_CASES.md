# Reference Edge Cases

**Document:** EDGE_CASES  
**Module:** knowledge/references  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Document recurring edge cases in reference identity, edition handling, multilingual titles, and cross-linking.

---

## 1. Multiple Titles for One Work

**Case:** A classic has Chinese, English, Vietnamese, and variant romanizations.

**Rule:**

- One Reference ID
- Put preferred display title in `Title`
- Put language-specific titles in dedicated fields
- Put aliases in `mapping/reference_alias.json`

---

## 2. Contested Authorship

**Case:** Traditional attribution differs from modern scholarly attribution.

**Rule:**

- Set `Author` to the conventional attribution used by BTE
- Note contestation in Summary or Notes placeholder
- Reliability SHOULD NOT be `Primary` if identity is unresolved

---

## 3. Edition Families

**Case:** Many modern reprints of one classical work.

**Rule (V1.0.0):**

- Prefer one Reference ID per work-family
- Record a specific modern edition in `Edition` / `Publisher` / `Year` / `ISBN` when citing a particular print
- If an edition diverges enough to change doctrine citations, allocate a new ID and link via Related References

---

## 4. Anthology / “Other Classics” Bucket

**Case:** `REF-000010` Other Classics.

**Rule:**

- Bucket holds pointers and placeholders only
- Important works SHOULD graduate to dedicated files and dedicated IDs
- Do not cite the bucket ID for precise doctrinal claims

---

## 5. Missing ISBN / Pre-modern Sources

**Case:** Classical texts have no ISBN.

**Rule:**

- Set `ISBN` to `N/A`
- Capture edition cues in `Edition`, `Publisher`, `Year` when known

---

## 6. Multilingual Documentation Constraint

**Case:** Module documentation is English-only, but titles are multilingual.

**Rule:**

- Explanatory text in English
- Original-script titles allowed in metadata fields
- Do not translate doctrinal quotes into unverified English as if authoritative

---

## 7. Governance ID Shape Differences

**Case:** Governance examples use `REF-CLASSIC-0001`; library uses `REF-000001`.

**Rule:**

- Keep library primary key as `REF-NNNNNN`
- Store Governance category code in metadata
- Do not edit frozen Governance documents

---

## 8. Empty Related Lists

**Case:** New reference has no Knowledge / Rule / Sentence links yet.

**Rule:**

- Empty lists are valid
- Do not invent placeholder fake asset IDs

---

## 9. Duplicate Detection

**Case:** Two editors create near-duplicate records.

**Rule:**

- Search `REFERENCE_INDEX.md`, aliases, and Chinese/English titles first
- Merge into the earlier Official/Placeholder ID
- Never recycle deleted numbers

---

## 10. Partial Actual Mapping

**Case:** Mapping JSON lists a REF ID not yet Official.

**Rule:**

- Allowed for Draft/Placeholder scaffolding
- Official Knowledge assets SHOULD cite Official references only

---

## 11. School Ambiguity

**Case:** Work spans multiple schools.

**Rule:**

- Choose primary `School`
- Add secondary schools in Keywords and `reference_school.json` mappings

---

## 12. Internal Notes vs External Authority

**Case:** Internal memo summarizes a classic.

**Rule:**

- Internal memo uses Internal category and its own REF ID
- Classic retains Classic category
- Cross-link both; do not replace the classic ID with the memo ID

---

## Resolution Log Template

When an edge case requires a policy decision, record:

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Reference ID | REF-NNNNNN |
| Edge Case | section number / title |
| Decision | short statement |
| Follow-up | index / mapping updates |
