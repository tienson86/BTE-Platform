# BTE Canonical Expert Knowledge

| Field | Value |
|-------|-------|
| Series | Canonical Expert Knowledge |
| ID Namespace | `CANON-NNNN` |
| Version | 1.0.0 |
| Status | Official |
| Owner | BTE Knowledge Team |

---

## Purpose

This series is the permanent expert reference layer of BTE.

Each Canon defines **one concept once**.

Downstream domains, engines, narratives, and reports **reference** Canons.

They do **not** redefine them.

This series is not:

- a Knowledge Asset catalog (`knowledge/knowledge_canon/`)
- a Knowledge Record pack (`knowledge/bazi/01_fundamental_knowledge/records/`)
- a Rule Database
- an engine specification
- customer-facing copy

---

## Architecture

```text
Fundamental Records (KR-*)
        │
        ▼
Canonical Expert Knowledge (CANON-*)   ← this series
        │
        ▼
Domain Knowledge
(Strength / Useful God / Pattern / Ten Gods / Shen Sha / Luck / Temperature)
        │
        ▼
Rule Database
        │
        ▼
Engines
        │
        ▼
Narrative / Report
```

---

## Identifier Rule

| Object | Prefix | Example |
|--------|--------|---------|
| Expert Canon | `CANON` | `CANON-0001` |
| Knowledge Record | `KR` | `KR-000004` |
| Knowledge Asset | `KNO` | `KNO-000001` |

Namespaces do not overlap.

A Canon ID is immutable after publication.

---

## Published Canons

| Canon ID | Title | File | Status |
|----------|-------|------|--------|
| CANON-0001 | Day Master Canon | [CANON_0001_DAY_MASTER.md](CANON_0001_DAY_MASTER.md) | Official |

---

## Reserved Roadmap

The following Canons are reserved. They are not authored in this task.

| Canon ID | Title | Notes |
|----------|-------|-------|
| CANON-0002 | Strength Canon | Day Master standing |
| CANON-0003 | Useful God Canon | Chart-need relative to Day Master |
| CANON-0004 | Pattern Canon | Structure relative to Day Master |
| CANON-0005 | Ten Gods Canon | Relations derived from Day Master |
| CANON-0006 | Luck Canon | Time interaction with Day Master |
| CANON-0007 | Temperature Canon | Climate context around Day Master |
| CANON-0008 | Shen Sha Canon | Auxiliary stars; Day Master as one possible axis |
| CANON-0011–0020 | Stem Canons | Giáp, Ất, Bính, Đinh, Mậu, Kỷ, Canh, Tân, Nhâm, Quý |

Stem Canons define Heavenly Stem identities.

They do **not** redefine the Day Master role.

---

## Governance

- One concept, one Canon.
- Copying explanations into domain modules is prohibited.
- Engines consume domain knowledge; they do not author Canon definitions.
- Stem-specific nature belongs only in Stem Canons.
