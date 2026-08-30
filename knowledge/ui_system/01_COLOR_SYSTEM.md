# 01_COLOR_SYSTEM.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- VISUAL_LANGUAGE_SYSTEM.md §10
- PACK_01_DESIGN_PRINCIPLES.md §7
- Existing commercial tokens (`--accent-primary`, `--bte-color-*`)

Do not invent colors. Values below are the official Commercial UI specification already present in Foundation implementation tokens.

---

# 1. Philosophy

Color communicates meaning.

Never use color only for decoration.

Each screen has one primary accent.

Typography, spacing, and contrast outrank color.

---

# 2. Roles

| Role | Purpose |
|------|---------|
| Primary | Brand identity and primary action |
| Secondary | Navigation and supporting chrome |
| Accent | Same family as Primary. One accent per screen. |
| Surface | Cards, callouts, overlays |
| Background | Page canvas |
| Success | Positive findings |
| Warning | Attention |
| Critical | Critical issues |
| Neutral | Supporting content and text |

---

# 3. Official tokens

## Primary / Accent

| Token | Value | Use |
|-------|-------|-----|
| `--accent-primary` | `#059669` | Brand, primary CTA, focus |
| `--accent-primary-hover` | `#047857` | Hover |
| `--accent-primary-soft` | `#ecfdf5` | Soft fill |
| `--bte-color-primary` | `--bte-color-primary-600` | Canonical primary |

Emerald is the commercial primary. Do not introduce a second brand hue.

## Secondary / Neutral

| Token | Value | Use |
|-------|-------|-----|
| `--bte-color-secondary-600` | `#475569` | Secondary chrome |
| `--text-primary` | `#1a1d23` | Body and titles |
| `--text-secondary` | `#4a5568` | Supporting text |
| `--text-muted` | `#6b7280` | Captions, meta |
| `--border-divider` | `#e2e5eb` | Quiet division |

## Surface / Background

| Token | Value | Use |
|-------|-------|-----|
| `--surface-background` | `#eef0f3` | Page background |
| `--surface-report-paper` | `#ffffff` | Card / report paper |
| `--surface-section` | `#f7f8fa` | Section well |
| `--surface-callout` | `#f0f3f7` | Nested callout |
| `--surface-overlay` | `#ffffff` | Overlay |

## Status

| Role | Token | Value |
|------|-------|-------|
| Success | `--feedback-success` | `#16a34a` |
| Success soft | `--feedback-success-soft` | `#f0fdf4` |
| Warning | `--feedback-warning` | `#d97706` |
| Warning soft | `--feedback-warning-soft` | `#fffbeb` |
| Critical | `--feedback-danger` | `#dc2626` |
| Critical soft | `--feedback-danger-soft` | `#fef2f2` |
| Info | `--feedback-info` | `#0284c7` |
| Info soft | `--feedback-info-soft` | `#f0f9ff` |

---

# 4. Meaning map (PACK_01)

| Meaning | Color family |
|---------|----------------|
| Positive / healthy | Success green |
| Attention / action | Warning amber |
| Critical / weakness | Critical red |
| Knowledge / analysis | Info blue (tertiary only) |
| Supporting | Neutral gray |

Do not color every metric. Most analytical content stays Neutral + Primary accent.

---

# 5. Rules

- No raw hex in future component CSS. Consume tokens only.
- Status color always pairs with a label or icon. Color is never the only signal.
- Charts use Neutral structure first; status colors only for meaning.
- Dark decorative gradients are forbidden.

---

END
