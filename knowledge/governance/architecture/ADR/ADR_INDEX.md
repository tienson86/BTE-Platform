# Architecture Decision Record Index

| Field | Value |
|-------|-------|
| **Document** | ADR_INDEX |
| **Platform version** | 1.0.0 |
| **Sprint** | AF-1 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

ADRs record why the frozen architecture is shaped as it is. They do not change runtime code.

| ID | Title | Status |
|----|-------|--------|
| [ADR-0001](ADR-0001.md) | Layered architecture and one-engine responsibility | Accepted |
| [ADR-0002](ADR-0002.md) | Canonical pipelines as the only supported execution model | Accepted |
| [ADR-0003](ADR-0003.md) | Knowledge Package system and sealed checksums | Accepted |
| [ADR-0004](ADR-0004.md) | Knowledge / analysis / presentation separation | Accepted |
| [ADR-0005](ADR-0005.md) | Result objects, contracts, trace, audit, diagnostics | Accepted |

New architectural decisions after v1.0 MUST add `ADR-0006+` and a Platform SemVer bump. Do not rewrite accepted v1.0 ADRs in place except for typographical PATCH.
