BTE Platform
Portal Typography System
Version: 1.0.0
Status: ACTIVE
Owner: Product Owner
Depends On
BTE_UI_BIBLE.md
PORTAL_DESIGN_PHILOSOPHY.md
PORTAL_READING_FLOW.md
PORTAL_DECISION_FLOW.md
PORTAL_LAYOUT_SYSTEM.md
PORTAL_GRID_SYSTEM.md
PORTAL_SPACING_SYSTEM.md
PORTAL_VISUAL_HIERARCHY.md
Applies To
applications/customer_portal
Desktop
Tablet
Mobile
1. Purpose
Portal Typography System định nghĩa toàn bộ ngôn ngữ chữ viết của Portal BTE.
Typography không chỉ quy định:
Font Family
Font Size
Font Weight
Typography còn quy định:
Information Priority
Reading Rhythm
Decision Emphasis
Cognitive Load
Visual Communication
Typography phải giúp người dùng hiểu điều gì quan trọng mà không cần đọc toàn bộ nội dung.
2. Core Principle
Typography không tồn tại để trang trí.
Typography tồn tại để dẫn dắt sự chú ý.
Portal luôn tuân theo chuỗi:
Business Priority

↓

Information Priority

↓

Visual Hierarchy

↓

Typography
Không được chọn cỡ chữ chỉ vì "đẹp".
3. Typography Pyramid
Portal sử dụng 7 cấp Typography.
Level	Vai trò
Display	Hero Identity
H1	Section Title
H2	Card Title
H3	Group Title
Body	Nội dung chính
Supporting	Thông tin bổ trợ
Caption	Metadata


Không được bỏ cấp.
4. Reading Priority
Typography phải phản ánh đúng thứ tự đọc:
Display

↓

H1

↓

H2

↓

Body

↓

Supporting

↓

Caption
Người dùng không được đọc Metadata trước Body.
5. Identity Typography
Identity luôn là Typography mạnh nhất.
Ví dụ:
Nhật Chủ
Mệnh Chủ
Đánh giá tổng quan
Không có thành phần nào khác được phép nổi bật hơn Identity trong First Viewport.
### Typography Weight Matrix

### Typography Weight Matrix

Typography phải phản ánh đúng trọng số nhận thức (Cognitive Weight) của thông tin.

Portal không sử dụng kích thước chữ chỉ để tạo sự khác biệt về hình thức.

Mỗi cấp Typography phải tương ứng với giá trị nghiệp vụ mà thông tin đó mang lại.

| Information Type | Typography Weight | Priority |
|------------------|------------------:|----------|
| Identity | 10 | ★★★★★ |
| Decision | 9 | ★★★★★ |
| Condition | 8 | ★★★★☆ |
| Evidence | 6 | ★★★☆☆ |
| Interpretation | 5 | ★★★☆☆ |
| Supporting | 3 | ★★☆☆☆ |
| Metadata | 2 | ★☆☆☆☆ |
| Learning | 1 | ★☆☆☆☆ |

Typography phải luôn phản ánh đúng bảng trọng số này.

Ví dụ:

Identity luôn nổi bật hơn Evidence.

Decision luôn nổi bật hơn Metadata.

Metadata không được cạnh tranh thị giác với Hero.

Metadata không được nổi bật hơn Decision.

Evidence không được nổi bật hơn Identity.

6. Decision Typography
Decision không cần lớn nhất.
Decision cần dễ hiểu nhất.
Ví dụ:
Dụng Thần
Hỷ Thần
Kỵ Thần
What / Why / Next
Typography phải giúp Decision được nhận biết ngay sau Identity.
### Typography Decision Map

Typography không được thiết kế theo góc nhìn của lập trình viên.

Typography phải được thiết kế theo câu hỏi của người dùng.

| User Question | Primary Typography |
|---------------|--------------------|
| Tôi là ai? | Nhật Chủ (Identity) |
| Tôi mạnh hay yếu? | Thân Vượng / Nhược |
| Điều gì quan trọng nhất? | Dụng Thần / Hỷ Thần |
| Vì sao lại như vậy? | Four Pillars + Element Balance |
| Tôi nên làm gì? | Interpretation Summary |

Decision Typography phải giúp người dùng nhận ra câu trả lời chỉ bằng cách quét mắt, trước khi đọc toàn bộ nội dung.

Nếu Typography không giúp trả lời nhanh các câu hỏi này thì cần xem xét lại Hierarchy.

7. Evidence Typography
Evidence bao gồm:
Four Pillars
Five Elements
Strength
Ten Gods
ShenSha
Typography phải trung lập.
Không cạnh tranh với Identity hoặc Decision.

8. Interpretation Typography
Luận giải là nội dung dài.
Typography phải ưu tiên:
dễ đọc
khoảng nghỉ
scan nhanh
Không sử dụng đoạn văn quá dài.

9. Metadata Typography
Metadata luôn có trọng số thấp nhất.
Ví dụ:
Mã lá số
Phiên bản
Thời gian phân tích
ID
Metadata không được gây nhiễu.

10. Font Scale
Portal sử dụng một thang Typography duy nhất.
Token	Mục đích
Display	
H1	
H2	
H3	
Body	
Supporting	
Caption	
### Semantic Typography

### Semantic Typography

Blueprint không sử dụng Typography theo tên kỹ thuật (H1, H2, H3).

