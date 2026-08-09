# Typography System — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1  
Source of values: `VISUAL_LANGUAGE_SYSTEM.md` §9 (frozen)

---

## 1. Purpose

Typography is the primary hierarchy tool of the Result Page.

PX-1 names **roles** used by the experience.  
PX-1 does **not** invent new sizes, families, or weights.

---

## 2. Role map

| PX-1 role | Visual Language level | Size | Weight | Line height | Used for |
|-----------|----------------------|------|--------|-------------|----------|
| **Display** | Display | 40px | Bold | 110% | Hero headline only when a short display line is needed |
| **Heading** | H1 | 32px | Bold | 120% | Page-level consultation title if shown outside Hero chrome |
| **Section** | H2 | 24px | SemiBold | 120% | Tóm tắt tư vấn · Định hướng chính · domain titles · other section titles |
| **Card title** | H3 | 20px | SemiBold | 120% | Recommendation / warning / chart / knowledge titles |
| **Group** | H4 | 18px | Medium | 120% | Group labels inside Định hướng chính (Sự nghiệp, Tài chính, …) if not using Tag |
| **Body** | Body | 16px | Regular | 150% | Summary bullets · Why · Expected result · Action · analysis prose |
| **Caption** | Caption | 14px | Regular | 140% | Chart captions · supporting lines · expand hints |
| **Note** | Meta | 12px | Medium | 140% | Status auxiliaries · appendix notes · technical field labels |
| **Button** | Body / Caption per DS button spec | — | Medium–SemiBold | — | All CTA labels |
| **Tag** | Caption / Meta | 12–14px | Medium | 140% | Domain tags · status tags |

Do not create sizes outside this map.

---

## 3. Reading width

| Surface | Rule |
|---------|------|
| Body prose | 45–75 characters per line (Visual Language §9.3) |
| Summary bullets | Same reading width; do not span ultra-wide |
| Recommendation Why / Action | Stay within reading width; prefer short sentences |
| Chart captions | Caption width ≤ chart width |
| Technical tables | May exceed reading width; live inside collapsed Technical |

Never stretch paragraphs to full 1600px content shell.

---

## 4. Rhythm

```
Display / Heading
  ↓
Section
  ↓
Card title
  ↓
Body
  ↓
Caption / Note
```

Users must understand importance without color.

---

## 5. Usage rules

1. Weight before color.  
2. Do not enlarge type merely to attract attention.  
3. One Display moment per page maximum (Hero).  
4. Section titles are Vietnamese and identical to IA titles.  
5. Button labels use sentence case Vietnamese — not English Title Case.  
6. Tags never replace readable titles.  
7. Notes never carry primary advice.  
8. Long-form interpretation (after expand) stays Body 16px / 150%.  

---

## 6. Section → role assignment

| Section | Title role | Body role |
|---------|------------|-----------|
| Hero headline | Display or Heading | Body for one-liner |
| Hero status | Tag / Note | — |
| Tóm tắt tư vấn | Section | Body |
| Định hướng chính | Section | Body inside cards |
| Lưu ý quan trọng | Section | Body |
| Life domains | Section | Body |
| Biểu đồ minh họa | Section | Caption |
| Chi tiết kỹ thuật | Section | Note + Body for values |
| Kiến thức bổ sung | Section | Caption teaser · Body after expand |
| Phụ lục | Section or Body | Note |

---

## 7. Alignment and wrapping

- Left-align Vietnamese body (no justified rag that creates rivers).  
- Do not center long paragraphs.  
- Hero identity may be composed centered only if the whole Hero stays calm and readable; body sections stay start-aligned.  
- Avoid mid-word wrapping of proper names when possible.

---

## 8. Forbidden

- Mixing a second type scale  
- English section titles in larger type than Vietnamese body  
- Using Display for metrics dashboards in Hero  
- Using Note size for primary recommendations  
- Decorative script / playful fonts  

---

## 9. Stop line

Typography V2 = frozen Visual Language scale + these role assignments.

END
