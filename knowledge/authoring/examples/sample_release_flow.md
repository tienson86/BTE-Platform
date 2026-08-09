# Sample Release Flow

**Status:** Pedagogical example — no artifact is published by this document.

Continues `bz_99_demo_strength` at `release_candidate`.

---

## Preconditions

- GATE-TECHNICAL and GATE-KNOWLEDGE recorded
- Required dependencies (if any) already `released`
- `CHANGELOG.md` describes `1.0.0`

## Release Manager steps

1. **Package validation** — `PVP-RELEASE` including Golden Dataset stage. If golden tests would fail, stop. Do not edit golden files.
2. **Checksum generation** — two-pass SHA-256; write hex into `PACKAGE.json` and `RELEASE.json`.
3. **Version verification** — `1.0.0` / schema `2.0.0` / knowledge `1.0.0`.
4. **Release notes** — fill `release_notes` and `migration_notes`.
5. **Compatibility verification** — platform ≥ `1.0.0`, `compatible_with_v1=true`.
6. **Publication readiness** — index entry path `.../bz_99_demo_strength`, license set.
7. **Seal and publish** — status `released`; artifact frozen.

Deprecation later updates the index only; sealed `1.0.0` bytes stay unchanged. A fix becomes `1.0.1` via a new draft workspace.

---

## Roles

| Step | Role |
|------|------|
| 1–7 execution | Release Manager |
| Golden/domain waiver | Domain Reviewer |
| Author | Does not sole-approve |
