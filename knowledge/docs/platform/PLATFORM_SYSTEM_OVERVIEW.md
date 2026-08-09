# Platform System Overview

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_SYSTEM_OVERVIEW |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

---

## Purpose

BTE Platform is a commercial BaZi analysis system. It separates knowledge, calculation, decision, interpretation, and presentation so each layer stays testable and replaceable without rewriting the others.

---

## Layers

```
Knowledge Database V2 + Knowledge Packages
        ↓
Rule Engine (evaluate records)
        ↓
Business Layer
  Calendar → Bazi → Score / Pattern
  Analysis Pipeline → Decision Pipeline → Luck Pipeline
        ↓
Interpretation Layer (select + assemble; no AI rewrite)
        ↓
Presentation / Report Layer (structure → layout → render)
        ↓
API / Portal (consume official results only)
```

### Knowledge

Canonical envelope schema 2.0.0. Rules, evidence, reasoning, and references live in independently versioned packages. Engines read; they never write the database.

### Rule Engine

Matches and evaluates rule records. It does not decide pipeline order and does not hard-code analytical trees that belong in packages.

### Business Layer

Calendar and Bazi produce chart facts. Analysis publishes analytical signals. Decision publishes Useful God outcomes. Luck publishes timeline impact and opportunity/risk. Each engine has one responsibility.

### Presentation Layer

Interpretation assembles consultant-facing structure from frozen upstream snapshots. Report Foundation defines document slots only.

### Rendering Layer

Layout assigns theme and block identities. Rendering produces in-memory mime envelopes (PDF/DOCX/HTML/Markdown/JSON). Export does not write the filesystem in v1.0. Publisher, email, and print are disabled.

---

## Execution flow (canonical)

```
User Request
  → Calendar / Bazi
  → Canonical Analysis Pipeline
  → Canonical Decision Pipeline
  → Canonical Luck Pipeline
  → Canonical Interpretation Pipeline
  → Canonical Report Pipeline
  → Canonical Report Artifact
  → API / Portal
```

New work MUST use these pipelines. Released components remain independently importable for backward compatibility only.

---

## Cross-cutting mechanisms

| Mechanism | Role |
|-----------|------|
| Contracts | Versioned published I/O |
| Registries | Stage / module / renderer catalogs |
| Contexts | Append-only, immutable upstream |
| Trace | Machine-readable execution history |
| Audit | Legality and determinism flags |
| Diagnostics | Structured codes; no leaked exceptions |

---

## Dependency direction

```
Calendar → Bazi → Analysis → Decision → Luck → Interpretation → Report → API
```

No reverse imports. Details: `PLATFORM_DEPENDENCY_GRAPH.md`.

---

## Foundation relationship

Foundation v1.0.0 remains frozen. Platform v1.0.0 extends it with Luck, Interpretation, and Report canonical lines without rewriting Foundation documents.
