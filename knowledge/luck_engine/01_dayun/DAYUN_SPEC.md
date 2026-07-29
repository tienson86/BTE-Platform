# Dayun Specification

> Version: 1.0
>
> Status: Draft
>
> Module: Luck Engine
>
> Document: Business Specification
>
> Location:
>
> knowledge/luck_engine/01_dayun/DAYUN_SPEC.md

---

# 1. Mục đích

Tài liệu này định nghĩa toàn bộ đặc tả nghiệp vụ (Business Specification) của Đại vận trong BTE Platform.

Đây là tài liệu chuẩn để tất cả các thành phần của hệ thống triển khai thống nhất.

Tài liệu này không mô tả mã nguồn và không chứa thuật toán chi tiết.

---

# 2. Phạm vi

Đặc tả bao gồm:

- Khái niệm Đại vận
- Điều kiện hình thành Đại vận
- Đầu vào
- Đầu ra
- Chu kỳ Đại vận
- Quy tắc xác định chiều vận
- Quy tắc xác định tuổi khởi vận
- Quy tắc sinh các trụ Đại vận
- Runtime Contract
- Validation Rules
- Business Rules
- Dependency Rules

Không bao gồm:

- Thuật toán chi tiết
- Mã nguồn
- Luận giải
- Chấm điểm
- Lưu niên
- Lưu nguyệt
- Lưu nhật
- Lưu thời

---

# 3. Định nghĩa

## 3.1 Đại vận

Đại vận là chu kỳ vận hạn kéo dài 10 năm, được xác định dựa trên:

- Giới tính
- Âm Dương của Thiên Can năm sinh
- Thời điểm sinh
- Tiết khí
- Quy tắc khởi vận

Đại vận phản ánh sự biến đổi dài hạn của khí vận sau khi con người được sinh ra.

---

## 3.2 Chu kỳ

Một Đại vận luôn có:

- Thời gian: 10 năm
- Một Thiên Can
- Một Địa Chi
- Một tập Tàng Can
- Quan hệ với Mệnh cục

---

## 3.3 Khởi vận

Khởi vận là thời điểm bắt đầu bước vào Đại vận đầu tiên.

Tuổi khởi vận được xác định theo quy tắc riêng của hệ thống.

Thuật toán chi tiết được mô tả trong:

DAYUN_ALGORITHM.md

---

# 4. Mục tiêu nghiệp vụ

Dayun Module phải cung cấp khả năng:

- Xác định chiều Đại vận
- Xác định tuổi khởi vận
- Sinh danh sách Đại vận
- Sinh thông tin từng Đại vận
- Cung cấp dữ liệu Runtime chuẩn hóa

Module không đánh giá cát hung.

---

# 5. Đầu vào (Input Contract)

Dayun Module sử dụng các dữ liệu sau:

## Calendar Context

- Dương lịch
- Âm lịch
- Tiết khí
- Can Chi
- Múi giờ

---

## Bazi Context

- Năm
- Tháng
- Ngày
- Giờ

- Thiên Can
- Địa Chi

---

## Pattern Context

Chỉ sử dụng Metadata khi cần.

Không được thay đổi.

---

## Rule Context

Chỉ đọc.

Không sửa.

---

# 6. Đầu ra (Output Contract)

Output duy nhất là:

DayunRuntimeCollection

Collection bao gồm nhiều DayunRuntime.

Mỗi DayunRuntime đại diện đúng một chu kỳ Đại vận.

---

# 7. Thuộc tính của DayunRuntime

Mỗi DayunRuntime phải có tối thiểu:

## Identity

- Index
- Sequence
- UUID

---

## Time

- Start Age
- End Age
- Start Year
- End Year

---

## Heavenly Layer

- Heavenly Stem
- Yin Yang
- Five Element

---

## Earth Layer

- Earthly Branch
- Hidden Stems
- Five Element

---

## Relationship

- Ten God
- Relation Metadata

---

## Runtime Metadata

- Provider
- Version
- Confidence
- Source

---

# 8. Chu kỳ Đại vận

Mỗi Đại vận có thời lượng:

10 năm

Chu kỳ phải liên tục.

Không được chồng lấn.

Không được tạo khoảng trống giữa hai Đại vận liên tiếp.

---

# 9. Quy tắc chiều vận

Dayun Module phải xác định:

- Thuận hành
- Nghịch hành

Việc xác định chiều vận phụ thuộc vào:

- Giới tính
- Âm Dương Thiên Can năm sinh

Quy tắc chi tiết được mô tả trong:

DAYUN_ALGORITHM.md

---

# 10. Quy tắc khởi vận

Module phải xác định:

- Tuổi khởi vận
- Năm bắt đầu
- Năm kết thúc

Quy tắc tính toán chi tiết được mô tả trong:

DAYUN_ALGORITHM.md

---

# 11. Quy tắc sinh Đại vận

Sau khi xác định:

- Chiều vận
- Tuổi khởi vận

Hệ thống phải sinh tuần tự các trụ Đại vận.

Mỗi trụ phải:

- Đúng thứ tự
- Không trùng lặp
- Không bỏ sót

---

# 12. Runtime Contract

DayunRuntime phải:

- Immutable
- Serializable
- Versioned
- Typed
- Testable

Không chứa:

- Business Logic
- Thuật toán
- Rule Matching
- Luận giải

---

# 13. Validation Rules

Mỗi DayunRuntime phải kiểm tra:

- Đủ dữ liệu
- Can hợp lệ
- Chi hợp lệ
- Tuổi hợp lệ
- Năm hợp lệ
- Không trùng Sequence
- Không trùng UUID

Nếu phát hiện lỗi:

Trả về ValidationResult.

Không làm hỏng toàn bộ Pipeline.

---

# 14. Business Rules

Dayun Module phải đảm bảo:

✓ Mỗi Đại vận kéo dài đúng 10 năm.

✓ Các Đại vận liên tục theo thời gian.

✓ Mỗi Đại vận có đúng một Can và một Chi.

✓ Mỗi Đại vận có Metadata đầy đủ.

✓ Runtime bất biến sau khi tạo.

---

# 15. Dependency Rules

Dayun Module phụ thuộc:

- Calendar Engine
- BaZi Engine

Không phụ thuộc:

- Interpretation Engine
- Report Engine
- UI
- Database
- API

---

# 16. Error Handling

Áp dụng nguyên tắc Fail Soft.

Nếu không thể sinh một Đại vận:

- Ghi Warning.
- Trả về ValidationResult.
- Không làm dừng Luck Engine.

---

# 17. Versioning

Mọi thay đổi về quy tắc nghiệp vụ phải:

- Tăng Version.
- Cập nhật CHANGELOG.md.
- Cập nhật TEST_CASES.
- Cập nhật ALGORITHM nếu cần.

---

# 18. Architecture Compliance

Dayun Module phải tuân thủ:

- Luck Engine Architecture
- Runtime Contract
- Immutable Contract
- Specification First
- Test First

Không được triển khai mã nguồn trái với tài liệu này.

---

# 19. Tài liệu liên quan

- README.md
- ARCHITECTURE.md
- DAYUN_ALGORITHM.md
- DAYUN_EDGE_CASES.md
- DAYUN_TEST_CASES.md
- CHANGELOG.md