# Platform Release Process

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_RELEASE_PROCESS |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | Release Manager |

Complements `knowledge/releases/process/` and `knowledge/governance/procedures/08_RELEASE_WORKFLOW.md`. AF-1 adds the Platform v1.0 architecture seal.

---

## Release types

| Type | When |
|------|------|
| Architecture freeze | AF-1 — this document set |
| Platform PATCH / MINOR / MAJOR | Per SemVer policy |
| Package release | KD-3 lifecycle to `released` |
| Hotfix | Defect only; no architecture change |

---

## v1.0 architecture freeze process (completed by AF-1)

1. Confirm Foundation 1.0.0 freeze remains intact.
2. Confirm canonical pipelines AX-2 / AX-3 / AX-4 / IX-1 / RX-1 are released.
3. Record component catalog, compatibility matrix, ADRs.
4. Record package and contract checksums.
5. Complete acceptance checklist.
6. Issue `RELEASE_CERTIFICATE.md`.

No runtime logic is introduced by this process.

---

## Subsequent platform release steps

1. Change request + SemVer class
2. Architecture / Knowledge / RM approvals (`PLATFORM_CHANGE_CONTROL.md`)
3. Quality gates (`PLATFORM_QUALITY_GATES.md`)
4. Module tests only for touched engines; full pytest only when RM requests
5. Update `knowledge/releases/<version>/` manifest and checksums
6. Update release notes; do not rewrite v1.0 identities

---

## Artifacts for a platform release

| Artifact | Purpose |
|----------|---------|
| `RELEASE_MANIFEST.json` | Engines, pipelines, packages, metadata |
| `COMPONENT_CHECKSUMS.json` | Sealed hashes |
| `PACKAGE_INDEX.json` | Package inventory |
| `PIPELINE_INDEX.json` | Pipeline inventory |
| `ENGINE_INDEX.json` | Engine inventory |
| `CONTRACT_INDEX.json` | Contract inventory |
| `VERSION_MATRIX.json` | Compatibility |
| `RELEASE_SUMMARY.md` | Human summary |
| `RELEASE_CERTIFICATE.md` | Official seal |

---

## Non-goals of AF-1

- Shipping a new API
- Rebuilding engines
- Re-sealing packages
- Commercial store publication (may follow under RM)
