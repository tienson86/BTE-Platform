# BTE Platform

# S00 Blueprint — Context Header

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Screen:

BaZi Result

Depends On

- BTE_UI_BIBLE.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_GRID_SYSTEM.md
- PORTAL_SPACING_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_TYPOGRAPHY_SYSTEM.md
- PORTAL_DECISION_FLOW.md
- PORTAL_SCREEN_SPECIFICATIONS.md

---

# 1. Purpose

S00 là lớp xác nhận ngữ cảnh (Context Verification Layer).

Mục tiêu duy nhất:

Để người dùng biết rằng hệ thống đang hiển thị đúng hồ sơ và đúng phiên phân tích.

S00 không đưa ra bất kỳ kết luận Bát Tự nào.

---

# 2. Business Goal

Tăng niềm tin trước khi người dùng đọc kết quả.

Người dùng phải xác nhận:

- đúng người
- đúng lá số
- đúng thời gian sinh
- đúng phiên phân tích

trong vài giây đầu.

---

# 3. User Questions

S00 phải trả lời:

✓ Đây có phải hồ sơ của tôi không?

✓ Đây có đúng ngày giờ sinh không?

✓ Đây có phải kết quả mới nhất không?

✓ Tôi có đang xem đúng lần phân tích không?

Nếu người dùng còn nghi ngờ,

không nên tiếp tục đọc S01.

---

# 4. Decision Goal

Sau S00,

người dùng đưa ra đúng một quyết định:

```
Tiếp tục xem kết quả

hoặc

Quay lại chỉnh hồ sơ.
```

Không có quyết định nào khác.

---

# 5. Reading Goal

Thời gian mục tiêu:

≤ 3 giây.

Thứ tự đọc:

```
Avatar

↓

Tên

↓

Ngày giờ sinh

↓

Mã lá số

↓

Trạng thái

↓

Chi tiết hồ sơ
```

Không được chen thông tin phân tích.

---

# 6. Information Architecture

## Primary

- Tên hồ sơ
- Avatar (nếu có)
- Giới tính
- Ngày giờ sinh
- Địa điểm sinh (nếu hiển thị)

## Secondary

- Mã lá số
- Phiên bản phân tích
- Thời điểm phân tích
- Trạng thái

## Supporting

- Link "Chi tiết hồ sơ"
- Link "Phân tích lại"

---

# 7. Visual Hierarchy

Visual Priority:

```
Tên

↓

Ngày giờ sinh

↓

Trạng thái

↓

Mã lá số

↓

Metadata khác
```

Avatar chỉ hỗ trợ nhận diện.

Không được nổi bật hơn tên.

---

# 8. Layout Blueprint

Desktop

```
+-------------------------------------------------------------+

Avatar

Tên hồ sơ

Giới tính

Ngày giờ sinh

------------------------

Mã lá số

Trạng thái

Phiên bản

Thời điểm

[Chi tiết hồ sơ]

+-------------------------------------------------------------+
```

Tablet

```
Avatar

↓

Tên

↓

Thông tin

↓

Metadata

↓

Action
```

Mobile

```
Avatar

↓

Tên

↓

Ngày giờ sinh

↓

Metadata

↓

Action
```

Không chia nhiều hàng phức tạp.

---

# 9. Component Composition

Cho phép sử dụng:

- Avatar
- Badge
- Chip
- Label
- Link Button
- Divider

Không sử dụng:

- Card lớn
- Hero
- Chart
- Progress
- Alert (trừ lỗi hệ thống)

---

# 10. Data Mapping

| UI | Engine/API |
|-----|------------|
| Tên | Profile.Name |
| Avatar | Profile.Avatar |
| Giới tính | Profile.Gender |
| Ngày giờ sinh | Profile.BirthDateTime |
| Địa điểm sinh | Profile.BirthPlace |
| Mã lá số | Analysis.Code |
| Phiên bản | Analysis.Version |
| Thời điểm | Analysis.GeneratedAt |
| Trạng thái | Analysis.Status |

S00 không xử lý Business Logic.

---

# 11. Typography Rules

Tên hồ sơ

→ HeadingPrimary

Ngày giờ sinh

→ BodyPrimary

Metadata

→ Caption

