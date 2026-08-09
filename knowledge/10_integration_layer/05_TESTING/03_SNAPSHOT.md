# Snapshot Framework

**Location**

```
knowledge/10_integration_layer/05_TESTING/03_SNAPSHOT.md
```

---

# Purpose

This document defines the canonical Snapshot Framework of the BTE Platform.

Snapshots preserve approved customer-facing outputs and detect unintended changes across releases.

A Snapshot represents the expected commercial experience for a specific Golden Dataset case.

Snapshots are Product assets.

---

# Status

Document Type

Testing Architecture

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE QA + Product

---

# Snapshot Philosophy

Snapshots validate the customer experience.

They do not validate engine algorithms.

They ensure the same input produces an approved customer-facing result.

Snapshots protect

- Report structure
- Commercial wording
- Reading experience
- Capability presentation
- Portal rendering
- Report consistency

---

# Position in QA Pipeline

```
Golden Dataset

↓

ReportResponse

↓

Snapshot Comparison

↓

PASS / REVIEW / FAIL

↓

Commercial QA
```

Snapshot validation occurs after contract validation.

---

# Snapshot Scope

Snapshots cover only public outputs.

Included

```
ReportResponse

Portal ViewModel

Rendered Sections

Executive Summary

Recommendations

Capability Outputs
```

Excluded

```
AnalyzeContext

BuilderContext

Diagnostics

Timing

Internal Metadata

Logs

Debug Information
```

---

# Snapshot Levels

The framework defines four snapshot levels.

```
Level 1

Contract Snapshot

↓

Level 2

Narrative Snapshot

↓

Level 3

Capability Snapshot

↓

Level 4

Portal Snapshot
```

---

# Level 1 — Contract Snapshot

Purpose

Verify ReportResponse structure.

Checks

- Section presence
- Ordering
- Required fields
- Schema compatibility

---

# Level 2 — Narrative Snapshot

Purpose

Verify customer-facing language.

Checks

- Executive Summary
- Recommendations
- Identity
- Commercial wording

Minor wording changes require Product approval.

---

# Level 3 — Capability Snapshot

Purpose

Verify capability output.

Examples

```
Career Selection

Promotion Readiness

Leadership

Finance

Marriage
```

Checks

- Activation
- Ordering
- Visibility
- Presentation

---

# Level 4 — Portal Snapshot

Purpose

Verify rendered customer experience.

Checks

- Reading order
- Visible cards
- Empty-state behavior
- Component hierarchy
- CTA placement

---

# Snapshot Structure

```
snapshot/

├── contract/

├── narrative/

├── capability/

├── portal/

└── metadata/
```

---

# Snapshot Metadata

Every snapshot records

```
Snapshot ID

Golden Case ID

Commercial Version

Knowledge Version

Capability Versions

Created Date

Approved By

Approval Date
```

---

# Snapshot Lifecycle

```
Create

↓

Review

↓

Approve

↓

Freeze

↓

Release

↓

Archive
```

Only approved snapshots may be frozen.

---

# Snapshot Comparison

Execution

```
Golden Case

↓

Generate ReportResponse

↓

Normalize

↓

Compare Snapshot

↓

PASS

REVIEW

FAIL
```

---

# Comparison Rules

Ignore

- timestamps
- request IDs
- execution time
- diagnostics
- internal identifiers

Compare

- customer-facing content
- section ordering
- capability visibility
- commercial wording
- layout structure

---

# Snapshot Status

## PASS

No meaningful differences.

Release continues.

---

## REVIEW

Expected changes detected.

Requires Product review.

May update baseline.

---

## FAIL

Unexpected differences detected.

Release blocked.

---

# Allowed Changes

Require Product approval

- Better commercial wording
- New capability
- Approved layout improvement
- Updated recommendation format

---

# Forbidden Changes

Never allowed automatically

- Missing Executive Summary
- Missing Identity
- Missing Recommendation
- Broken reading order
- Capability disappearance
- Invalid ReportResponse

---

# Snapshot Ownership

| Artifact | Owner |
|----------|-------|
| Contract Snapshot | Engineering |
| Narrative Snapshot | Product |
| Capability Snapshot | Product |
| Portal Snapshot | UX |
| Snapshot Approval | Product + Consulting |

---

# Baseline Policy

Every Commercial Release freezes

```
Snapshot Baseline
```

Example

```
Commercial V1

↓

Snapshot Baseline V1
```

Future releases compare against the previous baseline.

---

# Regression Policy

Unexpected snapshot differences are regressions.

Every regression must be

- Fixed
- Approved
- Deferred with documented justification

No silent changes are allowed.

---

# Snapshot Reports

Each execution generates

- Cases Compared
- Pass Count
- Review Count
- Failure Count
- Changed Sections
- Changed Capabilities

Reports become part of the Release Package.

---

# Future Extensions

Future versions may add

- Visual screenshot snapshots
- PDF snapshots
- Multi-language snapshots
- Mobile snapshots
- Accessibility snapshots

Current architecture remains unchanged.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_TEST_STRATEGY.md | Overall testing strategy |
| 02_GOLDEN_DATASET.md | Golden Dataset |
| 03_SNAPSHOT.md | Snapshot framework (this document) |
| 04_CONTRACT_TESTS.md | Contract validation |
| 09_RELEASE_VALIDATION.md | Release quality gates |

---

# Acceptance Criteria

The Snapshot Framework is accepted when

✓ Every Golden Case has an approved snapshot

✓ Snapshot comparison is automated

✓ Only customer-facing content is compared

✓ Internal runtime data is ignored

✓ Snapshot baselines are versioned

✓ Unexpected changes block release

✓ Approved changes create a new baseline

✓ Snapshot reports are included in every Release Candidate

---

# Official Status

Document

Snapshot Framework

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE QA + Product