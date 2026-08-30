# 06_ICON_SYSTEM.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- PACK_03_COMPONENT_STANDARD.md §19
- PACK_05_ACCESSIBILITY.md §6

---

# 1. Philosophy

Icons communicate meaning.

Never decorate.

Never replace a required label for status, error, or navigation.

Unified stroke style. No mixed icon families on one screen.

---

# 2. Official sizes

| Size | Token | Use |
|------|-------|-----|
| 12 | `--bte-icon-xs` | Dense meta only |
| 16 | `--bte-icon-sm` | Inline with Caption / Label |
| 20 | `--bte-icon-md` | Default UI |
| 24 | `--bte-icon-lg` | Header, empty state |
| 32 | `--bte-icon-xl` | Hero / empty illustration cap |
| 40 | `--bte-icon-2xl` | Rare. Empty-state only |

PACK_03 maximum set: 16, 20, 24, 32. Prefer those four. 12 and 40 are token extremes, not decoration sizes.

---

# 3. Style

- Outline / stroke, not filled marketing glyphs.
- Align to the text cap-height of the paired label.
- Color: Neutral by default. Status color only when the icon encodes Success, Warning, or Critical.
- One optical weight across the product.

---

# 4. Rules

- Icon + text for status. Icon alone is not sufficient (PACK_05).
- No animated icons except reduced-motion-safe loading spinners.
- No emoji as UI icons.
- No new icon pack this sprint. Specify unification only.

---

END
