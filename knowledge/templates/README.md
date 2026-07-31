# BTE Knowledge Record Template System

**Sprint:** 4A  
**Location:** `knowledge/templates/`  
**Status:** Documentation only (no runtime / no compiler code)

---

## Purpose

Reusable authoring templates for every Knowledge Record (KR). Authors copy a template, replace placeholders, and follow Governance, Compiler, and Validation requirements.

Golden Records continue to be authored manually; these templates do not modify `knowledge/bazi/**`.

---

## Folder tree

```text
knowledge/templates/
├── README.md
├── knowledge_record_template.md          # master KR shell
├── golden_record_template.md             # golden / official promotion track
├── foundational_concept_template.md      # Foundational Concept
├── entity_template.md                    # Entity
├── rule_template.md                      # Rule
├── example_template.md                   # Example
├── review_template.md                    # Academic / technical / governance review
└── release_template.md                   # Freeze + publication release note
```

---

## Which template to use

| Knowledge type | Start with |
|----------------|------------|
| Any KR (generic) | `knowledge_record_template.md` |
| Foundational Concept | `foundational_concept_template.md` |
| Entity | `entity_template.md` |
| Rule | `rule_template.md` |
| Example (EX-*) | `example_template.md` |
| Golden / official candidate | `golden_record_template.md` (+ type template) |
| Review package | `review_template.md` |
| Release / freeze package | `release_template.md` |

---

## Placeholder convention

All templates use double-brace placeholders:

```text
{{RECORD_ID}}
{{CANONICAL_NAME}}
{{TODO_REVIEW}}
```

Authors SHALL replace every `{{...}}` before submitting for review.  
Uncertain academic claims SHALL remain marked `TODO_REVIEW` — never invent classical attributions.

---

## Compliance map

| Concern | Follow |
|---------|--------|
| Governance lifecycle | `knowledge/governance/` (approval, freeze, release, retirement specs) |
| Compiler contracts | `knowledge/compiler/` + standards KR schema sections |
| Validation / quality | `knowledge/quality/` metrics and checklists |
| KR schema sections | `knowledge/standards/knowledge_record/` |
| Graph relations | `knowledge/graph/` edge types |
| Indexes | `knowledge/index/` registries (updated at publication) |

---

## Locked paths (Sprint 4A)

Do **not** modify:

- `knowledge/bazi/**`
- `knowledge/compiler/**`
- `knowledge/governance/**`
- `knowledge/bibliography/**`

---

## Out of scope

- Template engine / codegen
- Auto-filling academic content
- Compiling or publishing records
