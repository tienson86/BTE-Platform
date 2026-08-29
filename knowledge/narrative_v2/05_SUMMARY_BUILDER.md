# NARRATIVE V2 — SUMMARY BUILDER

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Summary Builder là Builder đầu tiên của Narrative V2.

Summary Builder chịu trách nhiệm tạo:

```
overview_summary
```

được sử dụng bởi:

- Dashboard Overview
- PDF Executive Summary
- DOCX Executive Summary
- Mobile Overview
- API Overview

Summary Builder không sinh:

Interpretation.

Không sinh:

Action.

Không sinh:

Commercial Consulting.

---

# 2. Mission

Summary Builder phải trả lời duy nhất một câu hỏi:

> Nếu khách hàng chỉ đọc đúng một đoạn duy nhất trong toàn bộ báo cáo thì họ phải hiểu điều gì?

Đây là nhiệm vụ của Executive Summary.

---

# 3. Design Philosophy

Summary không phải:

- liệt kê dữ liệu;
- ghép Engine;
- tóm tắt Report.

Summary là:

```
Insight.
```

Một Summary tốt giúp khách hàng:

- hiểu mình là ai;
- hiểu điểm nổi bật nhất;
- muốn đọc tiếp.

---

# 4. Builder Position

```
Evidence

↓

Reasoning

↓

Knowledge

↓

Commercial Rewrite

↓

Summary Builder

↓

OverviewSummary
```

Summary luôn chạy sau Rewrite.

Không đọc trực tiếp Engine.

---

# 5. Builder Input

Input duy nhất:

```
CommercialRewriteContext
```

Không nhận:

CanonicalAnalysis.

---

# 6. Builder Output

```
OverviewSummary
```

---

# 7. Summary Architecture

OverviewSummary gồm:

```
Headline

↓

Executive Summary

↓

Identity Summary

↓

Balance Summary

↓

Executive Conclusion
```

---

# 8. Headline

Headline là câu đầu tiên.

Không quá:

25 từ.

Headline không chứa:

JSON.

Thuật ngữ kỹ thuật.

---

# 9. Executive Summary

Executive Summary.

2–4 câu.

Đây là phần khách hàng đọc đầu tiên.

---

# 10. Identity Summary

Identity Summary.

Chỉ giữ:

- Nhật Chủ
- Thân
- Mệnh Cục

Không giải thích dài.

---

# 11. Balance Summary

Balance Summary.

Chỉ giữ:

- Dụng Thần
- Điều Hậu

Không Recommendation.

---

# 12. Executive Conclusion

Một kết luận.

Không quá:

2 câu.

Không Action.

---

# 13. Source Priority

Summary chỉ được đọc:

CommercialRewriteContext.

Không đọc Engine.

---

# 14. Builder Responsibilities

Builder được phép:

✓ chọn Insight.

✓ chọn Headline.

✓ chọn Conclusion.

Builder không được:

✗ rewrite.

✗ reasoning.

✗ recommendation.

---

# 15. Headline Rules

Headline phải:

- rõ;
- ngắn;
- cụ thể;
- không học thuật.

Ví dụ:

Không:

```
Thân vượng.
```

Nên:

```
Bạn có nội lực tốt và thiên về xây dựng nền tảng ổn định.
```

---

# 16. Executive Rules

Executive Summary.

40–90 từ.

Không Bullet.

Không Table.

---

# 17. Identity Rules

Identity Summary.

Không lặp.

Interpretation.

---

# 18. Balance Rules

Balance.

Không lặp.

Action.

---

# 19. Conclusion Rules

Conclusion.

Không tiên tri.

Không tuyệt đối.

---

# 20. Customer Language

Summary phải:

- đời thường;
- chuyên nghiệp;
- dễ hiểu.

---

# 21. Technical Language

Không xuất hiện:

- Chính Ấn.
- Kiếp Tài.
- Rule.

Nếu có.

Phải giải thích.

---

# 22. Duplicate Rules

Summary.

Không lặp.

Interpretation.

---

# 23. Length Rules

Headline

↓

1 câu.

Executive

↓

2–4 câu.

Conclusion

↓

2 câu.

---

# 24. Reading Time

Target:

20–30 giây.

---

# 25. Builder Validation

Validator kiểm tra:

✓ Length

✓ Duplicate

✓ Style

✓ Customer

---

# 26. Empty State

Không có Summary.

↓

Không publish.

---

# 27. Output Object

```
OverviewSummary

headline

summary

identity

balance

conclusion
```

---

# 28. Consumer

Dashboard.

PDF.

DOCX.

REST.

---

# 29. Forbidden

Không đọc:

Strength.

Pattern.

TenGod.

ShenSha.

trực tiếp.

---

# 30. Pipeline

```
Rewrite

↓

Summary

↓

Publish
```

---

# 31. Testing

Golden.

CASE.

Snapshot.

---

# 32. Validation

Schema.

Semantic.

Style.

---

# 33. Performance

Deterministic.

---

# 34. Traceability

Headline.

↓

Knowledge.

↓

Evidence.

---

# 35. Acceptance

Summary đạt khi:

