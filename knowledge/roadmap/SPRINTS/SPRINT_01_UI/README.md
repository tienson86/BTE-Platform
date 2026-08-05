# BTE Platform V1.0

# Sprint 01 — Portal UI Foundation

---

## Document Information

| Item | Value |
|------|-------|
| Sprint | 01 |
| Name | Portal UI Foundation |
| Version | 1.0 |
| Status | READY |
| Priority | P0 (Highest) |
| Owner | Frontend Team |
| Reviewer | ChatGPT |
| Target Release | BTE Platform V1.0 |

---

# 1. Sprint Mission

Mục tiêu của Sprint 01 là xây dựng và hoàn thiện nền tảng giao diện Portal đạt chất lượng thương mại cho BTE Platform V1.0.

Sprint này chỉ tập trung vào giao diện người dùng (UI/UX).

Không thay đổi nghiệp vụ.

Không phát triển Engine.

Không phát triển Rule.

Không thay đổi Database.

Không mở rộng phạm vi ngoài kế hoạch Release.

---

# 2. Sprint Objectives

Hoàn thành:

- Design System
- Component Library
- Portal Layout
- Dashboard
- BaZi Result UI
- Responsive
- UI Polish

Sau Sprint này Portal phải có giao diện thống nhất, sẵn sàng kết nối với Engine.

---

# 3. Out of Scope

Các nội dung sau tuyệt đối không thực hiện trong Sprint này:

- Rule Engine
- Analysis Engine
- Calendar Engine
- Interpretation Engine
- Report Engine
- PDF
- Authentication Logic
- API Refactor
- Database Refactor
- AI
- Phong Thủy
- Xem ngày
- Sim phong thủy

Nếu phát hiện vấn đề liên quan các mục trên:

→ Ghi TODO.

→ Không tự sửa.

---

# 4. Sprint Structure

Sprint được chia thành các Work Package độc lập.

Chỉ được phép thực hiện tuần tự.

```
WP01
 ↓
Review
 ↓
PASS
 ↓
WP02
 ↓
Review
 ↓
PASS
 ↓
...
 ↓
WP12
```

Không được bỏ qua Work Package.

Không được làm song song nhiều Work Package.

---

# 5. Work Package List

| WP | Name | Status |
|----|------|--------|
| WP01 | Design System | READY |
| WP02 | Component Library | PENDING |
| WP03 | App Layout | PENDING |
| WP04 | Dashboard | PENDING |
| WP05 | BaZi Result Header | PENDING |
| WP06 | Four Pillars Card | PENDING |
| WP07 | Five Elements Card | PENDING |
| WP08 | Ten Gods Card | PENDING |
| WP09 | Strength Card | PENDING |
| WP10 | Responsive | PENDING |
| WP11 | UI Polish | PENDING |
| WP12 | Final Review | PENDING |

---

# 6. Execution Rules

Cursor phải tuân thủ toàn bộ các quy tắc sau.

## Được phép

- Chỉnh sửa đúng phạm vi Work Package hiện tại.
- Tạo file được yêu cầu trong Work Package.
- Cập nhật component liên quan trực tiếp.

---

## Không được phép

- Refactor ngoài phạm vi.
- Đổi kiến trúc.
- Đổi cấu trúc thư mục.
- Đổi tên module.
- Đổi API.
- Thêm dependency.
- Thêm package.
- Thêm framework.
- Tối ưu ngoài yêu cầu.
- Tự ý thêm tính năng.

---

# 7. Coding Rules

- TypeScript Strict.
- Không sử dụng `any`.
- Không duplicate component.
- Không duplicate CSS.
- Không hardcode màu.
- Không hardcode spacing.
- Không inline style nếu không thật sự cần.
- Reuse component tối đa.

---

# 8. Review Process

Sau mỗi Work Package:

1. Cursor hoàn thành.
2. Cursor tự kiểm tra.
3. Cursor gửi kết quả.
4. ChatGPT review.
5. Nếu FAIL:
   - sửa đúng lỗi
   - review lại
6. Nếu PASS:
   - Merge
   - mở Work Package tiếp theo

Không được chuyển sang WP tiếp theo nếu WP hiện tại chưa PASS.

---

# 9. Quality Gate

Mỗi Work Package phải vượt qua toàn bộ các tiêu chí sau:

- Build thành công.
- Không lỗi TypeScript.
- Không warning mới.
- Không phá vỡ giao diện hiện có.
- Responsive đúng.
- Không phát sinh bug chức năng.
- Đúng phạm vi Work Package.

Nếu thiếu bất kỳ tiêu chí nào:

→ Không được Merge.

---

# 10. Definition of Done

Sprint chỉ được đánh dấu **DONE** khi:

- Tất cả 12 Work Package đều PASS.
- Portal hiển thị đúng trên Desktop, Tablet và Mobile.
- Không còn lỗi TypeScript.
- Không còn lỗi Build.
- Component thống nhất.
- Responsive đạt yêu cầu.
- Review hoàn tất.
- Merge vào nhánh phát triển.

---

# 11. Sprint Deliverables

Sau khi Sprint hoàn thành, Portal phải có:

- Design System thống nhất.
- Component Library hoàn chỉnh.
- Layout chuẩn.
- Dashboard hoàn chỉnh.
- BaZi Result UI hoàn chỉnh.
- Responsive hoàn chỉnh.
- UI sẵn sàng kết nối Engine.

---

# 12. Notes

Sprint 01 là Sprint nền tảng.

Mọi Sprint sau đều kế thừa kết quả của Sprint này.

Không được thay đổi các quyết định kiến trúc của Sprint 01 nếu chưa được cập nhật trong Release Master Plan.