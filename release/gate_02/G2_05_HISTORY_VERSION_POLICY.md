# G2-05 — History version policy

This freeze extends `G2_01R_HISTORY_VERSION_POLICY.md`. It does not backfill old rows.

## New History records (after this freeze)

Must contain:

| Metadata | Typical V1.0 value |
|----------|-------------------|
| Canonical `analysis_id` | Server request id copied into `data` and the History row |
| `created_at` | `result_meta.created_at` (analysis creation, UTC ISO) |
| Customer contract | `analysis_result.UsefulGodView@1.5` |
| Narrative contract | `pack05_narrative_result_v1` when Composer produced narrative |
| Gate/Core freeze | `G1` |
| Month Pillar standard | `BTE-MONTH-PILLAR-LUNAR-V1.0` |
| Release label | `BTE V1.0 — Gate 1 Core Engine` |

Missing metadata on a **new** save is a persistence defect. Do not fake it later.

## Old / unversioned records

Old records stay `legacy/unversioned`. Do **not** stamp `@1.5`, `G1`, or a new `created_at` onto them.

| State | Customer behavior |
|-------|-------------------|
| Identifiable as historical, and blob is compatible with UsefulGodView@1.5 | Display stored snapshot. History banner if explicit History |
| Unversioned / incompatible | Version notice. No Dụng/Hỷ cards from `pattern.dung_than` / `hy_than` |
| Corrupt / partial snapshot | Safe error. No mock. No mix with current |
| Missing id on explicit History URL | “Không tìm thấy hồ sơ.” Do **not** load current |

## Frozen version notice

Keep the G2-01R customer sentence (does not call the historical analysis “wrong”):

> Kết quả này được tạo bởi phiên bản dữ liệu cũ. Vui lòng phân tích lại để cập nhật kết quả.

Meaning freeze: the stored result is from an older data version; re-analysis is recommended for current V1.0 presentation.

CTA: **Phân tích lại** → `/analyze?reanalyze=1` with stored birth input. This creates a **new** analysis. The old History row is unchanged.

## Contract guard

Compatibility is checked **per selected History record**, not assumed from the runtime Portal contract.

If an old History lacks UsefulGodView@1.5, do **not** fall back to `pattern.dung_than` / `hy_than`.

## Narrative History

G2-03 remains frozen. Stored `narrative_result` is preserved. Do not regenerate with Composer unless the customer explicitly Re-analyzes. Missing narrative → limited empty narrative state, no fabricated essay.

## Portal rebuild

A new frontend bundle may change formatting. It must not reinterpret stored analytical content. Compatible stored contracts render. Incompatible stored contracts show the version notice.
