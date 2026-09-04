# P-RUNTIME-01 live ResultStore payload matrix

Source: fresh CASE-0001 `POST /api/v1/analyze` on 2026-09-04, not a fixture.

See `live_payload_matrix.json` and `live_dom_proof.json`.

| Field | Live CASE-0001 | P-001 fixture | P-003 fixture | P-004 fixture | Gap |
|---|---|---|---|---|---|
| `bazi.day_master` | Canh | Canh | Canh | Canh | none |
| `bazi.day_master_element` | Kim | Kim | (unused) | (unused) | none |
| `strength.strength_level` | strong → Thân vượng | strong | (unused) | strong | none |
| `pattern.cach_cuc` | Chính Ấn | Chính Ấn | (unused) | Chính Ấn | none |
| `useful_god.useful_display` | **Hỏa · Đinh · Chính Quan** | Thủy · Nhâm · Thực Thần | (unused) | Thủy · Nhâm · Thực Thần | **live Dụng differs from P-001/P-004 fixtures** |
| `useful_god.favorable_display` | `Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng` | same incomplete sentence | (unused) | (unused) | Hỷ omitted on purpose |
| `useful_god.unfavorable_display` | Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài | same | (unused) | (unused) | none |
| `ten_gods.visible` | Thất Sát, Kiếp Tài, Nhật Chủ, Thiên Ấn | (via narrative case) | same set | same set | none |
| `ten_gods.hidden` | present (Thiên Tài, Chính Ấn, …) | n/a | Thiên Tài, Chính Ấn | present | none |
| `shensha` | published on `bazi.shensha_matches` / `bazi.shensha`, not top-level `shensha` | n/a | n/a | flattened in P-004R audit | matrix helper key only |
| `luck` | present | n/a | n/a | current cycle used | none |
| `five_elements` | present | n/a | n/a | present | none |
| `temperature` | present | n/a | n/a | present | none |
| `narrative_v2_shadow` | present (`bte.presentation.v2.1`) | present | n/a | n/a | none |
| `calendar.calendar_rule_version` | G1-10C | often omitted in unit fixtures | omitted | omitted | live passes calendar gate |
| `useful_god_source.contract` | `analysis_result.UsefulGodView@1.5` | often omitted | omitted | included in P-004R | live passes contract gate |

## Adapter consequence

- P-001 live Hero shows Nhật Chủ / Thân / Mệnh Cục / Dụng / Kỵ. Hỷ omitted.
- P-003B live resolves supported triple **Kiếp Tài · Thất Sát · Thiên Ấn**.
- P-004 live domains: marriage, health, career, finance, property. Children omitted because live Dụng is Chính Quan, not Thực Thần / Thương Quan.
