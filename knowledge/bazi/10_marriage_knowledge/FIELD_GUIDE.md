# Field Guide — Marriage Knowledge

**Module:** `knowledge/bazi/10_marriage_knowledge`  
**Version:** V1.0.0  
**Status:** Draft (Blueprint)

---

## 1. How to populate future records

1. Copy `examples/template_record.json`
2. Place the new file under `knowledge_records/<slug>.json`
3. Replace every `TODO_AUTHOR` / `KNO-XXXXXX` / `REF-XXXXXX`
4. Keep uncertain scholarly fields as `TODO_REVIEW`
5. Do not invent bibliographic metadata
6. Submit for Technical then Academic Review

---

## 2. Writing rules

- Write identity-level definitions first; expand only after Academic Review
- Prefer clear English; keep original-script fields when known
- No scoring formulas or engine pseudocode in Knowledge Records
- No silent copy from other modules — link by ID instead

---

## 3. Naming rules

| Item | Rule |
|------|------|
| File name | `snake_case.json` matching `identity.slug` |
| Knowledge ID | `KNO-NNNNNN` allocated by registry / governance |
| Status | `draft` / `review` / `official` / `deprecated` / `archived` |

---

## 4. Reference rules

- Cite Foundation Reference IDs only (`REF-NNNNNN`)
- `title` SHOULD match Foundation `title_english`
- Unverified `chapter` / `notes` use `TODO_REVIEW`
- Follow `knowledge/citation_rules/citation_policy.md`

---

## 5. Terminology rules

- Prefer Foundation canonical terms (`TERM-*`)
- Do not invent parallel spellings for Official records
- Use aliases only via Foundation `aliases.json` mapping

---

## 6. Validation checklist (author)

- [ ] Required base sections present
- [ ] IDs correctly formatted
- [ ] References resolve
- [ ] Related Knowledge IDs resolve (or deferred with note)
- [ ] No academic invention marked as fact
- [ ] revision_history updated
