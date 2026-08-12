# DOMAIN_CLAIM_MODEL — DomainClaim

Every domain conclusion is normalized into `DomainClaim`.

## Required fields

claim_id, domain, claim_type, subject, value, scope, strength, dependencies, evidence_refs, confidence_state, customer_relevance, question_relevance, version

## Scopes (conflict only if overlapping)

| Scope | Example |
|-------|---------|
| BODY_STRENGTH | Strength level |
| STRUCTURAL_PATTERN | Pattern / Tòng |
| OPERATING_STYLE | Ten Gods primary |
| BALANCE_STRATEGY | Useful God |
| CAREER / RELATIONSHIP / GENERAL | reserved |

Two different values are **not** a conflict unless scopes actually conflict.

Normalizer: `cross_domain/claim_normalizer.normalize_claims`.
