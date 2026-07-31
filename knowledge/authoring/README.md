# BTE Knowledge Authoring

**Sprint:** 4B  
**Location:** `knowledge/authoring/`  
**Status:** Specification only (no runtime code)

---

## Purpose

Guides for humans (and future tools) on how to write Knowledge Records: naming, definitions, assertions, examples, relationships, ontology, review, and common mistakes.

Authoring produces markdown/JSON content. Compilation, scoring engines, and CI gates are out of scope here.

---

## Folder tree

```text
knowledge/authoring/
├── README.md
├── AUTHORING_GUIDE.md
├── STYLE_GUIDE.md
├── NAMING_CONVENTIONS.md
├── TERMINOLOGY_GUIDE.md
├── REVIEW_GUIDE.md
├── ANTI_PATTERNS.md
├── CHECKLIST.md
└── examples/
    └── authoring_mini_example.md
```

---

## Document map

| Document | Describes |
|----------|-----------|
| [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md) | End-to-end how to write a KR |
| [STYLE_GUIDE.md](STYLE_GUIDE.md) | Voice, structure, placeholder, citation style |
| [NAMING_CONVENTIONS.md](NAMING_CONVENTIONS.md) | IDs, files, canonical keys, aliases |
| [TERMINOLOGY_GUIDE.md](TERMINOLOGY_GUIDE.md) | Canonical names vs aliases; glossary use |
| [REVIEW_GUIDE.md](REVIEW_GUIDE.md) | Review workflow for authors and reviewers |
| [ANTI_PATTERNS.md](ANTI_PATTERNS.md) | Common mistakes |
| [CHECKLIST.md](CHECKLIST.md) | Pre-submit authoring checklist |
| [examples/](examples/) | Mini illustrative fragment (not a real KR) |

---

## Related infrastructure

| Concern | Location |
|---------|----------|
| Templates | `knowledge/templates/` |
| KR schema | `knowledge/standards/knowledge_record/` |
| Graph ontology | `knowledge/graph/` |
| Indexes | `knowledge/index/` |
| Quality | `knowledge/quality/` |
| Governance lifecycle | `knowledge/governance/` |
| Bibliography | `knowledge/bibliography/` |

---

## Hard rules (summary)

1. Never invent classical claims — use `TODO_REVIEW` when uncertain.
2. Never reuse or remap `KR-*` IDs.
3. Use only approved relationship / edge types.
4. Do not modify locked modules unless a sprint explicitly authorizes it.
5. Examples are pedagogical — not golden test expected outputs.
