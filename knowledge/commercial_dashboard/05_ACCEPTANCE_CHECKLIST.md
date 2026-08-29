# COMMERCIAL DASHBOARD
# 05_ACCEPTANCE_CHECKLIST
# PRODUCT ACCEPTANCE GATE

Version: V1.0
Status: CANONICAL
Owner: BTE Platform

---

# 1. Mục tiêu

Tài liệu này định nghĩa tiêu chí nghiệm thu chính thức cho Commercial Dashboard V1.0.

Đây là Product Acceptance Gate.

Mọi implementation chỉ được coi là hoàn thành khi:

- đúng Specification;
- đúng giao diện;
- đúng dữ liệu;
- đúng trải nghiệm;
- đúng Presentation Mapping;
- không phá kiến trúc đã Freeze.

Build PASS không đồng nghĩa Product PASS.

Unit Test PASS không đồng nghĩa UI PASS.

Implementation chỉ được APPROVE khi toàn bộ checklist bắt buộc đạt yêu cầu.

---

# 2. Acceptance Levels

Commercial Dashboard sử dụng bốn cấp nghiệm thu.

## LEVEL A — Architecture

Xác nhận:

- đúng nguồn dữ liệu;
- đúng Presentation Model;
- không tính toán tại UI;
- không tạo renderer cạnh tranh.

---

## LEVEL B — Content

Xác nhận:

- đúng trường dữ liệu;
- đúng thứ tự;
- đúng wording;
- không thiếu nội dung;
- không lặp nội dung.

---

## LEVEL C — Visual

Xác nhận:

- đúng bố cục;
- đúng hierarchy;
- đúng kích thước tương đối;
- đúng card placement;
- không overflow;
- không layout shift bất thường.

---

## LEVEL D — Experience

Xác nhận:

- người dùng hiểu luồng;
- Dashboard đọc được tự nhiên;
- Mobile sử dụng được;
- PDF/DOCX nhất quán;
- First Impression đạt yêu cầu.

Một release phải PASS cả bốn Level.

---

# 3. Canonical Source Check

□ Implementation đọc đúng Commercial Dashboard Specification.

□ Không tự tạo requirement mới.

□ Không thay đổi tên Screen/Card ngoài Specification.

□ Không tự đổi thứ tự Card.

□ Không tự thêm hoặc bỏ trường dữ liệu.

□ Không sửa CK-01 Commercial Knowledge.

□ Không sửa Astrology Engine ngoài bug được phê duyệt.

□ Không tạo Presentation Model cạnh tranh.

---

# 4. Customer Portal Navigation

Customer Portal chỉ có:

- Trang chủ
- Chọn ngày tốt
- Xem lá số

Acceptance:

□ Trang chủ mặc định là Xem ngày tốt/xấu.

□ Không còn Welcome Dashboard cũ.

□ Chọn ngày tốt là màn hình riêng.

□ Xem lá số là màn hình nhập dữ liệu Bát Tự.

□ Báo cáo không xuất hiện trong Customer Navigation.

□ Lịch sử không xuất hiện trong Customer Navigation.

□ Admin functions không xuất hiện trong Customer Portal.

□ Dashboard kết quả không phải menu chính.

---

# 5. Screen 01 — Xem lá số

Acceptance:

□ Giao diện đồng nhất phong cách với Chọn ngày tốt.

□ Chỉ có 5 trường:

- Họ và tên
- Giới tính
- Ngày sinh
- Giờ sinh
- Nơi sinh

□ Không hiển thị trường kỹ thuật.

□ Không yêu cầu nhập Âm lịch.

□ Không yêu cầu nhập Can Chi.

□ Không yêu cầu nhập Tiết khí.

□ Không yêu cầu nhập Cung Phi.

□ Có chú thích:

"Giờ sinh và nơi sinh càng chính xác thì kết quả luận giải càng đáng tin cậy."

□ Chỉ có một CTA chính.

□ CTA có tên:

PHÂN TÍCH LÁ SỐ

□ Sau khi phân tích thành công chuyển tới Bazi Dashboard.

□ Không mở tab mới.

□ Không popup kết quả.

---

# 6. Loading Experience

□ Không chỉ hiển thị "Loading...".

□ Có trạng thái xử lý có ý nghĩa.

Ví dụ:

- Đang lập Tứ Trụ...
- Đang phân tích Ngũ Hành...
- Đang xác định Mệnh Cục...
- Đang xây dựng luận giải...