✓ đọc 30 giây.

↓

hiểu.

---

# 36. Freeze Rules

Không Builder nào được sửa:

OverviewSummary.

---

# 37. Responsibility Matrix

| Thành phần | Trách nhiệm |
|------------|-------------|
| Summary Builder | Executive Summary |
| Rewrite | Ngôn ngữ |
| Interpretation | Giải thích |
| Action | Hành động |

---

# 38. Executive Summary Principles

Summary phải:

- dẫn dắt;
- không giải thích hết;
- tạo động lực đọc tiếp.

---

# 39. Quality Checklist

Một Summary tốt phải:

✓ đọc một lần là hiểu.

✓ không học thuật.

✓ không kỹ thuật.

✓ không lặp.

✓ không Action.

✓ không Prediction.

---

# 40. Final Principle

Summary Builder không tồn tại để tóm tắt dữ liệu.

Summary Builder tồn tại để tạo ra góc nhìn đầu tiên về toàn bộ lá số.

Nếu khách hàng đọc xong Executive Summary và nói:

> "Đúng là mình."

thì Summary Builder đã hoàn thành nhiệm vụ.
# 41. Executive Summary Formula

Executive Summary không được sinh theo cảm hứng.

Executive Summary phải được tạo theo một công thức thống nhất trên toàn bộ hệ thống.

Mọi Overview Summary của BTE đều phải tuân theo cùng một Narrative Formula.

Điều này giúp:

- Dashboard luôn nhất quán;
- PDF luôn nhất quán;
- DOCX luôn nhất quán;
- khách hàng luôn có cùng trải nghiệm.

---

# 41.1 Executive Formula

Executive Summary luôn được xây dựng theo pipeline:

```
Evidence
        ↓
Insight
        ↓
Meaning
        ↓
Commercial Rewrite
        ↓
Executive Summary
```

Đây là công thức chuẩn.

Không Builder nào được bỏ qua bước.

---

# 41.2 Evidence Stage

Builder trước tiên chỉ được đọc:

```
CommercialRewriteContext
```

Trong đó đã bao gồm:

- Identity
- Strength
- Pattern
- Useful God
- Temperature
- Five Elements
- Ten Gods
- ShenSha
- Luck

Builder không được đọc trực tiếp Engine.

---

# 41.3 Insight Stage

Từ Evidence.

Builder chọn:

một Insight quan trọng nhất.

Ví dụ:

```
Nội lực.

↓

Khả năng tổ chức.

↓

Khả năng học hỏi.

↓

Tính ổn định.
```

Chỉ chọn:

một.

Không nhiều.

Executive Summary luôn có một trọng tâm.

---

# 41.4 Meaning Stage

Insight phải được chuyển thành ý nghĩa.

Ví dụ:

Không:

```
Thân vượng.
```

Mà:

```
Bạn có nội lực tốt.
```

Hoặc.

Không:

```
Chính Ấn.
```

Mà:

```
Bạn có xu hướng làm việc theo hệ thống.
```

Meaning luôn trả lời:

> Điều này có ý nghĩa gì?

---

# 41.5 Commercial Rewrite Stage

Meaning sau đó được Rewrite.

Ví dụ.

```
Bạn có nội lực.

↓

Bạn thường chủ động nhận trách nhiệm và có xu hướng xây dựng nền tảng ổn định trước khi mở rộng.
```

Commercial Rewrite không được thay đổi ý nghĩa.

Chỉ thay đổi cách diễn đạt.

---

# 41.6 Executive Summary Stage

Đầu ra cuối cùng.

Executive Summary luôn gồm bốn thành phần.

```
Identity

↓

Core Strength

↓

Core Characteristic

↓

Executive Conclusion
```

Ví dụ.

```
Bạn là người có nội lực tốt.

Bạn phát huy hiệu quả khi làm việc có hệ thống.

Điểm nổi bật của lá số là khả năng duy trì sự ổn định trong các mục tiêu dài hạn.

Đây là nền tảng quan trọng để phát triển sự nghiệp theo hướng bền vững.
```

Đây chỉ là ví dụ về cấu trúc.

Không phải template cố định.

---

# 41.7 Formula Rules

Executive Summary phải tuân thủ:

✓ chỉ một Insight chính.

✓ không nhiều hơn một Executive Conclusion.

✓ không Action.

✓ không Prediction.

✓ không Recommendation.

Recommendation thuộc Interpretation.

Action thuộc Action Plan.

---

# 41.8 Forbidden Formula

Executive Summary không được tạo theo:

```
Strength

+

Pattern

+

Useful God

+

Ten Gods

↓

Paragraph
```

Đó là cách ghép dữ liệu.

Không phải Executive Summary.

---

Không được:

```
Liệt kê.

↓

Giải thích.

↓

Liệt kê.

↓

Giải thích.
```

Executive Summary phải có một dòng chảy tự nhiên.

---

# 41.9 Executive Reading Order

Khách hàng phải đọc theo thứ tự:

```
Identity

↓

Insight

↓

Meaning

↓

Conclusion
```

Nếu đảo thứ tự.

Narrative sẽ mất mạch.

