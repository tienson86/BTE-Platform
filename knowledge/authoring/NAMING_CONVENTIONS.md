# Naming Conventions

**Document:** NAMING_CONVENTIONS  
**Version:** 1.0.0  
**Status:** Specification

---

## 1. Identifier patterns

| Kind | Pattern | Example |
|------|---------|---------|
| Knowledge Record | `KR-[0-9]{6}` | `KR-000001` |
| Assertion | `ASR-[0-9]{6}` | `ASR-000001` |
| Relationship instance | `REL-[0-9]{6}` | `REL-000001` |
| Example | `EX-[0-9]{6}` | `EX-000001` |
| Bibliography source | `SRC-[0-9]{6}` | `SRC-000001` |
| Change request | `CR-[0-9]{6}` | `CR-000001` |
| Topic | `TOPIC-[0-9]{6}` | `TOPIC-000001` |
| Graph edge (index/graph docs) | `EDGE-[0-9]{6}` | `EDGE-000001` |

IDs are **globally sequential** within their prefix family unless a published policy states otherwise. Do not invent parallel ID schemes in a single module.

---

## 2. Immutability

- `KR-*` NEVER changes meaning or is reused after assignment.
- File renames MUST keep the same `KR-*` in the filename when the record already exists.
- Deprecation does not free the ID.

---

## 3. File names

```text
KR-NNNNNN_<CANONICAL_KEY>.md
```

| Rule | Example |
|------|---------|
| Uppercase prefix + zero-padded id | `KR-000003` |
| Canonical key: `snake_case`, ASCII | `WU_XING` or `wu_xing` — pick pack convention and stay consistent |
| No spaces | `KR-000001_YIN_YANG.md` |

Draft workspace design files may use other names; published records follow this pattern.

---

## 4. Canonical keys

Used in `canonical_index.json`:

- `snake_case`
- ASCII
- Unique
- Derived from Canonical Name (`Yin Yang` → `yin_yang`)

---

## 5. Pack & module names

| Kind | Form | Example |
|------|------|---------|
| Pack | `PACK_NN` | `PACK_01` |
| Module directory | `NN_snake_case` | `01_fundamental_knowledge` |

---

## 6. Edge / relationship type names

Use **exact** ontology codes (uppercase with underscores):

`FOUNDATIONAL_FOR`, `DEPENDS_ON`, `CLASSIFIES`, `REFERENCES`, `SUPPORTED_BY`, `RELATED_TO`, `CONFLICTS_WITH`, `IMPLEMENTS`

Do not invent synonyms (`SUPPORTS`, `based_on`) in new records — map historical prose at index time if needed.

---

## 7. Status & version fields

| Field | Form |
|-------|------|
| Version | SemVer `MAJOR.MINOR.PATCH` |
| Status | `draft` \| `review` \| `approved` \| `official` \| `deprecated` \| `archived` (as applicable) |
| Freeze | `unfrozen` \| `candidate` \| `frozen` |
| Release | `unreleased` \| `candidate` \| `released` \| `superseded` \| `withdrawn` |

---

## 8. Alias naming

- Aliases are labels, not IDs.
- Do not create `KR-*` for an alias.
- Deprecated spellings use alias_kind `deprecated` / `historical`.