□ Không hiển thị bước giả nếu runtime không thực hiện bước đó.

□ Không treo UI trong quá trình phân tích.

□ Error state có thông báo rõ ràng.

---

# 7. Bazi Dashboard Structure

Canonical order:

1. Identity Header
2. Overview
3. BaZi
4. Five Elements
5. Ten Gods
6. Pattern
7. ShenSha
8. Luck
9. Interpretation
10. Action Plan

Acceptance:

□ Có đủ 10 thành phần.

□ Đúng thứ tự.

□ Không có Card legacy chen giữa.

□ Không có Card duplicate.

□ Không có section Report cũ xuất hiện như Card riêng.

---

# 8. Identity Header

□ Identity là Header, không phải Analysis Card.

□ Nằm trên cùng Dashboard.

□ Hiển thị thông tin cá nhân.

□ Có Tứ Trụ.

□ Tứ Trụ giữ dạng bốn cột:

- Năm
- Tháng
- Ngày
- Giờ

□ Có Thiên Can.

□ Có Địa Chi.

□ Nhật Chủ được nhấn mạnh rõ.

□ Có Nạp Âm đầy đủ bốn trụ.

□ Có Cung Phi.

□ Có Mệnh Quái.

□ Có Nhóm Trạch.

□ Có Tiết khí nếu Canonical Analysis có dữ liệu.

□ Metadata không chiếm ưu tiên thị giác.

□ Không hiển thị:

- Thân vượng
- Dụng thần
- Hỷ thần
- Kỵ thần
- Mệnh cục

trong Identity Header.

---

# 9. Overview Card

□ Là Hero Card đầu tiên của Dashboard Body.

□ Có một Insight chính.

□ Có Nhật Chủ.

□ Có Strength state.

□ Có Mệnh Cục.

□ Có Dụng Thần.

□ Có Điều Hậu.

□ Không biến thành bảng kỹ thuật.

□ Không hiển thị Rule ID.

□ Không lặp toàn bộ Ngũ Hành.

□ Không lặp toàn bộ Thập Thần.

□ Có Quick Conclusion ngắn.

□ Khách hàng có thể hiểu Card trong khoảng 15 giây.

---

# 10. BaZi Card

□ Tiêu đề hiển thị là:

BÁT TỰ

□ Không dùng tiêu đề:

"Tứ Trụ chi tiết"

□ Có Thiên Can.

□ Có Địa Chi.

□ Có Nạp Âm.

□ Có Tàng Can.

□ Có Thập Thần.

□ Có Trường Sinh.

□ Giữ cấu trúc bốn trụ.

□ Nhật Chủ không bị nhầm thành Tỷ Kiên.

□ Không luận giải trong Card này.

□ Không có khuyến nghị.

□ Simple / Expert mode nếu được implementation theo Specification.

---

# 11. Five Elements Card

□ Có trạng thái cân bằng tổng quát.

□ Có đủ:

- Mộc
- Hỏa
- Thổ
- Kim
- Thủy

□ Có visual chart.

□ Có Summary hành mạnh/yếu.

□ Có Overall Comment.

□ Không dùng số lượng cấu trúc như kết luận vượng suy.

□ Không tự suy ra Dụng Thần từ histogram.

□ Không hiển thị Dụng Thần như kết luận của Card.

□ Không có lời khuyên bổ hành tại Card này.

---

# 12. Ten Gods Card

□ Có Thập Thần nổi bật.

□ Có Distribution đủ dữ liệu.

□ Có giải thích bằng ngôn ngữ khách hàng.

□ Có Personality / Capability Summary.

□ Không chỉ liệt kê tên Thập Thần.

□ Không kết luận nghề nghiệp trực tiếp.

□ Không luận Đại Vận.

□ Không tạo Action Plan.

□ Không đổi semantic Ten Gods từ Engine.

---

# 13. Pattern Card

□ Tiêu đề khách hàng:

MỆNH CỤC

□ Có Chính Cách.

□ Có Phụ Cách nếu tồn tại.

□ Có Pattern Status.

□ Có Formation flow hoặc evidence rõ ràng.

□ Formation không expose Rule ID.

□ Không hiển thị thuật toán matcher.

□ Không quyết định tốt/xấu tuyệt đối.

□ Không đưa hành động.

---

# 14. ShenSha Card

