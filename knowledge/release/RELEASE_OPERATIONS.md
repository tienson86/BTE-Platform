# Release Operations

| Field | Value |
|-------|-------|
| Document | RELEASE_OPERATIONS |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Release Manager |

---

## 1. Operational workflow

Every Beta-or-later issue follows this sequence. No step may be skipped by substituting a report.

```
Feature Complete
    ↓
Freeze
    ↓
Golden Dataset
    ↓
Regression
    ↓
Editorial Review
    ↓
Commercial Review
    ↓
Product Owner Approval
    ↓
Release
```

| Step | Meaning |
|------|---------|
| **Feature Complete** | Intended scope for this train is closed. During Beta, “feature complete” means **no new features**; only quality work already classified is in. |
| **Freeze** | No further scope enters this issue. V1 platform freeze is Beta0 and remains in force. |
| **Golden Dataset** | Frozen real cases regenerated. Placeholders and synthetic subjects are not used. |
| **Regression** | Golden PDFs, Executive PDFs, and Professional PDFs compared as product, not as edited snapshots. |
| **Editorial Review** | Editorial Standard V1 on the new artifacts. |
| **Commercial Review** | Consultation judged as a sellable (or Beta-reviewable) reading. |
| **Product Owner Approval** | Recorded on `RELEASE_SIGNOFF.md`. |
| **Release** | Version named, tagged, notes filed, artifacts stored in the stage folder. |

Development-phase work may exist before Feature Complete.
It is not an issued version.

---

## 2. Responsibilities

| Role | Responsibility |
|------|----------------|
| **Product Owner** | Opens or refuses a train. Signs or rejects the issue. Alone may authorise Architecture change or a move to RC / Production. |
| **Release Manager** | Runs this workflow. Owns checklist completeness, version name, artifact filing, changelog, tag after signoff. Does not override Product or Editorial FAIL. |
| **Engineering owner** | Produces a reproducible artifact from the frozen path. Engineering Gate. Does not declare customer-ready. |
| **Chief Editor** | Editorial Gate. ES-V1 admission. |
| **Commercial reviewer** | Commercial Gate. Consultant-grade value and bounded claims. |
| **QA** | Confirms checklist evidence exists: before/after PDFs, diff summary, Golden results. QA PASS is not Editorial PASS. |
| **Architecture Board** | Confirms no unauthorised subsystem entered the issue. |
| **Knowledge Board** | Confirms knowledge changes are records, not a new knowledge system. |

One person may hold two roles only if the signoff still shows each gate separately.
Product Owner may not be the sole Editorial reviewer of a Production issue.

---

## 3. Issue record

Each issued version files, under the matching stage folder:

- completed `RELEASE_CHECKLIST.md` copy or checklist section
- completed `RELEASE_SIGNOFF.md`
- changelog entry per `CHANGELOG_POLICY.md`
- artifact pack per `ARTIFACT_POLICY.md`

Unsigned drafts stay Internal.
They are not filed as Beta, RC, or Production.

---

## 4. Beta overlay

During Beta:

1. Classify work as Bug, Editorial, Knowledge, Engine-within-owner, or Product quality.
2. Refuse feature and Architecture work unless pre-approved.
3. Run the workflow above.
4. File under `beta1/`, `beta2/`, or later Beta folders. Beta0 holds freeze records, not quality-train issues, unless a freeze errata is signed.

---

## 5. Relation to older process

`knowledge/releases/process/01_RELEASE_WORKFLOW.md` remains a historical commercial-version workflow.
From 2026-08-17, **this document** is the operational workflow for cutting a version.
Product policy in `knowledge/product/PRODUCT_RELEASE_POLICY.md` remains the permission model.
