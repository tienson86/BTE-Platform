# TV-01 — TƯ VẤN HÔN NHÂN
## 04_SCORE_ENGINE.md

**Document ID:** TV-01-04
**Module:** TV-01_MARRIAGE
**Product:** BTE Platform
**Document Type:** Score Engine Specification
**Status:** DRAFT FOR PRODUCT OWNER REVIEW
**Version:** 1.0

---

# 1. Mục tiêu

Score Engine có nhiệm vụ:

- chuyển Decision Result thành điểm số;
- chuẩn hóa điểm các domain;
- tính Overall Score;
- xác định Grade;
- xác định mức ổn định của kết quả.

Score Engine không:

- đọc Birth Input;
- đọc trực tiếp Tứ Trụ;
- đọc trực tiếp Can Chi;
- đọc trực tiếp Thập thần;
- tự tạo Evidence;
- tự tạo Finding.

Input duy nhất:

MarriageDecisionResult

---

# 2. Triết lý chấm điểm

TV-01 không trả lời:

"Hợp bao nhiêu %"

mà trả lời:

"Nền tảng hôn nhân mạnh đến mức nào."

Do đó:

Score

≠

Xác suất kết hôn.

Score

≠

Xác suất hạnh phúc.

Score phản ánh:

Structural Compatibility.

---

# 3. Overall Score

Overall Score

0–100

chia thành:

0–20

Very Weak

21–40

Weak

41–60

Mixed

61–80

Good

81–100

Excellent

---

# 4. Grade

Grade

A

Excellent

B

Good

C

Balanced / Mixed

D

Weak

E

Critical

Grade không được tính độc lập.

Grade luôn map từ Overall Score.

---

# 5. Input

Score Engine chỉ nhận:

MarriageScoreInput

bao gồm:

Domain States

Finding Sets

Evidence Mass

Confidence

Cross-domain Modifiers

Timing Modifiers

---

# 6. Domain Weight

V1 đề xuất:

Five Elements

20%

Stem / Branch

18%

Ten Gods

18%

Interaction

15%

Finance

10%

Family

8%

Children

4%

Timing

7%

Tổng

100%

---

# 7. Tại sao Five Elements cao nhất

Vì:

Useful God

Strength

Pattern

đều hội tụ tại đây.

Nếu cấu trúc nền không bổ trợ nhau

thì:

Thần sát đẹp

Cung Phi đẹp

Nạp âm đẹp

không cứu được.

---

# 8. Timing chỉ 7%

Timing

không được quyền

đổi

một hôn nhân tốt

thành

một hôn nhân xấu.

Timing chỉ điều chỉnh.

---

# 9. Secondary sources

Secondary

không có weight riêng.

Ví dụ

Shen Sha

không có:

5%

10%

20%

Shen Sha chỉ tạo modifier.

---

# 10. Modifier

Modifier có thể:

increase

decrease

limit

cap

rescue

amplify

Không bao giờ:

replace.

---

# 11. Score Pipeline

Domain States

↓

Domain Raw Score

↓

Structural Adjustment

↓

Cross-domain Adjustment

↓

Timing Adjustment

↓

Confidence Adjustment

↓

Overall Score

↓

Grade

---

# 12. Domain Raw Score

Mỗi Domain

được tính riêng.

Ví dụ

Five Elements

không phụ thuộc

Finance.

---

# 13. Structural Adjustment

Nếu

core finding

rất mạnh

thì

secondary finding

không được kéo điểm quá xa.

---

# 14. Cross-domain Adjustment

Ví dụ

Interaction

xấu

+

Family

xấu

↓

Penalty

---

Five Elements

tốt

+

Ten Gods

tốt

↓

Bonus

---

# 15. Timing Adjustment

Timing

chỉ điều chỉnh

trong giới hạn.

Ví dụ:

Natal

82

Timing

↓

79

hoặc

↓

84

Không:

82

↓

35

---

# 16. Confidence Adjustment

Confidence thấp

không làm giảm Compatibility.

Confidence thấp

chỉ:

- giảm certainty;
- giảm precision;
- giảm wording.

---

# 17. Structural Floor

Nếu

Structural Compatibility

quá thấp

Overall

không được vượt

một ngưỡng nhất định.

Ví dụ:

Core

35

thì

Overall

không thể

95

chỉ vì

Shen Sha.

---

# 18. Structural Ceiling

Ngược lại.

Core

rất mạnh

thì

một vài

secondary conflict

không được kéo xuống quá mạnh.

---

# 19. Rescue

Rescue

không xóa

damage.

Rescue

chỉ

giảm

severity.

---

# 20. Damage

Damage

không xóa

support.

Damage

làm giảm

effective score.

---

# 21. Mixed State

Nếu

Positive

≈

Negative

Domain

↓

Mixed

Không ép

Positive.

---

# 22. Domain Independence

Mỗi domain

được score

độc lập.

Cross-domain

chỉ

modifier.

---

# 23. Missing Data

Thiếu giờ sinh

↓

không tạo

Penalty.

Chỉ:

Confidence↓

Availability↓

---

# 24. Domain Availability

Unavailable

↓

không sinh

score.

Không mặc định:

50.

---

# 25. Score Normalization

Tất cả domain

được chuẩn hóa

0–100.

---

# 26. Overall Formula

Conceptually:

Overall

=

Weighted Structural

+

Cross-domain Modifier

+

Timing Modifier

+

Caps

Không hard-code công thức tại đây.

---

# 27. Grade Mapping

A

81–100

B

61–80

C

41–60

D

21–40

E

0–20

---

# 28. Modifier Limit

Timing

không quá ±5

Secondary

không quá ±3

Cross-domain

không quá ±8

(Các giá trị trên là **giới hạn thiết kế V1**, có thể tinh chỉnh sau khi kiểm chứng dữ liệu thực tế.)

---

# 29. Score Stability

Cùng:

Input

↓

Score

không đổi.

---

# 30. Explainability

Mỗi điểm

đều truy được:

Score

↓

Domain

↓

Finding

↓

Evidence

↓

Canonical Data

---

# 31. No Hidden Bonus

Không tồn tại:

magic bonus

hard bonus

secret score

---

# 32. Audit

Audit lưu:

Domain Score

Modifier

Caps

Overall

Grade

Confidence

---

# 33. Customer View

Khách hàng

chỉ thấy:

Overall

Grade

Domain

Highlights

Không thấy

internal modifier.

---

# 34. Expert View

Expert Mode

được phép xem:

Raw Domain Score

Modifier

Evidence Weight

Rule IDs

---

# 35. Future Expansion

TV-02

TV-03

TV-04

reuse

Score Engine.

Chỉ thay:

Decision Profile.

---

# 36. Anti-pattern

Không được:

Tam hợp

+

10

Xung

-

10

Nạp âm

+

5

Đào Hoa

+

8

Đó không phải Score Engine của BTE.

---

# 37. Core Rule

Score

không đo

"hai người có cưới nhau hay không."

Score đo

"nền tảng tương hợp của hai cấu trúc Bát Tự."

---

# 38. Acceptance Checklist

FREEZE khi:

- [ ] Domain Weight được Product Owner duyệt.
- [ ] Secondary không override Primary.
- [ ] Timing chỉ là modifier.
- [ ] Confidence độc lập.
- [ ] Missing hour không bị phạt compatibility.
- [ ] Có Structural Floor.
- [ ] Có Structural Ceiling.
- [ ] Có Explainability.
- [ ] Có Audit.
- [ ] Deterministic.

---

# 39. Status

TV-01-04 STATUS: DRAFT

Sau khi FREEZE:

→ `05_REPORT_ENGINE.md`