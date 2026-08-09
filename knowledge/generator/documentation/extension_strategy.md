# Extension Strategy

| Field | Value |
|-------|-------|
| **Generator version** | 1.0.0 |
| **Status** | Canonical |

How the Generator grows without breaking the Knowledge Platform.

---

## 1. Principles

1. **Additive first** — new profiles, templates, constraints, and package types.
2. **Never rewrite released packages** to fit a new generator version.
3. **Dual-read** — old packages remain loadable.
4. **One generator** — Feng Shui / Qi Men / I Ching do not get a second root folder; they get new type/instance profiles.
5. **Spec before runtime** — validators, AI runners, and visual builders land in later sprints.

---

## 2. Adding a package type

1. MINOR or MAJOR `generator_version` if `package_type` enum grows.
2. Add `profiles/<type>.json` inheriting `GEN-PROFILE-COMMON`.
3. Declare component flags (`evidence_required`, `reasoning_required`, …).
4. Add at least one instance example profile before first official emit.
5. Do not modify engines to “support” the type until a dedicated engine sprint.

KD-3 `package.schema.json` already includes `feng_shui`, `qi_men`, `i_ching`. Generator v1.0.0 type profiles cover the five required reusable kinds; those three disciplines use `analytical` or a future type profile without a v1.0.0 enum break.

---

## 3. Adding a domain

1. Extend `knowledge/taxonomy/domains.json` in a taxonomy sprint (not ad hoc inside a package).
2. Point instance profile `domain.domain_id` at the new id.
3. Reserve `package_id` + rule prefix.

---

## 4. Adding evidence or reasoning requirements

Toggle flags on the type or instance profile. Do not fork templates. Strengthen Gold/Platinum floors via `quality_overrides` if needed.

---

## 5. Multilingual extension

- Keep machine ids stable.
- Add `languages[]` and language-specific payloads / sentence variants (`ONT-LANGUAGE_VARIANT`).
- Do not encode language in `package_id` unless the package is permanently monolingual with no twin.

---

## 6. Scale (100,000+ records)

- Zero-padded numeric suffixes (6+ digits).
- One purpose per file; shard by prefix, not by unbounded single JSON array when size demands (future packaging guideline).
- Checksum scope remains a sorted path list.
- Independent package releases — never require a monorepo-wide regenerate.

---

## 7. Future tooling

| Tool | Consumes | Must not |
|------|----------|----------|
| AI runner | profiles + templates + AI spec | auto-release |
| Visual builder | same contracts | bypass validation |
| Runtime validator | GV-* + PVP-* | mutate knowledge |
| Package index publisher | released packages | edit package bytes |

---

## 8. Compatibility matrix

| Change | Action |
|--------|--------|
| New optional template field | PATCH |
| New GC/GV id | PATCH if additive fail-open optional; MINOR if release-blocking |
| New pipeline stage | MINOR (append) or MAJOR (reorder) |
| Remove required profile field | MAJOR |
| Strength Core content edit via generator | **Forbidden** |