Blueprint phải sử dụng Typography theo vai trò nghiệp vụ.

| Semantic Role | Typography Token |
|---------------|-----------------|
| Identity | Display |
| Decision | HeadingPrimary |
| Condition | HeadingSecondary |
| Evidence | BodyPrimary |
| Interpretation | BodyPrimary |
| Supporting | BodySecondary |
| Metadata | Caption |

Điều này giúp Blueprint tập trung vào mục tiêu nghiệp vụ thay vì chi tiết trình bày.

React Implementation sẽ ánh xạ Semantic Role sang Typography Token cụ thể.

Không sử dụng trực tiếp H1/H2 khi mô tả nghiệp vụ.

Giá trị cụ thể được quản lý trong Design Tokens.
Blueprint chỉ sử dụng Token.

11. Font Weight
Portal chỉ sử dụng các mức chuẩn:
Weight	Mục đích
Regular	Nội dung
Medium	Hỗ trợ
Semibold	Heading
Bold	Hero


Không lạm dụng Bold.

12. Line Height
Line Height phải phục vụ khả năng đọc.
Nguyên tắc:
Heading: chặt hơn
Body: thoáng hơn
Interpretation: rộng nhất

13. Text Alignment
Portal ưu tiên:
Left Align
Không căn giữa các đoạn văn dài.
Không justify.

14. Reading Rhythm
### Canonical Scanning Pattern

### Canonical Scanning Pattern

Typography phải hỗ trợ ba giai đoạn quét thông tin.

#### Giai đoạn 1 (0–5 giây)

Identity

↓

Condition

↓

Decision

Người dùng phải hiểu:

- Tôi là ai.
- Tôi mạnh hay yếu.
- Điều gì quan trọng nhất.

---

#### Giai đoạn 2 (5–15 giây)

Overview

↓

Four Pillars

↓

Element Balance

Người dùng bắt đầu tìm hiểu nguyên nhân.

---

#### Giai đoạn 3 (15–60 giây)

Strength

↓

Ten Gods

↓

ShenSha

↓

Interpretation

↓

Learning

Typography phải giảm dần mức độ nhấn mạnh theo đúng thứ tự này.
Không để nhiều Heading liên tiếp.

15. Typography Anti-Patterns
Không được:
Hero quá nhỏ.
Metadata quá lớn.
Mọi tiêu đề đều Bold.
Quá nhiều chữ IN HOA.
Đổi font tùy ý.
Dùng quá nhiều kích thước chữ.

16. Typography Validation Checklist
□ Identity đọc đầu tiên.
□ Heading rõ ràng.
□ Body dễ đọc.
□ Metadata không gây nhiễu.
□ Decision nổi bật.
□ Interpretation không mỏi mắt.
### Attention Budget

Một Viewport không được tạo quá nhiều điểm nhấn Typography.

Giới hạn khuyến nghị:

| Typography Level | Maximum Visible |
|------------------|----------------:|
| Display | 1 |
| HeadingPrimary | 2 |
| HeadingSecondary | 4 |
| Body | Unlimited |
| Caption | Unlimited |

Nếu vượt quá giới hạn này, người dùng sẽ khó xác định đâu là thông tin quan trọng nhất.

---

### Typography Scorecard

Typography được đánh giá theo thang điểm 100.

| Category | Score |
|-----------|------:|
| Identity Visibility | 20 |
| Decision Visibility | 20 |
| Reading Rhythm | 20 |
| Information Priority | 20 |
| Consistency | 20 |

Kết quả đánh giá:

| Score | Decision |
|--------|----------|
| 95–100 | PASS |
| 80–94 | PASS WITH CHANGES |
| <80 | REJECT |

Typography Review phải được thực hiện trên ảnh chụp Desktop, Tablet và Mobile trước khi Product Owner phê duyệt.

17. Relationship
Typography System là nền tảng cho:
Component Library
Screen Blueprints
Report UI
Dashboard UI
Result UI
18. Typography Tokens
Blueprint chỉ sử dụng Typography Token.
Ví dụ:
Token	Mục đích
Display	
HeadingPrimary	
HeadingSecondary	
BodyPrimary	
BodySecondary	
Caption	
Label	


Không ghi trực tiếp:
18px
24px
32px
trong Blueprint.
19. Typography Evolution Policy
V1.x
Không đổi Pyramid.
Không đổi Token.
Có thể:
tinh chỉnh kích thước thực tế.
V2.x
bổ sung Token mới nếu cần.
Không loại bỏ Token cũ.
20. Typography Governance
Mọi thay đổi Typography phải:
Business Review

↓

Decision Review

↓

Blueprint Update

↓

Implementation

↓

Screenshot Review

↓

Freeze
Không sửa font trực tiếp trong React nếu chưa cập nhật Blueprint.
21. Closing Statement
Portal Typography không phải là một bộ quy định về font.
Đây là hệ thống truyền tải mức độ quan trọng của thông tin.
Mỗi chữ xuất hiện trên màn hình đều phải trả lời một câu hỏi:
"Dòng chữ này có giúp người dùng hiểu và đưa ra quyết định nhanh hơn không?"

Nếu câu trả lời là không, thì Typography cần được thiết kế lại.
Version History
Version	Status	Description
1.0.0	ACTIVE	Initial Canonical Portal Typography System