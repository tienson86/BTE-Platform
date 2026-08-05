# BTE Platform

# S05 Blueprint — Strength Analysis

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Screen

BaZi Result

Depends On

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_GRID_SYSTEM.md
- PORTAL_SPACING_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_TYPOGRAPHY_SYSTEM.md
- PORTAL_SCREEN_SPECIFICATIONS.md

---

# 1. Purpose

S05 giải thích vì sao hệ thống đánh giá:

- Thân Vượng
- Thân Trung Bình
- Thân Nhược

Đây là Analytical Evidence.

Không phải kết luận mới.

Không phải luận giải.

Không phải Recommendation.

---

# 2. Business Goal

Sau khi xem S05, người dùng phải hiểu:

- Điểm Strength được hình thành như thế nào.
- Những yếu tố nào ảnh hưởng nhiều nhất.
- Độ tin cậy của kết quả.
- Vì sao hệ thống đưa ra kết luận ở S01.

S05 tăng niềm tin vào Analysis Engine.

---

# 3. User Questions

S05 phải trả lời:

✓ Vì sao tôi được đánh giá Thân Vượng/Nhược?

✓ Điểm số được tính như thế nào?

✓ Yếu tố nào ảnh hưởng mạnh nhất?

✓ Kết quả này có đáng tin không?

Không trả lời:

- Dụng Thần
- Hỷ Thần
- Luận giải
- Khuyến nghị

---

# 4. Decision Goal

Sau S05 người dùng phải có cảm giác:

"Tôi hiểu cơ sở của kết luận."

↓

Tiếp tục:

S06 Ten Gods

---

# 5. Reading Goal

≤30 giây.

Reading Flow

```
Strength Summary

↓

Score

↓

Confidence

↓

Contributing Factors

↓

Evidence Notes
```

Không bắt đầu bằng bảng số liệu.

---

# 6. Information Architecture

## Zone A — Strength Summary

Hiển thị:

- Thân Vượng / Trung Bình / Nhược
- Điểm Strength
- Confidence

Một câu tóm tắt trung lập.

---

## Zone B — Strength Score

Hiển thị:

- Score
- Progress Bar
- Mức đánh giá

Không hiển thị công thức.

---

## Zone C — Contributing Factors

Hiển thị các yếu tố chính ảnh hưởng:

- Mùa sinh
- Nhật Chủ
- Ngũ Hành
- Thiên Can
- Địa Chi
- Tàng Can

Chỉ hiển thị mức độ ảnh hưởng.

Không hiển thị toàn bộ Rule Engine.

---

## Zone D — Confidence

Hiển thị:

- Confidence %
- Data Completeness
- Rule Coverage

---

## Zone E — Evidence Notes

Hiển thị:

2–5 ghi chú ngắn.

Ví dụ:

"Mùa sinh hỗ trợ Nhật Chủ."

"Tàng Can tăng sức mạnh Kim."

Không viết luận giải dài.

---

# 7. Visual Hierarchy

```
Strength Summary

↓

Strength Score

↓

Confidence

↓

Contributing Factors

↓

Evidence Notes
```

Score không được nổi hơn Summary.

Confidence không được nổi hơn Score.

---

# 8. Layout Blueprint

Desktop

```
+------------------------------------------------------+

Strength Summary

-------------------------------------------------------

Score

Progress

-------------------------------------------------------

Factors

-------------------------------------------------------

Confidence

-------------------------------------------------------

Evidence Notes

+------------------------------------------------------+
```

Tablet

Summary

↓

Score

↓

Factors

↓

Confidence

↓

Notes

Mobile

Stack hoàn toàn.

---

# 9. Component Composition

Cho phép:

- ProgressBar
- ScoreBar
- StatCard
- Badge
- Confidence Indicator
- Factor List
- Divider

Không:

- Pie Chart
- Radar Chart
- Timeline
- Hero
- Accordion

---

# 10. Data Mapping

| UI | Engine/API |
|-----|------------|
| Strength Level | Analysis.Strength.Level |
| Strength Score | Analysis.Strength.Score |
| Confidence | Analysis.Strength.Confidence |
| Factor List | Analysis.Strength.Factors |
| Evidence Notes | Analysis.Strength.Notes |
| Rule Coverage | Analysis.Strength.RuleCoverage |

---

# 11. Typography Rules

Strength Summary

→ HeadingPrimary

Strength Score

→ HeadingSecondary

Factor

→ BodyPrimary

Evidence Notes

→ BodySecondary

Confidence

→ Caption

Không sử dụng Display Typography.

---

# 12. Interaction Rules

Cho phép:

