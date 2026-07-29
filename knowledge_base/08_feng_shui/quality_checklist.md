# Quality Checklist
## Module: knowledge_base/08_feng_shui/01_gua

Version: 1.0

---

# Mục đích

Checklist này được sử dụng để kiểm tra chất lượng của mọi file JSON trong module:

knowledge_base/08_feng_shui/01_gua/

Một file chỉ được chấp nhận khi vượt qua **100%** các mục kiểm tra dưới đây.

---

# PHẦN A — Kiểm tra cấu trúc

## A1. Tên file

☐ Đúng quy ước đặt tên.

☐ Viết thường.

☐ Không có khoảng trắng.

☐ Đúng vị trí thư mục.

Ví dụ:

- kham.json
- ly.json
- chan.json

---

## A2. JSON

☐ JSON hợp lệ.

☐ Không lỗi dấu ngoặc.

☐ Không lỗi dấu phẩy.

☐ UTF-8.

☐ Không có comment.

---

## A3. Schema

☐ Đúng schema.json.

☐ Không thiếu field.

☐ Không thừa field.

☐ Đúng kiểu dữ liệu.

☐ Đúng thứ tự field.

---

# PHẦN B — Kiểm tra Metadata

☐ id đúng.

☐ name đúng.

☐ number đúng.

☐ group đúng.

☐ element đúng.

☐ direction đúng.

☐ aliases không rỗng.

☐ keywords không rỗng.

---

# PHẦN C — Kiểm tra nội dung

## overview

☐ Có đúng 5 đoạn.

☐ Giới thiệu đúng quẻ.

☐ Không đưa lời khuyên.

☐ Không tiên tri.

---

## personality

☐ Khoảng 20 ý.

☐ Chỉ mô tả tính cách.

☐ Không mô tả nghề nghiệp.

☐ Không trùng strengths.

---

## strengths

☐ Khoảng 25 ý.

☐ Chỉ mô tả điểm mạnh.

☐ Không lặp personality.

---

## weaknesses

☐ Khoảng 25 ý.

☐ Chỉ mô tả điểm cần cải thiện.

☐ Không phủ định tuyệt đối.

---

## career

☐ Khoảng 20 ý.

☐ Chỉ mô tả xu hướng nghề nghiệp.

☐ Không khẳng định thành công.

---

## wealth

☐ Khoảng 20 ý.

☐ Không nói giàu nghèo.

☐ Không tiên đoán tài vận.

---

## relationship

☐ Khoảng 20 ý.

☐ Bao gồm quan hệ xã hội.

☐ Không chỉ nói về hôn nhân.

---

## family

☐ Khoảng 20 ý.

☐ Nội dung nhất quán.

---

## health

☐ Khoảng 20 ý.

☐ Không chẩn đoán bệnh.

☐ Không kê đơn.

☐ Không dùng thuật ngữ y khoa.

---

## learning

☐ Khoảng 20 ý.

☐ Chỉ mô tả phong cách học.

---

## leadership

☐ Khoảng 20 ý.

☐ Chỉ mô tả phong cách lãnh đạo.

---

## communication

☐ Khoảng 20 ý.

☐ Chỉ mô tả giao tiếp.

---

## suitable_jobs

☐ Khoảng 20 ý.

☐ Là nhóm nghề.

☐ Không khẳng định thành công.

---

## unsuitable_jobs

☐ Khoảng 20 ý.

☐ Chỉ mô tả mức độ ít phù hợp.

☐ Không cấm nghề.

---

## development_advice

☐ Khoảng 20 ý.

☐ Là định hướng phát triển.

☐ Không ra lệnh.

---

## notes

☐ Metadata.

☐ Không luận giải.

---

## references

☐ Có nguồn.

☐ Không để trống.

---

# PHẦN D — Kiểm tra văn phong

☐ Văn phong thống nhất.

☐ Giọng văn trung lập.

☐ Không cảm tính.

☐ Không cường điệu.

☐ Không sử dụng dấu chấm than.

☐ Không dùng câu hỏi.

☐ Mỗi câu chỉ có một ý.

☐ Độ dài câu hợp lý.

---

# PHẦN E — Kiểm tra nội dung cấm

☐ Không tiên tri.

☐ Không mê tín.

☐ Không định mệnh.

☐ Không nghiệp báo.

☐ Không chẩn đoán bệnh.

☐ Không khẳng định tuyệt đối.

☐ Không kết luận chắc chắn.

☐ Không dùng từ "luôn luôn".

☐ Không dùng từ "100%".

☐ Không dùng từ "không bao giờ".

---

# PHẦN F — Kiểm tra phạm vi tri thức

☐ Không đưa Bát Tự.

☐ Không đưa Dụng Thần.

☐ Không đưa Hỷ Thần.

☐ Không đưa Kỵ Thần.

☐ Không đưa Đại Vận.

☐ Không đưa Lưu Niên.

☐ Không đưa Thần Sát.

☐ Không đưa Tử Vi.

☐ Không đưa Kỳ Môn.

☐ Không đưa hệ thống ngoài Bát Trạch.

---

# PHẦN G — Kiểm tra chất lượng

☐ Không trùng ý.

☐ Không mâu thuẫn.

☐ Không lặp câu.

☐ Không lặp cấu trúc quá nhiều.

☐ Nội dung tự nhiên.

☐ Đúng đặc điểm của quẻ.

☐ Chất lượng tương đương kham.json.

---

# PHẦN H — Kiểm tra kỹ thuật

☐ Validator PASS.

☐ Schema PASS.

☐ JSON PASS.

☐ Không warning.

☐ Không lỗi encoding.

☐ Có thể load trực tiếp bằng Python.

☐ Có thể sử dụng trực tiếp trong Interpretation Engine.

---

# PHẦN I — Tiêu chí nghiệm thu

Một file chỉ được đánh dấu **PASS** khi:

- PASS toàn bộ các mục trong Checklist.
- Không có lỗi JSON.
- Không có lỗi Schema.
- Không có lỗi Validator.
- Đạt chất lượng tương đương Golden Standard (`kham.json`).
- Sẵn sàng đưa vào Knowledge Base chính thức.

---

# Trạng thái kiểm định

| Hạng mục | Kết quả | Ghi chú |
|----------|----------|----------|
| JSON | ☐ PASS ☐ FAIL | |
| Schema | ☐ PASS ☐ FAIL | |
| Validator | ☐ PASS ☐ FAIL | |
| Editorial Rules | ☐ PASS ☐ FAIL | |
| Style Guide | ☐ PASS ☐ FAIL | |
| Nội dung | ☐ PASS ☐ FAIL | |
| Tổng thể | ☐ PASS ☐ FAIL | |

---

**Kết luận**

☐ Được phép đưa vào Knowledge Base.

☐ Cần chỉnh sửa trước khi đưa vào Knowledge Base.

Reviewer: ___________________

Ngày kiểm tra: ___________________