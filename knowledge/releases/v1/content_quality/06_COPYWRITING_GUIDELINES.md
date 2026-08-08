# 06 — Copywriting Guidelines

Version: 1.0  
Status: **Release B — Content Quality**  
Date: 2026-08-08  
Scope: Quality standards only — no runtime change

---

## 1. Purpose

Unify every visible string behind **one consultant product voice**.

Covers titles, buttons, labels, badges, descriptions, errors, empty states, and loading messages across commercial Portal surfaces.

Narrative body prose follows Pack 05 Sprint C + docs `02`–`05` in this folder. This document covers **UI chrome and system copy**.

---

## 2. One voice

BTE speaks as an **experienced BaZi consultant product**.

| We are | We are not |
|--------|------------|
| Calm | Hype marketing |
| Clear | Calculator widget |
| Respectful | Fortune-telling carnival |
| Professional | Developer console |
| Vietnamese-first on VI surfaces | Mixed EN/VI without reason |

Experience path (frozen Foundation): **trust → understanding → action**.

---

## 3. Language policy

| Surface | Language |
|---------|----------|
| Official Result Page (VI commercial) | Vietnamese |
| Pack 05 NarrativeResult customer body | Vietnamese |
| System states on Result path | Vietnamese |
| Aria / screen-reader on VI pages | Prefer Vietnamese (current EN = TECHNICAL debt) |
| Internal logs / developer tools | English allowed — never customer-facing |

Do not leave English defaults on Vietnamese commercial screens (Pack 06 gates are the main known debt).

---

## 4. String classes

### 4.1 Titles

| Standard | Examples to prefer | Avoid |
|----------|--------------------|-------|
| Commercial VI section titles | Tóm tắt điều hành, Khuyến nghị, Kiến thức | Executive Summary, Analysis Blocks, Dashboard |
| Sentence case / established ALL CAPS zone titles | Keep existing Result zone casing | Invent new shouty marketing titles |

### 4.2 Buttons / CTAs

| Standard | Prefer | Avoid |
|----------|--------|-------|
| Action + clarity | Luận giải, Xem tất cả khuyến nghị →, Mở rộng luận giải | Submit, Continue to Four Pillars (EN on VI) |
| One primary action per cluster | Keep | Competing CTAs with jargon |

### 4.3 Labels & badges

| Standard | Prefer | Avoid |
|----------|--------|-------|
| Human terms | Ưu tiên cao, Cần lưu ý, Nhật chủ | Critical, N/A, Score payload |
| Priority badges already GOOD | Cao / Trung bình / Thấp | Raw enums |

### 4.4 Descriptions

| Standard | Prefer | Avoid |
|----------|--------|-------|
| Short supporting sentence | Explain what the block helps the reader do | Architecture hints (“Explainable Analysis — mỗi khối…”) with EN product names |

### 4.5 Loading states

| Standard | Prefer | Avoid |
|----------|--------|-------|
| Calm progress | Đang tải kết quả…, Đang tải Tứ Trụ | Loading, Loading executive summary |
| Name the content in VI | Match section name | English screen codenames |

### 4.6 Empty states

| Standard | Prefer | Avoid |
|----------|--------|-------|
| Guide next step | Chưa có kết quả — hãy chọn Luận giải trước. | No data available |
| Honest insufficient | Chưa đủ dữ liệu để đưa ra kết luận. | Soft fake content |
| Respectful | No blame | “You haven’t completed setup correctly” shaming |

### 4.7 Error states

| Standard | Prefer | Avoid |
|----------|--------|-------|
| Clear + recoverable | Không tải được kết quả. / Không kết nối được máy chủ… | Unable to load content / Unexpected exception |
| No stack traces | User-facing message only | Raw API codes as headline |

Approved API-facing patterns already GOOD in `src/api/errors.ts` — keep that tone.

---

## 5. Terminology map (prefer → avoid)

| Prefer (VI commercial) | Avoid in customer UI |
|------------------------|----------------------|
| Bát Tự / Tứ trụ | BaZi (in VI nav — ACCEPTABLE debt), Four Pillars |
| Thiên Can / Địa Chi | Heavenly Stem / Earthly Branch |
| Tàng can | Hidden Stems |
| Ngũ hành | Five Elements (EN on VI) |
| Thập thần | Ten Gods (EN on VI) |
| Kiến thức | Knowledge / Insight |
| Tóm tắt điều hành | Executive Summary (EN on VI) |
| Kết luận | Conclusion (EN on VI) |
| Cần lưu ý | Risks (fear-tilted EN default) |
| Trang chủ | Dashboard (EN title debt) |

Traditional terms may appear when taught; pair with plain meaning in Knowledge.

---

## 6. Consistency rules

1. **One name per concept** across Result Page, Canonical Desktop, and BaZi path.  
2. **Same empty/insufficient line** for missing commercial prose: `Chưa đủ dữ liệu để đưa ra kết luận.`  
3. **Same expand/collapse verbs**: `Xem thêm` / `Thu gọn` / `Mở rộng luận giải`.  
4. **No mixed EN badges** on Vietnamese sections.  
5. **Parallel Pack 06 screens**, if still shown, must adopt the same VI voice before product launch on those routes.

---

## 7. Known debt inventory (copy)

High priority to retire in a later polish epic (not Release B implementation):

| Area | Debt |
|------|------|
| Pack 06 `presentationGate` | Loading / No data available / Unable to load content |
| Pack 06 panels | Conclusion, Explanation, Risks, Evidence, Knowledge Reference |
| `vi.json` report/knowledge keys | Knowledge, Insight, AI Knowledge Expert, Score payload |
| Aria zone names | Summary Zone, Recommendation Zone… |
| Dashboard title | `Dashboard` |
| Chrome | Occasional `Menu` EN |

---

## 8. Writing micro-rules

- Prefer verbs customers understand.  
- Prefer short sentences for gates and buttons.  
- Prefer calm certainty: say what happened; say what to do next.  
- Never expose engine, pack, mock, or placeholder words.  
- Never invent analytical claims in chrome copy.

---

## 9. Review questions

1. Would this string look native on a Vietnamese consulting product?  
2. Does it match Result Page voice?  
3. Does an error/empty state tell the user what to do next?  
4. Any TECHNICAL / PLACEHOLDER leakage?  
5. If translated back to “software English,” did we accidentally ship that instead of Vietnamese?