---

# 41.10 Executive Density

Một Executive Summary chuẩn:

Headline

↓

1 câu.

Executive Summary

↓

2–4 câu.

Identity Summary

↓

3–5 từ khóa.

Balance Summary

↓

2–3 từ khóa.

Executive Conclusion

↓

1–2 câu.

Không nhiều hơn.

---

# 41.11 Executive Consistency

Mọi Executive Summary của toàn bộ BTE phải cùng cấu trúc.

Không Builder nào được tự sáng tạo format mới.

Sự khác biệt chỉ nằm ở:

- Insight;
- Meaning;
- Rewrite.

Không nằm ở cấu trúc.

---

# 41.12 Executive Quality Checklist

Một Executive Summary chỉ được Publish khi:

✓ Có đúng một Insight chính.

✓ Có Meaning rõ ràng.

✓ Có Commercial Rewrite.

✓ Có Executive Conclusion.

✓ Không lặp Interpretation.

✓ Không Recommendation.

✓ Không Action.

✓ Không Prediction.

✓ Không Technical Language.

---

# 41.13 Formula Validation

Summary Validator phải kiểm tra:

✓ Có đúng Pipeline.

✓ Có đúng Formula.

✓ Có đúng số lượng Insight.

✓ Có đúng Executive Conclusion.

Nếu Builder vi phạm Formula.

↓

```
status = invalid
```

Không Publish.

---

# 41.14 Final Formula Principle

Executive Summary không phải là nơi chứa nhiều dữ liệu nhất.

Executive Summary là nơi chứa:

**Insight quan trọng nhất.**

Mọi Executive Summary đều phải trả lời đúng một câu hỏi:

> **"Nếu khách hàng chỉ đọc đúng phần này thì họ sẽ hiểu điều gì quan trọng nhất về chính mình?"**

Nếu không trả lời được câu hỏi đó.

Executive Summary chưa hoàn thành nhiệm vụ.

Narrative V2 chỉ được coi là thành công khi mọi Executive Summary đều được tạo ra từ cùng một Formula thống nhất, thay vì từ những đoạn văn ghép ngẫu nhiên.
---

# 41.15 Formula Architecture

Executive Summary Formula không phải là một công thức riêng của Summary Builder.

Đây là mẫu tư duy chuẩn của toàn bộ Narrative V2.

Mọi Narrative Builder trong hệ thống đều phải hoạt động theo cùng một triết lý:

```
Evidence
        ↓
Insight
        ↓
Meaning
        ↓
Commercial Rewrite
        ↓
Customer Narrative
```

Điều thay đổi giữa các Builder không phải là Pipeline.

Điều thay đổi là loại Narrative được tạo ra.

---

## Summary Builder

```
Evidence
        ↓
Insight
        ↓
Meaning
        ↓
Commercial Rewrite
        ↓
Executive Summary
```

Trả lời:

> Điều gì quan trọng nhất?

---

## Interpretation Builder

```
Evidence
        ↓
Reasoning
        ↓
Meaning
        ↓
Commercial Rewrite
        ↓
Interpretation
```

Trả lời:

> Điều này có ý nghĩa gì?

---

## Action Builder

```
Evidence
        ↓
Reasoning
        ↓
Recommendation
        ↓
Commercial Rewrite
        ↓
Action Plan
```

Trả lời:

> Tôi nên làm gì tiếp theo?

---

## Commercial Builder

```
Evidence
        ↓
Domain Reasoning
        ↓
Commercial Rewrite
        ↓
Commercial Consulting
```

Trả lời:

> Trong từng lĩnh vực cụ thể, tôi nên tiếp cận như thế nào?

---

# Formula vs Pipeline

Narrative V2 sử dụng đồng thời hai khái niệm:

## Pipeline

Pipeline quy định:

> Builder chạy theo thứ tự nào.

Ví dụ:

```
Evidence

↓

Reasoning

↓

Knowledge

↓

Rewrite

↓

Builders

↓

Validation

↓

Publish
```

Pipeline quản lý Runtime.

---

## Formula

Formula quy định:

> Builder tạo Narrative theo công thức nào.

Ví dụ:

```
Evidence

↓

Meaning

↓

Commercial Rewrite

↓

Executive Summary
```

Formula quản lý tư duy Narrative.

---

# Architectural Principle

Pipeline quyết định:

**Runtime Flow**

Formula quyết định:

**Narrative Thinking**

Một Builder chỉ được coi là hoàn thành khi:

✓ chạy đúng Pipeline;

✓ tuân thủ đúng Formula.

Nếu chỉ đúng Pipeline mà sai Formula:

Narrative vẫn chưa đạt chất lượng thương mại.

---

# Final Formula Principle

Narrative V2 không sinh câu theo Template.

Narrative V2 sinh câu theo Formula.

Template chỉ quyết định hình thức.

Formula quyết định cách tư duy.

Đây là khác biệt lớn nhất giữa Narrative V2 và các hệ thống chỉ ghép câu theo mẫu.

Mọi Builder trong Narrative V2 phải được xây dựng dựa trên Formula trước khi lựa chọn Template.