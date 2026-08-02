# BTE Frontend — Design System

**Package:** `@bte/design-system` (`frontend/design_system/`)  
**Version:** 1.0.0  
**Sprint:** UI Sprint 01 — Foundation only (no screen redesign)

## Purpose

Single shared Design System so Customer Portal (CSS tokens) and React consoles (components) can consume the same visual language.

## Theme

Light / Dark via `[data-theme="light"|"dark"]` or `.dark`.

## Color tokens

| Token | Role |
|-------|------|
| `--bte-color-primary` | Brand actions / highlights |
| `--bte-color-secondary` | Secondary text / chrome |
| `--bte-color-success` | Positive status |
| `--bte-color-warning` | Caution |
| `--bte-color-danger` | Errors |
| `--bte-color-info` | Informational |
| `--bte-color-neutral` | Neutral badge |
| `--bte-color-bg` / `panel` / `card` / `line` / `ink` / `muted` | Surfaces & text |

Components must reference these variables — never hard-code hex.

## Typography

| Class | Role |
|-------|------|
| `.bte-h1` | Page title |
| `.bte-h2` | Section title |
| `.bte-h3` | Card title |
| `.bte-subtitle` | Supporting headline |
| `.bte-body` | Body copy |
| `.bte-caption` | Hints / meta |
| `.bte-metric` | Large numeric |
| `.bte-label` | Uppercase field label |

## Spacing

Scale: `--bte-space-1` … `--bte-space-12` (4px → 48px). Helpers: `.bte-stack-*`, `.bte-row-*`, `.bte-p-*`.

## Animation

Fade-in, expand/collapse, skeleton pulse — durations via `--bte-motion-*`. Honors `prefers-reduced-motion`.

## Adoption

```ts
import "@bte/design-system/styles.css";
import { MetricCard, StatusBadge } from "@bte/design-system";
```

Portal CSS already uses an aligned Linear/Stripe token set; migrate imports to `@bte/design-system/tokens.css` in a follow-up wiring sprint (static hosting path permitting).

## Related

- [layout_architecture.md](layout_architecture.md)
- [component_catalog.md](component_catalog.md)
