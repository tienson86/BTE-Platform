# NARRATIVE V2 — ACTION BUILDER

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Action Builder là Builder cuối cùng của Narrative V2.

Builder này chịu trách nhiệm chuyển toàn bộ Narrative thành những hành động mà khách hàng có thể áp dụng trong thực tế.

Action Builder không giải thích.

Action Builder không tính toán.

Action Builder không sinh tri thức mới.

Action Builder chỉ trả lời một câu hỏi:

> **"Tôi nên làm gì tiếp theo?"**

---

# 2. Mission

Action Builder phải biến:

```
Evidence

↓

Reasoning

↓

Meaning
```

thành:

```
Decision

↓

Action
```

Đây là Builder duy nhất trong Narrative V2 chịu trách nhiệm sinh hành động.

---

# 3. Design Philosophy

Action không phải:

- Summary.
- Interpretation.
- Report.

Action là:

```
Decision.
```

Một Decision có thể dẫn tới nhiều Action.

---

# 4. Action Formula

Builder luôn tuân thủ công thức:

```
Evidence

↓

Reasoning

↓

Meaning

↓

Decision

↓

Action

↓

Priority
```

Không Builder nào được bỏ qua bước Decision.

---

# 5. Builder Position

```
Commercial Rewrite

↓

Interpretation Builder

↓

Action Builder

↓

ActionPlanNarrative
```

Action luôn chạy sau Interpretation.

---

# 6. Builder Input

Input duy nhất:

```
CommercialRewriteContext

+

InterpretationNarrative
```

Không đọc trực tiếp Engine.

Không đọc CanonicalAnalysis.

---

# 7. Builder Output

```
ActionPlanNarrative
```

---

# 8. Action Architecture

Action gồm:

```
Top Priority

↓

Recommended Actions

↓

Warnings

↓

Current Period
```

Đây là cấu trúc chuẩn.

---

# 9. Decision Layer

Đây là Layer mới.

Builder phải tạo:

```
DecisionContext
```

DecisionContext trả lời:

```
Điều gì cần ưu tiên?
```

Không phải:

```
Làm gì?
```

Action chỉ xuất hiện sau khi Decision đã rõ.

---

# 10. Top Priority

Top Priority.

Chỉ một.

Không nhiều.

Top Priority là quyết định quan trọng nhất.

---

# 11. Recommended Actions

Action.

3–6 mục.

Mỗi Action.

Một ý.

Không Paragraph.

---

# 12. Warning

Warning.

Không Prediction.

Không Fear.

Chỉ:

```
Điều cần lưu ý.
```

---

# 13. Current Period

Nếu Narrative có.

↓

Builder sinh.

Không tự suy luận từ Đại Vận.

---

# 14. Builder Responsibilities

Builder được:

✓ Decision.

✓ Priority.

✓ Action.

✓ Warning.

Builder không:

✗ Rewrite.

✗ Interpretation.

✗ Engine.

---

# 15. Action Rules

Action phải:

- cụ thể;
- ngắn;
- thực hiện được.

---

# 16. Decision Rules

Decision luôn trước Action.

Ví dụ.

Sai.

```
Mở rộng kinh doanh.
```

Đúng.

```
Ưu tiên phát triển nền hiện tại.

↓

Chỉ mở rộng sau khi...
```

---

# 17. Priority Rules

Một.

Không nhiều.

---

# 18. Warning Rules

Warning.

Không Hung.

Không Cát.

Không Tuyệt đối.

---

# 19. Customer Language

Action.

Đọc.

↓

Làm được.

---

# 20. Technical Language

Không:

```
Bổ Hỏa.

↓

Dùng đỏ.
```

Nếu có.

↓

Rewrite.

---

# 21. Duplicate Rules

Action.

Không lặp.

Interpretation.

---

# 22. Commercial Rewrite

Action luôn đọc:

Commercial Rewrite.

---

# 23. Action Categories

Optional.

```
Career

Finance

Relationship

Health

Leadership
```

Không bắt buộc.

---

# 24. Reading Order

Khách hàng đọc.

```
Priority

↓

Actions

↓

Warning

↓

Current Period
```

---

# 25. Reading Time

Target.

1 phút.

---

# 26. Builder Validation

Validator.

✓ Action.

✓ Priority.

✓ Duplicate.

✓ Style.

---

# 27. Progressive Disclosure

Nếu Action.

>6.

↓

Expand.

---

# 28. Empty State

Không Action.

↓

Không publish.

---

# 29. Output Object

```
ActionPlanNarrative

top_priority

actions

warnings

current_period
```

