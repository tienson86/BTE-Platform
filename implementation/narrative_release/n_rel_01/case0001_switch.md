# N-REL-01 CASE-0001 Switch

Birth input: Nguyễn Tiến Sơn · male · 1987-01-21 04:30 · Hà Tây, Việt Nam

Analyze once. Switch is render-only.

---

## 1. Provider = Pack05

URL: `/result?provider=pack05`

- `data-narrative-surface=production`
- `data-narrative-provider=pack05`
- `data-narrative-fallback=false`
- Overview uses canonical labels (Thân / Nhật chủ / Dụng thần)
- Interpretation uses Pack05 `narrative_result`
- Consulting flow from Narrative V2 is not shown

Screenshot: `screenshots/01_pack05_production.png`

---

## 2. Provider = V2

URL: `/result?provider=v2` (also the release default)

- Same Commercial Dashboard
- `data-narrative-provider=v2`
- Overview insight copies Presentation `headline`
- Interpretation lead copies `consulting_flow` unchanged
- Action Plan copies `top_priority` / `actions` / `warnings`
- Portal does not compose, rewrite, or join Narrative

CASE-0001 consulting_flow:

> Điểm nổi bật ở đây là bạn thường làm việc tốt hơn khi có chỗ dựa ổn định và khi công việc cần xây từ nền tảng. Điều này cho thấy bạn thường duy trì được sự ổn định tốt khi theo đuổi những việc cần thời gian và sự bền bỉ. Ở mặt tích cực, bạn cũng phù hợp với việc học có hệ thống và cần thời gian để ngấm dần. Điều đáng chú ý là điều này hữu ích khi bạn có lối để thể hiện năng lực và khi giới hạn được giữ rõ.

Screenshots:

- `screenshots/02_narrative_v2_production.png`
- `screenshots/02a_v2_overview.png`
- `screenshots/02b_v2_interpretation.png`
- `screenshots/02c_v2_action.png`

---

## 3. Rollback = Pack05

URL: `/result?provider=pack05`

- Same ResultStore payload
- Dashboard returns to Pack05
- Narrative V2 envelope remains stored
- No re-analyze, no migration, no data loss

Screenshot: `screenshots/03_rollback_pack05.png`

---

## Verdict

All three CASE-0001 states succeed.
