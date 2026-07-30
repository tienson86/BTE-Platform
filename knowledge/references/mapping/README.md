# Reference Mapping Framework

**Module:** knowledge/references/mapping  
**Version:** V1.0.0  
**Status:** Official Framework  

---

## Purpose

Provide cross-reference registries linking Reference IDs to Knowledge assets, Rules, Sentences, aliases, and schools.

These files are documentation registries (JSON), not runtime code.

---

## Registries

| File | Purpose |
|------|---------|
| [reference_to_knowledge.json](reference_to_knowledge.json) | REF → Knowledge asset IDs |
| [reference_to_rule.json](reference_to_rule.json) | REF → Rule IDs |
| [reference_to_sentence.json](reference_to_sentence.json) | REF → Sentence IDs |
| [reference_alias.json](reference_alias.json) | Alternate titles / spellings |
| [reference_school.json](reference_school.json) | REF → school labels |

---

## Conflict Rule

If a Markdown reference document and a JSON registry disagree:

1. Prefer the Markdown document for human review.
2. Reconcile the JSON registry in the next patch release.

---

## Empty Links

Empty arrays are valid for framework seed records.
