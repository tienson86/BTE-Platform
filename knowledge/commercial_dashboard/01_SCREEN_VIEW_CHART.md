# COMMERCIAL DASHBOARD
# SCREEN 01
# VIEW CHART
# XEM LÁ SỐ

Version: V1.0
Status: CANONICAL
Owner: BTE Platform

---

# 1. Mục tiêu

Đây là màn hình đầu tiên của quy trình phân tích Bát Tự.

Nhiệm vụ duy nhất của màn hình này là thu thập chính xác dữ liệu đầu vào để lập và phân tích lá số.

Màn hình không thực hiện:

- luận giải;
- hiển thị kết quả;
- hiển thị Dashboard;
- hiển thị PDF;
- hiển thị dữ liệu kỹ thuật.

Sau khi người dùng hoàn thành nhập liệu, hệ thống sẽ chuyển sang màn hình:

```

SCREEN 02
RESULT DASHBOARD

```

---

# 2. Đối tượng sử dụng

Màn hình này phục vụ:

- khách hàng phổ thông;
- chuyên gia nhập hộ khách;
- nhân viên tư vấn.

Không yêu cầu người dùng có kiến thức Bát Tự.

---

# 3. User Goal

Sau khi mở màn hình.

Khách hàng phải hiểu ngay:

> Tôi chỉ cần nhập thông tin sinh để hệ thống lập lá số.

Không được tạo cảm giác:

- nhiều bước;
- phức tạp;
- chuyên môn.

---

# 4. Business Goal

Sau khi người dùng bấm:

```

PHÂN TÍCH LÁ SỐ

```

hệ thống phải có đủ dữ liệu để:

- lập Tứ Trụ;
- tính Can Chi;
- tính Đại vận;
- tính Ngũ hành;
- chạy toàn bộ Analysis Engine.

Màn hình này không thực hiện bất kỳ tính toán nào.

---

# 5. Layout

```

┌──────────────────────────────────────────┐

              XEM LÁ SỐ

     Nhập thông tin để lập và phân tích
                 Bát Tự

└──────────────────────────────────────────┘


┌──────────────────────────────────────────┐

THÔNG TIN

Họ và tên

[____________________________]

Giới tính

○ Nam

○ Nữ

Ngày sinh

📅

Giờ sinh

🕒

Nơi sinh

📍

──────────────────────────────

Lưu ý

Giờ sinh và nơi sinh càng chính xác

thì kết quả luận giải càng đáng tin cậy.

──────────────────────────────

        PHÂN TÍCH LÁ SỐ

└──────────────────────────────────────────┘

```

---

# 6. Input Fields

## 6.1 Họ và tên

Kiểu:

Text

Required:

Không

Mục đích:

- hiển thị báo cáo;
- lưu hồ sơ.

Không tham gia tính toán.

---

## 6.2 Giới tính

Kiểu:

Radio

```

Nam

Nữ

```

Required:

Có

Tham gia:

- tính Đại vận;
- chiều vận;
- một số quy tắc luận giải.

---

## 6.3 Ngày sinh

Kiểu:

Date Picker

Required:

Có

Là dữ liệu bắt buộc của Analysis Engine.

Không cho nhập tự do.

---

## 6.4 Giờ sinh

Kiểu:

Time Picker

Required:

Khuyến nghị.

Nếu chưa biết giờ sinh:

Cho phép tiếp tục.

Hiển thị cảnh báo.

Ví dụ:

```

Bạn chưa nhập giờ sinh.

Một số kết quả sẽ có độ chính xác thấp hơn.

```

Không khóa người dùng.

---

## 6.5 Nơi sinh

Kiểu:

Autocomplete

Ví dụ:

- Hà Nội
- Bắc Ninh
- Hải Phòng
- TP Hồ Chí Minh

Required:

Khuyến nghị.

Dùng để:

- múi giờ;
- kinh độ;
- vĩ độ;
- lịch địa phương.

---

# 7. Validation

Bắt buộc:

- Giới tính
- Ngày sinh

Khuyến nghị:

- Giờ sinh
- Nơi sinh

Nếu thiếu dữ liệu khuyến nghị:

Cho phép tiếp tục.

Không chặn.