- Tooltip từng Factor.
- Xem chi tiết Rule (nếu có).
- Điều hướng tới Knowledge.

Không:

- Chỉnh sửa Score.
- Chỉnh Confidence.
- Mở Rule Engine.

---

# 13. Responsive Behaviour

Desktop

Summary + Score nổi bật.

Tablet

Stack.

Mobile

Một cột.

Reading Flow giữ nguyên.

---

# 14. Accessibility

- ProgressBar có giá trị text.
- Confidence có mô tả đầy đủ.
- Tooltip truy cập được bằng bàn phím.
- Không dùng màu sắc làm tín hiệu duy nhất.

---

# 15. Anti-Patterns

Không được:

❌ Hiển thị công thức tính.

❌ Hiển thị Rule JSON.

❌ Hiển thị hàng trăm Rule.

❌ Đưa Recommendation.

❌ Đưa Dụng Thần.

❌ Đưa Luận giải.

❌ Quá nhiều ProgressBar.

---

# 16. Screenshot Acceptance

Cursor phải gửi:

1. Desktop Full

2. Desktop Zoom (S05)

3. Tablet

4. Mobile

5. Hover State

6. Design Rationale

---

# 17. Cursor Implementation Rules

Cursor không được:

- thêm Chart
- thêm Hero
- đổi Reading Flow
- đổi Score Layout

Nếu dữ liệu chưa có:

sử dụng Placeholder đúng Blueprint.

---

# 18. Product Owner Review Checklist

Business

□ Hiểu vì sao có kết luận.

Decision

□ Tin tưởng kết quả.

Reading

□ Summary đọc đầu tiên.

Hierarchy

□ Score rõ.

Responsive

□ Desktop

□ Tablet

□ Mobile

---

# 19. Quality Scorecard

| Category | Score |
|----------|------:|
| Strength Clarity | 20 |
| Evidence Clarity | 20 |
| Reading Flow | 20 |
| Responsive | 20 |
| Blueprint Compliance | 20 |

95–100

PASS

80–94

PASS WITH CHANGES

<80

REJECT

---

# 20. Relationship

S05 sử dụng dữ liệu từ:

- S03 Four Pillars
- S04 Element Balance

S05 tạo nền tảng cho:

S06 Ten Gods

↓

S07 ShenSha

↓

S08 Interpretation

Strength Analysis là Evidence quan trọng nhất để hỗ trợ Decision Panel tại S01.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Strength Analysis Blueprint |

bổ sung 5 phụ lục

Appendix A – Strength Priority Matrix
Thành phần	Priority
Strength Summary	10
Score	9
Confidence	8
Contributing Factors	7
Evidence Notes	5


Appendix B – Canonical Wireframe
┌──────────────────────────────────────────────────────┐
│ THÂN VƯỢNG                                           │
│ Điểm Strength: 86 • Confidence: 92%                  │
├──────────────────────────────────────────────────────┤
│ ████████████ 86/100                                  │
├──────────────────────────────────────────────────────┤
│ Yếu tố chính                                         │
│ • Mùa sinh hỗ trợ                                    │
│ • Nhật Chủ được sinh                                │
│ • Kim chiếm ưu thế                                   │
├──────────────────────────────────────────────────────┤
│ Confidence: Cao                                      │
│ Rule Coverage: 98%                                   │
├──────────────────────────────────────────────────────┤
│ Ghi chú                                              │
│ • Mùa sinh tăng sức mạnh Nhật Chủ                    │
│ • Tàng Can bổ trợ đáng kể                            │
└──────────────────────────────────────────────────────┘

Appendix C – Reading Path
Strength Summary
        ↓
Strength Score
        ↓
Confidence
        ↓
Contributing Factors
        ↓
Evidence Notes
        ↓
S06 Ten Gods

Appendix D – Evidence Boundary
S05 chỉ trình bày Analytical Evidence.
Không hiển thị:
Dụng Thần.
Hỷ Thần.
Kỵ Thần.
Thập Thần.
Thần Sát.
Luận giải chi tiết.
Khuyến nghị hành động.
Điều này giữ ranh giới rõ ràng giữa phần phân tích và phần diễn giải.

Appendix E – Common Mistakes
Các lỗi cần tránh:
Biến S05 thành màn hình "điểm số" đơn thuần.
Hiển thị quá nhiều chi tiết kỹ thuật của Rule Engine.
Đưa công thức tính điểm hoặc dữ liệu debug lên giao diện.
Lặp lại kết luận đã có ở S01 thay vì giải thích nguyên nhân.
Thiếu mối liên hệ rõ ràng giữa S03, S04 và kết quả Strength.