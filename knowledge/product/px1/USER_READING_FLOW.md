# User Reading Flow — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1

---

## 1. Purpose

Define the canonical reading journey: what the user understands at each beat, in what order, and how the consultant voice leads.

Reading order is identical on every breakpoint.

---

## 2. Canonical flow

```
Hero
  ↓
Tóm tắt tư vấn
  ↓
Định hướng chính
  ↓
Lưu ý quan trọng
  ↓
Sự nghiệp
  ↓
Tài chính
  ↓
Quan hệ
  ↓
Sức khỏe
  ↓
Vận trình
  ↓
Biểu đồ minh họa
  ↓
Chi tiết kỹ thuật
  ↓
Kiến thức bổ sung
  ↓
Phụ lục
```

This sequence is mandatory.

---

## 3. Consultant script (experience metaphor)

The page should feel like this conversation:

| Beat | Consultant would say | User should feel |
|------|----------------------|------------------|
| Hero | “Đây là buổi tư vấn của anh/chị. Tinh thần chung như sau.” | Recognized, calm |
| Tóm tắt tư vấn | “Năm điều cần nắm trước khi đi vào chi tiết.” | Oriented |
| Định hướng chính | “Việc nên làm trước, theo từng mặt đời sống.” | Directed |
| Lưu ý quan trọng | “Có vài điểm không được chủ quan.” | Protected, not scared |
| Sự nghiệp → Vận trình | “Ta lần lượt xem từng lĩnh vực.” | Guided, not dumped |
| Biểu đồ minh họa | “Đây là bằng chứng trực quan cho những gì vừa nói.” | Confirmed |
| Chi tiết kỹ thuật | “Nếu muốn kiểm tra phần kỹ thuật, mở ở đây.” | In control |
| Kiến thức bổ sung | “Nếu muốn hiểu sâu thuật ngữ, đọc thêm.” | Invited, not tested |
| Phụ lục | “Phạm vi buổi này và cách đọc lại.” | Complete |

---

## 4. Timed map (first session)

| Time | Looks at | Understands |
|------|----------|-------------|
| 0–5s | Hero | Đúng người · đúng buổi tư vấn · một câu tinh thần |
| 5–25s | Tóm tắt tư vấn | Tối đa 5 điều cốt lõi |
| 25–60s | Định hướng chính | Việc nên làm trước, theo nhóm lĩnh vực |
| 60–80s | Lưu ý quan trọng | Rủi ro cần để ý |
| Next minutes | Five domains | Depth per life area, still advice-first |
| After advice is clear | Biểu đồ minh họa | Visual confirmation |
| On demand | Chi tiết kỹ thuật / Kiến thức | Apparatus and learning |
| Close | Phụ lục | Scope and return path |

If the user stops after Tóm tắt + Định hướng chính, the consultation has still delivered value.

---

## 5. Emotional arc

```
Arrival
  ↓
Recognition
  ↓
Understanding
  ↓
Direction
  ↓
Caution
  ↓
Domain depth
  ↓
Confirmation (charts)
  ↓
Optional mastery
  ↓
Reflection
```

Final emotion target:

> “Tôi hiểu tình huống của mình hơn và biết việc nên làm tiếp.”

Not:

> “Tôi vừa xem một bảng số.”

---

## 6. Progressive understanding vs page order

Experience Principles require: Overview → Evidence → Recommendation at the *unit* level.

PX-1 realizes this as:

| Layer | How “explain before act” is kept |
|-------|----------------------------------|
| Page | Overview (Hero + Tóm tắt) before action (Định hướng) |
| Card | Mỗi khuyến nghị: Vì sao → Kết quả kỳ vọng → Việc cần làm |
| Evidence | Charts after advice; technical collapsed |
| Learning | Knowledge after the journey |

Page-level charts-before-recs is **forbidden** in V2.

---

## 7. Interaction along the flow

| Moment | Allowed interaction | Forbidden interaction |
|--------|---------------------|------------------------|
| Hero | None required | Settings, export chrome as hero actions |
| Tóm tắt | Optional jump to Định hướng chính | Expand into essays |
| Định hướng | Expand one rec; one Primary CTA | Multiple primary buttons |
| Warnings | Expand mitigation | Dismiss without reading if severity is high — still readable |
| Domains | Expand analysis preview | Jump to charts mid-domain as the main path |
| Charts | Expand data table | Chart becoming a dashboard playground |
| Technical / Knowledge | Expand section | Auto-open on load |

Reading comes before interaction.  
Scrolling must feel like turning pages of a report, not hopping widgets.

---

## 8. Re-reading behavior

Return visitors may skip to a domain via TOC.

Rules:

- TOC never reorders sections  
- Deep links land on the same Vietnamese section titles  
- Collapsed sections stay collapsed until user opens them  
- Hero still confirms identity on every visit  

---

## 9. Anti-flows

| Anti-flow | Why it fails |
|-----------|--------------|
| Charts → tables → advice | Calculator |
| Technical strip → identity | Developer tool |
| Knowledge → recommendation | Classroom before consulting |
| All five domains equally loud with no Tóm tắt | Overwhelm |
| Warnings first | Fear, not trust |
| English headings then Vietnamese body | Mixed product |

---

## 10. Stop line

User reading flow V2 is canonical. Responsive layouts may not change it.

END