---

# 30. Consumer

Dashboard.

PDF.

DOCX.

REST.

---

# 31. Performance

Deterministic.

---

# 32. Traceability

Action.

↓

Knowledge.

↓

Evidence.

---

# 33. Testing

Golden.

Semantic.

Snapshot.

---

# 34. Validation

Schema.

↓

Customer.

↓

Semantic.

↓

Publish.

---

# 35. Builder Independence

Action Builder.

Không biết.

Dashboard.

---

# 36. Freeze Rules

Không Builder nào sửa.

ActionPlanNarrative.

---

# 37. Action Responsibility Matrix

| Stage | Trách nhiệm |
|---------|-------------|
| Decision | Quyết định |
| Priority | Ưu tiên |
| Action | Hành động |
| Warning | Lưu ý |
| Current Period | Theo dõi |

---

# 38. Action Formula Validation

Action Validator.

Kiểm tra.

```
Evidence

↓

Reasoning

↓

Meaning

↓

Decision

↓

Action
```

Nếu Builder bỏ qua Decision.

↓

FAIL.

---

# 39. Quality Checklist

Một Action Plan đạt khi:

✓ Có Priority.

✓ Có Decision.

✓ Có Action.

✓ Không Prediction.

✓ Không Generic.

✓ Không Technical.

✓ Không Hung/Cát.

✓ Không JSON.

---

# 40. Final Principle

Action Builder không tồn tại để đưa ra lời khuyên.

Action Builder tồn tại để giúp khách hàng ra quyết định.

Nếu khách hàng đọc xong và biết:

> "Ngày mai mình sẽ bắt đầu từ việc gì."

Action Builder đã hoàn thành nhiệm vụ.

---

# 41. Action Formula Architecture

Action Builder không sinh Action trực tiếp.

Builder luôn đi qua:

```
Evidence

↓

Reasoning

↓

Meaning

↓

Decision

↓

Priority

↓

Action
```

Decision.

là trái tim.

Action.

chỉ là kết quả.

---

# 42. Decision Architecture

Decision luôn trả lời:

```
Điều gì quan trọng nhất?
```

Action trả lời:

```
Làm điều gì?
```

Hai khái niệm.

Khác nhau.

Không Builder nào được bỏ qua Decision.

---

# 43. Action Responsibility Matrix

| Layer | Trả lời |
|---------|----------|
| Evidence | Điều gì đúng? |
| Reasoning | Tại sao? |
| Meaning | Có ý nghĩa gì? |
| Decision | Điều gì cần ưu tiên? |
| Action | Làm gì? |

Đây là Formula chính thức của Action Builder.

---

# 44. Final Builder Principle

Narrative không kết thúc ở Interpretation.

Narrative chỉ hoàn thành khi:

Khách hàng hiểu.

↓

Khách hàng quyết định.

↓

Khách hàng hành động.

Đó là nhiệm vụ cuối cùng của Action Builder.

Nếu Action Builder không giúp khách hàng biết:

> "Việc đầu tiên mình nên làm là gì."

thì Narrative V2 vẫn chưa hoàn thành.
# 45. Decision vs Action Principle

Action Builder không được xây dựng theo tư duy:

```
Recommendation

↓

Action
```

Đó là cách tiếp cận của hầu hết các hệ thống sinh khuyến nghị hiện nay.

Narrative V2 sử dụng một tư duy khác.

```
Evidence

↓

Reasoning

↓

Meaning

↓

Decision

↓

Action
```

Action luôn là kết quả cuối cùng của một quá trình nhận thức.

Không bao giờ là điểm bắt đầu.

---

# 45.1 Why Decision Matters

Một người chỉ thực hiện hành động một cách bền vững khi họ hiểu vì sao mình phải làm điều đó.

Nếu Narrative chỉ tạo Action:

```
Nên làm...

Nên tránh...
```

khách hàng rất dễ làm theo một cách máy móc.

Sau một thời gian:

Action sẽ biến mất.

Nhưng nếu khách hàng đã thay đổi Decision:

Action sẽ tự nhiên xuất hiện.

Vì vậy.

Narrative phải thay đổi Decision trước.

Action sau.

---

# 45.2 Decision Layer

Decision Layer luôn trả lời:

> Điều gì là ưu tiên quan trọng nhất ở thời điểm này?

Decision không phải là hành động.

Decision là lựa chọn.

Ví dụ:

Sai.

```
Mở rộng kinh doanh.
```

Đó là Action.

Đúng.

```
Ưu tiên phát triển ổn định trên nền tảng hiện có.
```

