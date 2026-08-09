# Review Checklist

**Use during:** `internal_review`, `technical_validation`, `knowledge_review`  
**Package:** `{{PACKAGE_ID}}` `{{PACKAGE_VERSION}}`

---

## Internal Review

Reviewer: `{{INTERNAL_REVIEWER}}`

- [ ] Draft checklist complete
- [ ] Documentation understandable without engine knowledge
- [ ] Style follows `STYLE_GUIDE.md` / Brand consultant tone where prose exists
- [ ] No secrets, engine source, or API contract copies
- [ ] Manifest `exported_objects` matches actual public ids
- [ ] Approve → technical_validation / Reject → draft with findings

## Technical Validation

Reviewer: `{{TECHNICAL_REVIEWER}}`

- [ ] Schema Validation pass (`PACKAGE`, `MANIFEST`, objects, `DEPENDENCIES`)
- [ ] Metadata Validation pass (identity ↔ manifest consistency)
- [ ] Dependency Validation pass (no cycles, lists agree)
- [ ] Reference Validation pass (ids resolve or documented external paths)
- [ ] Integrity Validation pass (declared files exist; unique ids)
- [ ] Compatibility Validation pass (schema/knowledge/platform/language/school ranges)
- [ ] Quality technical metrics ≥ Bronze
- [ ] `VALIDATION.json` updated
- [ ] Author is not the sole technical approver
- [ ] Approve → knowledge_review / Reject → draft

## Knowledge Review

Reviewer: `{{DOMAIN_REVIEWER}}`

- [ ] Domain meaning correct for declared school
- [ ] References adequate for claims (or explicit `TODO_REVIEW`)
- [ ] Multilingual labels do not change identifier semantics
- [ ] No silent override of another school’s package
- [ ] Intended quality level (Bronze–Platinum) justified
- [ ] Quality Validation stage recorded
- [ ] Author is not the sole domain approver
- [ ] Approve → release_candidate (`validated`) / Reject → draft
