# BTE Platform Release Notes v1.0.0

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_RELEASE_NOTES_v1.0 |
| **Platform version** | 1.0.0 |
| **Sprint** | AF-1 |
| **Status** | Official |
| **Date** | 2026-08-09 |

---

## Summary

BTE Platform v1.0.0 freezes the commercial architecture: Knowledge Database V2, sealed Knowledge Packages, canonical Analysis / Decision / Luck / Interpretation / Report pipelines, and Foundation 1.0.0.

AF-1 adds **governance and release documentation only**. No engine, package, API, contract, or test files were modified.

---

## Included capability (already shipped before AF-1)

- Foundation Freeze F-1
- Knowledge schema 2.0.0 and package spec 1.0.0
- Analytical packages `bz_01`–`bz_05`
- Decision packages `bz_06`–`bz_08`
- Luck timeline package `bz_09`
- Canonical pipelines: Analysis 2.0.0, Decision 1.0.0, Luck 1.0.0, Interpretation 1.0.0, Report 1.0.0
- Machine-readable trace, audit, and diagnostics on every canonical pipeline
- In-memory report artifacts (PDF/DOCX/HTML/Markdown/JSON envelopes; no filesystem persist)

---

## Explicitly not in v1.0 runtime

- Cloud publisher
- Email delivery
- Print
- Interpretation AI rewrite
- XLSX / PPTX renderers
- New analytical rules beyond sealed packages

These remain registered or reserved and disabled.

---

## Compatibility

Consumers of Foundation 1.0.0 and schema 2.0.0 remain compatible. See `PLATFORM_COMPATIBILITY_MATRIX.md`.

---

## Upgrade from pre-freeze lines

1. Bind new Analysis Knowledge work to `canonical_analysis_pipeline` 2.0.0.
2. Bind Decision / Luck / Interpretation / Report new work to their canonical pipelines.
3. Do not edit sealed packages; publish a new package version instead.
4. Keep public API wrappers; do not import engine internals.

---

## Known limitations

- Report rendering produces deterministic mime envelopes, not paginated print drivers.
- Interpretation does not generate free-form consultant prose beyond assembled candidates.
- Luck does not score fortune quality; it publishes timeline impact and opportunity/risk deltas.

---

## Certification

See `knowledge/releases/v1.0/RELEASE_CERTIFICATE.md`.
