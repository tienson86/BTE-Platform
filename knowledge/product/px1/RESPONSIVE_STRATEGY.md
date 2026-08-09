# Responsive Strategy — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1  
Source: PACK_02 grid · page padding (frozen)

---

## 1. Invariant

**Reading order is identical on Desktop, Tablet, and Mobile.**

Layout may stack.  
Meaning may not reorder.

```
Hero → Tóm tắt tư vấn → Định hướng chính → Lưu ý quan trọng
  → Sự nghiệp → Tài chính → Quan hệ → Sức khỏe → Vận trình
  → Biểu đồ minh họa → Chi tiết kỹ thuật → Kiến thức bổ sung → Phụ lục
```

---

## 2. Breakpoint intents

| Surface | Grid (PACK_02) | Page padding | Composition intent |
|---------|----------------|--------------|--------------------|
| **Desktop** | 12 columns | 32px | Report width; rec groups may sit 2–3 across *inside* Định hướng chính only |
| **Tablet** | 8 columns | 24px | Two columns max; domains still sequential |
| **Mobile** | 4 columns | 16px | Single column; thumb-reachable tertiary controls |

---

## 3. Desktop

- Hero spans full reading column  
- Tóm tắt is a single primary column (not three competing metric tiles)  
- Định hướng chính: groups labeled in Vietnamese; cards may wrap in a grid **without changing group order** (Sự nghiệp before Tài chính, etc.)  
- Life domains: full width, stacked in canonical order  
- Charts: 1–2 across after advice; never a widget dashboard above recs  
- In-page TOC may sit aside if product chrome allows — labels Vietnamese, order identical  

Desktop must not revive V1 “summary | indicators | destiny” as three equal heroes.

---

## 4. Tablet

- Stack Hero, then Tóm tắt, then Định hướng  
- Recommendation groups wrap to 2 then 1  
- Warnings full width  
- Charts one per row if captions would wrap poorly  
- Technical / Knowledge remain collapsed headers full width  

---

## 5. Mobile

- Strict single column  
- No horizontal card carousels for P1/P2  
- Primary CTA remains visible after Định hướng — not a floating gimmick that covers text  
- Expand targets are large enough for keyboard and touch  
- Chart may scroll internally if needed; page itself does not require horizontal pan  
- TOC becomes an in-page list or compact jump list — same labels, same order  

---

## 6. What responsive may change

- Columns inside a section  
- Padding  
- Chart size  
- TOC placement (side vs top vs inline)  

## 7. What responsive must not change

- Section sequence  
- Hero contents  
- Five-bullet summary cap  
- Recommendation card anatomy  
- Collapsed defaults for Technical and Knowledge  
- Language (still Vietnamese only)  
- One Primary CTA rule  

---

## 8. First viewport by device

| Device | Must see without hunting |
|--------|---------------------------|
| Desktop | Full Hero + Tóm tắt start |
| Tablet | Full Hero + Tóm tắt start |
| Mobile | Full Hero; Tóm tắt title + first bullets immediately below |

Charts never steal first viewport on any breakpoint.

---

## 9. Stop line

Responsive V2 is stacking and density — not a different product per device.

END
