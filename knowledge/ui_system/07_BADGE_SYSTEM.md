# 07_BADGE_SYSTEM.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- PACK_03_COMPONENT_STANDARD.md §22
- 01_COLOR_SYSTEM.md

---

# 1. Philosophy

Badges represent status.

Never use badges as buttons.

Official colors only.

Unified shape, type, and padding.

---

# 2. Anatomy

Label (required)

↓

Optional icon (16px)

↓

Optional metric (not a second badge)

Radius: Small 6px or Round 9999px. Pick one style per product surface and keep it.

Type: Label role, Medium weight.

Padding: 4px 8px (spacing scale).

---

# 3. Variants

| Variant | Color tokens | Meaning |
|---------|--------------|---------|
| Neutral | text-secondary + surface-section | Default state |
| Success | feedback-success | Positive / healthy |
| Warning | feedback-warning | Attention |
| Critical | feedback-danger | Critical |
| Info | feedback-info | Knowledge / analysis flag |
| Accent | accent-primary-soft + accent-primary | Brand highlight, rare |

One badge family per card. Do not stack five colors.

---

# 4. Rules

- Soft fill + matching text. Do not use neon fills.
- Do not encode meaning with color alone.
- Do not place badges on Hero in a way that competes with the headline.
- Score uses Numeric → Level → Color → Meaning (PACK_03 §23), not a loose badge cluster.

---

END
