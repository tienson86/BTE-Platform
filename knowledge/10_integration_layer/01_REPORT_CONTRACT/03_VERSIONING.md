# ReportResponse Versioning Policy

**Location**

```
knowledge/10_integration_layer/01_REPORT_CONTRACT/03_VERSIONING.md
```

---

# Purpose

This document defines the official versioning policy for the BTE ReportResponse contract.

Its purpose is to ensure long-term compatibility between:

- Applications API
- Customer Portal
- Report Engine
- Mobile Applications
- Third-party integrations
- Future SDKs

The ReportResponse contract is considered a public product interface and must evolve in a controlled manner.

---

# Status

Document Type

Architecture Governance

Status

Frozen after approval

Commercial Version

RC1

Owner

BTE Architecture

---

# Guiding Principles

The ReportResponse contract shall always be:

- Stable
- Backward Compatible
- Deterministic
- Extensible
- Traceable

Published contracts are never modified in-place.

---

# Version Format

ReportResponse follows Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

Example

```
1.0.0
1.1.0
1.2.0
2.0.0
```

---

# Major Version

A Major version indicates a breaking contract change.

Examples

- Removing a published field
- Renaming a field
- Changing field type
- Changing required → optional semantics
- Changing response hierarchy

Example

```
1.x.x

↓

2.0.0
```

Major versions require:

- Architecture Review
- Product Approval
- Migration Guide
- Portal Compatibility Review

---

# Minor Version

Minor versions introduce new capabilities without breaking compatibility.

Allowed

- Add optional field
- Add optional section
- Add new domain
- Add new diagnostics
- Add new metadata

Example

```
1.0.0

↓

1.1.0
```

No existing client should break.

---

# Patch Version

Patch versions fix implementation without changing the contract.

Allowed

- Documentation
- Validation improvements
- Bug fixes
- Internal Builder improvements

Not Allowed

- New fields
- Removed fields
- Contract changes

Example

```
1.0.0

↓

1.0.1
```

---

# Compatibility Rules

## Rule 1

Published fields must never disappear.

---

## Rule 2

Published field names never change.

---

## Rule 3

Published field types never change.

---

## Rule 4

New fields must be optional.

---

## Rule 5

Consumers must ignore unknown fields.

---

## Rule 6

Section ordering is not part of the contract.

---

## Rule 7

Builders may evolve internally without affecting consumers.

---

# Allowed Changes

Examples

```
✓ Add domains.business

✓ Add metadata.request_duration

✓ Add diagnostics.validation

✓ Add knowledge.references

✓ Add charts.radar
```

These are Minor changes.

---

# Forbidden Changes

Examples

```
✗ Remove executive_summary

✗ Rename identity

✗ Change recommendations list to object

✗ Remove chart

✗ Replace evidence structure
```

These require Major Version.

---

# Deprecation Policy

Deprecated fields remain available for at least one Major version.

Lifecycle

```
Current

↓

Deprecated

↓

Migration

↓

Removal (next Major)
```

Deprecation must include:

- reason
- replacement
- removal target
- migration guidance

---

# Extension Policy

Future functionality should extend existing sections whenever possible.

Preferred

```
domains

knowledge

charts

diagnostics
```

Avoid introducing unnecessary top-level sections.

---

# Consumer Responsibilities

Consumers shall:

- ignore unknown fields
- never depend on ordering
- validate schema version
- tolerate optional data

Consumers shall not:

- assume hidden fields
- access internal engine models
- reconstruct business logic

---

# Producer Responsibilities

Report Builder shall:

- publish valid ReportResponse
- preserve compatibility
- preserve traceability
- validate schema version

---

# Version Metadata

Every ReportResponse shall contain

```
metadata

├── report_version
├── contract_version
├── knowledge_version
├── capability_versions
├── generated_at
└── pipeline_version
```

---

# Capability Versioning

Each commercial capability maintains an independent version.

Example

```
Career Selection

1.0.0

Promotion Readiness

1.0.0

Leadership

0.1.0
```

Capabilities evolve independently.

The ReportResponse version changes only when the public contract changes.

---

# Knowledge Versioning

Knowledge Units evolve independently.

Example

```
KU-ID-001

1.0.0

↓

1.0.1
```

Knowledge revisions do not require ReportResponse version changes unless the contract changes.

---

# Builder Versioning

Section Builders may evolve internally.

Example

```
ExecutiveBuilder

2.4.1

RecommendationBuilder

1.9.0
```

Internal Builder versions are implementation details.

They do not affect the public contract.

---

# Migration Policy

Every Major version requires:

- Migration Guide
- Compatibility Matrix
- API Review
- Portal Validation
- Golden Dataset Validation

---

# Version Matrix

| Component | Versioned Independently |
|------------|-------------------------|
| ReportResponse Contract | YES |
| Analysis Engine | YES |
| Interpretation Engine | YES |
| Commercial Knowledge | YES |
| Knowledge Units | YES |
| Section Builders | YES |
| Customer Portal | YES |
| Mobile App | YES |

---

# Governance Rules

Changing the public contract requires:

✓ ADR approval

✓ Architecture approval

✓ Integration review

✓ Portal compatibility review

✓ Product approval

---

# Release Workflow

```
Proposal

↓

Architecture Review

↓

ADR Approval

↓

Implementation

↓

Golden Dataset

↓

Portal Validation

↓

Commercial QA

↓

Release
```

---

# Acceptance Checklist

The versioning policy is accepted when:

✓ Semantic Versioning is adopted

✓ Backward compatibility is enforced

✓ Deprecation policy is documented

✓ Migration policy exists

✓ Consumer responsibilities are defined

✓ Producer responsibilities are defined

✓ Version metadata is standardized

✓ Governance process is established

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| README.md | Integration Layer overview |
| 00_SYSTEM_FLOW.md | End-to-end pipeline |
| 00A_ARCHITECTURE_DECISIONS.md | Architecture decisions |
| 01_REPORT_RESPONSE_SPEC.md | Canonical contract |
| 01A_REPORT_SCHEMA_DIAGRAM.md | Structural overview |
| 02_FIELD_MAPPING.md | Data lineage |
| 03_VERSIONING.md | Contract evolution policy (this document) |

---

# Official Status

Document

Canonical Versioning Policy

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture