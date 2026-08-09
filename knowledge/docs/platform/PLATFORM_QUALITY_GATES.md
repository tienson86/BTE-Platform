# Platform Quality Gates

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_QUALITY_GATES |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | Architecture Board + Release Manager |

A change may not advance until every applicable gate passes.

---

## 1. Coding

- One engine, one responsibility
- Type hints and public docstrings
- Result objects, not tuples
- No `print()`; use logging
- No bare `except:`
- No circular imports
- Dependency injection over singletons
- Minimal, additive diffs
- Public API names preserved (wrappers if needed)

---

## 2. Contracts

- Published inputs / outputs declared
- SemVer constraints verified before execution
- Schema 2.0.0 required for V2 packages
- No undeclared publication
- No overwrite of published fields

---

## 3. Validation

- Input validate → calculate → output validate → result
- Package PVP MINIMAL / STANDARD / RELEASE unchanged
- Duplicate keys, missing values, invalid enums, broken references rejected
- Engines read database only

---

## 4. Testing

- Module pytest only per change
- Do not edit tests / golden / snapshots / expected to force pass
- Do not skip, comment, or delete asserts
- Prefer root-cause source fixes
- Determinism: identical inputs + clock ⇒ identical JSON

---

## 5. Release

- Change control approvals complete
- SemVer class assigned
- Manifest + checksums + notes updated for the *new* version (never rewrite v1.0 identities)
- Release Manager seal

---

## 6. Freeze

- Foundation 1.0.0 documents untouched except explicit Foundation upgrade
- Platform 1.0.0 architecture documents are the freeze surface
- Sealed packages immutable
- Canonical pipelines remain the only supported new execution models
- ADR required for architectural divergence

AF-1 itself passed the freeze gate by adding documentation only.
