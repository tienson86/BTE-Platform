# G2-06 — Analysis ID trace

Expected: one coherent identity per Analyze: `request_id` = `data.analysis_id` = Report `case_id` = export filename stem.

Source: `release/gate_02/G2_06_E2E_PROBE.json`

## Primary four

| Case | request_id | data.analysis_id | Report case_id | PDF | DOCX | Coherent |
|------|------------|------------------|----------------|-----|------|----------|
| Nguyễn Tiến Sơn | g2-06-0 | g2-06-0 | g2-06-0 | BTE_BaoCao_Nguyen_Tien_Son_19870121_V1.pdf | BTE_BaoCao_Nguyen_Tien_Son_19870121_V1.docx | yes |
| Vũ Thị Thanh Tuyền | g2-06-4 | g2-06-4 | g2-06-4 | BTE_BaoCao_Vu_Thi_Thanh_Tuyen_19840713_V1.pdf | BTE_BaoCao_Vu_Thi_Thanh_Tuyen_19840713_V1.docx | yes |
| Ngô Đắc Dũng | g2-06-9 | g2-06-9 | g2-06-9 | BTE_BaoCao_Ngo_Dac_Dung_19850918_V1.pdf | BTE_BaoCao_Ngo_Dac_Dung_19850918_V1.docx | yes |
| Cao Xuân Trường | g2-06-5 | g2-06-5 | g2-06-5 | BTE_BaoCao_Cao_Xuan_Truong_19890721_V1.pdf | BTE_BaoCao_Cao_Xuan_Truong_19890721_V1.docx | yes |

## Cross-case / re-analyze

| Role | ID | Notes |
|------|----|-------|
| Current after Tuyền Analyze | g2-06-4 | Current B |
| History Dũng snapshot | g2-06-9 | History A, immutable |
| History export files | Ngo_Dac_Dung 19850918 | Not Tuyen |
| Re-analyze Dũng | g2-06-reanalyze-dung | New C; A still g2-06-9 |

## Ten-control API identities

Each of the ten G1-FINAL cases received `X-Request-ID: g2-06-{index}` and returned the same value on `request_id` and `data.analysis_id`. Full list is in the probe JSON `ten[]` rows.

ResultStore current ID in the live portal is this same stamped `analysis_id` after `saveLastResult`. History row id is that declared id (G2-05).
