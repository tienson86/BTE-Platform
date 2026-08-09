# Release Pipeline

**Status:** Canonical  
**Sprint:** KD-4  
**Complements:** `knowledge/package_spec/release_process.md`

No runtime publisher is implemented in this sprint.

---

## Philosophy

A release is a deterministic publication of an immutable `(package_id, package_version)` artifact.

- Content was frozen at `release_candidate` / KD-3 `validated`.
- The release step adds `RELEASE.json`, non-null checksum, and index publication.
- After seal, bytes never change. Deprecation is registry-only.

---

## Stages

Machine form: `release_stages.json`. Requirements: `release_requirements.json`.

```text
1. package_validation
2. checksum_generation
3. version_verification
4. release_notes
5. compatibility_verification
6. publication_readiness
7. seal_and_publish
```

### 1. Package validation

Run `PVP-RELEASE` (validation stages 1–9). Fail → do not release.

### 2. Checksum generation

Apply KD-3 two-pass SHA-256 rule (`release_process.md`). Scope sorted locale `C`. Value MUST be non-null lowercase hex.

### 3. Version verification

Confirm SemVer on `package_version`, object versions, `schema_version` `2.0.0`, `knowledge_version` in range. MAJOR after a prior release requires `breaking_changes`.

### 4. Release notes

`RELEASE.json` `release_notes` non-empty. `migration_notes` non-empty or explicit empty string if additive. `CHANGELOG.md` matches.

### 5. Compatibility verification

Identity `compatibility` agrees with `RELEASE.json` `supported_platform_versions`. Language/school lists cover exported objects. `compatible_with_v1` declared.

This stage does **not** modify API, contracts, or engines.

### 6. Publication readiness

Index entry draft complete; folder name = `package_id`; license set; required dependencies already `released`; release checklist signed.

### 7. Seal and publish

Set KD-3 status `released`. Write checksum into identity + release record. Publish index. Artifact becomes immutable.

---

## Immutability

Released packages MUST be immutable. Corrections → new `package_version` restarting authoring from `draft` (or a branch of the sealed tree copied into a new version workspace).
