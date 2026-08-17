# Release Operations Foundation

| Field | Value |
|-------|-------|
| Document | Release Operations README |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Release Manager + Product Owner |
| Scope | How BTE is released, versioned, validated, approved, rolled back, and maintained. |

This folder is the permanent **Release Operations Foundation** of BTE.

It is not a software feature.
It is not architecture.
It is not an engine specification.

It defines the operating rules for issuing a version.

---

## 1. Purpose

Release Operations answers:

- Which state is this version in?
- What evidence is required to leave that state?
- Who may approve?
- What artifacts must exist?
- How is a bad issue withdrawn?
- How is an emergency repair issued?

A passing test suite does not answer these questions.
A completion report does not answer these questions.

---

## 2. Relationship with other folders

| Folder | Question it answers | Relation to this pack |
|--------|---------------------|------------------------|
| `knowledge/product/` | What the product is, when work is Done, what may be sold | **Governs** this pack. Release may not weaken Product Definition of Done, Acceptance, or Release Policy. |
| `knowledge/editorial/` | May this sentence reach a paying customer? | Editorial Gate in this pack uses Editorial Standard V1. Operations does not rewrite prose rules. |
| `knowledge/architecture/` | How the platform is structured and who owns truth | Architecture freeze constrains what a release may contain. Operations does not add subsystems. |
| `beta/` | V1 Beta 0 platform freeze | Current V1 lock. Beta issues in this pack must obey it. |
| `knowledge/releases/` | Historical commercial V1 process records and RC packages | Archive and prior process. Where they conflict with this pack after 2026-08-17, **this pack wins**. |

```
Product Governance          knowledge/product/
        ↓
Release Operations          knowledge/release/     ← this pack
        ↓
Beta 0 freeze               beta/
        ↓
Architecture                knowledge/architecture/
Editorial                   knowledge/editorial/
        ↓
Issued version + artifacts
```

---

## 3. Governance, Operations, Deployment, Support

| Discipline | Meaning | This pack |
|------------|---------|-----------|
| **Governance** | What is allowed, who decides, what Done means | Owned by `knowledge/product/`. This pack obeys it. |
| **Operations** | How a version is cut, evidenced, signed, stored, and withdrawn | **This pack.** |
| **Deployment** | How a signed version is placed into an environment | Out of scope here. Deployment may not precede signoff. |
| **Support** | How a live customer incident is handled after Production | Hotfix and Rollback in this pack. Day-to-day support playbooks are not this pack. |

Governance without operations produces policy that never issues.
Operations without governance issues whatever engineering finished.
Deployment without operations puts unsigned builds in front of people.
Support without rollback leaves a bad consultation live.

---

## 4. Documents

| Document | Purpose |
|----------|---------|
| [RELEASE_STRATEGY.md](RELEASE_STRATEGY.md) | Release philosophy and phase intent |
| [VERSIONING_POLICY.md](VERSIONING_POLICY.md) | Version names and bump rules |
| [RELEASE_OPERATIONS.md](RELEASE_OPERATIONS.md) | Operational workflow and responsibilities |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Mandatory pre-issue checklist |
| [QUALITY_GATES.md](QUALITY_GATES.md) | Engineering, Editorial, Commercial, Product, Customer Pilot |
| [ARTIFACT_POLICY.md](ARTIFACT_POLICY.md) | Artifact First evidence pack |
| [CHANGELOG_POLICY.md](CHANGELOG_POLICY.md) | Changelog categories and format |
| [ROLLBACK_POLICY.md](ROLLBACK_POLICY.md) | When and how to withdraw a version |
| [HOTFIX_POLICY.md](HOTFIX_POLICY.md) | Emergency patch and hotfix |
| [RELEASE_CALENDAR.md](RELEASE_CALENDAR.md) | Cadence, not dates |
| [RELEASE_SIGNOFF.md](RELEASE_SIGNOFF.md) | Signoff template |

Stage record folders:

| Folder | Stage |
|--------|-------|
| [beta0/](beta0/README.md) | Beta 0 freeze records |
| [beta1/](beta1/README.md) | First quality Beta train |
| [beta2/](beta2/README.md) | Second quality Beta train |
| [rc/](rc/README.md) | Release Candidates |
| [production/](production/README.md) | Production issues |
| [archive/](archive/README.md) | Superseded issue records |

---

## 5. Standing rules

- No feature development during Beta. Quality improvement only.
- Tests alone are insufficient.
- No issue without Product Owner signoff for Beta and later.
- No Architecture change inside a Beta, RC, Production, Emergency Patch, or Hotfix unless Product Owner approved it before work started.
