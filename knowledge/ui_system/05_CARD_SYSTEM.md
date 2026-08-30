# 05_CARD_SYSTEM.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- PACK_02_LAYOUT_SYSTEM.md §9–12
- PACK_03_COMPONENT_STANDARD.md §21
- PACK_04_UI_PRESENTATION_STANDARD.md §7
- PACK_06 / PACK_07 (Result architecture — do not redesign)

This sprint defines card types. It does not redesign existing Dashboard cards or geometry.

---

# 1. Philosophy

Cards are independent information blocks.

One card. One question.

Header

↓

Body

↓

Footer (optional)

Never mix unrelated purposes.

Never resize a card because content grew. Content adapts to the card.

---

# 2. Official V2 types

| Type | Question it answers | Height class | Visual weight |
|------|---------------------|--------------|---------------|
| Hero Card | What is the executive picture? | M or L | Primary |
| Analysis Card | What does this domain show? | M | Secondary |
| Reference Card | What knowledge supports this? | M or AUTO in reports | Tertiary |
| Summary Card | What are the key facts? | S | Secondary |
| Status Card | What is the current state? | XS | Secondary |

Height classes (PACK_04): XS 160px · S 220px · M 320px · L 420px · XL 560px · AUTO reports only.

AUTO is prohibited on Dashboard pages.

---

# 3. Type rules

## Hero Card

- One per major screen.
- Holds identity + headline insight.
- Display / Hero typography for the lead metric or title.
- No nested analysis tables.

## Analysis Card

- One analytical domain.
- Card Title + Body.
- Charts and lists stay inside the height class.
- Preview first; expand if needed.

## Reference Card

- Knowledge, sources, glossary.
- Lowest visual weight.
- Must not compete with Hero or Analysis.

## Summary Card

- Short facts, counts, distribution.
- S height. No long narrative.

## Status Card

- Badge, KPI, or state.
- XS height.
- Label + Metric. Color is meaning, not decoration.

---

# 4. Anatomy

Required: title (Card Title role), body region.

Optional: caption, badge, footer action.

Forbidden: nested cards, competing CTAs, horizontal card scroll.

---

# 5. Row rhythm

Same row → same height class.

Correct: M M M

Incorrect: S XL M

---

# 6. Mapping to current Result (no redesign)

Existing Commercial Dashboard cards remain. This table is classification only.

| Current surface | V2 type |
|-----------------|---------|
| Identity / Overview | Hero / Summary |
| Tứ Trụ, Ngũ Hành, Thập Thần, Mệnh Cục, Thần Sát, Đại Vận | Analysis |
| Luận giải, Kế hoạch | Analysis (narrative presentation) |
| Knowledge / technical notes | Reference |
| Contract / empty / error chips | Status |

Do not change layout in UI-13.

---

END
