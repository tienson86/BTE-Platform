# BTE Bibliography Infrastructure

**Module:** `knowledge/bibliography`  
**Version:** `1.0.0`  
**Status:** Draft (Infrastructure Ready)  
**Schema:** `bibliography.schema.json`  
**Role:** Reusable Academic Source registry for Compiler, Validation, Graph, and Docs  

---

## Purpose

This module provides the **bibliography infrastructure** for the BTE Knowledge Canon.

It is the machine-readable registry of Academic Sources identified by:

```text
SRC-NNNNNN
```

The module stores bibliographic identity, priority hierarchy, citation policy, and conflict decisions.

It does **not** author BaZi academic knowledge and is independent of any single Knowledge Record.

---

## Scope

### In scope

- Master bibliography registry (`bibliography.json`)
- JSON Schema for registry validation
- Source priority hierarchy
- Citation policy configuration
- Academic conflict registry
- Integration-oriented examples

### Out of scope

- Academic definitions or interpretations
- Knowledge Record JSON generation
- Runtime Compiler / Validation Engine code
- Modification of Foundation `REF-*` library contents in this module

---

## Relationship to Foundation References (`REF-*`)

| Namespace | Module | Purpose |
|-----------|--------|---------|
| `SRC-*` | `knowledge/bibliography` | Academic Source bibliography for Canon citations |
| `REF-*` | `knowledge/references` | Foundation Reference Library (frozen infrastructure) |

Crosswalk entries MAY appear under each source’s `references[]` array (`ref_type: foundation_reference`).

Crosswalks remain **candidates** until Academic Review verifies them. Numeric suffixes are independent across namespaces.

---

## Directory structure

```
knowledge/bibliography/
├── README.md
├── bibliography.json
├── bibliography.schema.json
├── source_priority.json
├── citation_rules.json
├── conflict_registry.json
└── examples/
    ├── bibliography.sample.json
    ├── citation.sample.json
    └── conflict.sample.json
```

---

## File descriptions

### `bibliography.json`

Master registry of Academic Sources.

Top-level fields:

- `metadata` — registry identity and consumer compatibility
- `version` — semantic version of the registry dataset
- `created_at` / `updated_at`
- `sources[]` — source records (`SRC-*`)

Each source includes identity titles, bibliographic slots, category, priority, confidence, status, tags, nested `metadata`, and optional cross-references.

Uncertain scholarly fields use `TODO_REVIEW`. Registry stubs may use `status: placeholder`.

### `bibliography.schema.json`

Draft 2020-12 JSON Schema for `bibliography.json`.

Validates:

- required fields
- `source_id` pattern `^SRC-[0-9]{6}$`
- enums for category / priority / confidence / status
- `additionalProperties: false` on core objects
- version pattern compatibility (`MAJOR.MINOR.PATCH`)

### `source_priority.json`

Central hierarchy:

| Level | Role |
|-------|------|
| Level1 | Classical Canonical Sources |
| Level2 | Classical Commentaries / Classical References |
| Level3 | Modern Academic Publications |
| Level4 | Internal BTE Standards |

Each level lists `description`, numeric `priority`, `allowed_categories`, and `source_ids`.

Extend by appending approved `source_ids` without redesigning the document shape.

### `citation_rules.json`

Configurable citation policy consumed by Compiler and Validation Engine:

- minimum sources
- primary / secondary source rules
- multi-cite limits
- confidence thresholds
- citation style templates
- fallback / translation / cross-reference / review / validation policies

### `conflict_registry.json`

Stores academic conflicts between sources:

- competing sources
- selected source
- decision + justification
- reviewer / approver / history

v1.0.0 includes one **example** conflict (`CFL-000001`) for integration demos only.

### `examples/`

Non-normative samples demonstrating:

- bibliography expansion
- citation blocks on records
- conflict lookup behavior

---

## How the Compiler uses this module

```text
Knowledge Record design / draft
        ↓
academic_sources: [SRC-…]
        ↓
Load bibliography.json
        ↓
Resolve metadata + priority (source_priority.json)
        ↓
Apply citation_rules.json
        ↓
Check conflict_registry.json
        ↓
Expand citations for Documentation Generator
        ↓
Emit validation flags for Validation Engine
```

Compiler responsibilities:

1. Reject unknown `SRC-*`
2. Expand human-readable citations from registry fields
3. Enforce minimum/primary source rules by record status
4. Block Official promotion when sources are `placeholder` if policy requires
5. Surface unresolved conflicts

---

## Validation workflow

1. **Schema validation** — `bibliography.json` against `bibliography.schema.json`
2. **Integrity** — unique `source_id`; priority membership consistent with category
3. **Citation validation** — record citations resolve to registry
4. **Policy validation** — `citation_rules.json` thresholds
5. **Conflict validation** — Official overrides require registry decision

Consumers: Knowledge Compiler, Validation Engine, Knowledge Graph (source nodes/edges), Documentation Generator, Future API.

---

## Governance

Changes to bibliography infrastructure require:

```text
Academic Proposal
  → Academic Review
  → Knowledge Canon Committee Approval
  → Version bump
  → Publication
```

Rules:

- Knowledge Records MUST NOT invent unofficial bibliographic entries
- New `SRC-*` IDs are allocated centrally (sequential)
- Priority changes require committee approval
- Conflicts that override hierarchy require conflict registry entries

---

## Versioning

| Asset | Version field | Current |
|-------|---------------|---------|
| Module / dataset | `bibliography.json` → `version` | `1.0.0` |
| Schema | `metadata.schema_version` / schema `$id` | `1.0.0` |
| Priority / rules / conflicts | top-level `version` | `1.0.0` |

Semantic versioning:

- **MAJOR** — breaking shape / ID semantics
- **MINOR** — additive sources or compatible policy keys
- **PATCH** — editorial / metadata corrections

---

## Future expansion

- Official bibliographic completion (replace `TODO_REVIEW`)
- Level3 modern academic registrations
- Automated SRC↔REF crosswalk verification
- Graph export of source dependency edges
- API endpoints for source lookup and conflict query
- Locale packs for Vietnamese titles after Academic Approval

---

## Quality constraints (v1.0.0)

- Valid JSON only (no inline comments)
- Schema-first
- Extensible level/policy documents
- Compiler-friendly identifiers (`SRC-NNNNNN`)
- Placeholder stubs clearly marked — not academic claims

---

## Stop line

Infrastructure ready for integration. Academic metadata completion and Official status promotion remain Academic Review tasks.
