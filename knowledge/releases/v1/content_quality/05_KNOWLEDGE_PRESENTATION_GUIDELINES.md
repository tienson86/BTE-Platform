# 05 — Knowledge Presentation Guidelines

Version: 1.0  
Status: **Release B — Content Quality**  
Date: 2026-08-08  
Scope: Quality standards only — no runtime change

---

## 1. Purpose

Knowledge content must **educate** so the reader understands the analysis better.

It must support reading — not interrupt it, and not turn the Result Page into a textbook.

In V1, Knowledge on the Portal is primarily a **structural / glossary zone** (Product Integration gap G5). It is not a Pack 05 `NarrativeResult` section. These guidelines define how Knowledge should present when shown.

---

## 2. Role of Knowledge

| Knowledge should | Knowledge should not |
|------------------|----------------------|
| Explain terms the analysis uses | Dump unused encyclopedia entries |
| Clarify why a concept matters here | Compete with Executive Summary for attention |
| Stay optional / expandable | Force a lecture before the briefing |
| Use consultant teaching voice | Use classroom / academic textbook voice |
| Stay Vietnamese on commercial VI surfaces | Expose English product jargon |

Existing accordion labels (GOOD — keep):

- Thuật ngữ  
- Tài liệu tham chiếu  
- Lý thuyết truyền thống  
- Phụ lục  

Zone title: **KIẾN THỨC**

---

## 3. Quality standards

### 3.1 Educate in context

✓ Prefer terms that appear in the current result  
✓ One concept → one short explanation  
✓ Lead with meaning for the person, then traditional name if needed  
✓ Keep entries skimmable  

### 3.2 Do not interrupt reading

✓ Place Knowledge after core analysis / as expandable detail  
✓ Do not require Knowledge to understand Executive Summary  
✓ Avoid modal walls of theory mid-flow  
✓ Keep references secondary to commercial prose  

### 3.3 Avoid textbook style

✗ Long historical essays with no link to this chart  
✗ Bullet forests of unrelated terms  
✗ Exam-style definitions without consulting relevance  
✗ Internal pack names, engine names, or API field names as “knowledge”

---

## 4. Voice

| Attribute | Standard |
|-----------|----------|
| Tone | Patient teacher-consultant |
| Density | Light — definition + why it matters |
| Certainty | Educational, not prophetic |
| Language | Vietnamese commercial terms; traditional terms allowed when explained |

### Preferred pattern

1. **Term** (familiar VI label)  
2. **Plain meaning** (one or two sentences)  
3. **Why it appears here** (optional, if tied to current analysis)

### Example direction

**GOOD:**

> **Nhật chủ** là trụ ngày — điểm tựa nhận diện tính cách và hướng ứng xử nổi bật trong lá số này.

**BAD:**

> Knowledge Expert · Insight · Score payload · strength_score (0–100) nếu có.

---

## 5. Forbidden Knowledge copy

Do not show as customer Knowledge:

| Pattern | Example | Why |
|---------|---------|-----|
| English product jargon | `Insight`, `Knowledge`, `AI Knowledge Expert` | Breaks VI commercial voice |
| Engine / payload talk | `Score payload`, `rule_id`, `ViewModel` | Technical |
| Pack / architecture names | `PACK_05`, Presentation Layer | Internal |
| Placeholder | `(mock)`, `chờ engine` | Non-commercial |
| Unrelated encyclopedia | Full theory chapter unused by this result | Interrupts |

---

## 6. Structural vs narrative Knowledge

| Type | V1 status | Guidance |
|------|-----------|----------|
| Glossary / terms | Present (structural) | Follow this document |
| Chart facts supporting understanding | Present | Keep factual; no invention |
| Pack 05 narrative paragraphs as Knowledge | Not required | Optional future mapping only if product asks |
| Timeline / destiny bone (S10) | Often unavailable | Prefer honest empty state over fake content |

---

## 7. Empty and partial Knowledge

| State | Preferred copy direction |
|-------|--------------------------|
| No links | `Chưa có liên kết tri thức` (ACCEPTABLE — polish to warmer consultant phrasing later) |
| Insufficient | Do not invent glossary filler |
| Coming later | `Sắp ra mắt` only when truly deferred |

---

## 8. Review questions

1. Does this help the reader understand the analysis they just read?  
2. Can it be skipped without blocking trust → understanding → action?  
3. Is the voice consultant teaching, not textbook drilling?  
4. Any English / engine / placeholder leakage?  
5. Is every term justified by relevance to this result?
