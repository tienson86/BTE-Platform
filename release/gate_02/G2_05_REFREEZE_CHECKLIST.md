# G2-05 — Refreeze checklist

Use this list before touching ResultStore, History routes, or export selection again.

## Must remain true

- [ ] History stores the Analyze snapshot (`input` + `data`), not a live engine rerun
- [ ] Canonical `analysis_id` is retained on the row and inside `data`
- [ ] Saved snapshot is immutable after write
- [ ] Opening History does not call Analyze
- [ ] New History rows have contract / release / `created_at` / analysis id
- [ ] Old History is not backfilled with new metadata
- [ ] Explicit History is isolated from current
- [ ] Viewing History does not replace `bte_last_result` / `bte_current_analysis_id`
- [ ] Refresh `/result` does not duplicate History
- [ ] Report / PDF / DOCX / Print of History use selected snapshot B
- [ ] Missing History id → “Không tìm thấy hồ sơ.” (not current)
- [ ] Corrupt snapshot → safe error (not current, not mock)
- [ ] Incompatible old contract → version notice + Re-analyze
- [ ] Re-analyze creates a **new** row; old row unchanged
- [ ] Ten control snapshots match save-time canonical result
- [ ] No Dũng/Tuyền field mixing
- [ ] Analytical engine/rule files changed: 0
- [ ] Visual captures under `release/gate_02/screenshots/g2_05/`

## Must not do

- [ ] Do not add a History database in this gate
- [ ] Do not add “set as current”
- [ ] Do not add per-row delete (not present)
- [ ] Do not make clear-all also wipe current unless product already defined that
- [ ] Do not silently remap `pattern.dung_than` / `hy_than`
- [ ] Do not regenerate stored narrative
- [ ] Do not start G2-06 from this checklist

## Commands

```
node applications/customer_portal/tests/js/result_store_flow.js
npx vitest run tests/js/g2_05_history_reload.test.tsx
python -m pytest applications/customer_portal/tests/test_g2_05_history.py applications/api/tests/test_g2_05_history_snapshot.py -q
python release/gate_02/_g2_05_history_probe.py
```

From `applications/customer_portal`: `npm run build:result`
