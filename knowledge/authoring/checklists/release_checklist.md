# Release Checklist

**Use before:** `release_candidate` → `released`  
**Package:** `{{PACKAGE_ID}}` `{{PACKAGE_VERSION}}`  
**Release Manager:** `{{RELEASE_MANAGER}}` — Date: `{{DATE}}`

---

## Preconditions

- [ ] Workflow state is `release_candidate` (KD-3 `validated`)
- [ ] GATE-TECHNICAL and GATE-KNOWLEDGE recorded
- [ ] Required dependencies are `released` at satisfying versions
- [ ] `CHANGELOG.md` describes this version
- [ ] MAJOR bump includes `breaking_changes` and migration notes

## Release pipeline

- [ ] Package validation (`PVP-RELEASE`) pass
- [ ] Quality Validation meets intended level
- [ ] Golden Dataset Validation pass or documented `not_applicable` with waiver
- [ ] Checksum generated via KD-3 two-pass rule; value non-null
- [ ] Version verification (package / schema / knowledge / compatibility)
- [ ] Release notes complete in `RELEASE.json`
- [ ] Migration notes present (empty string only if additive)
- [ ] Compatibility verification vs platform/API/engine bounds (data-only; no API edits)
- [ ] Publication readiness: index entry drafted, paths stable, license set
- [ ] `immutability.immutable` is `true`

## Publication

- [ ] Sealed artifact directory will not be edited in place
- [ ] Index/registry update planned (status `released`)
- [ ] Consumers informed if this is a breaking MAJOR

Release Manager sign-off: `{{RELEASE_MANAGER}}`  
Domain concurrence (if required): `{{DOMAIN_REVIEWER}}`
