# G2-02 — Refreeze checklist

Use after Product Owner accepts this freeze. Do **not** unfreeze Gate-1 engines to “fix” UI.

## Confirm before freeze

- [x] Canonical customer surface is `/result` Canonical Desktop V2 (PACK_07)
- [x] Legacy `/result?legacy=1` remains explicit legacy only
- [x] G2-01R identity / ResultStore / `@1.5` unchanged
- [x] Căn cứ chọn Dụng visible on `/result` (not PDF-only)
- [x] Hỷ HK-R1H: no Dụng duplication; insufficient copy when unsupported
- [x] Điều hậu separate from Dụng card
- [x] LEVEL-1 wording = detected, not override-absolute
- [x] Empty `/result` = empty gate + Analyze CTA, never mock
- [x] Contract mismatch = reanalyze notice, no stale analytical cards
- [x] Explicit History banner; no current/history mix
- [x] Ten control cases analytical MATCH + UI PASS
- [x] Portal tests: 277 passed (`tests/js` + `src/features/portal`)
- [x] Result bundle rebuilt (`applications/customer_portal/static/dist/result.js`)
- [x] Engine / rule files changed this phase: **0**

## Customer contract freeze (binding)

- Expected: `analysis_result.UsefulGodView@1.5`
- Gate core label: `G1`
- UI freeze does not change that contract

## Do not refreeze as Gate-1 truth

- Preview fixture (`?preview=1`)
- Legacy presenters
- Print HTML vs Report V1 PDF / DOCX (G2-04)
- Cân Xương (not in production pipeline)

## Next gate

G2-03 starts only after Product Owner accepts G2-02. This checklist does not auto-start G2-03.