□ Không trình bày theo kiểu bảng Có/Không đơn thuần.

□ Thần Sát được nhóm theo giá trị tư vấn khi dữ liệu hỗ trợ.

Ví dụ:

- Quý Nhân & Hỗ trợ
- Học tập & Danh tiếng
- Quan hệ & Tình cảm
- Di chuyển & Biến động
- Điều cần lưu ý

□ Mỗi Thần Sát có ý nghĩa ngắn nếu Knowledge có dữ liệu.

□ Không phóng đại tính hung/cát.

□ Không coi Thần Sát là yếu tố quyết định toàn bộ lá số.

□ Không tạo dự đoán sự kiện.

---

# 15. Luck Card

□ Có Đại Vận hiện tại.

□ Có Can Chi Đại Vận.

□ Có khoảng năm.

□ Có tuổi.

□ Có chiều vận.

□ Có tuổi khởi vận.

□ Đại Vận hiện tại được highlight.

□ Có Timeline / Roadmap rõ ràng.

□ Có Đại Vận kế tiếp.

□ Không bắt người dùng tự tìm vận hiện tại trong bảng 10 dòng.

□ Không luận Lưu niên trong Card này.

□ Không phán "chắc chắn tốt/xấu".

---

# 16. Interpretation Card

□ Là Decision Card.

□ Không dùng lại cấu trúc kỹ thuật cũ nếu Specification mới đã thay thế.

Ưu tiên canonical customer-facing structure:

- Tổng kết
- Điểm mạnh
- Điểm cần lưu ý
- Cơ hội
- Thách thức
- Kết luận

□ Không lặp bảng dữ liệu của các Card trước.

□ Không hiển thị raw Engine text.

□ Không expose internal wording.

□ Nội dung có nguồn từ Commercial Composer / approved narrative source.

□ Không invent advice tại UI.

□ Không mâu thuẫn với Overview.

□ Không mâu thuẫn với Luck.

□ Không mâu thuẫn với Pattern.

---

# 17. Action Plan Card

□ Là Card cuối cùng.

□ Trả lời:

"Tôi nên làm gì tiếp theo?"

□ Có Top Priorities.

□ Có Nên làm.

□ Có Nên hạn chế.

□ Có trọng tâm:

- Công việc
- Tài chính
- Quan hệ
- Sức khỏe

nếu Commercial Knowledge hỗ trợ.

□ Có Roadmap hành động nếu dữ liệu hỗ trợ.

□ Không tự tạo mốc thời gian giả.

□ Không tạo khuyến nghị không có nguồn.

□ Không mâu thuẫn với Interpretation.

□ Không mâu thuẫn với Dụng Thần / Kỵ Thần canonical.

---

# 18. Card Duplication Check

Đây là check bắt buộc.

□ Overview không lặp Interpretation.

□ Interpretation không lặp nguyên văn Overview.

□ Action Plan không lặp nguyên văn Interpretation.

□ Five Elements không lặp Useful God logic.

□ Ten Gods không lặp Pattern.

□ BaZi không lặp Identity Header ngoài phần cấu trúc cần thiết.

□ ShenSha không lặp Ten Gods.

□ Luck không lặp Action Plan.

Nếu cùng một đoạn customer text xuất hiện ở nhiều Card:

FAIL

trừ khi Specification cho phép rõ ràng.

---

# 19. Content Quality

□ Không có câu máy móc.

□ Không có câu debug.

□ Không có placeholder.

□ Không có:

"Chưa đủ căn cứ..."

trong vị trí gây cảm giác lỗi nếu có thể biểu diễn bằng empty state tốt hơn.

□ Không có câu tự mâu thuẫn.

□ Không có thuật ngữ nội bộ xuất hiện với khách hàng.

□ Không có tiếng Anh kỹ thuật xen vào UI trừ thương hiệu cần thiết.

□ Không có câu dài khó đọc trong Hero Cards.

---

# 20. Data Integrity

□ Tất cả trường hiển thị có nguồn canonical.

□ Không hard-code dữ liệu test.

□ Không dùng CASE-0001 data làm default production content.

□ Không có fallback sai giới tính.

□ Không có stale result.

□ Không lấy History result khi người dùng vừa phân tích lá số mới.

□ Analysis ID nhất quán xuyên suốt runtime.

□ Portal và Export cùng analysis.

---

# 21. Presentation Architecture

