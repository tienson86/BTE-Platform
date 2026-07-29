# Style Guide
## Module: knowledge_base/08_feng_shui/01_gua

Version: 1.0

---

# 1. Mục tiêu

Tài liệu này quy định tiêu chuẩn biên soạn dữ liệu cho toàn bộ module:

knowledge_base/08_feng_shui/01_gua/

Mục tiêu:

- đảm bảo mọi file có chất lượng đồng đều
- đảm bảo dữ liệu nhất quán
- tránh trùng lặp
- tránh mâu thuẫn
- dễ mở rộng trong các phiên bản sau
- phù hợp với Interpretation Engine của BTE Platform

---

# 2. Golden Standard

File chuẩn của toàn bộ module là:

kham.json

Mọi file còn lại phải đạt chất lượng tương đương:

- ly.json
- chan.json
- ton.json
- can.json
- khon.json
- doai.json
- can_gen.json

Không được đơn thuần sao chép nội dung của kham.json.

Mỗi file phải phản ánh đúng đặc điểm của từng quẻ.

---

# 3. Quy tắc chung

Mỗi câu phải là:

- một ý độc lập
- rõ nghĩa
- dễ hiểu
- không mơ hồ

Không sử dụng:

- tiên tri
- khẳng định tuyệt đối
- mê tín
- kết luận chắc chắn

Không dùng:

- luôn luôn
- chắc chắn
- 100%
- bắt buộc
- không bao giờ

Ưu tiên sử dụng:

- có xu hướng
- thường
- có khả năng
- phù hợp
- dễ
- nên
- có thể

---

# 4. Văn phong

Giọng văn:

- trung lập
- chuyên gia
- khách quan
- dễ đọc
- thống nhất

Không viết:

"Tính cách của người này cực kỳ..."

Ưu tiên:

"Có xu hướng..."

---

# 5. Độ dài

overview

5 đoạn.

personality

20 ý.

strengths

25 ý.

weaknesses

25 ý.

career

20 ý.

wealth

20 ý.

relationship

20 ý.

family

20 ý.

health

20 ý.

learning

20 ý.

leadership

20 ý.

communication

20 ý.

suitable_jobs

20 ý.

unsuitable_jobs

20 ý.

development_advice

20 ý.

notes

8 ý.

references

10–15 nguồn.

---

# 6. Quy tắc từng field

## overview

Giới thiệu:

- vị trí
- ngũ hành
- phương vị
- nhóm Đông/Tây Tứ Trạch
- đặc điểm tổng quan

Không đưa lời khuyên.

---

## personality

Chỉ mô tả:

- khí chất
- tư duy
- hành vi
- đặc điểm nội tâm

Không mô tả nghề nghiệp.

---

## strengths

Chỉ mô tả:

điểm mạnh.

Không lặp personality.

---

## weaknesses

Chỉ mô tả:

điểm cần cải thiện.

Không phủ định tuyệt đối.

---

## career

Mô tả:

xu hướng nghề nghiệp.

Không liệt kê nghề cụ thể.

---

## wealth

Mô tả:

xu hướng quản lý tài chính.

Không nói:

- giàu
- nghèo
- phát tài

---

## relationship

Quan hệ:

- xã hội
- tình cảm
- đối tác
- bạn bè

Không chỉ viết về hôn nhân.

---

## family

Quan hệ:

- cha mẹ
- con cái
- gia đình
- trách nhiệm

---

## health

Chỉ viết:

- xu hướng
- chăm sóc sức khỏe

Không:

- chẩn đoán
- kê đơn
- khẳng định bệnh

---

## learning

Mô tả:

- phong cách học
- khả năng tiếp thu
- nghiên cứu

---

## leadership

Mô tả:

- phong cách lãnh đạo
- quản trị
- điều phối

---

## communication

Mô tả:

- giao tiếp
- truyền đạt
- lắng nghe

---

## suitable_jobs

Liệt kê:

20 nhóm nghề phù hợp.

Không nói:

"chắc chắn thành công"

---

## unsuitable_jobs

Không ghi:

"không làm được"

Chỉ ghi:

"ít phù hợp"

---

## development_advice

Đưa ra:

định hướng phát triển.

Không:

ra lệnh.

---

## notes

Metadata.

Không luận giải.

---

## references

Chỉ ghi:

nguồn tri thức.

---

# 7. Chống trùng lặp

Không copy ý giữa:

personality

strengths

career

leadership

communication

relationship

Mỗi field có mục tiêu riêng.

---

# 8. Tiêu chuẩn chất lượng

Mỗi file phải:

✓ JSON hợp lệ

✓ đúng schema

✓ không lỗi validator

✓ không trùng ý

✓ không mâu thuẫn

✓ thống nhất văn phong

✓ có thể sử dụng trực tiếp trong Interpretation Engine

---

# 9. Quy trình tạo file mới

Khi tạo một quẻ mới:

Bước 1

Đọc:

style_guide.md

Bước 2

Đọc:

kham.json

Bước 3

Giữ nguyên schema.

Bước 4

Thay toàn bộ nội dung bằng đặc điểm của quẻ mới.

Bước 5

Kiểm tra:

- JSON
- số lượng mục
- văn phong
- trùng lặp
- validator

Chỉ khi vượt qua toàn bộ bước kiểm tra mới được coi là hoàn thành.