# 05 — Commercial Composition Rules

| Field | Value |
|-------|--------|
| Document | INT-03B Commercial Composition Rules |
| Version | 1.0.0 |
| Status | Canonical for INT-03B |
| Runtime | None. Editorial specification only. |

---

## 1. Purpose

Define deterministic editorial rules that later sprints use to turn Integrated Narrative into Commercial Narrative.

INT-03A remains frozen. This sprint does **not** change the composer runtime.

The Commercial Composer is an **editor**, not an author.

---

## 2. Customer-facing section order

Frozen presentation order:

```
1. Tổng quan
        ↓
2. Hiện trạng
        ↓
3. Điểm mạnh
        ↓
4. Điểm cần lưu ý
        ↓
5. Hướng điều chỉnh
        ↓
6. Kết luận
```

| Order | Customer title | INT-03A slot (frozen) | Role |
|-------|----------------|------------------------|------|
| 1 | Tổng quan | `executive_summary` | Highest-priority published findings |
| 2 | Hiện trạng | `current_situation` | What is already true |
| 3 | Điểm mạnh | `strengths` | Published constructive impact |
| 4 | Điểm cần lưu ý | `risks` | Published restraint / caution |
| 5 | Hướng điều chỉnh | `key_recommendation` | Published guidance, grouped |
| 6 | Kết luận | `conclusion` | Settled restatement |

`overall_reading` stays on the INT-03A unit. It is **not** a customer-facing page. Concatenating topic summaries as a second wrap repeats Tổng quan and Kết luận.

### Why this order

Experience Principles: trust → understanding → action.

1. **Tổng quan** earns trust with a short published reading.
2. **Hiện trạng** shows the facts the reading rests on.
3. **Điểm mạnh** then **Điểm cần lưu ý** give a balanced consulting frame before advice.
4. **Hướng điều chỉnh** is action, after the situation is understood.
5. **Kết luận** closes. It does not introduce a new finding.

Title **Điểm cần lưu ý** is calmer than “Rủi ro chính”. It does not forecast misfortune. The INT-03A slot name `risks` is unchanged.

Title **Hướng điều chỉnh** is consulting guidance, not a prediction.

---

## 3. Canonical rules

| Id | Name | Statement |
|----|------|-----------|
| C-001 | Executive priority | Tổng quan contains the highest-priority published findings only. Do not concatenate topic summaries. |
| C-002 | Emit once | Repeated statements and repeated meaning are emitted once. |
| C-003 | Group recommendations | Recommendations from multiple topics are grouped by meaning before presentation. |
| C-004 | Hide internals | Technical evidence ids, scores, and trace ids are never customer-facing. |
| C-005 | Drop machine-only | Machine-only wording (JSON, dumps, UNKNOWN runtime blobs) is removed. |
| C-006 | Preserve truth | Commercial wording must preserve analytical truth. No reinterpretation. |
| C-007 | Section order | Customer-facing order is the six titles above. |
| C-008 | Traceability | Every commercial sentence cites Integrated Narrative sentence ids. No orphan sentence. |
| C-009 | Strongest recommendation | Overlapping recommendations keep the strongest published version and preserve ownership. |
| C-010 | Consulting style | Clear, professional, calm. No alarmist, fortune-telling, or absolute-certainty language. |

---

## 4. Editorial operations

Allowed: reorder, merge, remove repetition, shorten, clarify, prioritize.

Forbidden: invent, expand, reinterpret, calculate, predict, infer, hallucinate, rewrite analytical meaning.

Shorten and clarify may drop words. They may not change the published finding.

---

## 5. Executive selection (C-001)

Select, prioritize, merge. Do not concatenate every topic summary.

Priority of published findings:

1. Nhật chủ / thân (strength classification)
2. Dụng thần
3. Cách cục
4. Đại Vận / Lưu Niên identity (names only)

A candidate is ineligible when it is a topic-summary restatement, a compact score dump, a rule id, or machine-only wording.

Every remaining sentence must originate from published Integrated Narrative.

---

## 6. Repetition (C-002)

Examples:

- `Thân vượng` appears once.
- Dụng thần Hỏa (or the published useful-god display) appears once.

Same meaning → merge into the first eligible published sentence.

---

## 7. Technical language (C-004, C-005)

Never expose:

- rule ids (`str_003`, `pat_ca_01`, `sea_001`, `tmp_001`)
- internal scores / compact evidence strings
- JSON
- source-path tokens as customer prose

---

## 8. Recommendations (C-003, C-009)

Merge published recommendations only.

Group by meaning (useful god, unfavorable / kỵ, climate / điều hậu).

If two published lines overlap, keep the longer / containing published version. Keep its Integrated ownership. Invent nothing.

---

## 9. Traceability (C-008)

Sentence id form:

`integrated.{slot}[{index}]`

Example: `integrated.observation[0]`

A commercial sentence without this reference is invalid.

---

## 10. Runtime boundary

Python freeze of this sprint:

`engines/commercial_composer/rules.py` → `commercial_composition_rules()`

Do not call these rules from `compose.py` in INT-03B.

---

END
