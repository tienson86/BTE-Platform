# G2-05 — Visual acceptance

Date: 2026-08-21. Captures: `release/gate_02/screenshots/g2_05/`

Live tree HTML from Portal render + PNG of those trees.

| File | Expected | Result |
|------|----------|--------|
| `history_list.html` / `.png` | History index distinguishes Tuyền and Dũng by name and birth | **PASS** |
| `history_dung.html` / `.png` | Explicit History Dũng; banner “Đang xem kết quả đã lưu…”; Dụng Thủy · Nhâm · Thực Thần; no Tuyền Dụng | **PASS** |
| `current_tuyen.html` / `.png` | After exiting History, current Tuyền; no History banner; Dụng Mộc · Ất · Chính Quan | **PASS** |
| `old_version.html` / `.png` | Version gate; “Kết quả này được tạo bởi phiên bản dữ liệu cũ…”; no stale Dụng card | **PASS** |
| `missing_record.html` / `.png` | “Không tìm thấy hồ sơ.”; not current Tuyền; CTA Về lịch sử | **PASS** |

## Banner coherence

| State | History banner | Version gate | Missing gate |
|-------|----------------|--------------|--------------|
| Current Tuyền | No | No | No |
| History Dũng ready | Yes | No | No |
| Old/unversioned History | No | Yes | No |
| Missing History id | No | No | Yes |

## Timestamp display

History list shows analysis `created_at` via `toLocaleString("vi-VN")`. That is presentation of creation time, not last viewed / last export. Birth timezone fields are not rewritten.

## Export from History (visual/action)

On History Dũng, **Xem báo cáo** is `/reports?from=history&id=id-dung`. **Tải PDF** / **Tải DOCX** send `source=history` and Dũng payload. **In** prints the History Result view.
