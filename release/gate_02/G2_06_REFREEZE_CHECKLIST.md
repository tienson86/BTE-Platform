# G2-06 — Refreeze checklist

Use this list before starting G2-FINAL. Do **not** unfreeze Gate-1 engines.

## Confirm before freeze

- [x] Four primary full journeys PASS (Sơn, Tuyền, Dũng, Trường)
- [x] Ten control analytical probes MATCH (0 diffs vs Frozen Truth)
- [x] Analyze creates one coherent `analysis_id`
- [x] Result / Narrative / Full Report use the stored snapshot
- [x] Official PDF is Report V1 Playwright (`Tải PDF`)
- [x] DOCX is editable Unicode (`Tải DOCX`)
- [x] Print is convenience **In**, not official PDF
- [x] History writes once per successful Analyze
- [x] History snapshot immutable
- [x] Current / History isolated
- [x] History exports the selected record
- [x] Re-analyze creates a new record
- [x] Empty / missing / corrupt / old-contract states safe
- [x] No field mixing, no stale `pattern.dung_than` / `hy_than` fallback
- [x] No customer rule IDs in Report HTML/DOCX
- [x] Analytical engine/rule files changed: **0**
- [x] Final E2E probe rerun PASS
- [x] Artifacts under `release/gate_02/screenshots/g2_06/`

## Must not do

- [ ] Do not retune analytics
- [ ] Do not redesign Result UI
- [ ] Do not add a History database
- [ ] Do not treat browser Print as official PDF
- [ ] Do not start G2-FINAL from this checklist automatically

## Commands

```
python release/gate_02/_g2_06_e2e_probe.py
python -m pytest applications/api/tests/test_g2_06_e2e.py -q
```

From `applications/customer_portal`:

```
npx vitest run tests/js/g2_06_customer_e2e.test.tsx
```