Status

→ Label

Không có Display Typography.

Display dành cho S01.

---

# 12. Interaction Rules

Cho phép:

- Mở Chi tiết hồ sơ
- Phân tích lại
- Copy mã lá số (nếu có)

Không:

- Sửa trực tiếp dữ liệu
- Chỉnh ngày giờ sinh
- Thay đổi kết quả

---

# 13. Responsive Behaviour

Desktop

Một hàng.

Tablet

Hai tầng.

Mobile

Một cột.

Reading Flow phải giữ nguyên.

---

# 14. Accessibility

- Avatar có alt text.
- Status có text, không chỉ màu.
- Link có keyboard focus.
- Thứ tự tab đúng Reading Flow.
- Semantic Header.

---

# 15. Anti-Patterns

Không được:

❌ Đưa Nhật Chủ vào S00.

❌ Đưa Dụng Thần vào S00.

❌ Đưa Thập Thần vào S00.

❌ Đưa Hero vào S00.

❌ Đưa luận giải vào S00.

❌ Biến S00 thành Dashboard.

---

# 16. Screenshot Acceptance

Cursor phải cung cấp:

1. Desktop Full
2. Desktop Zoom (S00)
3. Tablet
4. Mobile

Không crop mất Header.

Không crop mất TOC.

---

# 17. Cursor Implementation Rules

Cursor phải triển khai đúng Blueprint.

Không được:

- thêm Card
- thêm Hero
- đổi Layout
- đổi Reading Flow
- tự ý thêm trường dữ liệu

Nếu dữ liệu chưa có,

dùng Placeholder theo đúng cấu trúc.

---

# 18. Product Owner Review Checklist

Business

□ Xác nhận đúng hồ sơ

Decision

□ Có thể quyết định tiếp tục hay quay lại

Reading

□ Đọc trong ≤3 giây

Hierarchy

□ Không cạnh tranh với S01

Layout

□ Gọn

Responsive

□ Desktop
□ Tablet
□ Mobile

---

# 19. Quality Scorecard

| Tiêu chí | Điểm |
|----------|------:|
| Business Goal | 20 |
| Reading Flow | 20 |
| Information Hierarchy | 20 |
| Responsive | 20 |
| Blueprint Compliance | 20 |

Kết quả:

95–100 → PASS

80–94 → PASS WITH CHANGES

<80 → REJECT

---

# 20. Relationship

S00 là đầu vào của:

S01 Identity & Decision Panel.

Nếu S00 không được xác nhận,

Decision Flow không nên tiếp tục.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial S00 Context Header Blueprint |

bổ sung thêm 3 phụ lục cho riêng S00
Đây là điểm mình nghĩ sẽ giúp Cursor gần như không thể hiểu sai.

Appendix A – S00 Information Priority

Xếp hạng mức độ ưu tiên hiển thị:
Thành phần	Priority
Tên hồ sơ	10
Ngày giờ sinh	9
Trạng thái	8
Mã lá số	6
Phiên bản	4
Thời điểm phân tích	3


=> Cursor sẽ biết chữ nào phải nổi hơn.

Appendix B – S00 Wireframe (ASCII)

Một wireframe chi tiết hơn với vị trí từng thành phần, ví dụ:
┌─────────────────────────────────────────────────────────────┐
│ Avatar │ Hồ sơ: Nguyễn Văn A                  [Đã phân tích] │
│        │ Nam • 21/01/1987 • 04:15 • Hà Tây                 │
│        │ Mã: BTE-2026-000123                               │
│        │ Phân tích: 05/08/2026 21:30 • v1.0                │
│        │ [Chi tiết hồ sơ] [Phân tích lại]                  │
└─────────────────────────────────────────────────────────────┘
Appendix C – S00 Review Questions

Khi review screenshot, Product Owner chỉ cần trả lời:
Tôi có biết ngay mình đang xem hồ sơ nào không?
Tôi có biết ngay đây có đúng ngày giờ sinh không?
Tôi có biết đây là kết quả nào không?
Tôi có bị phân tán bởi thông tin phân tích không?
Nếu có bất kỳ câu trả lời nào là "Không", thì S00 phải được chỉnh sửa trước khi chuyển sang S01.