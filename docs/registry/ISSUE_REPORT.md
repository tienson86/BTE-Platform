# Registry Infrastructure Issues / TODOs

**Sprint:** Infrastructure Completion V1.1  
**Date:** 2026-07-30  
**Scope:** Registry service layer only  

This file records infrastructure findings. It does **not** modify locked Specs,
Knowledge Canon, or Rule Database.

---

## TODO

1. Full dependency graph cycle detection (current: pairwise mutual only).
2. Object checksum convention that excludes `object.checksum` from the hashed payload.
3. Confirm whether derived indexes should eventually replace on-disk `*_index.json`
   stubs inside each domain folder, or remain under `.derived/`.
4. Wire `tools/run_tests.py` suite selector to include `tests/registry` (optional).
5. Add ruff target for `services/` in `tools/lint.py` (optional).

---

## Architecture Recommendations for Chief Architect

1. **Spec location mismatch**  
   Root Registry Specs declare Module `knowledge/registry` but currently live under
   `knowledge/knowledge_canon/registry/`. Recommend a single canonical documentation
   home to avoid dual authority.

2. **Empty sample vs publication schema**  
   `samples/empty_registry_record.json` is a structural template and intentionally
   fails publication schema (`minLength` on IDs). Recommend documenting
   `template` vs `publishable_record` explicitly in Specs.

3. **Prior locator dirs vs `*_registry/` catalogs**  
   Both coexist under `knowledge/registry/`. Recommend a deprecation policy for
   `references/`, `rules/`, etc. once metadata catalogs are populated.

4. **Report prefix `PREG`**  
   ID Standard uses `PREG` for Report Registry. Confirm this remains intentional
   vs a `RPREG`/`RPTREG` style prefix.
