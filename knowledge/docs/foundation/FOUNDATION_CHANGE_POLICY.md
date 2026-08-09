# Foundation Change Policy

| Field | Value |
|-------|-------|
| **Document** | FOUNDATION_CHANGE_POLICY |
| **Foundation version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

---

## 1. SemVer for Foundation

Foundation version is independent of individual package versions and engine internal versions.

```
MAJOR.MINOR.PATCH
```

Current: **1.0.0**

---

## 2. Patch (`1.0.x`)

Allowed:

- Clarifying freeze documentation without changing rules
- Correcting typos, broken links, catalog owner names
- Filling the release-date placeholder when RM seals

Not allowed:

- New stages, new contracts, new schema fields
- Any runtime or package change

Approval: Release Manager.

---

## 3. Minor (`1.x.0`)

Allowed only when **additive and backward compatible**:

- New optional documentation axes
- New *optional* catalog entries that do not alter existing stage order
- New compatibility notes that do not invalidate 1.0.0 consumers

Not allowed:

- Inserting a stage into a frozen canonical order
- Changing existing published field names or enums in a breaking way

Approval: Architecture Board + Release Manager.

A minor Foundation bump does **not** rewrite sealed Knowledge Packages.

---

## 4. Major (`x.0.0`)

Required for any breaking Foundation change, including:

- New Knowledge schema generation
- Reordering or removing canonical pipeline stages
- Changing checksum two-pass substitution rules
- Removing or renaming public orchestration types
- Changing Decision / Analysis result field contracts incompatibly

Approval: Architecture Board + Knowledge Board + Release Manager.

Major upgrades MUST ship:

- Migration notes
- Compatibility window (if any)
- Explicit “Foundation N is frozen; Foundation N+1 is additive successor or breaking successor”

---

## 5. Breaking change

A breaking change is any change that causes a previously valid Foundation 1.0.0 consumer, package, or pipeline run to fail or silently change meaning.

Examples:

- Renaming `final_useful_god`
- Requiring a new published input on a frozen stage
- Changing `package_type` enum membership in a way that rejects existing `decision` packages
- Altering AX-2 active stage order

Breaking changes are **major only**. They are never patches.

---

## 6. Deprecation

Deprecation rules:

1. Announce in Foundation release notes (next Foundation version).
2. Keep the old surface working for at least one minor line, unless a security exception is approved.
3. Mark `deprecated` in catalog; do not delete identifiers.
4. Provide a successor path (new package, new engine, or new contract field).
5. Removal happens only on a Foundation **major**.

Released package bytes are never deprecated in place. Publish a new package version; leave the old checksum sealed.

---

## 7. Migration

Migrations MUST document:

| Item | Required |
|------|----------|
| From / to Foundation versions | yes |
| Affected pipelines | yes |
| Affected package ids | yes |
| Dual-read / wrapper period | if any |
| Consumer action | yes |
| Rollback | yes |

Package-level SemVer migrations follow KD-3. Foundation migrations wrap those; they do not replace them.

---

## 8. Approval workflow

```
Proposal
  → Impact review (Architecture + Knowledge as applicable)
  → Compatibility review
  → SemVer classification (patch / minor / major)
  → Approval per FOUNDATION_GOVERNANCE.md
  → Documentation update under knowledge/docs/foundation/
  → Release Manager seal (version + date)
  → Consumers notified
```

No Foundation change is valid without an updated freeze-document set.

Runtime engines and packages are **not** edited “to match” a proposed Foundation change. The Foundation version changes first; implementations follow only if the upgrade authorizes them.

---

## 9. Forbidden change patterns

- Edit a sealed `PACKAGE.json` checksum to make a test pass
- “Small” pipeline order tweak without a major
- Dual-write of the same analytical output from two stages
- Recompute upstream analysis inside a Decision Package
- Bypass stage registry
