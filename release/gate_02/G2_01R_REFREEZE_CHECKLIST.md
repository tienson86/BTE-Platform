# G2-01R — Refreeze checklist

Use after this repair is accepted. Do not unfreeze Gate-1 engines to “fix” binding.

## Confirm before freeze

- [ ] Ten control cases still 0 analytical diffs vs `G1_PREFINAL_CONTROL_CASES.json`
- [ ] HTTP Analyze still stamps `data.analysis_id = request_id`
- [ ] Production `/result` with empty ResultStore shows empty copy, never mock fixture
- [ ] History open URL is `?from=history&id=...`
- [ ] `/result?legacy=1` banner visible; Desktop `/result` does not call `loadForView`
- [ ] Missing `@1.5` shows reanalyze notice, not `pattern.dung_than`
- [ ] Portal bundle rebuilt (`applications/customer_portal/static/dist/result.js`)
- [ ] No Calendar / BaZi / Strength / Pattern / Useful God / ShenSha / Luck / Score engine diffs

## Customer contract freeze (binding)

- Expected: `analysis_result.UsefulGodView@1.5`
- Gate core label: `G1`
- Month pillar standard (when published): `BTE-MONTH-PILLAR-LUNAR-V1.0`

## Do not refreeze as Gate-1 truth

- ResultStore keys
- Preview fixture
- Legacy presenters
- Print HTML vs Report V1 PDF split (G2-04)

## Next gate

G2-02 starts only after Product Owner accepts G2-01R. This checklist does not auto-start G2-02.
