# 09_MOTION_SYSTEM.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- PACK_04_UI_PRESENTATION_STANDARD.md §16
- PACK_05_ACCESSIBILITY.md §14

Do not invent durations. Use official motion tokens.

---

# 1. Philosophy

Motion guides, explains, and confirms.

It never entertains.

Information over animation.

Calm over excitement.

---

# 2. Official durations

| Token | Value | Use |
|-------|-------|-----|
| `--motion-instant` | 0ms | Reduced motion / snaps |
| `--motion-fast` / `--bte-motion-fast` | 120ms | Collapse, small state |
| `--motion-normal` / `--bte-motion-normal` | 200ms | Fade, expand |
| `--motion-slow` / `--bte-motion-slow` | 320ms | Rare. Overlay enter |

PACK_04 bands: Short 100–150ms · Normal 200–300ms · Long 400ms maximum. Nothing exceeds 500ms.

Easing: `--motion-ease-out` / `--bte-motion-easing` `cubic-bezier(0.22, 1, 0.36, 1)`.

---

# 3. Allowed

Fade · Slide · Expand · Collapse · Loading skeleton · Progress.

---

# 4. Hierarchy

| Priority | Motion |
|----------|--------|
| Highest | State change |
| Medium | Expansion |
| Lowest | Decorative (discouraged) |

---

# 5. Reduced motion

When `prefers-reduced-motion: reduce`, all motion tokens are 0ms.

Layout must remain stable without animation.

---

# 6. Forbidden

- Looping decorative motion
- Layout jumps after load
- Motion that is the only status signal
- Chart celebration effects

---

END
