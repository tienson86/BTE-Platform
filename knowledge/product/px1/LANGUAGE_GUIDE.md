# Language Guide — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1

---

## 1. Law

**Everything visible to users is Vietnamese.**

No English titles.  
No mixed labels.  
No internal IDs.  
No engine terminology as UI language.

---

## 2. Scope

Applies to:

- Section titles  
- Card titles  
- Tags  
- Buttons  
- Status  
- Empty / error  
- Chart titles and captions  
- TOC  
- Expand labels  
- Aria-visible names  
- Appendix  

Does **not** require translating Design System token names in code.  
Code identifiers may stay English. Users never see them.

---

## 3. Canonical section titles

| Design ID | Visible title |
|-----------|---------------|
| Hero | *(no English word “Hero”; identity speaks for itself)* |
| ExecutiveSummary | **Tóm tắt tư vấn** |
| Recommendation | **Định hướng chính** |
| ImportantWarnings | **Lưu ý quan trọng** |
| Career | **Sự nghiệp** |
| Wealth / Finance | **Tài chính** |
| Relationship | **Quan hệ** |
| Health | **Sức khỏe** |
| Luck | **Vận trình** |
| Charts | **Biểu đồ minh họa** |
| TechnicalInfo | **Chi tiết kỹ thuật** |
| Knowledge | **Kiến thức bổ sung** |
| Appendix | **Phụ lục** |

Do not publish aliases like Summary, Recs, Charts, Tech, FAQ.

---

## 4. Canonical field labels (recommendation)

| Field | Visible label |
|-------|---------------|
| Why | **Vì sao** |
| Expected Result | **Kết quả kỳ vọng** |
| Action | **Việc cần làm** |
| Expand | **Xem thêm** |
| Collapse | **Thu gọn** |

---

## 5. Status language

| Intent | Visible examples |
|--------|------------------|
| Ready | **Sẵn sàng tư vấn** |
| Limited | **Tư vấn một phần** |
| In progress | **Đang hoàn thiện** |
| Error | **Không thể hiển thị phần này** |

Forbidden: `OK`, `READY`, `NULL`, `200`, `schema_v3`, `pipeline_pass`.

---

## 6. Traditional terms vs engine terms

Traditional Vietnamese metaphysics terms may appear when they help understanding (e.g. nhật chủ, ngũ hành) **if** a human gloss is nearby on first use in P1/P2.

Engine / platform terms must not appear:

| Forbidden in UI | Use instead |
|-----------------|-------------|
| Engine, pipeline, ViewModel | *(omit)* |
| Golden Dataset, snapshot | *(omit)* |
| schema, contract, payload | Chi tiết kỹ thuật only, Vietnamese labels |
| UUID, report_id | Ẩn; only inside Chi tiết kỹ thuật as **Mã hồ sơ** if truly needed |
| Day Master (English) | **Nhật chủ** |
| Ten Gods (English heading) | **Thập thần** (in technical/knowledge, not Hero) |
| Useful God as raw dump | Human support framing in Vietnamese |
| Score / Pattern internal enums | Human sentences |

---

## 7. Mixed-language ban

Forbidden patterns:

- `Career · Sự nghiệp`  
- `Summary` as a section chip  
- `Why / Vì sao` dual labels  
- `Read more`  
- `Error 500` as the only message  

Can Chi symbols (Giáp, Dần, …) may appear as values under Vietnamese headings.

---

## 8. Voice

Language is consultant Vietnamese:

Calm · precise · respectful · evidence-based · non-absolute.

See `COPYWRITING_GUIDE.md` and `MICROCOPY_GUIDE.md`.

---

## 9. Stop line

If a user can see it, it is Vietnamese.

END
