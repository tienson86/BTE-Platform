# BTE Platform — Knowledge Governance

| Field | Value |
|-------|-------|
| **Governance version** | 1.0 |
| **Platform version** | 1.0.0 |
| **Last updated** | 2026-07-27 |

Official entry point for **knowledge asset governance** — rules, sentences, templates, and editorial content that drive BTE engines.

**Architecture V1.0 is frozen.** Knowledge evolution must not change production pipeline order, API contracts, or Portal JSON requirements without platform version policy.

---

## Quick links

| Document | Purpose |
|----------|---------|
| [KNOWLEDGE_ARCHITECTURE.md](KNOWLEDGE_ARCHITECTURE.md) | Hierarchy, SSOT tiers, dependencies, lifecycle |
| [KNOWLEDGE_VERSIONING.md](KNOWLEDGE_VERSIONING.md) | Patch / minor / major knowledge versions |
| [RULE_AUTHORING_STANDARD.md](RULE_AUTHORING_STANDARD.md) | How to write CSV rules — IDs, priority, conditions |
| [DATA_QUALITY_STANDARD.md](DATA_QUALITY_STANDARD.md) | Completeness, duplicates, conflicts, review checklist |
| [KNOWLEDGE_REVIEW_PROCESS.md](KNOWLEDGE_REVIEW_PROCESS.md) | Draft → release → retirement workflow |
| [KNOWLEDGE_CHANGELOG.md](KNOWLEDGE_CHANGELOG.md) | Official knowledge version history |

---

## Knowledge asset locations

| Tier | Path | Role |
|------|------|------|
| **Rule Database** | `database/` | Executable CSV rules — **production SSOT** |
| **Engine knowledge** | `engines/interpretation_engine/knowledge/` | Sentence library, report templates |
| **Editorial** | `knowledge_base/` | Style guides, feng shui gua JSON, validators |
| **Governance** | `knowledge/docs/` | This directory |

Engines read knowledge **read-only**. Business rules are not hard-coded in Python.

---

## Relationship to platform docs

| Topic | Document |
|-------|----------|
| Platform knowledge overview | [../../docs/project/KNOWLEDGE_BASE_GUIDE.md](../../docs/project/KNOWLEDGE_BASE_GUIDE.md) |
| Software versioning | [../../docs/project/VERSION_POLICY.md](../../docs/project/VERSION_POLICY.md) |
| Contributing / PRs | [../../docs/project/CONTRIBUTING.md](../../docs/project/CONTRIBUTING.md) |
| Development workflow | [../../docs/project/DEVELOPMENT_WORKFLOW.md](../../docs/project/DEVELOPMENT_WORKFLOW.md) |
| Architecture freeze | [../../docs/releases/architecture_v1_frozen.md](../../docs/releases/architecture_v1_frozen.md) |
| Production bugs (knowledge-related) | [../../docs/production_bug_tracker.md](../../docs/production_bug_tracker.md) |

---

## Current knowledge version

**1.0.0** — baseline with BTE Platform 1.0.0 Production Stable (2026-07-27).

See [KNOWLEDGE_CHANGELOG.md](KNOWLEDGE_CHANGELOG.md) for details.

---

## Who should read what

| Role | Start with |
|------|------------|
| **Rule author (domain)** | RULE_AUTHORING_STANDARD → DATA_QUALITY → REVIEW_PROCESS |
| **Engineer** | KNOWLEDGE_ARCHITECTURE → VERSIONING → REVIEW_PROCESS |
| **Knowledge lead** | All docs + KNOWLEDGE_CHANGELOG |
| **QA** | DATA_QUALITY (checklist) + smoke runner |
| **Product** | KNOWLEDGE_ARCHITECTURE + ROADMAP in `docs/project/PRODUCT_ROADMAP.md` |

---

## Quick workflow

1. Branch per `CONTRIBUTING.md`
2. Edit knowledge files per `RULE_AUTHORING_STANDARD.md`
3. Validate per `DATA_QUALITY_STANDARD.md`
4. PR → technical + domain review per `KNOWLEDGE_REVIEW_PROCESS.md`
5. Bump knowledge version per `KNOWLEDGE_VERSIONING.md`
6. Record in `KNOWLEDGE_CHANGELOG.md`
7. Run smoke if output changes: `py -3.13 validation/production_smoke_runner.py`

---

## Principles

1. **Database first** — rules live in CSV/approved JSON, not code `if/else`
2. **Single SSOT** — one authoritative file per rule family; no duplicates
3. **Priority not order** — resolution via priority columns, not file row order
4. **Commercial prose** — no internal rule IDs on customer wire
5. **Additive compatibility** — patch/minor default; major requires migration plan
6. **Domain review mandatory** — Bát tự correctness before production release

---

## Directory structure

```
knowledge/docs/
├── README.md                      ← this file
├── KNOWLEDGE_ARCHITECTURE.md
├── KNOWLEDGE_VERSIONING.md
├── RULE_AUTHORING_STANDARD.md
├── DATA_QUALITY_STANDARD.md
├── KNOWLEDGE_REVIEW_PROCESS.md
└── KNOWLEDGE_CHANGELOG.md
```

---

**BTE Knowledge Governance — Version 1.0 — Official Reference**
