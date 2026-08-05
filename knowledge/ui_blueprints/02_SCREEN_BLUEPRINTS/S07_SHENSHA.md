BTE Platform
S07 Blueprint — ShenSha
Version: 1.0.0
Status: ACTIVE
Owner: Product Owner
Screen
BaZi Result
Depends On
BTE_UI_BIBLE.md
PORTAL_DESIGN_PHILOSOPHY.md
PORTAL_READING_FLOW.md
PORTAL_DECISION_FLOW.md
PORTAL_LAYOUT_SYSTEM.md
PORTAL_GRID_SYSTEM.md
PORTAL_SPACING_SYSTEM.md
PORTAL_VISUAL_HIERARCHY.md
PORTAL_TYPOGRAPHY_SYSTEM.md
PORTAL_SCREEN_SPECIFICATIONS.md

1. Purpose
S07 trình bày các Thần Sát xuất hiện trong lá số dưới góc nhìn Contextual Evidence.
Thần Sát được xem là tín hiệu bổ trợ.
Không phải bằng chứng chính.
Không phải kết luận.
Không phải Prediction.

2. Business Goal
Sau khi xem S07, người dùng phải hiểu:
Lá số có những Thần Sát nào.
Thần Sát nào đáng chú ý.
Mức độ xuất hiện của chúng.
Không đánh giá:
tốt
xấu
may
rủi

3. User Questions

S07 phải trả lời:
✓ Tôi có những Thần Sát nào?
✓ Thần Sát nào đáng chú ý?
✓ Những tín hiệu phụ nào đang xuất hiện?
Không trả lời:
Tôi sẽ gặp chuyện gì.
Tôi có vận hạn gì.
Tôi nên làm gì.
Hung hay cát.

4. Decision Goal
Sau S07,
người dùng phải hiểu:
"Tôi đã biết các tín hiệu phụ."
↓
Tiếp tục:
S08 Interpretation
5. Reading Goal
≤20 giây.
Reading Flow
ShenSha Summary

↓

Highlighted ShenSha

↓

All ShenSha

↓

Notes

↓

Interpretation
Không bắt đầu bằng danh sách dài.

6. Information Architecture
Zone A — Summary
Hiển thị:
Tổng số Thần Sát
Nhóm nổi bật
Nhận xét trung lập (1 câu)
Zone B — Highlighted ShenSha
Hiển thị 2–5 Thần Sát nổi bật.
Mỗi mục:
Tên
Nhóm
Mức độ xuất hiện
Không diễn giải.
Zone C — Complete ShenSha
Danh sách đầy đủ.
Mỗi Thần Sát:
Name
Category
Presence
Không đưa Prediction.
Zone D — Notes
Hiển thị:
2–5 ghi chú trung lập.
Ví dụ:
Xuất hiện nhiều Thần Sát hỗ trợ.
Có nhiều tín hiệu liên quan Quan Lộc.
Không viết luận giải.

7. Visual Hierarchy
Summary

↓

Highlighted ShenSha

↓

Complete List

↓

Notes
Summary luôn nổi bật nhất.
Danh sách chỉ là Evidence.
8. Layout Blueprint
Desktop
+------------------------------------------------------+

ShenSha Summary

-------------------------------------------------------

Highlighted ShenSha

-------------------------------------------------------

ShenSha Grid

-------------------------------------------------------

Notes

+------------------------------------------------------+
Tablet
Summary
↓
Highlights
↓
Grid
↓
Notes
Mobile
Summary
↓
Highlights
↓
Stack
↓
Notes
9. Component Composition
Cho phép:
Badge
Chip
StatCard
Tag
Tooltip
Divider
Không:
Hero
Pie Chart
Radar
Timeline
Accordion
10. Data Mapping
UI	Engine/API
Summary	Analysis.ShenSha.Summary
Highlighted	Analysis.ShenSha.Highlighted
Name	Analysis.ShenSha.Items.Name
Category	Analysis.ShenSha.Items.Category
Presence	Analysis.ShenSha.Items.Presence
Notes	Analysis.ShenSha.Notes


11. Typography Rules
Summary
→ HeadingPrimary
Highlighted
→ HeadingSecondary
Name
→ BodyPrimary
Notes
→ BodySecondary
Metadata
→ Caption
Không sử dụng Display Typography.

