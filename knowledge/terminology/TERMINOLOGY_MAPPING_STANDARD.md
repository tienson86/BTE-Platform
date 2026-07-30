# Terminology Mapping Standard

**Document:** TERMINOLOGY_MAPPING_STANDARD  
**Module:** knowledge/terminology  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define how Terminology IDs map to References, Knowledge Assets, Rules, Sentences, and related terms.

---

## Mapping Targets

| Target | ID Pattern | Field |
|--------|------------|-------|
| Related Terms | `TERM-NNNNNN` | Related Terms |
| References | `REF-NNNNNN` | References |
| Knowledge Assets | Knowledge asset IDs per Governance | Knowledge Assets |
| Rules | Rule IDs per module conventions | Rules |
| Sentences | Sentence IDs per module conventions | Sentences |

---

## Mapping Principles

1. **Explicit over implied** — Do not rely on filename similarity.
2. **Stable IDs only** — Map to allocated identifiers.
3. **Minimal necessary links** — Link what is needed for traceability.
4. **No invented targets** — Empty is better than fake.
5. **Directionality** — Related Terms SHOULD be reciprocal when both Official.

---

## Domain-to-Knowledge Guidance

| Terminology Domain | Typical Knowledge Domains |
|--------------------|---------------------------|
| heavenly_stems / earthly_branches / hidden_stems / five_elements | Foundations / Calendar / BaZi |
| ten_gods | Ten Gods |
| strength | Strength |
| patterns | Pattern |
| useful_gods | Useful God |
| combinations / clashes / punishments / harms / transformations | Combination |
| shensha | ShenSha |
| fortune | Luck |
| fengshui / astrology | Adjacent / optional modules |
| glossary / basic | Cross-cutting |

This table is guidance only; each term records its own links.

---

## Alias Mapping

Spelling / script / language variants of the same concept:

- Prefer one Official `TERM-*`
- Put variants in Aliases
- Do not create a second Official ID for a pure alias

If a historical alias must remain citable:

- Create a Deprecated term record pointing to the surviving Official ID

---

## Conflict Resolution

If two Official terms collide conceptually:

1. Keep the earlier Official ID when possible.
2. Deprecate the later duplicate.
3. Update Related Terms and indexes.
4. Record decision in Revision History.

---

## Framework Phase Note

V1.0.0 creates no populated mapping rows. Mapping rules apply when content is added later.
