# BETA0 Release Workflow

| Field | Value |
|-------|-------|
| Document | BETA0_RELEASE_WORKFLOW |
| Date | 2026-08-17 |
| Status | **OFFICIAL** |
| Owner | Product Owner + Release Manager |

---

## 1. Release states

Every change and every build must be classified into one state:

```
Research
    ↓
Development
    ↓
Beta0 Freeze     ← official platform state as of 2026-08-17
    ↓
Beta
    ↓
Release Candidate
    ↓
Production
```

| State | Meaning |
|-------|---------|
| Research | Documents, probes, no product claim |
| Development | Implementation inside frozen ownership |
| Beta0 Freeze | Governance lock. Current official state. |
| Beta | Stabilization releases against frozen architecture |
| Release Candidate | Candidate for commercial production |
| Production | Shipped to paying customers |

No skip from Development to Production.
No Production without Product Owner signoff.

---

## 2. Change control

Any future modification must be classified **before work starts**:

| Class | Allowed during Beta | Notes |
|-------|---------------------|-------|
| Bug Fix | Yes | Defect inside frozen owner |
| Editorial Improvement | Yes | ES-V1 quality of customer prose |
| Knowledge Improvement | Yes | Records / coverage; not a new knowledge system |
| Engine Improvement | Yes | Correctness inside frozen engine; no new engine |
| Product Improvement | Yes | Consultation quality; no new subsystem |
| Architecture Change | **No** unless Product Owner explicitly approves | New Engine / Framework / Matrix / Publisher / Composer / Canon / Layer / Runtime |

If the class is unclear, it is Architecture Change until the Product Owner says otherwise.

---

## 3. Workflow for a Beta release

```
Classify change
    ↓
Implement inside frozen ownership
    ↓
Regenerate Golden Dataset artifacts
    ↓
Regenerate Executive PDFs
    ↓
Regenerate Professional PDFs
    ↓
Editorial review
    ↓
Commercial review
    ↓
Release checklist
    ↓
Product Owner signoff (BETA0_SIGNOFF.md)
    ↓
Release
```

A Completion Report after implementation does not skip PDF regeneration or signoff.

---

## 4. Relation to prior platform process

`knowledge/docs/platform/PLATFORM_RELEASE_PROCESS.md` remains the engineering release process.

This document is the **product** overlay for Beta 0:

- Artifact First
- no new subsystems without approval
- no release without signoff

Where they conflict on product readiness, this freeze wins.

---

## Official status

**Release workflow and versioning states are frozen for Beta 0.**
