# 17_WORDING_RULES.md

Version: 1.0

Status: DRAFT — Sprint C Writing System

Pack: 05 (Narrative Engine)

Depends on: Sprint A (frozen) · Sprint B (frozen) · `13`–`16`

---

# 1. Purpose

This document defines **allowed wording**, **forbidden wording**, and terminology discipline for BTE Narrative.

It is a writing contract.

It is not a runtime dictionary implementation.

---

# 2. Terminology Principles

| Principle | Rule |
|-----------|------|
| Customer-first | Prefer understandable wording; introduce technical terms with plain framing |
| Consistency | Same concept → same term within one NarrativeResult |
| Source fidelity | Keep analytical labels that Evidence uses (e.g., Dụng thần) when narrating those facts |
| No internal jargon | Pack names, engine names, adapter names stay internal |

---

# 3. Allowed Wording Classes

| Class | Examples of class (not templates) | Where used |
|-------|-----------------------------------|------------|
| Identity terms | Nhật chủ, cách cục, thân vượng/nhược (as evidenced) | Observation, Executive identity |
| Structure terms | Ngũ hành, thập thần (when explaining observed structure) | Observation / Reasoning |
| Guidance terms | Ưu tiên, nên tập trung, hướng phát huy | Recommendation |
| Caution terms | Cần lưu ý, hạn chế, tránh thiên lệch | Warning |
| Closing terms | Tóm lại, điểm then chốt | Conclusion / Executive |
| Insufficient state | Platform insufficient-data outcome wording | Any insufficient slot |

---

# 4. Forbidden Wording Classes

| Class | Forbidden signals | Why |
|-------|-------------------|-----|
| Rule-engine prose | “Kích hoạt khi…”, “Áp dụng bảng…”, “Ưu tiên xác định mùa theo…” | Technical Interpretation leakage |
| Developer prose | mock, placeholder, TODO, PACK_0x, Presentation Layer, ViewModel | Breaks trust |
| Absolute prophecy | “chắc chắn sẽ…”, “định mệnh không thể đổi” | Overclaim |
| Shame / insult | “bạn kém”, “mệnh xấu tuyệt đối” | Unsafe / unbranded |
| Calculator dump | Bare score lists as the whole narrative | Not consultant |
| Invented certainty | Made-up percentages / guarantees | No evidence |
| English UI residue in body | Observation / Explanation / Critical as customer labels | Localization break |
| Sales fear | Panic escalation beyond source | Manipulation |

---

# 5. Preferred vs Avoided Phrasing Patterns

| Prefer (pattern) | Avoid (pattern) |
|------------------|-----------------|
| “Xu hướng nổi bật là…” | “Hệ thống kích hoạt rule X…” |
| “Điểm mạnh được hỗ trợ bởi…” | “Matched_rules chứng minh…” |
| “Ưu tiên phát huy…” | “Bạn phải làm ngay nếu không…” |
| “Cần lưu ý yếu tố…” | “Thảm họa sẽ đến…” |
| Insufficient Evidence state | Speculative filler to hide gaps |

Patterns guide writers/systems later; they are not fill-in templates.

---

# 6. Technical Terms — Usage Gate

Technical BaZi terms are allowed when:

1. Present in Evidence / Interpretation, and  
2. Useful for understanding, and  
3. Not left as unexplained raw codes  

Technical terms are forbidden when:

1. They are internal IDs (`str_004`, `flo_001`)  
2. They are engine/pack identifiers  
3. They appear only to sound “expert” without helping the customer  

---

# 7. Numbers and Scores

| Allowed | Forbidden |
|---------|-----------|
| Grade / score when narrating evidenced assessment | Leading with numbers without meaning |
| Relative language already supported by source | Invented precision (“73.2% vận may”) |
| Priority labels as semantics | English Critical/High as customer-facing default |

---

# 8. Recommendation / Warning Lexicon Discipline

| Component | Allowed actionality | Forbidden |
|-----------|---------------------|-----------|
| Recommendation | Clear do / prioritize / develop | Scare language as the action |
| Warning | Caution / limit / watch | Fake action list replacing Recommendation |
| Impact | Meaning / implication | New commands |

---

# 9. Consistency Rules

1. Do not call the same evidence “điểm mạnh” in one section and “rủi ro” in another without source basis.  
2. Do not rename Dụng thần mid-narrative without cause.  
3. Executive Summary wording must not contradict body components.  

---

# 10. Anti-patterns (Wording)

✗ Pasting Interpretation rule text into customer fields  
✗ Mixing languages inside one sentence without need  
✗ Buzzwords with no chart referent  
✗ Softening invention (“có thể”, “dường như”) to hide missing evidence  

---

END
