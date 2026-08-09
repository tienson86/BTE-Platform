# Spacing System — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1  
Source of values: PACK_02 Layout System · Visual Language §14 (frozen)

---

## 1. Purpose

Spacing creates consulting calm.

PX-1 defines **where** rhythm applies.  
PX-1 does not invent spacing numbers.

---

## 2. Official scale (frozen)

PACK_02 scale (px):

```
4 · 8 · 12 · 16 · 24 · 32 · 40 · 48 · 64 · 80 · 96
```

Visual Language rhythm aliases:

| Alias | Value |
|-------|-------|
| XS | 8px |
| S | 16px |
| M | 24px |
| L | 32px |
| XL | 48px |
| XXL | 64px |

No arbitrary values.

---

## 3. Page margins

| Breakpoint | Page padding (PACK_02) |
|------------|------------------------|
| Desktop | 32px |
| Tablet | 24px |
| Mobile | 16px |

Content max-width: 1600px desktop · 1800px ultra-wide · centered.  
Reading column inside cards follows typography reading width, not full shell width.

---

## 4. Vertical rhythm (experience mapping)

| Relationship | Intent | Frozen token |
|--------------|--------|--------------|
| Major zone gap (Hero → Tóm tắt → Định hướng → …) | Clear chapter break | XL / XXL (48 / 64) |
| Section block gap | Between peer sections | L / 32 (PACK_02 sections) |
| Row / card stack gap | Between cards | M / 24 |
| Inside card | Header → body → footer | S / 16 |
| Component gap | Icon–label, tag–title | 12 |
| Tight inline | Icon optical padding | 8 or 4 |

Prefer more space *between* sections than *inside* a card.

---

## 5. Card padding

| Card type | Padding intent |
|-----------|----------------|
| Hero | Generous (M–L) |
| Summary / Recommendation | M (24) |
| Analysis / Warning | M (24) |
| Chart | M (24) |
| Knowledge / Technical / Empty / Error | M (24) |
| Appendix | S–M (16–24) |

Inner elements rely on spacing, not nested borders.

---

## 6. Reading gaps (content)

| Content pair | Intent |
|--------------|--------|
| Section title → first card | S–M |
| Summary bullets | 8–12 between bullets |
| Rec fields Vì sao / Kết quả / Việc cần làm | 12–16 between fields |
| Domain intro → rec list | M |
| Chart figure → caption | 8–12 |
| Collapsed header → next section | Keep zone gap so collapse does not glue chapters |

---

## 7. Whitespace philosophy

```
Whitespace
  ↓
Typography
  ↓
Background contrast
  ↓
Border
```

Whitespace separates chapters of the consultation.  
Do not use hairline grids to fake a dashboard.

---

## 8. Responsive spacing

| Breakpoint | What changes | What does not |
|------------|--------------|---------------|
| Desktop | Wider page padding; possible multi-column rec groups | Section order |
| Tablet | 24px page padding; groups may become 2 columns then 1 | Section order |
| Mobile | 16px page padding; single column | Section order |

Never reduce zone gaps so far that P1 and P3 feel like one blob.

---

## 9. Forbidden

- Custom 20px / 28px / 36px “because it looked better”  
- Zero gap between Hero and Tóm tắt  
- Chart gallery tighter than Summary  
- Padding used to hide overflow instead of density control  

---

## 10. Stop line

Spacing V2 = frozen scale + consultation rhythm.

END
