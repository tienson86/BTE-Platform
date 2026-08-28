# 08 — Commercial Knowledge Final Freeze

| Field | Value |
|-------|--------|
| Document | CK-01E Commercial Knowledge Final Freeze |
| Version | 1.0.0 |
| Status | **FINAL FROZEN** |
| Contract id | `bte.commercial.knowledge.v1` |

---

## Purpose

Freeze the approved CK-01 commercial knowledge contract.

This sprint does not add features. It does not render HTML, PDF, or DOCX. It does not start CK-02.

---

## Frozen runtime

```
Orchestrator
        ↓
match_published_knowledge
        ↓
compose_commercial_consulting
        ↓
CommercialComposerResult
        ↓
ReportInputV1.commercial_consulting
        ↓
API data.commercial_consulting
```

---

## Two composer paths (do not merge)

| Path | Owner | Input | Output |
|------|-------|-------|--------|
| `compose_commercial_consulting` | CK-01 | Matched knowledge units | `CommercialComposerResult` |
| `compose_commercial_narrative` | INT-03 | Integrated Narrative | `CommercialNarrativeUnit` |

These remain separate.

---

## Frozen facts

- Catalog id: `bte.consulting.knowledge.catalog.v1`
- 22 units, 10 domains, stable `unit_id`
- Composer does not call matcher
- Grouping uses `CONSULTING_DOMAINS`
- Unmatched domains omitted
- Every section has `source_unit_ids`
- Zero matches → `insufficient`, empty sections
- Report field optional and backward compatible
- Rendering HTML / PDF / DOCX / UI: **off**
- No LLM

---

## Allowed after freeze

- Bugfix that does not change the contract
- Additive consumers that read `commercial_consulting` without changing engines

## Forbidden after freeze

- Catalog content edits
- New domains without a major version
- Merging the two composer paths
- Matching inside Composer
- Invented advice
- HTML / PDF / DOCX / Portal rendering of commercial consulting without a new epic
- Astrology engine changes to “support” this freeze

---

END