Đó là Decision.

Sau đó mới sinh:

```
Hoàn thiện sản phẩm.

↓

Chuẩn hóa quy trình.

↓

Đánh giá kết quả.

↓

Mở rộng.
```

Đó mới là Action.

---

# 45.3 Decision Formula

Decision luôn được sinh theo công thức:

```
Evidence

↓

Reasoning

↓

Meaning

↓

Decision
```

Action Builder không được bỏ qua Decision.

Nếu không có Decision.

Action không được Publish.

---

# 45.4 Action Formula

Sau khi Decision đã được xác định.

Builder mới sinh:

```
Decision

↓

Priority

↓

Action

↓

Warning

↓

Current Period
```

Action luôn là hệ quả của Decision.

Không bao giờ ngược lại.

---

# 45.5 Decision Quality

Một Decision tốt phải:

✓ rõ ràng;

✓ có trọng tâm;

✓ không mâu thuẫn;

✓ không phụ thuộc giao diện;

✓ không phụ thuộc Presentation.

Decision là Narrative.

Không phải UI.

---

# 45.6 Action Quality

Một Action tốt phải:

✓ cụ thể;

✓ thực hiện được;

✓ có thể kiểm chứng;

✓ gắn với Decision;

✓ không chung chung.

Ví dụ.

Không nên:

```
Sống tích cực.
```

Đó không phải Action.

Nên:

```
Hoàn thiện quy trình đang triển khai trước khi mở thêm dự án mới.
```

Đó là Action.

---

# 45.7 Decision vs Recommendation

Recommendation:

```
Điều nên lưu ý.
```

Decision:

```
Điều nên lựa chọn.
```

Action:

```
Điều nên thực hiện.
```

Ba khái niệm này khác nhau.

Builder không được trộn lẫn.

---

# 45.8 Decision vs Prediction

Decision không dự đoán tương lai.

Decision chỉ xác định:

điều gì nên ưu tiên.

Prediction thuộc các tầng Narrative khác (nếu có).

Action Builder không được tạo Prediction.

---

# 45.9 Decision Traceability

Mỗi Decision đều phải truy ngược được:

```
Decision

↓

Meaning

↓

Reasoning

↓

Evidence

↓

Canonical Analysis
```

Nếu không truy ngược được.

Decision không được Publish.

---

# 45.10 Decision Validation

Validator phải kiểm tra:

✓ Decision có Evidence không.

✓ Decision có Meaning không.

✓ Decision có Priority không.

✓ Action có phụ thuộc Decision không.

Nếu Builder tạo Action mà không có Decision:

```
status = invalid
```

Không Publish.

---

# 45.11 Decision Independence

Decision không được sinh từ:

- UI;
- Dashboard;
- PDF;
- DOCX;
- REST;
- Frontend.

Decision chỉ được sinh trong Narrative.

Consumer chỉ đọc.

---

# 45.12 Decision Consistency

Một Decision chỉ có một cách diễn đạt chuẩn.

Ví dụ.

Nếu Decision đã chuẩn hóa:

```
Ưu tiên phát triển trên nền tảng hiện tại.
```

Không nơi khác được viết:

```
Nên duy trì như hiện nay.
```

hoặc:

```
Không nên thay đổi.
```

Decision phải thống nhất trên:

Dashboard

↓

PDF

↓

DOCX

↓

REST

---

# 45.13 Decision Lifecycle

```
Evidence

↓

Reasoning

↓

Meaning

↓

Decision

↓

Priority

↓

Action

↓

Publish
```

Đây là Lifecycle chuẩn.

---

# 45.14 Architectural Principle

Narrative không thay đổi cuộc sống của khách hàng bằng Action.

Narrative thay đổi cuộc sống của khách hàng bằng Decision.

Action chỉ là biểu hiện bên ngoài của Decision.

Nếu Decision đúng.

Action sẽ bền vững.

Nếu Decision sai.

Action chỉ mang tính tạm thời.

---

# 45.15 Final Principle

Action Builder không tồn tại để đưa ra nhiều việc phải làm.

Action Builder tồn tại để giúp khách hàng đưa ra quyết định đúng.

Khi Decision thay đổi.

Action sẽ thay đổi.

Khi Action thay đổi.

Kết quả mới thay đổi.

Đó là mục tiêu cuối cùng của Narrative V2.

> **Narrative không thay đổi cuộc đời khách hàng bằng lời khuyên.**
>
> **Narrative thay đổi cuộc đời khách hàng bằng cách giúp họ đưa ra những quyết định đúng hơn.**
