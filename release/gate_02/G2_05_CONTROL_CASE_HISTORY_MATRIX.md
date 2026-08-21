# G2-05 — Control-case History matrix

Probe: `python release/gate_02/_g2_05_history_probe.py` → `G2_05_HISTORY_PROBE.json`  
Result: **10/10 MATCH**, `mismatch_count: 0`

Each row is the stored snapshot at save time versus the live Analyze payload copied into History. Opening History must keep this fingerprint. Debug fingerprint (not customer-visible): `analysis_id` · Four Pillars · Strength · Pattern · Dụng · Luck.

| Case | ID | Pillars | Strength | Pattern | Điều hậu | Dụng | Hỷ | Luck | Stored vs save-time | Export name uses this identity |
|------|----|---------|----------|---------|----------|------|----|------|---------------------|--------------------------------|
| Nguyễn Tiến Sơn | g2-05-0 | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần | 0.87 strong | Chính Ấn | Hỏa | Hỏa · Đinh · Chính Quan | insufficient | Ất Tỵ | MATCH | `BTE_BaoCao_Nguyen_Tien_Son_19870121_V1.pdf` |
| Lương Ngọc Huỳnh | g2-05-1 | (stored blob) | 0.64 balanced | Chính Tài | Hỏa | Kim · Tân · Chính Tài | insufficient | (stored) | MATCH | `..._Luong_Ngoc_Huynh_19660924_V1.pdf` |
| Đặng Thị Dung | g2-05-2 | (stored blob) | 0.24 weak | Sát Ấn… | Thủy | Thủy · Nhâm · Chính Ấn | supported Mộc · Ất · Tỷ Kiên | (stored) | MATCH | `..._Dang_Thi_Dung_19820522_V1.pdf` |
| Đoàn Quang Hưng | g2-05-3 | (stored blob) | 0.61 balanced | Thực Thần | Hỏa | Thủy · Nhâm · Chính Tài | insufficient | (stored) | MATCH | `..._Doan_Quang_Hung_19810829_V1.pdf` |
| Vũ Thị Thanh Tuyền | g2-05-4 | Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi | 0.66 strong | Kiếp Tài | Thủy | Mộc · Ất · Chính Quan | insufficient | (stored) | MATCH | `..._Vu_Thi_Thanh_Tuyen_19840713_V1.pdf` |
| Cao Xuân Trường | g2-05-5 | (stored blob) | 0.34 weak | Quan Ấn… | Thủy | Kim · Tân · Chính Ấn | Thủy · Nhâm · Tỷ Kiên | (stored) | MATCH | `..._Cao_Xuan_Truong_19890721_V1.pdf` |
| Lưu Hoàng Sơn | g2-05-6 | (stored blob) | 0.51 balanced | Sát Ấn… | Hỏa climate ≠ Overall | Mộc · Ất · Chính Tài | insufficient | (stored) | MATCH | `..._Luu_Hoang_Son_19961129_V1.pdf` |
| Phạm Thị Huyền | g2-05-7 | (stored blob) | 0.74 strong | Thương Quan | Hỏa | Kim · Tân · Thực Thần | insufficient | (stored) | MATCH | `..._Pham_Thi_Huyen_19870907_V1.pdf` |
| Lương Văn Mạnh | g2-05-8 | (stored blob) | 1.00 strong | Giá Vượng LEVEL-1 override false | Thủy | Kim · Tân · Thực Thần | insufficient | (stored) | MATCH | `..._Luong_Van_Manh_19870629_V1.pdf` |
| Ngô Đắc Dũng | g2-05-9 | Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn | 1.00 strong | Giá Sắc LEVEL-1 override false | Hỏa / Cần ôn ấm | Thủy · Nhâm · Thực Thần | insufficient | (stored) | MATCH | `..._Ngo_Dac_Dung_19850918_V1.pdf` |

Customer Hỷ insufficient copy: `Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng`.

## Primary cross-case (Dũng = A, Tuyền = B)

| Step | Expected fingerprint |
|------|----------------------|
| Analyze Dũng | Current = Dũng |
| Analyze Tuyền | Current = Tuyền; History still has Dũng snapshot |
| Open History Dũng | Display Dũng; current id remains Tuyền |
| Report / PDF / DOCX / Print | Dũng identity and Dụng `Thủy · Nhâm · Thực Thần` |
| Refresh History Dũng | Still Dũng |
| Normal `/result` | Current Tuyền `Mộc · Ất · Chính Quan` |

No field mixing. Filename for History Dũng must not contain Tuyền.

## Secondary cross-case

Cao Xuân Trường vs Đặng Thị Dung: same isolation. Supported Hỷ on Dung must not appear on Trường History, and vice versa.
