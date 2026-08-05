# BTE Platform V1.0

# Work Package 01 — Design System Foundation

---

## Document Information

| Item | Value |
|------|-------|
| Sprint | 01 |
| Work Package | WP01 |
| Name | Design System Foundation |
| Version | 1.0 |
| Status | READY |
| Priority | P0 |
| Estimated | 4–6 giờ |

---

# 1. Goal

Thiết lập Design System thống nhất cho toàn bộ Portal BTE Platform.

WP này **chỉ xây dựng nền tảng giao diện**, không chỉnh sửa các màn hình nghiệp vụ.

Kết quả của WP01 sẽ được sử dụng cho tất cả các Work Package tiếp theo.

---

# 2. Scope

## Được phép

- Theme
- Color Tokens
- Typography
- Spacing
- Border Radius
- Shadows
- Icon Size
- Breakpoints
- Motion Tokens
- Z-Index Scale

## Không được phép

- Chỉnh sửa page
- Chỉnh sửa layout
- Chỉnh sửa logic
- Thay đổi routing
- Thêm package
- Thay đổi API

---

# 3. Files Allowed

Cursor chỉ được chỉnh sửa trong các thư mục:

```
applications/portal/src/theme/
applications/portal/src/styles/
applications/portal/src/constants/
```

Nếu chưa tồn tại thì được phép tạo.

Không chỉnh sửa file ngoài phạm vi trên.

---

# 4. Deliverables

Sau WP01 phải có tối thiểu:

```
theme/
├── colors.ts
├── spacing.ts
├── typography.ts
├── radius.ts
├── shadows.ts
├── breakpoints.ts
├── motion.ts
├── zindex.ts
├── index.ts
```

---

# 5. Design Tokens

## Colors

- Primary
- Secondary
- Success
- Warning
- Error
- Info
- Background
- Surface
- Border
- Text

Mỗi màu phải có các mức:

- 50
- 100
- 200
- 300
- 400
- 500
- 600
- 700
- 800
- 900

Không hardcode màu trong component.

---

## Typography

Định nghĩa:

- Font Family
- Font Size
- Font Weight
- Line Height
- Letter Spacing

Bao gồm:

- Display
- H1
- H2
- H3
- H4
- Body Large
- Body
- Body Small
- Caption

---

## Spacing

Áp dụng hệ lưới 8px.

Ví dụ:

```
0
4
8
12
16
20
24
32
40
48
64
80
96
```

---

## Border Radius

```
0
4
8
12
16
20
24
9999
```

---

## Shadows

Định nghĩa:

- xs
- sm
- md
- lg
- xl

---

## Breakpoints

```
mobile

tablet

laptop

desktop

wide
```

---

## Motion

Định nghĩa:

- Fast
- Normal
- Slow

Transition thống nhất.

---

# 6. Coding Rules

- TypeScript Strict.
- Không dùng any.
- Export tập trung qua index.ts.
- Không duplicate token.
- Không hardcode.

---

# 7. Acceptance Criteria

WP được coi là PASS khi:

- Build thành công.
- Không lỗi TypeScript.
- Không warning mới.
- Token được tổ chức rõ ràng.
- Chưa làm thay đổi giao diện hiện tại.

---

# 8. Cursor Instructions

Cursor chỉ thực hiện đúng các nội dung trong tài liệu này.

Không chỉnh sửa ngoài phạm vi.

Nếu phát hiện vấn đề khác:

→ ghi TODO.

→ không tự sửa.