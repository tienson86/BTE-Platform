# Information Architecture — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1

---

## 1. Purpose

Define what exists on the Result Page, why it exists, and which customer question it answers.

If a block cannot name its question, it does not belong.

---

## 2. IA tree

```
Kết quả tư vấn (Result Page)
│
├── Điều hướng trong trang (optional, Vietnamese TOC)
│
├── Hero
│     Danh tính · Tiêu đề · Một câu tóm tắt · Trạng thái tư vấn
│
├── Tóm tắt tư vấn
│     Tối đa 5 luận điểm hành động
│
├── Định hướng chính
│     ├── Sự nghiệp (khuyến nghị ưu tiên)
│     ├── Tài chính
│     ├── Quan hệ
│     ├── Sức khỏe
│     └── Vận trình
│
├── Lưu ý quan trọng
│     Cảnh báo quyết định
│
├── Sự nghiệp          (phân tích theo lĩnh vực)
├── Tài chính
├── Quan hệ
├── Sức khỏe
├── Vận trình
│
├── Biểu đồ minh họa
│     Bằng chứng trực quan cho lời khuyên đã nêu
│
├── Chi tiết kỹ thuật     [collapsed]
│     Lịch · Tứ trụ · Múi giờ · Schema · Định danh · Metadata
│
├── Kiến thức bổ sung     [collapsed]
│     Định nghĩa · Giải thích · Đọc thêm
│
├── Phụ lục
│     Phạm vi · Cách đọc lại · Giới hạn
│
└── Chân trang
```

---

## 3. Section catalog

| ID | Visible title | Customer question | Default state | May contain |
|----|---------------|-------------------|---------------|-------------|
| HERO | *(no English title; identity block)* | Đây có phải tư vấn của tôi? Tinh thần chung là gì? | Open | Identity, headline, one-liner, status |
| SUM | Tóm tắt tư vấn | Tôi cần nắm điều gì trước? | Open | ≤5 action sentences |
| REC | Định hướng chính | Tôi nên làm gì trước tiên? | Open | Grouped recommendation cards |
| WARN | Lưu ý quan trọng | Điều gì không được bỏ qua? | Open if any; empty pattern if none | Warning cards |
| CAREER | Sự nghiệp | Hướng nghề nghiệp của tôi? | Open | Domain framing + rec + optional analysis preview |
| WEALTH | Tài chính | Tôi nên xử lý tiền bạc thế nào? | Open | Same pattern |
| REL | Quan hệ | Tôi nên ứng xử ra sao trong quan hệ? | Open | Same pattern |
| HEALTH | Sức khỏe | Tôi cần giữ nhịp sống thế nào? | Open | Same pattern |
| LUCK | Vận trình | Giai đoạn này nên tăng / giảm gì? | Open | Same pattern |
| CHART | Biểu đồ minh họa | Có bằng chứng trực quan nào xác nhận? | Open, quiet | Charts + Vietnamese captions |
| TECH | Chi tiết kỹ thuật | Tôi muốn kiểm tra phần kỹ thuật? | **Collapsed** | Calendar, pillars, timezone, schema, IDs, metadata |
| KNOW | Kiến thức bổ sung | Tôi muốn hiểu thuật ngữ / lý thuyết? | **Collapsed** | Knowledge teasers + đọc thêm |
| APPX | Phụ lục | Tư vấn này bao gồm / không gồm gì? | Open, quiet | Scope, reread, limits |
| FOOT | *(product footer)* | Tôi đang ở đâu trong sản phẩm? | Open | Minimal chrome |

---

## 4. What lives where

### 4.1 Hero owns identity of the session

Allowed: name / profile display name, consultation headline, one human sentence, status in Vietnamese.

Forbidden: chart IDs, report UUIDs, schema version, pipeline timestamps, timezone abbreviations, engine names.

### 4.2 Tóm tắt tư vấn owns first understanding

Allowed: five decision-ready sentences spanning the whole consultation.

Forbidden: full 90-day plans, chart commentary, knowledge essays, duplicate of every domain.

### 4.3 Định hướng chính owns action

Allowed: top recommendations grouped by five life domains.

Forbidden: raw scores as the message; charts; technical dumps.

### 4.4 Lưu ý quan trọng owns risk that changes decisions

Allowed: bounded warnings with mitigation posture.

Forbidden: scare language; exhaustive caveat lists; engine error codes.

### 4.5 Domain sections own depth per life area

Each domain answers one life question more fully than the grouped rec strip.

Forbidden: repeating the entire Exec verbatim; inserting charts before the domain advice is clear.

### 4.6 Charts own visual confirmation

Allowed: visual models that support advice already stated.

Forbidden: leading the page; unlabeled axes in English; advice essays inside chart chrome.

### 4.7 Technical owns apparatus

Allowed: everything a specialist would inspect.

Forbidden: appearing open by default; leaking into Hero.

### 4.8 Knowledge owns optional learning

Allowed: definition → explanation → further reading.

Forbidden: blocking the advice path; hard sell; English headings.

### 4.9 Appendix owns closure

Allowed: scope, how to return, what this session does not cover.

Forbidden: new primary commercial push; technical dump.

---

## 5. Information that must move out of first read

| Content | Must live in |
|---------|--------------|
| Calendar system, solar/lunar conversion notes | Chi tiết kỹ thuật |
| Four pillars / stem-branch strings | Chi tiết kỹ thuật |
| Timezone, UTC offset | Chi tiết kỹ thuật |
| Schema, contract version, analysis version | Chi tiết kỹ thuật |
| Internal IDs | Chi tiết kỹ thuật |
| Deep theory | Kiến thức bổ sung |
| Full chart gallery | Biểu đồ minh họa |
| Secondary caveats | Domain expand or Phụ lục |

---

## 6. In-page navigation (optional)

If a table of contents exists, labels must match visible section titles exactly:

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

No English TOC. No IDs in TOC. Hero is not a TOC target named “Hero”.

---

## 7. Conflict rules

| Conflict | Winner |
|----------|--------|
| Chart drama vs Exec clarity | Tóm tắt tư vấn |
| Technical completeness vs first-read calm | Collapse technical |
| Knowledge depth vs action | Action |
| Domain length vs one-pass reading | Preview + expand |
| English specialist term vs Vietnamese label | Vietnamese label |
| Two equal “most important” recs | Rank; one leads |

---

## 8. Stop line

Information architecture V2 is binding for future Result Experience implementation.

END
