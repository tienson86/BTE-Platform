# G2-05 — History / reload freeze report

**Status: G2-05: SAVE / HISTORY / RELOAD FROZEN — READY FOR G2-06**

Date: 2026-08-21  
Entry: G2-04 report / PDF / DOCX frozen  
Invariant:

```
ANALYZE → SAVE SNAPSHOT → HISTORY → OPEN SAVED ANALYSIS → RESULT / REPORT / PDF / DOCX
```

must preserve the same stored analytical truth. History is a snapshot. It must not silently re-run current engines.

## Hard freeze

Gate-1 analytical engines and rules were not changed. G2-01R identity/precedence, G2-02 Result semantics, G2-03 narrative source, and G2-04 canonical export model stay frozen.

If a stored analysis had differed because engines changed, this gate would have **stopped**. Ten control snapshots: **0 analytical diffs**.

## What was repaired (persistence only)

| Defect | Repair |
|--------|--------|
| Explicit History (`?from=history&id=`) silently fell back to current when the view pointer missed | Missing/corrupt History is a safe error. Current is not loaded into a History route |
| Refresh of History required session `bte_view_result` | Lookup uses the History list snapshot by `analysis_id` |
| Same `analysis_id` could be appended again | Declared Analyze id is saved once. Refresh / report / PDF / DOCX do not write History |
| History list lacked customer context | Name, birth date/time, analysis time, id, legacy badge |
| “Xem báo cáo” from History always opened `/reports` (latest/current) | History keeps `?from=history&id=...` |
| Re-analyze did not reuse stored birth | `/analyze?reanalyze=1&...` prefills birth. New Analyze gets a new id. Old row stays |

Allowed files: ResultStore, History/report/analyze adapters, route selection, version guards, tests, release docs, Result bundle. Analytical engine/rule files changed: **0**.

## Save policy (frozen)

**A — automatic.** Every successful Analyze appends exactly one History snapshot (`BtePortal.ResultStore.save` from `/analyze`).

- Refresh `/result` does not save.
- Report / PDF / DOCX / Print do not save.
- Two intentional Analyze runs of the same birth may create two rows (new server `analysis_id` each time).
- The same declared `analysis_id` is not duplicated.

## Snapshot vs recompute

Opening History does **not** call Analyze. It does **not** rebuild Strength / Pattern / Useful God from birth. It renders the stored blob.

Presentation formatting of that stored blob through the current Report V1 builder is allowed (G2-04). Analytical recomputation is forbidden.

Re-analyze is explicit, uses stored birth input, and creates a **new** record.

## Persistence architecture

Customer current + History are **browser-local** (`localStorage` + `sessionStorage`). There is no History database in V1.0. Backend restart does not invent a new analysis id and does not delete History unless the browser store is cleared.

## Tests

```
node applications/customer_portal/tests/js/result_store_flow.js
npx vitest run tests/js/g2_05_history_reload.test.tsx
python -m pytest applications/customer_portal/tests/test_g2_05_history.py applications/api/tests/test_g2_05_history_snapshot.py -q
python release/gate_02/_g2_05_history_probe.py
```

- ResultStore harness: **61 passed**
- Portal G2-05: **9 passed** (G2-01R / G2-02 / G2-04 regression still green)
- API/portal pytest: **17 passed**
- Probe: **10/10 MATCH**, `mismatch_count: 0`

## Cross-case

Primary: Analyze Dũng → Analyze Tuyền → open History Dũng → report/PDF/DOCX Dũng → refresh History Dũng → normal `/result` = current Tuyền. No mixing.

Secondary: Cao Xuân Trường / Đặng Thị Dung covered in the ten-control snapshot matrix.

## Diff audit (this phase)

Analytical engine / rule files changed: **0**.

## Final status

**G2-05: SAVE / HISTORY / RELOAD FROZEN — READY FOR G2-06**

Do not start G2-06 automatically.
