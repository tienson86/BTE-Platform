# 18_GOOD_AND_BAD_EXAMPLES.md

Version: 1.0

Status: DRAFT — Sprint C Writing System

Pack: 05 (Narrative Engine)

Depends on: Sprint A (frozen) · Sprint B (frozen) · `13`–`17`

---

# 1. Purpose

This document provides **illustrative** good vs bad writing contrasts.

Examples teach the writing system.

They are **not** runtime templates.

They are **not** approved sentence libraries for generation.

Do not copy these examples into engines as hard-coded output.

---

# 2. How to Use These Examples

| Use | Do not use |
|-----|------------|
| Train reviewers / writers | As production NLG templates |
| QA against tone/wording rules | As facts for a real chart |
| Clarify anti-patterns | As Evidence substitutes |

All “good” examples assume evidence exists. If evidence is missing, use Insufficient Evidence — do not force a “good” sentence.

---

# 3. Observation

**Bad (rule-engine leakage)**

> Áp dụng bảng trạng thái ngũ hành của mùa đã được xác định. Nếu chưa có Tiết khí thì xác định mùa theo Địa Chi tháng.

**Why bad:** Procedure text, not customer observation.

**Good (consultant observation pattern)**

> Nhật chủ và cục diện cho thấy một cấu trúc rõ nét, với các yếu tố nổi bật đã được khẳng định trong phần phân tích.

**Why good:** States what is seen; no invented specifics beyond a structural claim pattern.

---

# 4. Reasoning

**Bad (new inference / scoring voice)**

> Vì điểm số 51.25 nên chắc chắn sự nghiệp sẽ thất bại trong 3 năm tới.

**Why bad:** Invents timeline outcome; misuses score as prophecy.

**Good (explanation pattern)**

> Cục diện này được lý giải từ các yếu tố đã có trong luận giải: cấu trúc hỗ trợ và điểm hạn chế đi cùng nhau, chứ không đứng riêng lẻ.

**Why good:** Explains relationship without new predictions.

---

# 5. Impact

**Bad (fear / shame)**

> Bạn mang mệnh xấu, cuộc sống sẽ đổ vỡ nếu không mua dịch vụ nâng cấp.

**Why bad:** Shame + sales fear; unsupported escalation.

**Good (measured consequence pattern)**

> Ảnh hưởng thực tế là bạn cần cân bằng giữa thế mạnh đang có và các điểm dễ mất nhịp nếu chủ quan.

**Why good:** Human consequence, respectful, non-absolute.

---

# 6. Recommendation

**Bad (invented action / absolute)**

> Hãy chuyển nghề ngay lập tức sang ngành Thủy để đổi số.

**Why bad:** Invents career command; over-certain.

**Good (priority guidance pattern)**

> Ưu tiên phát huy đúng hướng đã được chỉ ra trong luận giải, thay vì dàn trải năng lực sang nhiều hướng xung đột.

**Why good:** Actionable, non-invented, consultant tone.

---

# 7. Warning

**Bad (panic)**

> Nếu không làm theo, thảm họa chắc chắn xảy ra.

**Why bad:** Absolute threat; not caution.

**Good (calm caution pattern)**

> Cần lưu ý các yếu tố dễ tạo lệch nhịp đã được nêu, để tránh quyết định nóng khi áp lực tăng.

**Why good:** Caution without doom.

---

# 8. Executive Summary slots

**Bad (developer / placeholder)**

> Nội dung luận giải sẽ được nối Interpretation Engine sau. (mock)

**Why bad:** Internal/product language.

**Bad (technical English labels)**

> Observation: … Explanation: … Critical

**Why bad:** UI/dev residue in customer narrative.

**Good (slot discipline pattern)**

- Identity: short who-statement from evidence  
- Strengths / weaknesses: short evidenced lists  
- Priority / next action: clear, single-focus guidance  

(Exact chart wording must come from that chart’s Evidence — not from this doc.)

---

# 9. Insufficient Evidence

**Bad (bluffing)**

> Dù thiếu dữ liệu, có thể khẳng định bạn hợp kinh doanh online.

**Why bad:** Invention masked as insight.

**Good (honest state)**

> Use the platform Insufficient Evidence outcome for that slot/component.

**Why good:** Honors Sprint B failure grammar.

---

# 10. Conclusion

**Bad (new claim at the end)**

> Ngoài ra, năm sau bạn sẽ gặp quý nhân lớn chưa từng xuất hiện trong phân tích.

**Why bad:** New unsupported conclusion.

**Good (closing pattern)**

> Điểm then chốt là giữ đúng hướng ưu tiên và kiểm soát các điểm cần lưu ý đã nêu ở trên.

**Why good:** Closes without new analysis.

---

# 11. Reminder

If an example ever conflicts with a real chart’s Evidence, **Evidence wins**.

Examples illustrate style — they do not authorize content.

---

END
