# Domain Interpretation Contract

## DomainInterpretationResult

| Field | Customer | Validation |
|-------|----------|------------|
| domain | Yes | Yes |
| status | Yes | Yes |
| conclusion | Yes | Yes |
| sections | Yes (body only) | Yes |
| recommendations | Yes | Yes |
| executive_claims | Yes | Yes |
| missing_data | Yes | Yes |
| version | Yes | Yes |
| diagnostics | **No** | Yes |
| claims / theme_ids | **No** | Yes |
| knowledge_status | **No** | Yes |

## Status Values

`AVAILABLE` | `PARTIAL` | `NOT_AVAILABLE` | `INSUFFICIENT`

## KnowledgeStatus (diagnostics only)

`FROZEN` | `DRAFT_KNOWLEDGE` | `PILOT` | `MISSING`

## Hidden from Customer

rule IDs, scores, weights, reason codes, claim traces, evidence internals, DRAFT_KNOWLEDGE labels