---

# 8. UX Principles

Màn hình này chỉ có:

- một Form;
- một Button.

Không xuất hiện:

- Reset
- Export
- PDF
- Lưu
- Báo cáo
- Dashboard
- Thống kê

---

# 9. Primary Action

Tên nút:

```

PHÂN TÍCH LÁ SỐ

```

Đây là CTA duy nhất của màn hình.

Không có CTA phụ.

---

# 10. Loading

Sau khi bấm:

```

PHÂN TÍCH LÁ SỐ

↓

Kiểm tra dữ liệu

↓

Loading

↓

Analysis Engine

↓

Dashboard

```

Không Popup.

Không mở Tab mới.

Không tải file.

---

# 11. Điều hướng

```

Trang chủ

↓

Chọn ngày tốt

↓

Xem lá số

↓

PHÂN TÍCH LÁ SỐ

↓

SCREEN 02
RESULT DASHBOARD

```

---

# 12. Không hiển thị

Không xuất hiện trên màn hình:

- Âm lịch
- Can Chi
- Tứ Trụ
- Ngũ hành
- Thập thần
- Dụng thần
- Hỷ thần
- Kỵ thần
- Đại vận
- Thần sát
- Điểm số
- Dashboard

Đây là dữ liệu của SCREEN 02.

---

# 13. Responsive

Desktop

Tablet

Mobile

đều giữ cùng một trình tự nhập liệu.

Không thay đổi luồng.

---

# 14. Accessibility

- Label luôn hiển thị.
- Không dùng Placeholder thay Label.
- Tab Order từ trên xuống.
- Hỗ trợ Enter để chuyển trường.
- Nút PHÂN TÍCH LÁ SỐ luôn là điểm dừng cuối.

---

# 15. Acceptance Checklist

□ Chỉ có 5 trường nhập.

□ Chỉ có 1 nút hành động.

□ Không có dữ liệu phân tích.

□ Không có Dashboard.

□ Có chú thích về giờ sinh và nơi sinh.

□ Cho phép tiếp tục nếu thiếu giờ sinh.

□ Sau khi thành công chuyển sang SCREEN 02.

□ Đồng nhất phong cách với màn hình Chọn ngày tốt.

---

# 16. Future Compatibility

Màn hình này là chuẩn cho:

- Web
- Mobile
- Tablet
- Kiosk
- Desktop

Mọi nền tảng đều sử dụng cùng một Business Specification.

Không tạo phiên bản riêng theo từng nền tảng.

---

# 17. CUSTOMER EMOTION
# TRẢI NGHIỆM CẢM XÚC NGƯỜI DÙNG

Commercial Dashboard không chỉ được thiết kế để hiển thị dữ liệu.

Dashboard còn phải tạo ra một hành trình trải nghiệm giúp khách hàng cảm thấy:

- dễ sử dụng;
- tin tưởng;
- chuyên nghiệp;
- có giá trị;
- muốn tiếp tục khám phá.

Mỗi màn hình đều phải hướng tới cảm xúc của người dùng.

Đây là một tiêu chuẩn thiết kế bắt buộc.

---

## 17.1 Mở màn hình

### Mục tiêu

Khách hàng không được cảm thấy:

- rối;
- nhiều bước;
- khó hiểu;
- mang tính kỹ thuật.

Thay vào đó phải có cảm giác:

> "Việc này rất đơn giản."

Thời gian để hiểu màn hình:

≤ 5 giây.

---

## 17.2 Nhập thông tin

Khách hàng chỉ nhập những gì hệ thống chưa biết.

Không yêu cầu khách hàng:

- tính Can Chi;
- chọn Âm lịch;
- nhập Tiết khí;
- chọn Nhật chủ.

Hệ thống tự động xử lý toàn bộ.

Khách hàng chỉ cần tập trung vào thông tin cá nhân.

Cảm xúc mong muốn:

> "Tôi chỉ cần nhập vài thông tin là đủ."

---

## 17.3 Chú thích

Thông báo không được mang tính cảnh báo.

Ví dụ:

❌

"Thiếu giờ sinh."

✔

"Lưu ý: Giờ sinh và nơi sinh càng chính xác thì kết quả luận giải càng đáng tin cậy."

