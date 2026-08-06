# BTE Platform

# BAGUA_HAUTHIEN SVG ASSET

# BAGUA_ASSET_SPEC.md

---

Version

1.0.0

Status

CANONICAL

Asset

Bagua_HauThien.svg

Module

Desktop Canonical UI

Section

S09 – Cung Phi / Quái Mệnh & Nhóm Trạch

Owner

BTE Platform

---

# 1. Mục đích

Tài liệu này định nghĩa tiêu chuẩn kỹ thuật và quy tắc sử dụng của tài nguyên đồ họa:

```
Bagua_HauThien.svg
```

Đây là tài sản đồ họa (Graphic Asset) dùng để hiển thị Hậu Thiên Bát Quái trong Desktop Canonical UI.

Asset này không chứa dữ liệu người dùng.

Thông tin như:

- Cung mệnh
- Ngũ hành
- Số quái

sẽ được hiển thị động bởi giao diện.

---

# 2. Phạm vi

Trong phiên bản Desktop Canonical V1, asset này chỉ được sử dụng cho:

- S09 – Cung Phi / Quái Mệnh & Nhóm Trạch

Các mục đích sử dụng khác sẽ được xem xét ở các phiên bản sau.

---

# 3. Thành phần Asset

Asset gồm:

- Vòng bát giác ngoài.
- Tám cung Hậu Thiên.
- Tên quẻ.
- Phương vị.
- Hào âm dương.
- Vùng trung tâm để hiển thị dữ liệu động.

Không chứa:

- Dữ liệu người dùng.
- Văn bản động.
- Logic nghiệp vụ.

---

# 4. Hệ Bát Quái

Asset sử dụng:

```
HẬU THIÊN BÁT QUÁI
(Văn Vương)
```

Không sử dụng Tiên Thiên Bát Quái.

---

# 5. Thứ tự các quẻ

Theo chiều kim đồng hồ:

| Phương vị | Quẻ |
|-----------|------|
| Bắc | Khảm |
| Đông Bắc | Cấn |
| Đông | Chấn |
| Đông Nam | Tốn |
| Nam | Ly |
| Tây Nam | Khôn |
| Tây | Đoài |
| Tây Bắc | Càn |

Đây là thứ tự chuẩn và không được thay đổi.

---

# 6. Chính tả

Tên quẻ phải hiển thị đúng:

- KHẢM
- CẤN
- CHẤN
- TỐN
- LY
- KHÔN
- ĐOÀI
- CÀN

Tên phương vị:

- BẮC
- ĐÔNG BẮC
- ĐÔNG
- ĐÔNG NAM
- NAM
- TÂY NAM
- TÂY
- TÂY BẮC

Không sử dụng cách viết khác.

---

# 7. Hào âm dương

Mỗi quẻ phải hiển thị đúng hào âm dương theo Hậu Thiên Bát Quái.

Không được thay đổi hình thức biểu diễn.

---

# 8. Vùng trung tâm

Trung tâm Asset là vùng dành cho giao diện hiển thị dữ liệu động.

Ví dụ:

```
Ly Hỏa

9
```

Asset không chứa sẵn các giá trị này.

---

# 9. Định dạng

Định dạng chuẩn:

```
SVG
```

Preview:

```
PNG
```

Không sử dụng ảnh raster trong giao diện chính.

---

# 10. Quy định sử dụng

Frontend chỉ được:

- Hiển thị Asset.
- Hiển thị dữ liệu động tại vùng trung tâm.

Không được:

- Thay đổi vị trí các quẻ.
- Thay đổi phương vị.
- Thay đổi hào âm dương.
- Tự vẽ lại bát quái.

---

# 11. Kiểm tra

Một Asset được coi là đạt khi:

✓ Đúng Hậu Thiên Bát Quái.

✓ Đúng thứ tự tám quẻ.

✓ Đúng phương vị.

✓ Đúng chính tả.

✓ Hiển thị sắc nét.

✓ Là SVG.

---

# 12. Freeze Policy

Asset này thuộc Desktop Canonical UI V1.

Mọi thay đổi về:

- Hình học.
- Thứ tự quẻ.
- Phương vị.
- Hào âm dương.

đều phải được Product Owner phê duyệt trước khi cập nhật.

---

# 13. Design Decision Record

Trong Desktop Canonical UI V1, Bát Quái được chuẩn hóa thành một Graphic Asset độc lập nhằm đảm bảo:

- Tính chính xác học thuật.
- Tính nhất quán giao diện.
- Khả năng tái sử dụng.
- Dễ bảo trì.

Các khả năng mở rộng hoặc tái cấu trúc asset sẽ được xem xét ở các phiên bản sau và không thuộc phạm vi của tài liệu này.

---

# 14. Single Source of Truth

BAGUA_ASSET_SPEC.md là tài liệu chuẩn mô tả Asset:

```
Bagua_HauThien.svg
```

Mọi triển khai trong Desktop Canonical UI V1 phải tuân thủ tài liệu này.

Nếu có khác biệt giữa Asset và tài liệu thì:

**BAGUA_ASSET_SPEC.md là Single Source of Truth cho Bagua_HauThien.svg.**