12. Interaction Rules
Cho phép:
Tooltip giải thích tên Thần Sát.
Mở Knowledge Panel.
Highlight khi hover.
Không:
Prediction.
Rule Detail.
Engine Debug.

13. Responsive Behaviour
Desktop
Grid.
Tablet
2 cột.
Mobile
Stack.
Reading Flow không đổi.

14. Accessibility
Tooltip truy cập bằng bàn phím.
Badge luôn có text.
Không dùng màu làm tín hiệu duy nhất.
Semantic List.

15. Anti-Patterns
Không được:
❌ Biến Thần Sát thành Prediction.
❌ Đưa "Hung/Cát".
❌ Đưa Recommendation.
❌ Đưa Luận giải.
❌ Dùng quá nhiều màu.
❌ Làm toàn bộ Thần Sát nổi bật.
❌ Tạo cảm giác mê tín.

16. Screenshot Acceptance
Cursor phải cung cấp:
Desktop Full

Desktop Zoom (S07)

Tablet

Mobile

Hover State

Design Rationale

17. Cursor Implementation Rules
Cursor không được:
thêm Hero
thêm Prediction
đổi Reading Flow
thêm Chart
Nếu dữ liệu chưa có,
sử dụng Placeholder đúng Blueprint.

18. Product Owner Review Checklist
Business
□ Hiểu đây là tín hiệu phụ.
Decision
□ Không gây hiểu nhầm.
Reading
□ Summary đọc trước.
Hierarchy
□ Highlight hợp lý.
Responsive
□ Desktop
□ Tablet
□ Mobile

19. Quality Scorecard
Category	Score
Summary Clarity	20
Context Clarity	20
Reading Flow	20
Responsive	20
Blueprint Compliance	20


95–100
PASS
80–94
PASS WITH CHANGES
<80
REJECT

20. Relationship
S07 sử dụng dữ liệu từ:
Four Pillars
Strength
Ten Gods
S07 là lớp Contextual Evidence.
Không tạo kết luận.
Không Prediction.
S07 chỉ cung cấp tín hiệu bổ trợ cho:
↓
S08 Interpretation

21. Version History
Version	Status	Description
1.0.0	ACTIVE	Initial ShenSha Blueprint


Appendix A — ShenSha Priority Matrix
Thành phần	Priority
Summary	10
Highlighted ShenSha	9
Complete List	7
Notes	5


Appendix B — Canonical Wireframe
┌──────────────────────────────────────────────────────┐
│ THẦN SÁT                                             │
│ Tổng cộng: 12 • Nổi bật: Thiên Đức, Văn Xương        │
├──────────────────────────────────────────────────────┤
│ Thiên Đức      ★                                    │
│ Văn Xương      ★                                    │
│ Thiên Ất Quý Nhân                                  │
├──────────────────────────────────────────────────────┤
│ [Grid các Thần Sát]                                 │
│ Tên • Nhóm • Có/Không                               │
├──────────────────────────────────────────────────────┤
│ Ghi chú: Có nhiều Thần Sát hỗ trợ học tập và quý nhân│
│ → Tiếp tục S08 để xem ý nghĩa tổng hợp.              │
└──────────────────────────────────────────────────────┘
Appendix C — Reading Path
Summary
      ↓
Highlighted ShenSha
      ↓
Complete ShenSha
      ↓
Notes
      ↓
S08 Interpretation

Appendix D — Contextual Evidence Boundary
S07 chỉ hiển thị Contextual Evidence.
Không hiển thị:
Dự đoán tương lai.
Hung/Cát.
Luận giải chi tiết.
Khuyến nghị hành động.
Dụng Thần.
Hỷ Thần.
Kỵ Thần.
Tất cả nội dung mang tính tổng hợp và diễn giải thuộc S08 Interpretation.

Appendix E — Common Mistakes
Các lỗi cần tránh:
Biến Thần Sát thành danh sách dài khó đọc.
Dùng ngôn ngữ khẳng định hoặc gây sợ hãi.
Làm tất cả Thần Sát có trọng số thị giác như nhau.
Thiếu Summary nên người dùng không biết điều gì đáng chú ý.
Trộn nội dung Thần Sát với phần luận giải.