# G2-01 — Control-case binding matrix

**Method:** live `OrchestratorService.analyze` vs `G1_PREFINAL_CONTROL_CASES.json`.  
**Date:** 2026-08-20. **Mismatch count: 0.**  
**Contract:** `analysis_result.UsefulGodView@1.5`

Presentation columns are **copy rules** (`useful_display`, `favorable_display`) — adapters do not recompute engines. `/result` and Full Report share the same stored `data` blob after Analyze.

Customer Hỷ ≠ internal `canonical_favorable_display` / `favorable_gods` on all ten cases.

| Case | Frozen vs API | Four Pillars | Strength | Pattern / override | Điều hậu | Overall Dụng | Archetype | Customer Hỷ | Kỵ | Luck |
|------|---------------|--------------|----------|--------------------|----------|--------------|-----------|-------------|-----|------|
| Nguyễn Tiến Sơn | MATCH | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần | 0.87 strong | Chính Ấn / false | Hỏa · Bính · Thất Sát | Hỏa · Đinh · Chính Quan | CHẾ | insufficient | Canh Tỷ / Tân Kiếp | Ất Tỵ 35–44 |
| Lương Ngọc Huỳnh | MATCH | Bính Ngọ / Đinh Dậu / Bính Tuất / Canh Dần | 0.64 balanced | Chính Tài / false | Hỏa · Đinh · Kiếp Tài | Kim · Tân · Chính Tài | BALANCED-WEALTH | insufficient | Đinh Kiếp | Quý Mão 55–64 |
| Đặng Thị Dung | MATCH | Nhâm Tuất / Ất Tỵ / Ất Tỵ / Tân Tỵ | 0.24 weak | Sát Ấn… / false | Thủy · Nhâm · Chính Ấn | Thủy · Nhâm · Chính Ấn | SINH / TRỢ | Mộc · Ất · Tỷ Kiên | Mậu/Kỷ Tài | Tân Sửu 36–45 |
| Đoàn Quang Hưng | MATCH | Tân Dậu / Đinh Dậu / Kỷ Mão / Bính Dần | 0.61 balanced | Thực Thần / false | Hỏa · Đinh · Thiên Ấn | Thủy · Nhâm · Chính Tài | BALANCED-WEALTH | insufficient | Mậu Kiếp | Quý Tỵ 37–46 |
| Vũ Thị Thanh Tuyền | MATCH | Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi | 0.66 strong | Kiếp Tài / false | Thủy · Nhâm · Thiên Tài | Mộc · Ất · Chính Quan | CHẾ | insufficient | Mậu Tỷ / Kỷ Kiếp | Bính Dần 42–51 |
| Cao Xuân Trường | MATCH | Kỷ Tỵ / Tân Mùi / Nhâm Ngọ / Mậu Thân | 0.34 weak | Quan Ấn… / false | Thủy · Nhâm · Tỷ Kiên | Kim · Tân · Chính Ấn | SINH / TRỢ | Thủy · Nhâm · Tỷ Kiên | Đinh/Bính Tài | Đinh Mão 35–44 |
| Lưu Hoàng Sơn | MATCH | Bính Tý / Kỷ Hợi / Canh Ngọ / Ất Dậu | 0.51 balanced | Sát Ấn… / false | Hỏa · Bính · Thất Sát | Mộc · Ất · Chính Tài | BALANCED-WEALTH | insufficient | Tân Kiếp | Nhâm Dần 23–32 |
| Phạm Thị Huyền | MATCH | Đinh Mão / Mậu Thân / Kỷ Mùi / Ất Sửu | 0.74 strong | Thương Quan / false | Hỏa · Đinh · Thiên Ấn | Kim · Tân · Thực Thần | TIẾT | insufficient | Kỷ Tỷ / Mậu Kiếp | Tân Hợi 30–39 |
| Lương Văn Mạnh | MATCH | Đinh Mão / Đinh Mùi / Kỷ Dậu / Đinh Mão | 1.00 strong | LEVEL-1 `jia_wang` / **false** | Thủy · Nhâm · Chính Tài | Kim · Tân · Thực Thần | TIẾT | insufficient | Kỷ Tỷ / Mậu Kiếp | Quý Mão 38–47 |
| Ngô Đắc Dũng | MATCH | Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn | 1.00 strong | LEVEL-1 `gia_sac` / **false** | Hỏa · Đinh · Chính Quan | Thủy · Nhâm · Thực Thần | TIẾT | insufficient | Canh Tỷ / Tân Kiếp | Tân Tỵ 34–43 |

`analysis_id` inside API `data`: **null** on all ten (identity is ResultStore-synthetic after save).

Machine dump: `release/gate_02/G2_01_BINDING_PROBE.json`.
