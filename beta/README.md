# BTE Beta 0 — Product Stabilization Freeze

| Field | Value |
|-------|-------|
| Program | Beta 0 Product Stabilization Freeze |
| Date | 2026-08-17 |
| Status | **OFFICIAL FREEZE** |
| Platform | BTE V1.0 |
| Code changed | **NONE** |

This folder is the quality-governance surface for commercial beta.

It is not a development sprint.
It is not an architecture sprint.
It is not a feature sprint.

---

## What Beta 0 is

Beta 0 freezes the product so later work can improve the consultation, not redesign the platform.

Frozen:

- Architecture
- Analytical truth ownership
- Knowledge ownership
- Narrative pipeline
- Publishing pipeline
- Editorial Standard
- Golden Dataset
- Product workflow
- Release and regression workflow

After this point, no new subsystem may be added without Product Owner approval.

---

## Documents

| Document | Role |
|----------|------|
| [BETA0_PRODUCT_FREEZE.md](BETA0_PRODUCT_FREEZE.md) | Freeze declaration |
| [BETA0_ARCHITECTURE_LOCK.md](BETA0_ARCHITECTURE_LOCK.md) | Frozen architecture |
| [BETA0_ANALYTICAL_TRUTH_LOCK.md](BETA0_ANALYTICAL_TRUTH_LOCK.md) | Engine truth owners |
| [BETA0_KNOWLEDGE_LOCK.md](BETA0_KNOWLEDGE_LOCK.md) | Knowledge and canon owners |
| [BETA0_NARRATIVE_LOCK.md](BETA0_NARRATIVE_LOCK.md) | Frozen narrative pipeline |
| [BETA0_PUBLISHING_LOCK.md](BETA0_PUBLISHING_LOCK.md) | Frozen publication editions |
| [BETA0_EDITORIAL_LOCK.md](BETA0_EDITORIAL_LOCK.md) | Frozen editorial constitution |
| [BETA0_GOLDEN_DATASET.md](BETA0_GOLDEN_DATASET.md) | Frozen production cases |
| [BETA0_PRODUCT_REGRESSION.md](BETA0_PRODUCT_REGRESSION.md) | Artifact-first regression |
| [BETA0_RELEASE_WORKFLOW.md](BETA0_RELEASE_WORKFLOW.md) | Release states and change classes |
| [BETA0_RELEASE_CHECKLIST.md](BETA0_RELEASE_CHECKLIST.md) | Gate before every Beta release |
| [BETA0_SIGNOFF.md](BETA0_SIGNOFF.md) | Product Owner signoff |
| [BETA0_PRODUCT_STABILIZATION_FREEZE_REPORT.md](BETA0_PRODUCT_STABILIZATION_FREEZE_REPORT.md) | Freeze report |

Prior research and RC3 protocol remain in `knowledge/beta/`. They do not replace this freeze.

---

## Allowed during Beta

- Bug Fix
- Editorial Improvement
- Knowledge Improvement
- Engine Improvement (within frozen ownership)
- Product Improvement (consultation quality)

## Forbidden during Beta without Product Owner approval

- Architecture Change
- New Engine
- New Framework
- New Matrix
- New Publisher
- New Composer
- New Canon
- New Layer
- New Runtime component

---

## Definition of Done

```
Artifact
    ↓
Product Review
    ↓
Product Owner approval
    ↓
Done
```

A Completion Report is not sufficient.
Tests PASS is not sufficient.
No release without Product Owner signoff.