Ngôn ngữ luôn:

- tích cực;
- thân thiện;
- dễ hiểu.

Không tạo áp lực cho người dùng.

---

## 17.4 Nút hành động

Nút:

```
PHÂN TÍCH LÁ SỐ
```

phải là điểm nhấn duy nhất của màn hình.

Người dùng không phải suy nghĩ:

"Tôi nên bấm nút nào?"

Chỉ tồn tại một hành động chính.

---

## 17.5 Trong lúc xử lý

Sau khi người dùng bấm:

```
PHÂN TÍCH LÁ SỐ
```

hệ thống chuyển sang trạng thái xử lý.

Không để màn hình đứng yên.

Hiển thị:

- thanh tiến trình;
- trạng thái đang phân tích;
- thông điệp ngắn.

Ví dụ:

```
Đang lập Tứ Trụ...

↓

Đang phân tích Ngũ hành...

↓

Đang tính Đại vận...

↓

Đang xây dựng báo cáo...
```

Khách hàng có cảm giác:

> "Hệ thống đang thực sự phân tích lá số của tôi."

Không nên chỉ hiển thị:

```
Loading...
```

---

## 17.6 Chuyển sang Dashboard

Khi hoàn thành.

Dashboard phải tạo cảm giác:

- chuyên nghiệp;
- đầy đủ;
- đáng tin cậy.

Khách hàng nhìn trong khoảng 30 giây đầu phải hiểu:

- Tôi là ai?
- Lá số của tôi thuộc nhóm nào?
- Điều gì là quan trọng nhất?
- Tôi nên làm gì tiếp theo?

Không để khách hàng phải đọc toàn bộ báo cáo mới hiểu.

---

## 17.7 Tư vấn trực tiếp

Commercial Dashboard được thiết kế để chuyên gia có thể:

- xoay màn hình;
- chỉ từng Card;
- giải thích ngay.

Không cần mở PDF.

Không cần tìm từng mục.

Dashboard phải đủ trực quan để trở thành công cụ tư vấn.

---

## 17.8 Trải nghiệm sau khi xem

Sau khi xem Dashboard.

Khách hàng phải có cảm giác:

> "Tôi đã hiểu bức tranh tổng thể về lá số của mình."

Đồng thời muốn tìm hiểu sâu hơn thông qua:

- từng Card;
- PDF;
- tư vấn chuyên gia.

Dashboard đóng vai trò mở đầu cho toàn bộ quá trình tư vấn.

---

## 17.9 Nguyên tắc cảm xúc

Mỗi màn hình phải tạo được ít nhất một trong các cảm xúc sau:

✓ Đơn giản

✓ Tin tưởng

✓ Chuyên nghiệp

✓ Rõ ràng

✓ Có giá trị

Nếu một màn hình chỉ hiển thị dữ liệu mà không tạo được bất kỳ cảm xúc nào trong số trên thì màn hình đó chưa đạt tiêu chuẩn Commercial Dashboard.

---

## 17.10 Acceptance Checklist

□ Người dùng hiểu mục đích màn hình trong ≤ 5 giây.

□ Không có quá một hành động chính.

□ Không sử dụng thuật ngữ kỹ thuật khi không cần thiết.

□ Có thông điệp hướng dẫn thân thiện.

□ Có trạng thái xử lý rõ ràng khi phân tích.

□ Dashboard tạo được cảm giác chuyên nghiệp ngay khi xuất hiện.

□ Người dùng biết bước tiếp theo sau khi xem kết quả.

---

## 17.11 Success Metrics

Màn hình được coi là thành công khi:

- Người dùng mới có thể hoàn thành việc nhập liệu mà không cần hướng dẫn.
- Chuyên gia có thể bắt đầu tư vấn ngay sau khi Dashboard xuất hiện.
- Khách hàng cảm thấy quá trình phân tích có giá trị và đáng tin cậy.
- Dashboard trở thành điểm trung tâm của toàn bộ trải nghiệm BTE.

Customer Emotion là tiêu chuẩn thiết kế bắt buộc cho mọi màn hình trong Commercial Dashboard V1.0.

---

