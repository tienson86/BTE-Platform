# BTE Platform — Rule Contract V1

**Work Package:** WP2B-1 — Rule Contract Audit + Design  
**Status:** Design only (no code / CSV changes)  
**Date:** 2026-07-24  

---

## 1. Mục tiêu

Thống nhất **một chuẩn condition** dùng chung cho:

- Pattern Engine
- Score Engine
- Priority Engine
- Interpretation Engine

để matcher không còn hiểu sai nhãn trạng thái thành Python expression.

---

## 2. Phạm vi audit

| Nguồn yêu cầu | Thực tế |
|---|---|
| `database/14_pattern` | Có — `01_main_pattern.csv` |
| `database/15_score_engine` | Có — 58 CSV (1 file parse lỗi: `09_final_score/05_recommendation.csv`) |
| `database/16_priority_engine` | **Không tồn tại** |
| Priority thực tế | `engines/interpretation_engine/knowledge/05_rule_database/08_priority_rules/` |
| Interpretation (tham chiếu) | `knowledge/05_rule_database` + `07_sentence_library/sentence_schema.json` |

---

## 3. Kết quả audit — loại condition đang tồn tại

### 3.1 Tổng hợp toàn hệ thống

| Loại (as-is) | Số lượng (ước lượng) | Nơi xuất hiện | Matcher hiện tại hiểu? |
|---|---:|---|---|
| **STATUS_PHRASE** (VN / mixed) | 217 cells | Score `condition` | Không (`eval` → False) |
| **BOOLEAN_FACT_KEY** | 56 terms | Priority `required_conditions` | Có (Priority matcher) |
| **ENUM_TOKEN_ASCII** | 43 cells | Score wuxing (`PRESENT`, `STRONG`, …) | Không |
| **IMPLICIT_COLUMN_SCHEMA** | 24 files | Score không có cột `condition` | Bị skip |
| **FIELD_COMPARE_EXPR** | 11 terms | Priority (`strength_score >= 80`) | Có (Priority only) |
| **EMPTY_COLLECTION** (`[]`) | 5 rows | Pattern `conditions` | Pass-through (match all) |
| **JSON_ARRAY_FIELD_OPS** | 52 rules | Interpretation knowledge | Schema có; engine chưa unify |
| **JSON_OBJECT_MAP** | 3+ rules | Interpretation `pattern_rules` | Ad-hoc keys |
| **PYTHON_EXPRESSION** | 0 trong DB | — | Score matcher *kỳ vọng* loại này nhưng DB không dùng |
| **BOOLEAN literal** | 0 trong DB | — | — |
| **RANGE schema** (`min_score`/`max_score`) | nhiều file | Score final/strength level | Không qua `condition` |

### 3.2 `database/14_pattern`

| File | Cột | Kiểu | Ghi chú |
|---|---|---|---|
| `01_main_pattern.csv` | `conditions` | `EMPTY_COLLECTION` (`[]`) | JSON array rỗng; Pattern matcher = match-all |

### 3.3 `database/15_score_engine`

- **33 file** có cột `condition`
- **24 file** không có `condition` — dùng cột thay thế:
  - `month_status`, `root_level`, `support_type`, `control_type`, …
  - `min_score` / `max_score`, `min_ratio` / `max_ratio`
- Giá trị `condition` chủ đạo:
  - ENUM: `PRESENT`, `STRONG`, `WEAK`, `IN_SEASON`, …
  - STATUS_PHRASE: `Hiện diện`, `Cách thành`, `Đại vận trợ Dụng thần`, …

→ Đây là **status enum / phrase**, không phải expression.

### 3.4 Priority (thay cho `16_priority_engine`)

File: `08_priority_rules/priority_conditions.json` (JSON bị ghép nhiều array — cần fix parse ở WP sau).

