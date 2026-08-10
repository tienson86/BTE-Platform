# Strength Evidence Ledger

Source JSON: `evidence/CASE-000N.json`  
Pipeline stages recorded; unavailable stages marked `NOT_EXPOSED`.

## Shared pipeline (all cases)

```text
Chart (Calendar→BaZi)
→ Season Context (month_status, season, season_phase)
→ Temperature Context (StrengthContext branch map + separate TemperatureEngine)
→ Supporting / Resource elements (visible-stem ten gods)
→ Restricting elements (officer / output / wealth)
→ Root evidence (hidden-stem same-element branch count)
→ Strength Evidence (matched CSV rules)
→ Weighted Evidence (bucket sums)
→ Raw Strength Score (Σ rule scores)
→ Normalized Score ((raw+50)/100)
→ Current Band / Label / Confidence
→ Published StrengthResult contract
```

**NOT_EXPOSED to StrengthContext / scorer:**

- TemperatureEngine `temperature_score` / `temperature_level` (engine runs separately; Strength uses branch-derived `temperature_type` only)
- Dedicated `supporting_elements` / `restricting_elements` fields (proxied via companion/resource/officer/output/wealth lists)
- Combination geometry evidence (combination bucket always 0 in this sample)

---

## CASE-0001 — Canh / Tân Sửu

| Stage | Value |
|---|---|
| Chart | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| Season | winter / late_winter / **Tướng** (Thổ→Kim) |
| Temp (context) | cold |
| Temp (engine) | hot / 0.72 — **not used by Strength scorer** |
| Support | Kiếp Tài; Thiên Ấn |
| Restrict | Thất Sát |
| Root | Thông căn 1 chi |
| Raw / Norm | 37 / **0.87** |
| Band / Label | strong / Thân vượng |
| Confidence | 1.0 |

Matched rules: `sea_002(+25), root_003(+12), sup_001(+8), ctl_001(-10), ctl_006(-8), spc_004(+10)`

---

## CASE-0002 — Bính / Nhâm Dần

| Stage | Value |
|---|---|
| Chart | Đinh Tỵ / Nhâm Dần / Bính Ngọ / Tân Mão |
| Season | spring / Tướng (+25) |
| Root | Thông căn 3 chi (+30) |
| Raw / Norm | 39 / **0.89** |
| Band / Label | strong / Thân vượng |

Directionally aligns with expert “very strong”; taxonomy collapses intensity.

---

## CASE-0003 — Nhâm / Giáp Thân (boundary)

| Stage | Value |
|---|---|
| Chart | Ất Mùi / Giáp Thân / Nhâm Tuất / Giáp Thìn |
| Season | autumn / Tướng (+25) |
| Root | Thông căn 2 chi (+22) |
| Drain | heavy (−23) |
| Raw / Norm | 16 / **0.66** |
| Band / Label | strong / Thân vượng |

Barely over strong threshold. Expert: slightly weak.

---

## CASE-0004 — Mậu / Canh Thân

| Stage | Value |
|---|---|
| Raw / Norm | 34 / **0.84** |
| Band / Label | strong / Thân vượng |

Agrees with expert “strong”.

---

## CASE-0005 — Bính / Đinh Dậu

| Stage | Value |
|---|---|
| Season | Tù (−10) |
| Root | Thông căn 3 (+30) |
| Raw / Norm | 16 / **0.66** |
| Band / Label | strong / Thân vượng |

Expert: balanced / slightly strong — taxonomy + threshold cliff.

---

## CASE-0006 — Quý / **Mậu Ngọ** (corrected)

| Item | Value |
|---|---|
| Original expert month | Đinh Tỵ (invalid under tiết khí — PILOT-1A) |
| Corrected live month | **Mậu Ngọ** |
| Season | summer / **Tù** (−10) for Thủy in Hỏa month |
| Raw / Norm | 0 / **0.50** |
| Band / Label | balanced / Trung hòa |

Calendar closed. Remaining gap vs “thiên nhược” = taxonomy (and possible expert disagreement on mid tilt).

---

## CASE-0007 — Mậu / Tân Mùi

| Stage | Value |
|---|---|
| Season | Đắc lệnh (+35) |
| Raw / Norm | 26 / **0.76** |
| Band / Label | strong / Thân vượng |

Agrees with expert “strong”.

---

## Bucket summary

| Case | sea | root | sup | drain | ctl | spc | raw | norm |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0001 | 25 | 12 | 8 | 0 | −18 | 10 | 37 | 0.87 |
| 0002 | 25 | 30 | 8 | −6 | −18 | 0 | 39 | 0.89 |
| 0003 | 25 | 22 | 0 | −23 | −8 | 0 | 16 | 0.66 |
| 0004 | 10 | 30 | 8 | −8 | −6 | 0 | 34 | 0.84 |
| 0005 | −10 | 30 | 13 | −11 | −6 | 0 | 16 | 0.66 |
| 0006 | −10 | 12 | 8 | 0 | −10 | 0 | 0 | 0.50 |
| 0007 | 35 | 22 | 0 | −13 | −18 | 0 | 26 | 0.76 |
