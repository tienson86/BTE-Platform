# G2-01R — History version policy

## New saves (after this repair)

Each new History row copies non-analytical metadata from the Analyze payload:

| Field | Source |
|-------|--------|
| `analysis_id` / `id` | canonical server id |
| `created_at` | `data.result_meta.created_at` (else save time) |
| `saved_at` | save time |
| `customer_contract` | `useful_god_source.contract` or `result_meta.customer_contract` |
| `gate_core_freeze` | `result_meta.gate_core_freeze` (`G1` when present) |
| `month_pillar_standard` | `result_meta.month_pillar_standard` |
| `release_label` | `result_meta.release_label` |
| `data` | full structured snapshot (unchanged analytical blob) |

Old records are **not** backfilled. Missing metadata means `legacy/unversioned`.

## Old / unversioned snapshots

- Do **not** recompute with current Gate-1 engines.
- Do **not** mutate the stored row.
- If the blob is compatible with `analysis_result.UsefulGodView@1.5`, display it as historical truth (explicit History URL only).
- If incompatible / unversioned: show the version notice and offer re-analysis through normal Analyze. Do not silently map old `pattern.dung_than` / `hy_than` into customer Dụng/Hỷ.

## Current vs History

Opening old History does not replace current. Only a new Analyze updates `bte_last_result`.
