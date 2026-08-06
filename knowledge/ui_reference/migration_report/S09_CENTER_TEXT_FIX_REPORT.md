# S09 Center Text Fix

| Item | Value |
|------|-------|
| Task | **S09 Final Center Text Fix** |
| Status | **Complete** |
| Date | **2026-08-06** |

---

## Scope

Center text only. Bagua SVG asset, geometry, layout, CSS spacing, and component tree otherwise unchanged.

---

## Changes

| Element | Before | After |
|---------|--------|-------|
| Ly Hỏa | 16px / 700 | **12px / 600** (−25%) |
| 9 | 24px / 700 | **30px / 700** (+25%) |
| Rendering | HTML overlay | **SVG `<text>`** over `<image>` of approved asset |

Optical stack (centered in inner circle):

```
Ly Hỏa
  9
```

---

## Screenshot

`knowledge/ui_reference/migration_report/screenshots/s09_final/01_s09_only.png`

---

## Verification

| Check | Result |
|-------|--------|
| Build | **PASS** |
| TypeScript | **PASS** |
| Tests | **PASS** |

---

## Files

| File | Change |
|------|--------|
| `S09FengShuiGuidance.tsx` | Center text via SVG `<text>` |
| `screenshots/s09_final/01_s09_only.png` | Updated |
| `S09_CENTER_TEXT_FIX_REPORT.md` | This report |

`Bagua_HauThien.svg` — **not modified**.
