# Section Priority — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1

---

## 1. Purpose

Rank every Result section by consulting value.

Higher priority wins space, type weight, and default openness.  
Lower priority is quieter, denser, or collapsed.

---

## 2. Priority bands

| Band | Name | Job |
|------|------|-----|
| **P1** | Decide with me | Identity, summary, core direction |
| **P2** | Protect and deepen | Warnings + five life domains |
| **P3** | Confirm | Charts as evidence |
| **P4** | Inspect / learn | Technical, knowledge, appendix |

---

## 3. Full ranking

| Rank | Section | Band | Default |
|-----:|---------|------|---------|
| 1 | Hero | P1 | Always visible, compact |
| 2 | Tóm tắt tư vấn | P1 | Always visible — highest content priority |
| 3 | Định hướng chính | P1 | Always visible |
| 4 | Lưu ý quan trọng | P2 | Visible when content exists |
| 5 | Sự nghiệp | P2 | Visible |
| 6 | Tài chính | P2 | Visible |
| 7 | Quan hệ | P2 | Visible |
| 8 | Sức khỏe | P2 | Visible |
| 9 | Vận trình | P2 | Visible |
| 10 | Biểu đồ minh họa | P3 | Visible but quiet |
| 11 | Chi tiết kỹ thuật | P4 | **Collapsed** |
| 12 | Kiến thức bổ sung | P4 | **Collapsed** |
| 13 | Phụ lục | P4 | Visible, minimal |
| 14 | Footer | P4 | Minimal chrome |

Within P2 domains, **Sự nghiệp** is the default commercial lead when capabilities compete. Other domains remain first-class in reading order; they do not outshout Career visually.

---

## 4. Attention budget

| Band | Share of first-session attention (intent) |
|------|-------------------------------------------|
| P1 | Majority — user can stop here and still have a consultation |
| P2 | Substantial — guided depth |
| P3 | Supporting — confirmation only |
| P4 | Optional — user-initiated |

If P3 or P4 visually outranks P1, the page has failed.

---

## 5. Space and openness rules

| Band | Space | Openness |
|------|-------|----------|
| P1 | Generous whitespace; low density | Fully open |
| P2 | Comfortable; one job per card | Open with expand for depth |
| P3 | Contained; no dashboard chrome | Open charts; tables collapsed if heavy |
| P4 | Compact teaser | Section collapsed |

---

## 6. Conflict matrix

| Conflict | Winner |
|----------|--------|
| Chart size vs Tóm tắt length | Tóm tắt |
| Domain essay vs Định hướng chính | Định hướng chính stays shorter and higher |
| Knowledge “interesting” vs Warnings | Warnings |
| Technical completeness vs Hero calm | Hero |
| Five domains all claiming P1 | Only Hero + Tóm tắt + Định hướng are P1 |
| Promotion / secondary milestone vs Career | Career leads; others stay in their domain |

---

## 7. Empty priority

If a P2 domain has no content, show its empty state (see `EMPTY_STATE_GUIDE.md`).  
Do not promote a P3/P4 block to fill the gap.

If Warnings has nothing qualified, do not invent P2 drama.

---

## 8. Stop line

Section priority V2 controls future emphasis. It does not invent tokens.

END