□ UI không gọi Engine trực tiếp ngoài canonical orchestration.

□ UI không gọi matcher.

□ UI không gọi Commercial Composer.

□ Presentation Layer không tính Astrology.

□ Presentation Layer không tự generate advice.

□ Có một canonical presentation path.

□ Không còn renderer legacy cạnh tranh trong customer runtime.

---

# 22. Desktop Layout

□ Dashboard không phải tập hợp card kích thước ngẫu nhiên.

□ Visual hierarchy rõ.

□ Identity được nhìn đầu tiên.

□ Overview được nhìn tiếp theo.

□ Analysis Cards có trọng số thấp hơn Hero.

□ Interpretation và Action Plan có không gian đủ lớn.

□ Không có card quá cao chỉ vì whitespace.

□ Không có card quá thấp khiến nội dung bị ép.

□ Không horizontal overflow.

□ Không card overlap.

□ Không text clipping.

---

# 23. Mobile Layout

□ Mobile dùng một cột.

□ Nội dung không bị mất.

□ Không phụ thuộc hover.

□ Không có page horizontal overflow.

□ Tứ Trụ vẫn đọc được.

□ Chart responsive.

□ CTA đủ lớn để chạm.

□ Interpretation không bị nén thành chữ quá nhỏ.

□ Action Plan vẫn là Card cuối.

---

# 24. PDF Mapping

□ PDF dùng cùng Presentation Model.

□ PDF không compose lại.

□ PDF không có content riêng.

□ Identity nằm đầu báo cáo.

□ Card order giống Dashboard.

□ Không mất Card khi export.

□ Không có nội dung trong PDF nhưng không có trên Dashboard, trừ metadata print được Specification cho phép.

□ Không có Dashboard content bị silently bỏ khỏi PDF.

---

# 25. DOCX Mapping

□ DOCX dùng cùng content source.

□ Không có wording khác PDF.

□ Không có section legacy chen vào.

□ Heading hierarchy đúng.

□ Nội dung editable nhưng semantic không đổi.

---

# 26. Print Experience

□ Identity Header không bị cắt vô lý.

□ Card không bị split giữa hai trang nếu có thể tránh.

□ Heading không nằm cuối trang một mình.

□ Chart không bị crop.

□ Chart không quá nhỏ.

□ Timeline đọc được trên A4.

□ Interpretation có spacing hợp lý.

□ Action Plan không bị chia vụn nếu có thể tránh.

□ Có số trang.

□ Header/Footer print nhất quán.

---

# 27. One Source of Truth

Thực hiện cùng một analysis.

So sánh:

- Dashboard
- Print from Dashboard
- PDF Export
- DOCX Export

Acceptance:

□ Cùng Tứ Trụ.

□ Cùng Nhật Chủ.

□ Cùng Strength.

□ Cùng Mệnh Cục.

□ Cùng Useful God.

□ Cùng Luck.

□ Cùng Interpretation.

□ Cùng Action Plan.

Nếu một trong bốn khác semantic:

FAIL.

---

# 28. Visual Reference Review

Implementation phải được so sánh bằng screenshot với canonical visual reference đã được Product Owner duyệt.

Không nghiệm thu bằng code inspection đơn thuần.

Bắt buộc có screenshot:

□ Desktop full page.

□ Desktop first viewport.

□ Identity Header.

□ Overview + BaZi.

□ Five Elements + Ten Gods + Pattern.

□ ShenSha + Luck.

□ Interpretation.

□ Action Plan.

□ Mobile first viewport.

□ Mobile full flow.

□ PDF sample pages.

---

# 29. Screenshot Acceptance

Mỗi screenshot phải được đánh giá theo:

- bố cục;
- tỷ lệ;
- alignment;
- spacing;
- hierarchy;
- readability;
- consistency.

Không được báo:

"UI PASS"

chỉ vì:

- CSS build thành công;
- DOM chứa đúng text;
- snapshot test pass.

Product Owner phải có thể nhìn screenshot và xác nhận giao diện đúng.

---

# 30. Golden Case Validation

Ít nhất một Golden Case phải chạy xuyên suốt.

CASE-0001 có thể dùng cho validation.

Acceptance:

□ Input đúng.

□ Analysis đúng.

□ Dashboard đúng.

□ PDF đúng.

□ DOCX đúng.

□ Không stale data.

□ Không legacy route.

---

# 31. Multi-Case Validation