## 17.12 THE FIRST IMPRESSION MOMENT
## KHOẢNH KHẮC ẤN TƯỢNG ĐẦU TIÊN

Commercial Dashboard phải tạo ra một "Khoảnh khắc ấn tượng đầu tiên" ngay khi màn hình kết quả xuất hiện.

Đây là thời điểm quan trọng nhất trong toàn bộ trải nghiệm của khách hàng.

Nếu khoảnh khắc này thành công, khách hàng sẽ có niềm tin vào hệ thống và sẵn sàng tiếp tục khám phá các nội dung chuyên sâu hơn.

Nếu khoảnh khắc này thất bại, toàn bộ giá trị của Analysis Engine và Commercial Knowledge sẽ không được cảm nhận đầy đủ.

---

### Mục tiêu

Trong vòng **30 giây đầu tiên**, người dùng phải có được ba cảm nhận sau:

**1. Hệ thống đã hiểu lá số của tôi.**

Dashboard phải đưa ra được một kết luận tổng quát, rõ ràng và dễ hiểu.

Khách hàng không phải tự đọc hàng chục mục dữ liệu để suy luận.

---

**2. Hệ thống có đủ chiều sâu để đáng tin cậy.**

Ngay trên màn hình đầu tiên, khách hàng phải nhìn thấy:

- Tứ Trụ
- Nhật chủ
- Mệnh cục
- Dụng thần
- Đại vận hiện tại
- Luận giải tổng quan

Điều này giúp tạo niềm tin rằng kết quả được xây dựng từ một nền tảng phân tích đầy đủ.

---

**3. Hệ thống biết tôi nên làm gì tiếp theo.**

Dashboard không chỉ dừng lại ở việc mô tả.

Dashboard phải dẫn người dùng đến hành động tiếp theo thông qua:

- Khuyến nghị
- Định hướng
- Kế hoạch hành động
- Các bước cải vận

Khách hàng phải có cảm giác:

> "Tôi không chỉ biết mình là ai, mà còn biết mình nên làm gì."

---

### Thiết kế hỗ trợ

Khoảnh khắc ấn tượng đầu tiên không được tạo ra bằng hiệu ứng hình ảnh.

Không sử dụng:

- Animation phức tạp
- Hiệu ứng chuyển cảnh dài
- Popup
- Âm thanh

Khoảnh khắc này phải đến từ:

- Bố cục rõ ràng
- Thông tin ưu tiên đúng
- Màu sắc dễ đọc
- Nội dung có giá trị

---

### Thứ tự nhận thức

Dashboard phải được thiết kế theo đúng trình tự người dùng tiếp nhận thông tin.

```
Tôi là ai?

↓

Lá số của tôi thuộc nhóm nào?

↓

Điểm mạnh là gì?

↓

Điều gì cần lưu ý?

↓

Tôi nên làm gì tiếp theo?
```

Không được đảo ngược trình tự này.

Ví dụ:

Không hiển thị ngay các chi tiết như:

- Tàng can
- Trường sinh
- Điểm thành phần
- Rule Engine

trước khi khách hàng hiểu bức tranh tổng thể.

---

### Vai trò của Dashboard

Dashboard không phải là nơi hiển thị toàn bộ dữ liệu phân tích.

Dashboard là nơi kể lại câu chuyện của lá số bằng ngôn ngữ mà khách hàng có thể hiểu.

Các phân tích chi tiết sẽ được trình bày trong từng Card hoặc trong PDF.

---

### Tiêu chuẩn đánh giá

Một Dashboard đạt tiêu chuẩn "First Impression Moment" khi:

□ Người dùng hiểu được bức tranh tổng thể trong khoảng 30 giây.

□ Chuyên gia có thể bắt đầu tư vấn ngay mà không cần mở PDF.

□ Khách hàng muốn tiếp tục xem chi tiết từng Card.

□ Dashboard tạo được cảm giác chuyên nghiệp và đáng tin cậy.

□ Dashboard trở thành trung tâm của toàn bộ quá trình tư vấn.

---

### Nguyên tắc

Một Dashboard thành công không phải là Dashboard hiển thị nhiều thông tin nhất.

Một Dashboard thành công là Dashboard giúp khách hàng hiểu đúng điều quan trọng nhất trong thời gian ngắn nhất.

