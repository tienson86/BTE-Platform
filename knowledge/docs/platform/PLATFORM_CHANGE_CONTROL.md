# Platform Change Control

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_CHANGE_CONTROL |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

---

## Principle

After AF-1, architecture is frozen. Change is exceptional, reviewed, versioned, and additive whenever possible.

---

## Required approvals

| Change class | Architecture Review | Knowledge Review | Release Manager | SemVer |
|--------------|---------------------|------------------|-----------------|--------|
| Freeze documentation clarification | No (unless rules change) | No | Yes | PATCH if published |
| Engine defect, no contract change | Yes if boundary risk | No | Yes | PATCH |
| New Knowledge Package | Yes | Yes | Yes | Package SemVer; Platform MINOR if catalogued |
| New pipeline stage / enable reserved stage | Yes | If packages | Yes | MINOR or MAJOR |
| Contract / schema / API break | Yes | Yes | Yes | MAJOR |
| Sealed package content | Forbidden in-place | — | — | New version only |

---

## Review sequence

```
Proposal
  → Architecture Review
  → Knowledge Review (when applicable)
  → Contract / compatibility check
  → Module tests (no golden/snapshot edits to force green)
  → Release Manager approval
  → SemVer bump + release notes
```

---

## Forbidden without this process

- Editing Foundation freeze documents to make implementation easier
- Mutating sealed `PACKAGE.json` checksums or Golden Dataset expected outputs
- Importing downstream engines
- Bypassing canonical pipelines for new Analysis / Decision / Luck / Interpretation / Report work
- Enabling publisher, email delivery, print, or AI rewrite informally

---

## Roles

| Role | Duty |
|------|------|
| Architecture Board | Freeze integrity, ADR, dependency direction |
| Knowledge Board | Packages, schema, taxonomy, authoring gates |
| Engine owner | Module correctness within one-engine responsibility |
| Release Manager | Seal, version, certificate, publication |

---

## Records

Every approved architectural change MUST update, as applicable:

- ADR index
- Component catalog
- Compatibility / version matrix
- Release notes
- Checksums (new versions only)
