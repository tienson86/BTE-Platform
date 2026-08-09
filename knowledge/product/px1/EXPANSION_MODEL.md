# Expansion Model — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1

---

## 1. Purpose

Progressive disclosure is a BTE signature.

```
Preview
  ↓
Expand
  ↓
Detail
```

First load must feel complete as a consultation, not as a locked teaser wall.

---

## 2. Default states

| Surface | Default | After user intent |
|---------|---------|-------------------|
| Hero | Open | — |
| Tóm tắt tư vấn | Open (no expand for the 5 bullets) | Overflow not allowed — cut to 5 |
| Định hướng chính cards | Why / Expected / Action visible | Detail / longer How via **Xem thêm** |
| Lưu ý quan trọng | Title + essential caution visible | Mitigation depth via expand if long |
| Domain intro | Open | — |
| Domain analysis | Preview | **Xem phân tích chi tiết** |
| Charts | Figure + caption open | Heavy tables collapsed |
| Chi tiết kỹ thuật | **Collapsed** | Toggle opens panel |
| Kiến thức bổ sung | **Collapsed** | **Đọc thêm** |
| Phụ lục | Open, short | No nested mystery |

---

## 3. What must never be collapsed

- Hero identity, headline, one-liner, status  
- The five summary bullets  
- The visible Why / Expected Result / Action of top recommendations  
- Warning titles that change a decision  

Collapsing those turns the product into a scavenger hunt.

---

## 4. What must start collapsed

- Entire Chi tiết kỹ thuật  
- Entire Kiến thức bổ sung  
- Long How / 90-day detail  
- Heavy numeric tables under charts  
- Deep analysis essays  
- Schema, IDs, versions, timestamps, timezone, calendar apparatus  

---

## 5. Control pattern

Every expandable control:

1. Visible Vietnamese label  
2. Clear state: expanded vs collapsed  
3. Keyboard operable  
4. Does not move Primary CTA out of understanding  
5. Prefers in-place expand over modal  

Canonical labels:

| State change | Label |
|--------------|-------|
| Open more rec detail | **Xem thêm** |
| Close rec detail | **Thu gọn** |
| Open analysis | **Xem phân tích chi tiết** |
| Open chart table | **Xem bảng số liệu** |
| Open technical section | **Xem chi tiết kỹ thuật** |
| Close technical section | **Ẩn chi tiết kỹ thuật** |
| Open knowledge section | **Đọc thêm** |
| Open one knowledge card | **Đọc tiếp** |

No English “Show more” / “Read more” / “Details”.

---

## 6. Accordion rules

- Multiple recommendation cards may be expanded independently  
- Opening Technical does not auto-open Knowledge  
- Opening Knowledge does not scroll away Primary content without user control  
- Do not auto-expand anything on first load except the mandated open sections  

---

## 7. Motion intent

Motion supports orientation only.

- Short, calm expand  
- Respect reduced motion  
- No bounce, no confetti, no staggered card theatre  

Tokens / durations: Design System motion if present later — do not invent a motion brand in PX-1.

---

## 8. Content splitting rule

When content grows:

```
Split
  ↓
Collapse
  ↓
Navigate
```

Never shrink type below Body to avoid expand.  
Never hide the advice itself behind expand.

---

## 9. Stop line

Expansion realizes P3/P4 demotion without deleting truth.

END
