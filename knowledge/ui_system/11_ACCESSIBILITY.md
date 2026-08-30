# 11_ACCESSIBILITY.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- PACK_05_ACCESSIBILITY.md
- 01_COLOR_SYSTEM.md
- 02_TYPOGRAPHY.md
- 03_SPACING_SYSTEM.md
- 09_MOTION_SYSTEM.md

---

# 1. Philosophy

A commercial consulting product is unusable if it is unreadable.

Accessibility is not a theme. It is part of Visual System V2.

WCAG alignment follows PACK_05.

---

# 2. Contrast

- Body and titles on paper: `--text-primary` `#1a1d23` on `--surface-report-paper` `#ffffff`.
- Secondary text: `--text-secondary` `#4a5568`.
- Muted text is Caption / Label only, never long narrative.
- Status color is never the only signal.
- Decorative tints must not reduce text contrast.

---

# 3. Spacing

- Touch target minimum: `--touch-target-min` 44px.
- Inside-card padding 16px. Between cards 24px.
- Focus ring must not sit on the clipping edge of a tight badge. Prefer 8px inline padding on controls.

---

# 4. Focus

Token: `--focus-ring` `0 0 0 3px rgba(5, 150, 105, 0.32)` with `--border-focus` `#059669`.

- Visible focus on every interactive control.
- Focus order follows reading order.
- Keyboard: navigate, select, expand, collapse, submit without a mouse.

---

# 5. Type and motion

- Body 16px minimum for customer narrative.
- Do not scale type below Caption for essential content on mobile.
- Honor `prefers-reduced-motion`.

---

# 6. Charts, badges, icons

Color + label. Color + icon. Never color alone.

---

END
