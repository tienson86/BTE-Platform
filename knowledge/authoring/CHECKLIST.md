# Authoring Checklist

**Document:** CHECKLIST  
**Version:** 1.0.0  
**Status:** Specification  
**Use before:** Submit for review (`draft` → `review`)

Record: `{{RECORD_ID}}` — `{{CANONICAL_NAME}}`  
Author: `{{PRIMARY_AUTHOR}}` — Date: `{{DATE}}`

---

## A. Identity & naming

- [ ] `KR-*` assigned and not reused
- [ ] Filename matches naming convention
- [ ] Canonical Name unique
- [ ] Vietnamese / Chinese / Pinyin filled or `TODO_REVIEW`
- [ ] Status is `draft` (or `review` only after submit)
- [ ] Version is SemVer

## B. Canonical Definition

- [ ] Single clear definition
- [ ] Scope present
- [ ] Out of scope present
- [ ] No engine/business hard-coding in definition

## C. Academic Assertions

- [ ] Non-trivial claims sourced or asserted
- [ ] All `SRC-*` exist (or explicitly pending with `TODO_REVIEW`)
- [ ] Assertion IDs use `ASR-*`
- [ ] No `confidence=high` with open `TODO_REVIEW`

## D. Examples

- [ ] Examples use `EX-*` when present
- [ ] Parent KR linked
- [ ] Not used as golden test expected output

## E. Relationships

- [ ] Only approved edge types
- [ ] No dependency cycles introduced
- [ ] No duplicate triples
- [ ] Targets are real or planned `KR-*` / `SRC-*` with notes

## F. Ontology

- [ ] Correct knowledge / node type (Concept, Entity, Rule, Example, …)
- [ ] One canonical concept identity
- [ ] Aliases are aliases, not new IDs

## G. Validation readiness

- [ ] No leftover `{{PLACEHOLDERS}}`
- [ ] Self-check against quality dimensions (completeness … governance)
- [ ] Open issues listed honestly

## H. Review workflow

- [ ] [CHECKLIST](CHECKLIST.md) complete (this document)
- [ ] Author is not requesting self-approval for official
- [ ] Review template prepared or scheduled
- [ ] Known conflicts documented

---

## Sign-off

| Role | Name | Result |
|------|------|--------|
| Author self-check | | Pass / Fail |
| Ready for RV-01 Submit | | Yes / No |

Notes:

{{NOTES}}
