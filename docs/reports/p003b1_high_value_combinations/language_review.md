# P-003B.1 Language review

Date: 2026-09-04  
Scope: Ten Gods combination consulting copy only. P-003 single-god cards were not rewritten.

---

## Rule

Remove internal shorthand unless it is genuinely natural customer language:

- cửa
- khung
- lối
- món

Preferred tone: clear, professional, consulting, direct, customer-readable.

Do not generate prose algorithmically. Each combination is an authored asset.

---

## Scan

`tenGodsCombinationAssets.ts` after rewrite:

| Token | Occurrences in combination assets |
|-------|-----------------------------------|
| cửa | 0 |
| khung | 0 |
| lối | 0 |
| món | 0 |

The exact rejected title **“Bứt cửa hiểm bằng lối không theo khuôn”** is gone.

The ticket example **“Xử lý việc khó bằng cách linh hoạt và khác biệt”** was **not** used. Semantic review: it is generic, does not name the three published capabilities (áp lực, tốc độ, kỹ năng khó chuẩn hóa), and would flatten CASE-0001 into a slogan. Shipped title is more specific and still customer-readable.

---

## Rewritten titles (pilot → customer)

| Members | Pilot title | Customer title |
|---------|-------------|----------------|
| Thực Thần · Thiên Tài | Đổi cửa lệch thành món thấy được | Biến cơ hội không cố định thành sản phẩm có hạn |
| Thương Quan · Thiên Tài | Sửa khung bằng cửa không cố | Sửa quy trình kém và mở kênh phụ |
| Chính Quan · Chính Ấn | Chạy việc trong khung có nền | Làm việc có chuẩn, có chỗ tích lũy trước khi bung |
| Kiếp Tài · Thất Sát | Mở cửa khi việc đang khó | Chớp việc khó đúng lúc nguồn đang kẹt |
| Kiếp Tài · Thất Sát · Thiên Ấn | Bứt cửa hiểm bằng lối không theo khuôn | Gánh việc khó theo cách linh hoạt, có điểm dừng |

Hidden support:

| Before | After |
|--------|--------|
| Phía ẩn giữ cửa lệch và chỗ ủ. Đó là nền, chưa phải mô hình tiền đang chạy. | Phần ẩn giữ cơ hội phụ và chỗ tích lũy. Đó là nền tảng, chưa phải cách bạn đang kiếm tiền. |

---

## Substitutions used

| Internal | Customer |
|----------|----------|
| cửa / cửa lệch / cửa hiểm | kênh, hướng, việc khó, cơ hội phụ |
| khung / khung phép | quy trình, chuẩn, tổ chức, cấp bậc |
| lối / lối lệch | cách làm riêng, kỹ năng không nằm trên chức danh |
| món | sản phẩm, thành phẩm, hàng |

Field label **Cầm việc** is kept (UI-07 forbids “Lãnh đạo” in card source). Body copy uses “cầm việc” as work-holding, not rank.

---

## Safety language

Combination describes tendency, not outcome.

Forbidden in this library:

- wealth guaranteed
- leadership guaranteed
- entrepreneur guaranteed
- marriage outcomes
- good/bad luck labels

Voice stays “Bạn tạo giá trị khi…”, “Tiền đến từ…”, “Bạn hợp việc…”, “Rủi ro:”.
