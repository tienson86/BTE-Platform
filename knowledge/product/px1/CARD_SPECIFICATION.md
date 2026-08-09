# Card Specification — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1

---

## 1. Purpose

Standardize every Result card type.

Rule: **one card answers one customer question.**

---

## 2. Card types

| Type | Design ID | Visible context |
|------|-----------|-----------------|
| Hero | `CardHero` | Opening identity |
| Summary | `CardSummary` | Tóm tắt tư vấn |
| Recommendation | `CardRecommendation` | Định hướng + domains |
| Analysis | `CardAnalysis` | Domain depth preview |
| Chart | `CardChart` | Biểu đồ minh họa |
| Knowledge | `CardKnowledge` | Kiến thức bổ sung |
| Technical | `CardTechnical` | Chi tiết kỹ thuật |
| Empty | `CardEmpty` | Missing content |
| Error | `CardError` | Recovery |

---

## 3. Shared anatomy

Every card has:

```
Header   (title · optional tag · optional status)
Body     (one job)
Footer   (optional expand / secondary text action)
```

Rules:

- One visual boundary  
- No card-inside-card chrome  
- Vietnamese only  
- Expand is tertiary, not a second primary CTA  

---

## 4. CardHero

| Field | Definition |
|-------|------------|
| **Question** | Đây là tư vấn của ai, tinh thần chung là gì? |
| **Contains** | Danh tính · Tiêu đề · Một câu tóm tắt · Trạng thái tư vấn |
| **Does not contain** | IDs, timestamps, schema, versions, charts, pillar dumps |
| **Density** | Very low |
| **CTA** | None required |
| **Success** | User feels recognized and calm within 5 seconds |

---

## 5. CardSummary

| Field | Definition |
|-------|------------|
| **Question** | Tôi cần nắm điều gì trước? |
| **Contains** | Section title **Tóm tắt tư vấn** + ≤5 bullets |
| **Bullet rule** | One sentence · action-oriented · one idea |
| **Does not contain** | Nested lists, charts, full plans, English headings |
| **Density** | Low |
| **CTA** | Optional quiet jump: **Xem định hướng chính** |
| **Success** | User can restate the consultation without scrolling further |

---

## 6. CardRecommendation

| Field | Definition |
|-------|------------|
| **Question** | Tôi nên làm gì về lĩnh vực này, vì sao, và kỳ vọng gì? |
| **Contains** | Domain tag · title · **Vì sao** · **Kết quả kỳ vọng** · **Việc cần làm** · **Xem thêm** |
| **Group titles** | Sự nghiệp · Tài chính · Quan hệ · Sức khỏe · Vận trình |
| **Does not contain** | Charts, schema, engine scores as the message |
| **Density** | Medium · How ≤5 action bullets when listed |
| **CTA** | Primary CTA lives once at region level, not on every card |
| **Expand** | Detail / longer How / timing |
| **Success** | User knows what to do and why |

Required internal order on every recommendation card:

```
Vì sao
  ↓
Kết quả kỳ vọng
  ↓
Việc cần làm
  ↓
Xem thêm
```

---

## 7. CardAnalysis

| Field | Definition |
|-------|------------|
| **Question** | Vì sao kết luận lĩnh vực này phù hợp với tôi? |
| **Contains** | Short structured explanation · optional expand |
| **Lives in** | Domain sections, after or beside that domain’s advice |
| **Does not contain** | Primary CTA · chart galleries · knowledge essays |
| **Default** | Preview visible · detail collapsed |
| **Success** | Understanding without calculator feel |

---

## 8. CardChart

| Field | Definition |
|-------|------------|
| **Question** | Bằng chứng trực quan nào xác nhận lời khuyên đã nêu? |
| **Contains** | Vietnamese title · figure · caption linking back to advice |
| **Does not contain** | The primary recommendation itself |
| **Table** | Collapsed if heavy |
| **Success** | Confirms; never replaces advice |

---

## 9. CardKnowledge

| Field | Definition |
|-------|------------|
| **Question** | Tôi muốn hiểu thêm khái niệm nào? |
| **Contains** | Title · teaser · **Đọc thêm** |
| **Structure after expand** | Định nghĩa → Giải thích → Tham chiếu |
| **Does not contain** | Hard sell · English headings · engine IDs |
| **Default** | Section collapsed; card teaser after open |
| **Success** | Learning without derailing action |

---

## 10. CardTechnical

| Field | Definition |
|-------|------------|
| **Question** | Tôi muốn kiểm tra phần kỹ thuật? |
| **Contains** | Lịch · Tứ trụ · Múi giờ · Schema · Định danh · Metadata |
| **Default** | Entire section collapsed |
| **Language** | Labels Vietnamese; raw values may remain conventional symbols (Can Chi) with Vietnamese headings |
| **Success** | Available, never ambient |

---

## 11. CardEmpty

| Field | Definition |
|-------|------------|
| **Question** | Lĩnh vực này chưa có nội dung — tôi làm gì? |
| **Contains** | Calm explanation + next step (see `EMPTY_STATE_GUIDE.md`) |
| **Tone** | Consultant, not system log |
| **Does not contain** | Error red · technical codes · English “No data” |

---

## 12. CardError

| Field | Definition |
|-------|------------|
| **Question** | Có sự cố — tôi khôi phục thế nào? |
| **Contains** | What happened in human language + recovery action |
| **Tone** | Honest, calm, specific |
| **Does not contain** | Stack traces · schema names as the message |

---

## 13. Elevation intent

Map to Visual Language elevation roles — do not invent shadows.

| Card type | Elevation intent |
|-----------|------------------|
| Hero / Summary / Recommendation | Level 1–2 (readable, not theatrical) |
| Analysis / Chart | Level 1 |
| Knowledge / Technical / Appendix | Level 0–1 |
| Error | Level 2 only to aid recovery, not alarm |
| Empty | Level 1, quiet |

---

## 14. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Summary card with 12 bullets | Hard cap 5 |
| Rec card missing Vì sao | Incomplete — do not ship |
| Chart card giving advice | Move advice to Recommendation |
| Hero showing report UUID | Move to Technical |
| Nested bordered cards | One boundary · inner spacing only |

---

## 15. Stop line

Card types above are the only Result Experience V2 card families.

END
