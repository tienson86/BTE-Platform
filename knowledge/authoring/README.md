# BTE Knowledge Authoring

**Location:** `knowledge/authoring/`  
**Status:** Specification only (no runtime code)

This folder contains two additive layers:

| Layer | Origin | Focus |
|-------|--------|--------|
| Knowledge Record authoring | Sprint 4B | How to write KR markdown/JSON records |
| Package Authoring & Validation Pipeline | Sprint KD-4 | How Knowledge Packages are drafted, validated, reviewed, approved, and released |

KD-4 does not replace Sprint 4B guides. Future knowledge contributions MUST pass the KD-4 pipeline before joining the official Knowledge Database.

---

## Purpose

- Guide humans and future tools (including AI-assisted authoring) through package creation.
- Define deterministic validation and release gates.
- Preserve academic honesty: never invent classical claims.

Authoring produces package files. Engines, APIs, and CI executors are out of scope.

---

## Folder tree

```text
knowledge/authoring/
├── README.md
├── AUTHORING_GUIDE.md
├── authoring_pipeline.md
├── STYLE_GUIDE.md                    # Sprint 4B — keep
├── NAMING_CONVENTIONS.md             # Sprint 4B — keep
├── TERMINOLOGY_GUIDE.md              # Sprint 4B — keep
├── REVIEW_GUIDE.md                   # Sprint 4B — keep
├── ANTI_PATTERNS.md                  # Sprint 4B — keep
├── CHECKLIST.md                      # Sprint 4B KR checklist — keep
├── package_template/                 # KD-4 copyable package skeleton
├── checklists/
│   ├── draft_checklist.md
│   ├── review_checklist.md
│   └── release_checklist.md
├── templates/
│   ├── RULE_TEMPLATE.json
│   ├── PACKAGE_TEMPLATE.json
│   ├── MANIFEST_TEMPLATE.json
│   └── METADATA_TEMPLATE.json
├── workflow/
│   ├── states.json
│   ├── transitions.json
│   └── approvals.json
├── validation/
│   ├── VALIDATION_PIPELINE.md
│   ├── validation_profiles.json
│   └── validation_sequence.json
├── quality/
│   ├── quality_rules.json
│   ├── quality_metrics.json
│   └── quality_levels.json
├── release/
│   ├── RELEASE_PIPELINE.md
│   ├── release_stages.json
│   └── release_requirements.json
└── examples/
    ├── authoring_mini_example.md     # Sprint 4B — keep
    ├── sample_authoring_flow.md
    └── sample_release_flow.md
```

---

## Document map

| Document | Describes |
|----------|-----------|
| [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md) | Philosophy + package and KR authoring |
| [authoring_pipeline.md](authoring_pipeline.md) | End-to-end workflow and governance model |
| [package_template/](package_template/) | Copyable KD-3 package skeleton |
| [checklists/](checklists/) | Draft / review / release gates |
| [templates/](templates/) | Rule, package, manifest, metadata JSON templates |
| [workflow/](workflow/) | States, transitions, approvals |
| [validation/](validation/) | Validation sequence (spec only) |
| [quality/](quality/) | Quality rules, metrics, Bronze–Platinum levels |
| [release/](release/) | Release stages and requirements |
| [STYLE_GUIDE.md](STYLE_GUIDE.md) | Voice and citation style (KR) |
| [NAMING_CONVENTIONS.md](NAMING_CONVENTIONS.md) | KR naming |
| [REVIEW_GUIDE.md](REVIEW_GUIDE.md) | KR review workflow |
| [CHECKLIST.md](CHECKLIST.md) | KR pre-submit checklist |

Architecture summary: `knowledge/docs/architecture/KNOWLEDGE_AUTHORING_VALIDATION_PIPELINE.md`

---

## Related infrastructure

| Concern | Location |
|---------|----------|
| Package spec (KD-3) | `knowledge/package_spec/` |
| Taxonomy / ontology (KD-2) | `knowledge/taxonomy/`, `knowledge/ontology/` |
| Knowledge Database V2 (KD-1) | `knowledge/schema/v2/`, `knowledge/docs/architecture/KNOWLEDGE_DATABASE_V2.md` |
| KR templates | `knowledge/templates/` |
| Governance | `knowledge/governance/` |
| V2 validation specs | `knowledge/validation/v2/` |

---

## Hard rules (summary)

1. Never invent classical claims — use `TODO_REVIEW` when uncertain.
2. Never reuse or remap published identifiers (`KR-*`, rule ids, `package_id`).
3. Do not modify existing Rule Database or released packages in place.
4. Do not modify engines, API, or contracts from this folder.
5. Examples and templates are pedagogical — not Golden Dataset expected outputs.
6. Released packages are immutable.
7. Parallel authoring is allowed; official publication is gated and deterministic.