Không chỉ test một lá số.

Tối thiểu phải có các nhóm:

□ Thân vượng.

□ Thân nhược.

□ Trường hợp gần trung hòa.

□ Có nhiều Thần Sát.

□ Ít Thần Sát.

□ Đại Vận hiện tại đầu chu kỳ.

□ Đại Vận hiện tại cuối chu kỳ.

□ Missing optional data nếu runtime hỗ trợ.

Mục tiêu:

Đảm bảo UI không chỉ đẹp với CASE-0001.

---

# 32. Regression Gate

Trước khi PASS:

□ Frontend build PASS.

□ TypeScript PASS.

□ Portal tests PASS.

□ Analysis regression PASS.

□ Commercial Knowledge regression PASS.

□ Composer regression PASS.

□ Report Engine regression PASS.

□ Export regression PASS.

□ Golden Dataset PASS.

Không sửa Engine để làm UI test PASS.

---

# 33. Forbidden Shortcuts

Tuyệt đối không:

- hard-code screenshot;
- hard-code CASE data;
- duplicate report content trong frontend;
- tạo static HTML thay runtime;
- bypass canonical adapter;
- sửa Golden Dataset chỉ để test xanh mà không review semantic;
- thay visual reference mà không Product Owner approval.

---

# 34. Product Owner Review

Implementation completion report phải bao gồm:

1. Status
2. Routes implemented
3. Canonical presentation path
4. Screens completed
5. Header completed
6. Cards completed
7. Desktop screenshots
8. Mobile screenshots
9. PDF screenshots / exports
10. DOCX validation
11. Tests
12. Regression
13. Known deviations
14. Out-of-scope confirmation
15. Final verdict

Cursor không được tự tuyên bố:

FINAL FROZEN

trước Product Owner review.

---

# 35. PASS Criteria

Commercial Dashboard V1.0 chỉ PASS khi tất cả điều kiện sau đúng:

```
Architecture PASS

AND

Content PASS

AND

Visual PASS

AND

Experience PASS

AND

Desktop PASS

AND

Mobile PASS

AND

PDF PASS

AND

DOCX PASS

AND

Regression PASS

AND

Product Owner APPROVED
```

Thiếu bất kỳ điều kiện nào:

```
NOT PASS
```

---

# 36. Freeze Criteria

Chỉ sau Product Owner Approval mới tạo:

```
COMMERCIAL DASHBOARD V1.0
FINAL FROZEN
```

Sau Freeze:

- bug fix được phép;
- semantic change phải review;
- layout redesign phải mở package mới;
- không silent mutation.

---

# 37. Definition of Done

Definition of Done không phải:

"Code đã viết xong."

Không phải:

"Build PASS."

Không phải:

"Tests PASS."

Definition of Done là:

> Khách hàng nhìn thấy đúng trải nghiệm mà Commercial Dashboard Specification đã định nghĩa.

Và:

> Dashboard, PDF và DOCX kể cùng một câu chuyện từ cùng một nguồn dữ liệu.

---

# 38. FINAL ACCEPTANCE CHECKLIST

## Navigation

□ PASS

## View Chart Screen

□ PASS

## Identity Header

□ PASS

## Overview

□ PASS

## BaZi

□ PASS

## Five Elements

□ PASS

## Ten Gods

□ PASS

## Pattern

□ PASS

## ShenSha

□ PASS

## Luck

□ PASS

## Interpretation

□ PASS

## Action Plan

□ PASS

## Desktop

□ PASS

## Mobile

□ PASS

## PDF

□ PASS

## DOCX

□ PASS

## One Source of Truth

□ PASS

## Regression

□ PASS

## Product Owner Review

□ APPROVED

---

# 39. Final Verdict

Chỉ sử dụng một trong hai trạng thái:

```
COMMERCIAL DASHBOARD V1.0

ACCEPTED
```

hoặc:

```
COMMERCIAL DASHBOARD V1.0

NOT ACCEPTED
```

Không có trạng thái "gần PASS".

---

# 40. Nguyên tắc cuối cùng

Commercial Dashboard là sản phẩm mà khách hàng nhìn thấy.

Do đó:

> Technical correctness là điều kiện cần.

> Customer experience là điều kiện đủ.

Một implementation đúng code nhưng sai trải nghiệm vẫn là implementation thất bại.

Đây là Product Acceptance Standard chính thức của Commercial Dashboard V1.0.