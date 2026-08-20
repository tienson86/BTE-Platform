# G1-PREFINAL — V1.0 Final Human Validation Set

**Date:** 2026-08-20  
**Oracle:** current production `OrchestratorService.analyze` only. Old reference sheets are not the oracle.  
**Contract:** `analysis_result.UsefulGodView@1.5`  
**Timezone:** Asia/Bangkok except Hưng (`Asia/Ho_Chi_Minh`).

Override authority = Pattern `ug_override_eligible` (PAT-R1F / G1-X01). Detection of LEVEL-1 special is listed separately and does **not** grant Overall override.

Customer Hỷ is `favorable_display`, not internal `favorable_gods`.

| Case | Four Pillars | Strength | Pattern | Override authority | Điều hậu | Overall Dụng | Reason archetype | Customer Hỷ | Kỵ | Current Luck |
|------|--------------|----------|---------|--------------------|----------|--------------|------------------|-------------|-----|--------------|
| Nguyễn Tiến Sơn | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần | 0.87 strong | Chính Ấn | false (none) | Hỏa · Bính · Thất Sát | Hỏa · Đinh · Chính Quan | CHẾ | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài | Ất Tỵ · ages 35–44 |
| Lương Ngọc Huỳnh | Bính Ngọ / Đinh Dậu / Bính Tuất / Canh Dần | 0.64 balanced | Chính Tài | false (none) | Hỏa · Đinh · Kiếp Tài | Kim · Tân · Chính Tài | BALANCED-WEALTH | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | Hỏa · Đinh · Kiếp Tài | Quý Mão · ages 55–64 |
| Đặng Thị Dung | Nhâm Tuất / Ất Tỵ / Ất Tỵ / Tân Tỵ | 0.24 weak | Sát Ấn tương sinh — Thất Sát chế bởi Chính Ấn | false (detected, not follow) | Thủy · Nhâm · Chính Ấn | Thủy · Nhâm · Chính Ấn | SINH / TRỢ | Mộc · Ất · Tỷ Kiên | Thổ · Mậu · Chính Tài / Thổ · Kỷ · Thiên Tài | Tân Sửu · ages 36–45 |
| Đoàn Quang Hưng | Tân Dậu / Đinh Dậu / Kỷ Mão / Bính Dần | 0.61 balanced | Thực Thần | false (none) | Hỏa · Đinh · Thiên Ấn | Thủy · Nhâm · Chính Tài | BALANCED-WEALTH | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | Thổ · Mậu · Kiếp Tài | Quý Tỵ · ages 37–46 |
| Vũ Thị Thanh Tuyền | Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi | 0.66 strong | Kiếp Tài | false (none) | Thủy · Nhâm · Thiên Tài | Mộc · Ất · Chính Quan | CHẾ | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | Thổ · Mậu · Tỷ Kiên / Thổ · Kỷ · Kiếp Tài | Bính Dần · ages 42–51 |
| Cao Xuân Trường | Kỷ Tỵ / Tân Mùi / Nhâm Ngọ / Mậu Thân | 0.34 weak | Quan Ấn tương sinh — Chính Quan sinh Chính Ấn trợ Nhật chủ | false (detected, not follow) | Thủy · Nhâm · Tỷ Kiên | Kim · Tân · Chính Ấn | SINH / TRỢ | Thủy · Nhâm · Tỷ Kiên | Hỏa · Đinh · Chính Tài / Hỏa · Bính · Thiên Tài | Đinh Mão · ages 35–44 |
| Lưu Hoàng Sơn | Bính Tý / Kỷ Hợi / Canh Ngọ / Ất Dậu | 0.51 balanced | Sát Ấn tương sinh — Thất Sát chế bởi Chính Ấn | false (detected, not follow) | Hỏa · Bính · Thất Sát | Mộc · Ất · Chính Tài | BALANCED-WEALTH | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | Kim · Tân · Kiếp Tài | Nhâm Dần · ages 23–32 |
| Phạm Thị Huyền | Đinh Mão / Mậu Thân / Kỷ Mùi / Ất Sửu | 0.74 strong | Thương Quan | false (none) | Hỏa · Đinh · Thiên Ấn | Kim · Tân · Thực Thần | TIẾT | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | Thổ · Kỷ · Tỷ Kiên / Thổ · Mậu · Kiếp Tài | Tân Hợi · ages 30–39 |
| Lương Văn Mạnh | Đinh Mão / Đinh Mùi / Kỷ Dậu / Đinh Mão | 1.00 strong | LEVEL-1 detected: Giá Vượng (`jia_wang`) | **false** (PAT-R1F) | Thủy · Nhâm · Chính Tài | Kim · Tân · Thực Thần | TIẾT | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | Thổ · Kỷ · Tỷ Kiên / Thổ · Mậu · Kiếp Tài | Quý Mão · ages 38–47 |
| Ngô Đắc Dũng | Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn | 1.00 strong | LEVEL-1 detected: Giá Sắc (`gia_sac`) | **false** (PAT-R1F) | Hỏa · Đinh · Chính Quan | Thủy · Nhâm · Thực Thần | TIẾT | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài | Tân Tỵ · ages 34–43 |

Births used (not Golden case IDs):

| Case | Civil |
|------|-------|
| Nguyễn Tiến Sơn | 1987-01-21 04:30 male |
| Lương Ngọc Huỳnh | 1966-09-24 04:15 male |
| Đặng Thị Dung | 1982-05-22 09:30 female |
| Đoàn Quang Hưng | 1981-08-29 04:30 male |
| Vũ Thị Thanh Tuyền | 1984-07-13 21:01 female |
| Cao Xuân Trường | 1989-07-21 15:45 male |
| Lưu Hoàng Sơn | 1996-11-29 17:20 male |
| Phạm Thị Huyền | 1987-09-07 02:00 female |
| Lương Văn Mạnh | 1987-06-29 06:00 male |
| Ngô Đắc Dũng | 1985-09-18 08:00 male |

Machine JSON: `release/gate_01/G1_PREFINAL_CONTROL_CASES.json`.
