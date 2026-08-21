# G2-04 — Control-case export matrix

Probe: `python release/gate_02/_g2_04_export_probe.py`  
Oracle: Gate-1 frozen fingerprint (`COMPARE_KEYS`) vs live orchestrator payload vs `PresentedReportV1`.

`mismatch_count`: **0**. Analytical diffs: **0**. Model parity: **10/10**.

Full PDF/DOCX rendered for Dũng, Tuyền, Trường, Đặng Thị Dung (long narrative). Other six cases: presentation model only.

| Case | analysis_id (probe) | Four Pillars / Strength / Pattern | Dụng | Reason | Hỷ | Kỵ | Điều hậu | Luck | Export |
|------|---------------------|-------------------------------------|------|--------|----|----|----------|------|--------|
| Sơn | g2-04-probe-0 | MATCH · 0.87 strong · Chính Ấn | Hỏa · Đinh · Chính Quan | yes | insufficient | frozen | Hỏa separate | cycles present | model |
| Huỳnh | g2-04-probe-1 | MATCH · 0.64 balanced · Chính Tài | Kim · Tân · Chính Tài | yes | insufficient | frozen | Hỏa separate | cycles present | model |
| Dung | g2-04-probe-2 | MATCH · 0.24 weak · Sát Ấn… | Thủy · Nhâm · Chính Ấn | yes | Mộc · Ất · Tỷ Kiên | frozen | Thủy separate | cycles present | PDF+DOCX |
| Hưng | g2-04-probe-3 | MATCH · 0.61 balanced · Thực Thần | Thủy · Nhâm · Chính Tài | yes | insufficient | frozen | Hỏa separate | cycles present | model |
| Tuyền | g2-04-probe-4 | MATCH · 0.66 strong · Kiếp Tài | Mộc · Ất · Chính Quan | yes | insufficient | frozen | Thủy separate | cycles present | PDF+DOCX |
| Trường | g2-04-probe-5 | MATCH · 0.34 weak · Quan Ấn… | Kim · Tân · Chính Ấn | yes | Thủy · Nhâm · Tỷ Kiên | frozen | Thủy separate | cycles present | PDF+DOCX |
| Lưu Hoàng Sơn | g2-04-probe-6 | MATCH · 0.51 balanced · Sát Ấn… | Mộc · Ất · Chính Tài | yes | insufficient | frozen | Hỏa separate | cycles present | model |
| Huyền | g2-04-probe-7 | MATCH · 0.74 strong · Thương Quan | Kim · Tân · Thực Thần | yes | insufficient | frozen | Hỏa separate | cycles present | model |
| Mạnh | g2-04-probe-8 | MATCH · 1.00 strong · LEVEL-1 jia_wang override false | Kim · Tân · Thực Thần | yes | insufficient | frozen | Thủy separate | cycles present | model |
| Dũng | g2-04-probe-9 | MATCH · 1.00 strong · LEVEL-1 gia_sac override false | Thủy · Nhâm · Thực Thần | yes | insufficient | frozen | Hỏa / Cần ôn ấm separate | cycles present | PDF+DOCX |

Customer insufficient Hỷ copy (all insufficient cases):

`Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng`

Forbidden strings not used as Overall:

- Dũng: no old Hỷ Nhâm/Quý, no Thổ/Mậu special winner, no climate merged into Overall
- Tuyền: no Tòng Tài, no cực nhược
- Trường: no cực nhược unless frozen truth contains it (it does not)

Cân Xương is not in the V1.0 production pipeline (G2-02) and was not added as a new analytical section.