| Thuộc tính | Giá trị |
|---|---|
| Conditions | 40 |
| Terms | 67 |
| `match_type` | `all`=28, `first`=8, `any`=4 |
| Term types | BOOLEAN_FACT_KEY (56), FIELD_COMPARE_EXPR (11) |

Ví dụ:

- Fact: `day_master_extremely_strong`
- Compare: `strength_score >= 80`, `birth_season = spring`

### 3.5 Interpretation (tham chiếu contract)

| Kiểu | Ví dụ |
|---|---|
| JSON_ARRAY_FIELD_OPS | `{field, operator, value}` — chuẩn `sentence_schema.json` |
| JSON_OBJECT_MAP | `{month_branch_contains: ..., day_master_strength: [...]}` |

---

## 4. Root conflict (vì sao hệ thống lệch)

```text
Score CSV ──► condition = ENUM / STATUS_PHRASE
Score Matcher ──► eval(Python expression)
Result ──► 0 match ──► Score = 0

Pattern CSV ──► conditions = [] (JSON)
Pattern Matcher ──► list[{field,operator,value}]

Priority JSON ──► fact keys + field compare
Priority Matcher ──► đúng với data của nó

Interpretation ──► JSON field/operator/value (schema V1)
```

**Không có một Rule Contract chung** → mỗi engine “đoán” format khác nhau.

---

## 5. Rule Contract V1 — thiết kế

### 5.1 Nguyên tắc

1. **Không dùng `eval` / Python expression trong Rule Database.**
2. Condition là **dữ liệu có cấu trúc**, không phải code.
3. Một rule có thể có nhiều predicate; kết hợp bằng `condition_group`.
4. Fact / enum / range / compare đều biểu diễn được bằng cùng schema.
5. CSV chỉ là **serialization** của contract (JSON cell hoặc cột phẳng + normalize lúc load).

### 5.2 Schema chuẩn (JSON)

```json
{
  "condition_group": "AND",
  "conditions": [
    {
      "condition_id": "C001",
      "field": "context.element.wood.status",
      "operator": "eq",
      "value": "PRESENT"
    }
  ]
}
```

#### Trường bắt buộc / tùy chọn

| Field | Required | Mô tả |
|---|---|---|
| `condition_group` | no (default `AND`) | `AND` \| `OR` |
| `conditions` | yes (có thể `[]`) | danh sách predicate |
| `conditions[].condition_id` | yes | id ổn định |
| `conditions[].field` | yes | đường dẫn context (`dot.path`) |
| `conditions[].operator` | yes | xem enum bên dưới |
| `conditions[].value` | no | tùy operator |

#### Operator enum (V1)

| Operator | Meaning |
|---|---|
| `eq` | bằng |
| `neq` | khác |
| `in` | value ∈ list |
| `not_in` | value ∉ list |
| `gt` / `gte` / `lt` / `lte` | so sánh số |
| `exists` / `not_exists` | field có/không |
| `contains` | string/list chứa |
| `between` | `[min, max]` inclusive |

> Align với `07_sentence_library/sentence_schema.json` (+ thêm `contains`, `between` cho Score/Pattern).

#### `conditions: []`

Nghĩa: **always true** (unconditional rule).  
Dùng có kiểm soát (Pattern hiện đang dùng kiểu này).

### 5.3 Ánh xạ as-is → Contract V1

| As-is | Mapping V1 |
|---|---|
| `PRESENT` + cột `element=WOOD` | `field=wuxing.wood.status`, `op=eq`, `value=PRESENT` |
| `Cách thành` + `pattern_name=...` | `field=pattern.status`, `op=eq`, `value=thanh_cach` (+ normalize slug) |
| `month_status=Đắc lệnh` (không có condition) | `field=strength.month_status`, `op=eq`, `value=dac_lenh` |
| `min_score`/`max_score` | `field=total_score`, `op=between`, `value=[min,max]` |
| Priority fact `day_master_extremely_strong` | `field=facts.day_master_extremely_strong`, `op=eq`, `value=true` **hoặc** `op=exists` trên `facts` set |
| Priority `strength_score >= 80` | `field=strength_score`, `op=gte`, `value=80` |
| Interpretation JSON_OBJECT_MAP | normalize từng key → predicate (`month_branch_contains` → `contains`) |
| Pattern `[]` | `conditions: []` (always) |

