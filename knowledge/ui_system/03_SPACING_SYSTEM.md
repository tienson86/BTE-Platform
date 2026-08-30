# 03_SPACING_SYSTEM.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- PACK_02_LAYOUT_SYSTEM.md §7–8, §20

Do not invent spacing. The PACK_02 scale is canonical.

---

# 1. Philosophy

Whitespace is information.

Visual rhythm lets users scan.

Never remove space to fit more data.

No custom spacing values.

---

# 2. Official scale

```
4
8
12
16
24
32
40
48
64
80
96
```

Tokens

| Step | Token |
|------|-------|
| 4 | `--bte-space-4` / `--space-1` |
| 8 | `--bte-space-8` / `--space-2` |
| 12 | `--bte-space-12` / `--space-3` |
| 16 | `--bte-space-16` / `--space-4` |
| 24 | `--bte-space-24` / `--space-5` |
| 32 | `--bte-space-32` / `--space-6` |
| 40 | `--bte-space-40` |
| 48 | `--bte-space-48` / `--space-7` |
| 64 | `--bte-space-64` / `--space-8` |
| 80 | `--bte-space-80` |
| 96 | `--bte-space-96` / `--space-9` |

PACK_02 wins if an implementation token is missing a step. Use `--bte-space-*` for the full scale.

---

# 3. Vertical rhythm

| Context | Space |
|---------|-------|
| Sections | 32px |
| Rows | 24px |
| Between cards | 24px |
| Inside card | 16px |
| Component gap | 12px |
| Inline | 8px |

---

# 4. Page padding

| Viewport | Padding |
|----------|---------|
| Desktop | 32px |
| Tablet | 24px |
| Mobile | 16px |

---

# 5. Radius

PACK_03 official radii (components):

| Size | Value | Use |
|------|-------|-----|
| Small | 6px | Controls, badges |
| Medium | 10px | Cards |
| Large | 14px | Overlays |
| Round | 9999px | Pills, avatars |

Tokens: `--radius-control` 6px, `--radius-overlay` 8px, `--bte-radius-md` 12px. Prefer PACK_03 6 / 10 / 14 when specifying new Commercial UI. Do not introduce 11px, 13px, or other one-off radii.

---

# 6. Elevation / shadow

Subtle only. Avoid heavy shadows.

| Level | Use | Token |
|-------|-----|-------|
| 0 | Flat / paper | `--elevation-none` |
| 1 | Card | `--elevation-soft` / `--bte-shadow-sm` |
| 2 | Dropdown | `--bte-shadow-md` |
| 3 | Dialog | `--elevation-overlay` |
| 4 | Modal | `--elevation-modal` / `--bte-shadow-xl` |

Surfaces should separate mainly by spacing and paper contrast, not by stacked shadows.

---

END