Đây là tiêu chuẩn thiết kế bắt buộc đối với tất cả các Dashboard của BTE Platform.

---

## 17.13 CONFIDENCE BEFORE COMPLEXITY
## NIỀM TIN TRƯỚC ĐỘ PHỨC TẠP

Commercial Dashboard được xây dựng theo nguyên tắc:

> Người dùng phải có niềm tin trước khi tiếp cận các nội dung chuyên sâu.

Không phải khách hàng nào cũng có kiến thức về Bát Tự.

Do đó, hệ thống không được bắt đầu bằng các thuật ngữ chuyên môn hoặc dữ liệu kỹ thuật.

Dashboard phải giúp người dùng:

- hiểu kết quả trước;
- tin tưởng kết quả;
- sau đó mới khám phá cách hệ thống đi đến kết luận.

---

### Không bắt đầu bằng dữ liệu

Không mở màn hình kết quả bằng:

- Tàng can
- Trường sinh
- Điểm thành phần
- Rule Engine
- Nhật chủ 0.xx
- Các chỉ số kỹ thuật

Những thông tin này rất quan trọng, nhưng không phải là điểm bắt đầu của trải nghiệm.

---

### Bắt đầu bằng sự thấu hiểu

Dashboard phải mở đầu bằng những thông điệp mà khách hàng có thể hiểu ngay.

Ví dụ:

✓ Bạn thuộc nhóm Thân vượng.

✓ Giai đoạn hiện tại là thời kỳ phát triển.

✓ Bạn phù hợp với vai trò dẫn dắt hơn là hỗ trợ.

✓ Hỏa là yếu tố cần được tăng cường trong giai đoạn này.

Sau khi khách hàng hiểu các kết luận này, Dashboard mới dẫn dắt họ đến các Card phân tích chi tiết.

---

### Thông tin theo từng tầng

Commercial Dashboard được tổ chức theo ba tầng thông tin.

#### Tầng 1 — Insight

Trả lời:

"Tôi là ai?"

"Tôi đang ở giai đoạn nào?"

"Tôi nên làm gì?"

Khách hàng phải hiểu trong khoảng 30 giây.

---

#### Tầng 2 — Analysis

Giải thích vì sao Dashboard đưa ra kết luận.

Bao gồm:

- Ngũ hành
- Thập thần
- Mệnh cục
- Đại vận
- Thần sát

Đây là tầng dành cho người muốn hiểu sâu hơn.

---

#### Tầng 3 — Technical

Bao gồm các dữ liệu chuyên sâu và có tính kiểm chứng.

Ví dụ:

- Tàng can
- Trường sinh
- Điều hậu
- Quy tắc chọn Dụng thần
- Các điều kiện phân tích

Đây là tầng dành cho chuyên gia hoặc người nghiên cứu.

---

### Vai trò của chuyên gia

Dashboard không thay thế chuyên gia.

Dashboard giúp chuyên gia:

- bắt đầu buổi tư vấn nhanh hơn;
- tập trung vào điều quan trọng nhất;
- giải thích từng Card theo đúng trình tự.

Mỗi Card là một bước đi từ:

Insight

↓

Analysis

↓

Technical Detail

Không đi ngược chiều.

---

### Tiêu chuẩn đánh giá

Một Dashboard đạt nguyên tắc "Confidence Before Complexity" khi:

□ Khách hàng hiểu được kết luận trước khi đọc dữ liệu.

□ Không bị quá tải bởi thuật ngữ chuyên môn.

□ Có thể dừng ở tầng Insight mà vẫn nhận được giá trị.

□ Người muốn nghiên cứu vẫn có thể mở rộng sang tầng Analysis và Technical.

□ Chuyên gia có thể sử dụng Dashboard như công cụ tư vấn trực tiếp.

---

### Nguyên tắc cuối cùng

Commercial Dashboard không được thiết kế để chứng minh hệ thống tính toán phức tạp đến đâu.

Commercial Dashboard được thiết kế để giúp khách hàng hiểu bản thân rõ hơn và đưa ra quyết định tốt hơn.

Đây là nguyên tắc nền tảng của toàn bộ BTE Platform.