### 5.4 Context Contract (đi kèm)

Matcher chỉ đọc **RuleContext** chuẩn (dict), không đọc object engine tùy ý:

```text
RuleContext
├── bazi.*
├── wuxing.*          # status per element: PRESENT|STRONG|WEAK|MISSING|EXCESS
├── strength.*        # month_status, root_level, score, level
├── pattern.*         # name, status (thanh_cach|pha_cach|...)
├── useful_god.*
├── shensha.*         # stars present
├── luck.*
├── score.*           # module scores, total_score
└── facts.*           # boolean facts for Priority
```

Score/Pattern/Priority/Interpretation **đều** consume cùng RuleContext.

### 5.5 Serialization theo store

| Store | Cách ghi V1 |
|---|---|
| JSON knowledge | dùng schema trực tiếp |
| CSV Score/Pattern | cột `conditions_json` (JSON string) **hoặc** giữ cột phẳng + **Adapter Loader** convert → Contract lúc load (không eval) |
| Priority JSON | migrate `required_conditions[]` → predicates; giữ `match_type` = `condition_group` mapping (`all→AND`, `any→OR`) |

**WP2B khuyến nghị:** Adapter Loader trước (không đụng bulk CSV), migrate CSV dần.

### 5.6 Matcher chung (thiết kế API — chưa code)

```text
RuleConditionMatcher.match(rule, context) -> bool
RuleConditionMatcher.match_all(rules, context) -> list[MatchedRule]
```

- Input: rule đã normalize về Contract V1
- Không `eval`
- Không hard-code BaZi trong matcher (chỉ so sánh field/op/value)

### 5.7 Engine adoption

| Engine | Việc cần làm (WP sau) |
|---|---|
| Pattern | Parse `conditions` JSON theo V1; bỏ match-all vô điều kiện khi có predicate thật |
| Score | Thay `eval` matcher bằng V1; adapter ENUM/STATUS/implicit columns |
| Priority | Map fact/compare → V1; giữ `match_type` |
| Interpretation | Dùng lại sentence/rule schema đã gần V1; deprecate JSON_OBJECT_MAP |

---

## 6. Non-goals (V1)

- Không cho phép Python expression trong DB
- Không đổi Blueprint pipeline
- Không rewrite toàn bộ Rule Engine trong một PR
- Không so sánh nội dung luận giải

---

## 7. Đề xuất WP tiếp theo

| WP | Mục tiêu |
|---|---|
| **WP2B-2** | Implement `RuleConditionMatcher` + normalize adapters (Score ENUM/STATUS + Priority fact/compare) |
| **WP2B-3** | ScoreContext builder → RuleContext; thoát Score=0 trên case_0001 |
| **WP2B-4** | Fix `05_recommendation.csv` + FinalScore aggregation |
| **WP2C** | Migrate dần CSV/JSON sang `conditions_json` V1 (không phá schema cũ — thêm cột) |

---

## 8. Kết luận audit

1. Hệ thống đang có **ít nhất 7 family** condition as-is (STATUS_PHRASE, ENUM, FACT_KEY, FIELD_COMPARE, EMPTY JSON, IMPLICIT COLUMN, JSON field-ops / object-map).
2. Score DB **không** dùng Python expression; Score matcher lại giả định expression → **đứt contract**.
3. `database/16_priority_engine` chưa có; Priority đang ở Interpretation knowledge.
4. **Rule Contract V1** lấy chuẩn gần nhất từ Interpretation `sentence_schema` (`field` + `operator` + `value`) và mở rộng vừa đủ cho Score/Pattern/Priority.
