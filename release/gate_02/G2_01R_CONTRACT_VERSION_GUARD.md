# G2-01R — Contract version guard

## Expected customer contract

`analysis_result.UsefulGodView@1.5`

Read from `data.useful_god_source.contract` or `data.result_meta.customer_contract`.

## Status

| Status | Meaning | Customer UI |
|--------|---------|-------------|
| `ok` | Contract matches and `@1.5` display fields are present (or `overall_incomplete`) | Bind structured result |
| `mismatch` | Contract string present but not `@1.5` | Reanalyze notice |
| `unversioned` | Structured blob without contract (old History) | Reanalyze notice |
| `incomplete` | `@1.5` declared but required display fields missing | Incomplete notice |

Copy (may match current UI language):

- Empty: `Chưa có kết quả phân tích. Vui lòng nhập thông tin ngày giờ sinh để bắt đầu.`
- Mismatch / unversioned: `Kết quả này được tạo bởi phiên bản dữ liệu cũ. Vui lòng phân tích lại để cập nhật kết quả.`
- Incomplete: `Kết quả phân tích chưa đủ hợp đồng hiển thị. Vui lòng phân tích lại.`

## Binding rule

For a structured Gate-1 result that is `ok`:

- Dụng ← `useful_god.useful_display`
- Hỷ ← `useful_god.favorable_display`
- Kỵ ← `useful_god.unfavorable_display` (then `unfavorable_gods` of the same `@1.5` object)
- Reason ← `useful_god.short_reason`
- Điều hậu ← temperature labels + `climate_preference_label`

**Do not** fall back to `pattern.dung_than` / `pattern.hy_than` / `pattern.ky_than`.

If the contract is not `ok`, do not render stale Dụng/Hỷ as valid. `/reports` structured composer shows the same notice instead of executive presenters.

## Stale API / new Portal

Portal expects `@1.5`. Older payload → mismatch/unversioned/incomplete → reanalyze state. No legacy Dụng/Hỷ.

## New API / stale stored result

Fresh Analyze writes `@1.5` current. Old History stays unversioned until opened explicitly; it never becomes current implicitly.
