# Knowledge Specification — Interpretation Layer (K1)

## KnowledgeEntity

Generic contract for one knowledge item.

| Field | Required | Description |
|---|---|---|
| id | yes | Stable identifier |
| domain | yes | Canonical domain name |
| key | yes | Lookup key within domain |
| title | yes | Human title |
| meaning | no | Core expert meaning |
| positive_meaning | no | Favorable expression |
| negative_meaning | no | Unfavorable expression |
| applications | no | Domain application notes |
| recommendations | no | Structured recommendation hints |
| warnings | no | Structured warning hints |
| related_entities | no | Cross-references `{domain, key}` |
| evidence_notes | no | Explainability notes |
| metadata | yes | author, version, status, etc. |

Partial entities are supported — only `id`, `domain`, `key`, `title`, `metadata` are required at load time.

## Canonical domains (K1 registry)

```text
UsefulGod
Strength
Pattern
Temperature
TenGods
ShenSha
Luck
FiveElements
FengShui
Calendar
ExecutiveSummary
Recommendations
```

## Metadata

```text
author
version
created
updated
status   → draft | review | approved | deprecated
source
quality
```

## Loader sources (future)

JSON (K1), YAML, Markdown, Generated, Database

K1 implements JSON only.

## Validation

- duplicate ids
- missing keys within domain
- broken related_entities references
- unknown domains
- invalid metadata / status enum
