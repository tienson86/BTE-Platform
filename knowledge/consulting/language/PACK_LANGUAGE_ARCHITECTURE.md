# CONSULTING LANGUAGE PACK

# PACK_LANGUAGE_ARCHITECTURE.md

Document ID: LANG-PACK-00

Version: 0.1.0-skeleton

Status: DRAFT — ARCHITECTURE + SKELETON ONLY

---

# 1. Purpose

Tài liệu này định nghĩa kiến trúc Consulting Language Pack.

Language Pack là nguồn kiểm soát wording cho khách hàng.

Language Pack không phải Decision Engine.

Language Pack không phải Assessment Engine.

Language Pack không phải Canonical Mathematics.

---

# 2. Problem

TV1-R02 đã cố định cấu trúc Question-first.

Assessment trả về semantic meaning.

Nếu wording được viết trực tiếp từ technical label.

↓

Khách hàng nhận được ngôn ngữ kỹ thuật, không phải ngôn ngữ tư vấn.

Language Pack tách hai tầng đó.

---

# 3. Two Layers

## Semantic Truth

Assessment / Decision đã kết luận nghĩa gì.

Ví dụ:

`marriage.q1.mixed`

Đây là truth đã được approve bởi Question Logic.

## Customer Wording

Nghĩa đó được nói với khách hàng như thế nào.

Tầng này do Product Owner / consulting team soạn.

LANG-01 không viết commercial prose.

---

# 4. Required Flow

```
Decision
  ↓
Assessment          (semantic conclusion — frozen in LANG-01)
  ↓
Language Key        (deterministic)
  ↓
Language Catalog    (YAML)
  ↓
Controlled Customer Wording
  ↓
Narrative
  ↓
Report / UI
```

Language Pack chỉ bắt đầu sau khi Assessment đã có semantic_key / semantic_state.

LANG-01 không bật flow này trên live TV-01.

Live TV-01 tiếp tục dùng R02 wording cho đến ticket tích hợp sau.

---

# 5. Position Relative To Frozen Pipeline

COMMON Assessment / Recommendation vẫn là siblings của Decision.

Language Pack không đứng giữa Decision và Recommendation.

Language Pack đứng trên wording surface của Assessment (và sau này Recommendation, nếu được authorize).

```
                    Decision
                   /        \
          Assessment      Recommendation
                   \        /
              Language Pack   ← wording only; not yet live
                      ↓
                   Narrative
                      ↓
                    Report
                      ↓
                 Presentation
```

Assessment must never consume Language Pack to invent a new conclusion.

Language Pack must never consume Recommendation to invent Assessment meaning.

---

# 6. Responsibility

Language Pack trả lời:

> Semantic meaning đã được approve này nên diễn đạt cho khách hàng như thế nào?

Language Pack không trả lời:

> Kết luận đúng là gì?

> Khách hàng nên làm gì?

> Canonical fact nào tồn tại?

---

# 7. Must Not

Language Pack không được:

- tạo Decision
- tạo Assessment
- đổi Assessment answer / semantic_key
- tạo hoặc đổi Recommendation
- suy Canonical facts
- gọi LLM / external AI / freeform completion
- dùng `random()` cho wording
- silently replace live customer wording
- hard-code nhãn UI (Kết luận / Ý nghĩa / Cơ sở / Lưu ý) vào mọi YAML entry

---

# 8. Assessment Card Language Contract

Mọi Assessment Card customer output theo thứ tự:

1. Kết luận
2. Ý nghĩa
3. Cơ sở
4. Lưu ý
5. Closing / Xem chi tiết nếu applicable

Nhãn 1–5 thuộc UI / Presentation layer.

Language Entry cung cấp nội dung cho các slot:

| UI slot | Language field |
|---|---|
| Kết luận | `headline` (plain_customer_text of verdict) |
| Ý nghĩa | `meaning` |
| Cơ sở | `supporting_fact_templates` |
| Lưu ý | `limitation_templates` |
| Closing | `closing` |

Technical reason, nếu cần, nằm ở `technical_explanation`, không trộn vào headline.

---

# 9. Catalog Layout

```
knowledge/consulting/language/
  PACK_LANGUAGE_ARCHITECTURE.md
  01_LANGUAGE_MODEL.md
  02_LANGUAGE_CATALOG.md
  03_SENTENCE_RULES.md
  04_VARIATION_ENGINE.md
  05_STYLE_GUIDE.md
  06_CUSTOMER_WORDING.md
  07_REVIEW_CHECKLIST.md
  schema.yaml
  marriage/
    compatibility.yaml   # Q1
    support.yaml         # Q2
    personality.yaml     # Q3
    stability.yaml       # Q4
    children.yaml        # Q5
    overall.yaml         # Q6
```

TV-02 / TV-03 / TV-04 thêm thư mục module. Không đổi loader / validator / selector.

---

# 10. Code Skeleton

```
consulting/language/
  models.py
  catalog.py
  loader.py
  selector.py
  validator.py
  renderer.py          # skeleton compose only
  bindings/marriage.py # key map seam; not wired into TV-01 runtime
```

Skeleton được phép load YAML và validate schema.

Skeleton không được thay R02 Narrative / Report / UI.

---

# 11. Versioning

| Token | Scope |
|---|---|
| `language_pack_version` | Architecture + loader behavior |
| `catalog_version` | One module catalog file set |
| `module_language_version` | TV-01 / TV-02 / … language surface |
| `entry.version` | One language_key |

Wording behavior change → version change.

Không được thay wording đã FROZEN bằng cách sửa YAML im lặng.

---

# 12. Integration Rule (LANG-01)

Không switch live TV-01 sang Language Pack.

Không rewrite Assessment answers.

Không sửa Decision Mathematics.

Không sửa Canonical Mathematics.

Tích hợp production chỉ sau khi:

1. Product Owner soạn wording
2. Review checklist PASS
3. Entry status = `approved` rồi `frozen`
4. Ticket tích hợp riêng authorize Narrative/UI binding

---

# 13. Future Modules

TV-02 Business, TV-03 Career, TV-04 Child / Family reuse:

- Language Entry schema
- Loader
- Validator
- Variation selector
- Sentence rules
- Style guide
- Review checklist

Chỉ thay:

- Question Set
- Language Keys
- Language Entries
