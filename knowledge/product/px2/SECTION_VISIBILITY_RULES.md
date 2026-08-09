# Section Visibility Rules

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2

---

## 1. Law

Never leave blank cards.

Hidden = not mounted.  
Empty = explicit EmptyStateCard where the section must remain in order.  
Collapsed = mounted header, body closed.

---

## 2. Rules

| Section | If content present | If content absent |
|---------|--------------------|-------------------|
| Hero | visible | page **error** (not empty card) |
| Tóm tắt tư vấn | visible | page **error** |
| Định hướng chính | visible | region **empty** card (keep section) |
| Lưu ý quan trọng | visible | **hidden** |
| Sự nghiệp … Vận trình | visible or empty card | **empty** card (keep order) |
| Biểu đồ minh họa | visible | **hidden** |
| Chi tiết kỹ thuật | collapsed header | collapsed empty technical or **hidden** if `available=false` and no metadata |
| Kiến thức bổ sung | collapsed | **hidden** |
| Phụ lục | visible quiet | **hidden** |

---

## 3. Charts

Visible **only if** `report.charts.length > 0`.

Layout `chart_placeholder` without envelope charts ≠ visible blank chart.

---

## 4. Warnings

Hidden if `report.warnings.length === 0`.  
Do not invent calm “no warnings” theatre unless Product later requires a quiet line. PX-2 default: hide.

---

## 5. Technical / Knowledge

Default **collapsed** when shown.  
Technical may remain as a collapsed header if any technical field or artifact metadata exists.  
If nothing at all → hidden.

---

## 6. Nav sync

`NavModel.items[].visible` mirrors these rules.  
Do not list hidden sections.

---

## 7. Partial page

`partial_ready` does not hide P1.  
It may hide P3/P4 sections and show domain empty cards.

---

## 8. Stop line

Visibility protects consulting calm. No hollow chrome.

END
