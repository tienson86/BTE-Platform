# Navigation Flow — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-1

---

## 1. Primary path (first session)

```
Enter Result
  ↓
Skip link available
  ↓
Hero (confirm identity)
  ↓
Scroll / read Tóm tắt tư vấn
  ↓
Scroll / read Định hướng chính
  ↓
Optional: Primary CTA
  ↓
Read Lưu ý quan trọng
  ↓
Read domains in order
  ↓
Optional: Biểu đồ minh họa
  ↓
Optional: open Chi tiết kỹ thuật
  ↓
Optional: Đọc thêm kiến thức
  ↓
Phụ lục → leave or reread
```

No route change is required for this journey.

---

## 2. In-page jump list

Optional TOC / jump list targets, in order:

1. Tóm tắt tư vấn  
2. Định hướng chính  
3. Lưu ý quan trọng  
4. Sự nghiệp  
5. Tài chính  
6. Quan hệ  
7. Sức khỏe  
8. Vận trình  
9. Biểu đồ minh họa  
10. Chi tiết kỹ thuật  
11. Kiến thức bổ sung  
12. Phụ lục  

Landing on a collapsed section still shows the section header; Technical/Knowledge remain collapsed until toggled.

---

## 3. Disclosure flows

```
RecommendationCard
  → Xem thêm → RecDetail → Thu gọn

Domain AnalysisPreview
  → Xem phân tích chi tiết → AnalysisCard detail → Thu gọn

ChartCard
  → Xem bảng số liệu → table → Ẩn bảng số liệu

TechnicalToggle
  → Xem chi tiết kỹ thuật → TechnicalPanel
  → Ẩn chi tiết kỹ thuật

KnowledgeToggle
  → Đọc thêm → KnowledgeList
  → card Đọc tiếp → detail
```

Opening one disclosure does not auto-open others.

---

## 4. Error / empty navigation

```
Section empty → stay in order → continue next section
Section error → local recovery → or jump to Tóm tắt tư vấn
Page error → retry consultation · no fake Hero
```

---

## 5. Forbidden navigation shapes

- Deep link that opens Charts as the first paint without Hero/Summary  
- Auto-scroll to Technical on load  
- Modal funnel that removes reading context  
- English hash routes shown to users (`#hero`, `#tech`)  

If hashes exist internally, visible labels remain Vietnamese section titles.

---

## 6. Stop line

Navigation supports reading. It does not invent a second information architecture.

END
