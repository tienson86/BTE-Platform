# Foundation Release Notes — v1.0.0

| Field | Value |
|-------|-------|
| **Document** | FOUNDATION_RELEASE_NOTES |
| **Foundation version** | 1.0.0 |
| **Release date** | `YYYY-MM-DD` *(placeholder)* |
| **Sprint** | F-1 |
| **Status** | Official |

---

## Summary

BTE Foundation **1.0.0** freezes the platform knowledge, analysis, and decision baseline. No new runtime behavior is introduced in F-1. This release is governance, architecture, and versioning only.

---

## Major milestones

1. Knowledge Database V2 (schema 2.0.0) established with dual-read compatibility to V1.
2. Taxonomy and Ontology (KD-2) published as the package design reference.
3. Knowledge Package Specification (KD-3) sealed: SemVer, lifecycle, PVP, two-pass SHA-256.
4. Authoring and Validation Pipeline (KD-4) defined RELEASE admission.
5. Knowledge Package Generator v1.0 delivered.
6. Analysis cores released: Strength 1.2.0, Seasonal 1.0.0, Temperature 1.0.0, Pattern 1.0.0, Pattern Evaluation 1.0.0.
7. Decision cores released: Useful God Foundation / Priority / Override 1.0.0.
8. AX-1 Analysis Pipeline Integration and AX-2 Canonical Analysis Pipeline 2.0.0 delivered.
9. AX-3 Canonical Decision Pipeline 1.0.0 delivered as a standalone Decision Engine.
10. F-1 freeze documentation published under `knowledge/docs/foundation/`.

---

## Architecture achievements

- One engine, one responsibility: Analysis does not decide; Decision does not recompute analysis.
- Canonical pipelines are the only supported execution models for their package classes.
- Packages are independently versioned and independently deployable.
- Published contracts are the only legal coupling between stages.
- Execution Trace and Decision Trace are append-only.
- Public `run()` surfaces emit diagnostics; they do not raise to API callers.
- Override is a Decision layer, not an Analysis rewrite.
- Reserved stages exist for Luck / Interpretation / Report without activating them.

---

## Known limitations

- Luck Cycle, Annual, Monthly, Interpretation, and Report stages are **inactive**.
- Stem-resolved Yong Shen detail beyond Foundation-era Useful God packages is deferred.
- Interpretation Engine and Report Engine exist as product modules but are **not** Foundation-canonical stages.
- UI Foundation V1.0 is a separate freeze (`knowledge/ui_reference/foundation/`); this release does not merge the two catalogs.
- Release date is a placeholder until Release Manager seal.
- Foundation 1.0.0 loaders reject unknown schema generations (no speculative forward parse).

---

## Future direction

See `FOUNDATION_ROADMAP.md`:

- Phase IV — Luck Engine
- Phase V — Interpretation Engine
- Phase VI — Report Engine

All future work **extends** Foundation. Foundation 1.0.0 remains frozen until an explicit SemVer upgrade.

---

## Upgrade / migration

There is no prior Foundation line. Consumers adopt 1.0.0 as the first official baseline.

Subsequent upgrades follow `FOUNDATION_CHANGE_POLICY.md`.
