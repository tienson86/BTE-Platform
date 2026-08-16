# Findings — EV-0003

## Live vs PO stated truth

| Field | PO stated | Live 2026-08-16 | Discrepancy |
|-------|-----------|-----------------|-------------|
| Day Master | Bính Hỏa | Bính Hỏa | None |
| Strength | balanced / Trung hòa / ~0.54 | balanced / Trung hòa / 0.54 | None |
| Pattern | Chính Ấn | Chính Ấn | None |
| Useful God | Canh | Canh | None |
| Hỷ | Canh, Tân, Nhâm | Canh, Tân, Nhâm | None |
| Kỵ | Giáp, Ất | Giáp, Ất | None |
| Five Elements | 6/1/3/1/3 | 6/1/3/1/3 | None |
| Current Da Yun | Đinh Tỵ 2024–2033 | Đinh Tỵ 2024–2033 | None |

Do not hardcode PO values as expected; they currently match. Cover class `Người điều tiết` vs body `Người chỉnh trục` is mapping, not analytical.

## Flags

| Code | Severity |
|------|----------|
| generic_case_narrative | Critical (recs/career vs Trung/CASE-0003) |
| luck_list_only | Critical |
| conclusion_restart | Critical |
| ten_god_catalogue_dump | Major |
| useful_god_application_missing | Major (life stage) |
| hy_ky_undifferentiated | Minor (rec 5 list) |
