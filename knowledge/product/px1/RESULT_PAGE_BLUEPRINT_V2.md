# Result Page Blueprint V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1  
Owner: BTE Product

---

## 1. Purpose

This is the master blueprint for the BTE Result Page experience V2.

All other PX-1 documents elaborate this file.  
Future implementation must preserve this composition.

---

## 2. Design thesis

The page is a guided consultation report.

An experienced consultant would:

1. Confirm who the client is  
2. State the situation in plain language  
3. Give the core direction  
4. Name important cautions  
5. Walk through life domains  
6. Show charts only as supporting evidence  
7. Keep technical apparatus available but quiet  
8. Offer optional learning  
9. Close with a calm appendix / next-step frame  

The interface must reproduce that sequence.

---

## 3. Canonical page composition

User-visible titles are Vietnamese only.

```
┌────────────────────────────────────────────────────────────┐
│  HERO                                                      │
│  Danh tính · Tiêu đề · Một câu tóm tắt · Trạng thái tư vấn │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  TÓM TẮT TƯ VẤN                                            │
│  Tối đa 5 gạch đầu dòng · mỗi gạch một câu · hướng hành động│
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  ĐỊNH HƯỚNG CHÍNH                                          │
│  Các khuyến nghị ưu tiên nhất, nhóm theo lĩnh vực          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  LƯU Ý QUAN TRỌNG                                          │
│  Cảnh báo có hậu quả nếu bỏ qua                            │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  SỰ NGHIỆP                                                 │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  TÀI CHÍNH                                                 │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  QUAN HỆ                                                   │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  SỨC KHỎE                                                  │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  VẬN TRÌNH                                                 │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  BIỂU ĐỒ MINH HỌA          (supporting evidence)           │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  CHI TIẾT KỸ THUẬT         (collapsed by default)          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  KIẾN THỨC BỔ SUNG         (collapsed · đọc thêm)          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  PHỤ LỤC                                                   │
└────────────────────────────────────────────────────────────┘

Footer
```

---

## 4. Hero rules

Hero contains **only**:

| Element | Vietnamese role | Purpose |
|---------|-----------------|---------|
| Identity | Danh tính | Who this consultation is for |
| Headline | Tiêu đề tư vấn | One professional headline |
| One-line summary | Câu tóm tắt | The essence in one sentence |
| Consultation status | Trạng thái tư vấn | Ready / in progress / limited — human language |

Hero **never** shows:

- timestamps  
- IDs  
- schema names  
- versions  
- engine names  
- timezone codes  
- calendar system labels as metadata  
- raw pillar strings as the hero message  

Those belong in **Chi tiết kỹ thuật**, collapsed.

---

## 5. Executive Summary rules

Section title: **Tóm tắt tư vấn**

- Most important section after Hero  
- Maximum **5 bullets**  
- Each bullet = **one sentence**  
- Action-oriented  
- No charts  
- No technical terms without a human gloss  
- No more than one idea per bullet  

The user must be able to restate the consultation after this section alone.

---

## 6. Core Recommendation rules

Section title: **Định hướng chính**

Top recommendations, grouped by:

| Group key | Visible title |
|-----------|---------------|
| career | Sự nghiệp |
| wealth | Tài chính |
| relationship | Quan hệ |
| health | Sức khỏe |
| luck | Vận trình |

Each recommendation card contains:

1. **Vì sao**  
2. **Kết quả kỳ vọng**  
3. **Việc cần làm**  
4. **Xem thêm** (expand)

See `CARD_SPECIFICATION.md` and `EXPANSION_MODEL.md`.

---

## 7. Warnings

Section title: **Lưu ý quan trọng**

Only risks that change a decision if ignored.

Not a dump of every analytical caveat.  
If nothing qualifies, use the empty-state pattern — do not invent drama.

---

## 8. Life-domain sections

Each domain deepens the matching recommendation group.

Order is fixed:

1. Sự nghiệp  
2. Tài chính  
3. Quan hệ  
4. Sức khỏe  
5. Vận trình  

Each domain may include:

- short domain framing (one question answered)  
- domain recommendation cards  
- optional analysis preview (expand for depth)  

Domains must not reopen Hero or dump charts.

---

## 9. Charts

Section title: **Biểu đồ minh họa**

Charts are **supporting evidence**.

They never appear before Định hướng chính.  
They never carry the primary advice.  
They never dominate visual weight.

Caption every chart in Vietnamese: what it shows and why it matters to the advice already given.

---

## 10. Technical information

Section title: **Chi tiết kỹ thuật**

Collapsed by default.

Contains all of:

- lịch / calendar  
- tứ trụ / pillars  
- múi giờ  
- schema  
- IDs  
- metadata  
- versions  

Visible only when the user chooses to inspect apparatus.

---

## 11. Knowledge

Section title: **Kiến thức bổ sung**

Optional. Collapsed. Entered via **Đọc thêm**.

Knowledge teaches. It does not sell.  
It never interrupts the advice journey.

---

## 12. Appendix

Section title: **Phụ lục**

Quiet close: scope of this consultation, how to reread, what is not covered.

No new primary CTA.  
No technical dump (that stays in Chi tiết kỹ thuật).

---

## 13. First viewport target

Within the first calm viewport the user should see:

1. Hero (identity + headline + one-line + status)  
2. Beginning of Tóm tắt tư vấn  

Within ~30 seconds of reading:

3. Full Tóm tắt tư vấn  
4. Start of Định hướng chính  

Never in first viewport:

- chart grids  
- pillar tables  
- schema / IDs  
- knowledge essays  

---

## 14. What this blueprint does not do

- Does not change Engine truth  
- Does not invent Design System tokens  
- Does not implement Portal  
- Does not rewrite frozen Foundation documents  

It defines the experience future implementation must realize.

---

## 15. Stop line

Result Page Blueprint V2 is the canonical composition for PX-1.

END
