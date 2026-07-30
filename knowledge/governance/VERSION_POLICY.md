# Version Policy

**Module:** `knowledge/governance`  
**Document:** VERSION_POLICY  
**Version:** V1.0.0  
**Status:** Official Foundation  

---

## 1. Version format

Knowledge Foundation assets use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

Displayed forms MAY use a `V` prefix (example: `V1.0.0`).

---

## 2. When to bump

| Change type | Bump |
|-------------|------|
| Breaking ID remapping or incompatible catalog shape | MAJOR |
| Additive records / fields / docs (compatible) | MINOR |
| Typo, formatting, clarification only | PATCH |

---

## 3. Identifier immutability

- Published `REF-*`, `TERM-*`, and `KNO-*` IDs are immutable
- Meaning of an ID MUST NOT silently change after Official release
- If a work must move, allocate a new ID and deprecate the old one

---

## 4. Catalog version fields

JSON catalogs (`references.json`, `glossary.json`, etc.) MUST include a top-level `version` string aligned with the module CHANGELOG.

---

## 5. Related detailed documents

- `policies/01_VERSIONING_POLICY.md`
- `architecture/06_VERSIONING_MODEL.md`
