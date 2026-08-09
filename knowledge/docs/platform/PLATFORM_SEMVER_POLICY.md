# Platform Semantic Versioning Policy

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_SEMVER_POLICY |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

This policy governs **BTE Platform** SemVer. It complements Foundation (`FOUNDATION_CHANGE_POLICY.md`), Knowledge (`knowledge/docs/standards/VERSIONING_POLICY.md`), and governance (`knowledge/governance/policies/01_VERSIONING_POLICY.md`). Higher freeze layers win conflicts for frozen identities.

```
MAJOR.MINOR.PATCH
```

Current: **1.0.0**

Platform, Foundation, engines, pipelines, packages, and schemas are versioned independently. Compatibility is declared, never assumed.

---

## PATCH (`1.0.x`)

Allowed:

- Clarifying freeze documentation without changing rules
- Typo / link / owner-name corrections
- Defect fixes that do not change public contracts, pipeline order, or checksums of sealed packages
- Filling a release-date placeholder when Release Manager seals

Not allowed:

- New stages, new public fields, new schema generations
- Mutation of sealed Knowledge Packages
- Public API rename or removal

Approval: Release Manager.

---

## MINOR (`1.x.0`)

Allowed only when **additive and backward compatible**:

- New optional catalog entries that do not alter existing canonical order
- New packages with new `package_id`
- New optional published outputs
- Enabling a previously registered inactive stage without renaming existing outputs
- New compatibility notes that do not invalidate 1.0.0 consumers

Not allowed:

- Inserting a stage into a frozen active order in a breaking way
- Renaming existing published fields or diagnostic code meanings
- Enabling AI rewrite or print/email/publisher without an explicit minor + ADR

Approval: Architecture Board + Release Manager. Knowledge Board when packages are involved.

---

## MAJOR (`x.0.0`)

Required for any breaking platform change, including:

- New Knowledge schema generation
- Reordering or removing canonical pipeline stages incompatibly
- Changing checksum substitution rules
- Removing or renaming public orchestration types or API fields
- Changing result field contracts incompatibly

Approval: Architecture Board + Knowledge Board + Release Manager.

Major upgrades MUST ship migration notes and MUST NOT reuse the prior MAJOR.MINOR.PATCH identity.

---

## Compatibility guarantees

Platform 1.0.0 guarantees:

1. Released package checksums remain valid.
2. Canonical pipeline IDs and active stage orders remain stable.
3. Published contract functions keep their names and required fields.
4. `run()` on canonical pipelines does not raise to API callers (diagnostics only).
5. Engines do not write the Rule / Knowledge database.
6. Independent RE-1 / RE-2 / RE-3, IE-1 / IE-2 / IE-3, LE-1 / LE-2 / LE-3, AX-1 remain importable for backward compatibility.

Consumers of 1.0.0 MUST continue to work against any 1.0.x patch.

Consumers of 1.0.0 MUST continue to work against 1.x.0 minors if they ignore unknown optional fields.

---

## Deprecation policy

1. A public identity MAY be marked deprecated only in a MINOR or MAJOR.
2. Deprecated identities remain callable for at least one MINOR line.
3. Removal requires MAJOR.
4. Deprecation MUST be recorded in release notes and, when architectural, an ADR.
5. Wrappers preserve renamed internals; public names are not deleted in a PATCH.

---

## Package SemVer

Packages follow KD-3:

- `package_id` immutable
- `package_version` SemVer
- `status=released` ⇒ checksum sealed
- New content = new version or new id

Platform PATCH MUST NOT change sealed package checksums.
