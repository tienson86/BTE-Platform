# G2-03 — Refreeze checklist

Use after Product Owner accepts this freeze. Do **not** unfreeze Gate-1 engines to “fix” prose.

## Confirm before freeze

- [x] One canonical customer narrative path: Composer V2 → `pack05_narrative_result_v1`
- [x] Pack 05 NarrativeEngine is compatibility fallback only
- [x] HTTP `data.analysis_id` = `narrative_result.run_id` when request_id is present
- [x] Report/PDF consumes the same `narrative_result` (G2-04 still owns rendering)
- [x] Ten control cases analytical MATCH + narrative PASS
- [x] No Strength / Pattern / Dụng contradictions on those cases
- [x] Insufficient Hỷ is not later stated as a definite Hỷ
- [x] Điều hậu remains separate from Overall Dụng
- [x] LEVEL-1 special wording = detected, not override-absolute
- [x] Tuyền has no stale Tòng Tài
- [x] No rule IDs / unresolved placeholders in live narrative
- [x] Missing `narrative_result` → limited empty interpretation, not a fake chart essay
- [x] Unversioned History → G2-01R contract notice, not silent V1.0 reinterpret
- [x] Gate-1 analytical engine/rule files changed this phase: **0**
- [x] Narrative length was not expanded

## Customer contract freeze (binding)

- Expected: `analysis_result.UsefulGodView@1.5`
- Narrative consumer: `pack05_narrative_result_v1`
- Gate core label: `G1`

## Do not refreeze as Gate-1 truth

- Preview fixture (`?preview=1`)
- Legacy presenters
- Pack 04 `interpret_from_analysis()` expert pipeline
- Historical launch_08 / pilot snapshots
- PDF/DOCX layout (G2-04)

## Next gate

G2-04 starts only after Product Owner accepts G2-03. This checklist does not auto-start G2-04.
