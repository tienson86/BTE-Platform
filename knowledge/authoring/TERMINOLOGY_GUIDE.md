# Terminology Guide

**Document:** TERMINOLOGY_GUIDE  
**Version:** 1.0.0  
**Status:** Specification

---

## 1. Purpose

Keep Canonical Names, aliases, and glossary terms consistent so indexes, compiler artifacts, and reviews do not diverge.

---

## 2. Canonical Name vs alias

| Term | Role |
|------|------|
| Canonical Name | Single official name for the concept in the KR and `canonical_index` |
| Vietnamese Name | Official Vietnamese rendering |
| Chinese / Pinyin | Classical rendering |
| Alias | Alternate spelling or common name that **resolves to** the same `KR-*` |

Rules:

1. One Canonical Name per `KR-*`.
2. Aliases never become a second Canonical Name without a governed rename (rare; usually prefer alias).
3. “Vital Qi”, “Universal Qi”, etc. are descriptive phrases — do not promote them to Canonical Name without Academic Review.

---

## 3. Glossary & terminology libraries

When `knowledge/terminology/` (or module glossary) defines a term:

- Prefer the glossary’s preferred form for Canonical Name.
- Register abbreviations in the abbreviations registry when applicable.
- Do not redefine a glossary term inside a KR with a conflicting meaning — open a change request.

---

## 4. Cross-language consistency

| Language | Guidance |
|----------|----------|
| English / romanization | Use the form already in Pack inventory when present |
| Vietnamese | Preserve diacritics (`Khí`, `Ngũ Hành`) |
| Chinese | Be consistent within a pack; note script variant if required |

---

## 5. Domain vocabulary (authoring)

| Phrase | Meaning in BTE authoring |
|--------|---------------------------|
| Foundational Concept | Base academic concept; graph `Concept` |
| Entity | Catalog / named set |
| Rule | Formal conditional knowledge |
| Golden Record | Official-quality candidate meeting golden checklist |
| `TODO_REVIEW` | Explicit uncertainty marker |
| Useful God / Pattern / … | Use only when the owning module’s terminology is defined — do not invent pack-local jargon |

---

## 6. Assertion wording

Prefer:

> In classical BaZi usage, {{X}} denotes …

Avoid:

> Everyone knows {{X}} always means …

---

## 7. When terms conflict

1. Record `CONFLICTS_WITH` or conflict notes.
2. Keep both source IDs.
3. Do not silently normalize contested meanings into one assertion with `confidence=high`.
