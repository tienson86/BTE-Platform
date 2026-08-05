# BTE Platform

# Responsive Pattern — Touch Interaction

---

Version

1.0.0

Status

ACTIVE

Module

04_RESPONSIVE_PATTERNS

Document

05_TOUCH_INTERACTION

Owner

Product Owner

---

# 1. Purpose

Tài liệu này định nghĩa toàn bộ quy tắc tương tác của người dùng trên các thiết bị.

Interaction bao gồm:

- Mouse
- Keyboard
- Touch
- Gesture

Interaction không thay đổi:

- Business Logic
- Information Hierarchy
- Decision Flow

Interaction chỉ thay đổi cách người dùng thao tác.

---

# 2. Design Philosophy

Interaction phải:

- đơn giản
- dễ đoán
- nhất quán

Người dùng không cần học lại cách thao tác khi đổi thiết bị.

Desktop

↓

Tablet

↓

Mobile

chỉ thay đổi phương thức nhập.

Không thay đổi hành vi nghiệp vụ.

---

# 3. Input Model

Desktop

- Mouse
- Keyboard

Tablet

- Touch

Mobile

- Touch

BTE không xây dựng UI phụ thuộc vào Hover.

---

# 4. Pointer Behaviour

Desktop

Hover được phép.

Tablet

Không sử dụng Hover.

Mobile

Không sử dụng Hover.

Mọi chức năng quan trọng phải truy cập được bằng Tap.

---

# 5. Click & Tap Rules

Desktop

Single Click.

Tablet

Single Tap.

Mobile

Single Tap.

Không yêu cầu Double Click.

Không yêu cầu Double Tap.

---

# 6. Touch Target

Kích thước tối thiểu:

44 × 44 px.

Áp dụng cho:

- Button
- Chip
- Badge tương tác
- Menu
- Drawer
- CTA

Không ngoại lệ.

---

# 7. Gesture Rules

Cho phép:

- Scroll
- Swipe (nếu có)
- Pull to Refresh (nếu có)

Không bắt buộc:

- Pinch
- Rotate
- Multi-touch

Gesture chỉ dùng khi mang lại giá trị rõ ràng.

---

# 8. Keyboard Interaction

Desktop bắt buộc hỗ trợ:

- Tab
- Shift + Tab
- Enter
- Space
- ESC

Không có thành phần nào chỉ dùng được bằng chuột.

---

# 9. Focus Management

Focus phải:

- luôn nhìn thấy
- đúng thứ tự
- không bị mất khi mở Drawer hoặc Dialog

Khi đóng Drawer:

Focus phải quay lại phần tử đã mở Drawer.

---

# 10. Tooltip Behaviour

Desktop

Hover hoặc Focus.

Tablet

Tap.

Mobile

Tap.

Tooltip không được phụ thuộc vào Hover.

---

# 11. Drawer Interaction

Desktop

- Click mở
- ESC đóng
- Click ngoài để đóng (nếu phù hợp)

Tablet

Tap mở.

Mobile

Tap mở.

Vuốt xuống để đóng chỉ là hành vi bổ sung, không bắt buộc.

---

# 12. Accordion Interaction

Desktop

Click.

Tablet

Tap.

Mobile

Tap.

Một thao tác duy nhất để mở hoặc đóng.

---

# 13. Action Bar Interaction

Desktop

Hiển thị đầy đủ.

Tablet

Overflow khi cần.

Mobile

Primary Action luôn hiển thị.

Secondary Action đưa vào Overflow.

---

# 14. Navigation Interaction

Desktop

Sidebar + TOC.

Tablet

Collapsed TOC.

Mobile

Drawer.

Navigation phải luôn truy cập được trong tối đa hai thao tác.

---

# 15. Scroll Behaviour

Cho phép:

- Vertical Scroll

Không khuyến khích:

- Horizontal Scroll

Ngoại lệ:

- Bảng dữ liệu lớn
- Biểu đồ đặc biệt

Portal không được phụ thuộc vào cuộn ngang.

---

# 16. Feedback Rules

Mọi thao tác phải có phản hồi.

Ví dụ:

- Hover (Desktop)
- Focus
- Pressed
- Loading
- Success
- Error

Người dùng không được đoán hệ thống đã nhận thao tác hay chưa.

---

# 17. Anti-Patterns

Không:

❌ Double Click.

❌ Hover bắt buộc.

❌ Touch Target nhỏ.

❌ Gesture bí mật.

❌ Swipe để truy cập chức năng quan trọng.

❌ Horizontal Scroll cho nội dung chính.

---

# 18. Cursor Rules

Cursor không được:

- tạo Gesture mới.
- dùng Hover cho chức năng bắt buộc.
- tạo Touch Target nhỏ hơn chuẩn.
- thay đổi thứ tự Focus.

Nếu Interaction chưa có Pattern:

STOP.

Không suy luận.

---

# 19. Product Owner Checklist

□ Tap dễ.

□ Click đúng.

□ Focus rõ.

□ Keyboard đầy đủ.

□ Drawer đúng.

□ Tooltip đúng.

□ Navigation đúng.

□ Touch Target đạt chuẩn.

---

# 20. Definition of Done

Touch Interaction hoàn thành khi:

✓ Desktop thao tác đầy đủ.

✓ Tablet thao tác thuận tiện.

✓ Mobile thao tác bằng một tay.

✓ Keyboard hoạt động.

✓ Accessibility đạt yêu cầu.

✓ Không phụ thuộc Hover.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Touch Interaction Pattern |

---

# Appendix A — Interaction Matrix

| Interaction | Desktop | Tablet | Mobile |
|-------------|----------|---------|---------|
| Hover | ✓ | ✗ | ✗ |
| Click | ✓ | ✗ | ✗ |
| Tap | ✗ | ✓ | ✓ |
| Keyboard | ✓ | Limited | Limited |
| Swipe | ✗ | Optional | Optional |

---

# Appendix B — Input Priority

Desktop

Mouse

↓

Keyboard

Tablet

Touch

↓

Keyboard (nếu có)

Mobile

Touch

↓

Keyboard (nếu có)

---

# Appendix C — Touch Target Matrix

| Component | Minimum Target |
|------------|---------------:|
| Button | 44×44 px |
| Chip | 44×44 px |
| Badge (interactive) | 44×44 px |
| Menu Item | 44×44 px |
| Drawer Action | 44×44 px |
| Action Bar | 44×44 px |

---

# Appendix D — Common Mistakes

- Chỉ hoạt động khi Hover.
- Double Click mới kích hoạt.
- Focus bị mất khi đóng Drawer.
- Touch Target quá nhỏ.
- Swipe bắt buộc cho thao tác chính.

---

# Appendix E — Interaction Principles

Interaction của BTE phải tuân thủ 5 nguyên tắc:

1. Một thao tác cho một hành động.
2. Không phụ thuộc vào Hover.
3. Mọi chức năng đều truy cập được bằng bàn phím khi phù hợp.
4. Touch là ưu tiên trên thiết bị cảm ứng.
5. Người dùng luôn nhận được phản hồi sau khi tương tác.

Mục tiêu cuối cùng là:

**Tương tác tự nhiên – Dễ học – Dễ nhớ – Không cần hướng dẫn.**