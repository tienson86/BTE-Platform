# Knowledge Naming Conventions

**Status:** Canonical  
**Version:** 1.0.0

---

## Identifiers

| Kind | Pattern | Example |
|------|---------|--------|
| Domain | `DOM-<UPPER_SNAKE>` | `DOM-STRENGTH` |
| Entity | `ENT-<UPPER_SNAKE>` | `ENT-RULE` |
| Relationship | `REL-<UPPER_SNAKE>` | `REL-DEPENDS_ON` |
| Rule (module packs) | `<PREFIX>-<6 digits>` | `STR-000001` |
| Knowledge Record | `KR-<6 digits>` | `KR-000001` |
| Package | lowercase path-safe slug | `01_strength_rules` |
| Migration | `MIG-YYYY-MM-DD-NNN` | `MIG-2026-08-09-001` |

Published identifiers are immutable.

---

## Naming rules

1. Use English machine IDs; localized display names may differ.
2. Prefer stable semantic tokens over school-specific nicknames in IDs.
3. Do not encode version numbers inside IDs.
4. Tags are lowercase `snake_case` or lowercase words.
5. File and folder names for packages remain lowercase with underscores.
6. Ontology concept IDs use `ONT-<UPPER_SNAKE>`.

---

## Multilingual support

- `id` stays language-neutral.
- `language` field carries BCP 47 tags (`vi`, `en`, `zh-Hans`, ...).
- Display labels live in metadata or language-specific payload fields.

---

## Compatibility

Existing Rule Database prefixes (`STR`, `SEA`, `TMP`, `PAT`, ...) remain valid and map into taxonomy domains via package metadata / category.
