# Commercial UI V3 — Foundation Architecture

Version: 3.0.0  
Work Package: WP-0001 (+ WP-0001A Hardening)  
Status: Architecture Stabilization

This document describes the **code** presentation foundation for Commercial UI V3
(tokens, folders, providers).

It does **not** replace platform Foundation V1.0.

## Platform Foundation V1.0 (read first)

```
Product Manifesto
↓
Experience Principles
↓
Brand Language
↓
Visual Language
↓
Design System (PACK_01–07)
↓
UI Implementation Guide
```

Entry: `knowledge/ui_reference/foundation/FOUNDATION_INDEX.md`  
Developer guide: `knowledge/ui_reference/foundation/FOUNDATION_DEVELOPER_GUIDE.md`  
Compliance: `knowledge/ui_reference/foundation/FOUNDATION_COMPLIANCE_CHECKLIST.md`

This document describes the presentation foundation for Commercial UI V3.
It defines folder ownership only. It does not define business screens,
business components, or analysis behaviour.

---

## Purpose

The foundation provides:

- Design Tokens and CSS variables
- Theme infrastructure (light / dark)
- Typography, spacing, grid, and surface systems
- Global layout shell classes
- Application providers (theme, error, loading)
- Typed environment configuration
- Stable import surfaces via barrel exports

Subsequent Work Packages (WP-0002 → WP-0012) consume this foundation.
They must not redefine it.

---

## Architecture Laws

1. Presentation only — no business logic, engine calls, or rule evaluation.
2. Design Tokens are the only visual source of truth.
3. Dependency flows downward: Screen → Layout → Business → Shared → Base → Tokens.
4. Public imports use barrel `index.ts` exports only.
5. No circular imports.

---

## Directory Responsibilities

### `app/`

Application bootstrap and provider composition.

Owns:

- Foundation bootstrap (`bootstrapFoundation`)
- `AppProviders` composition root
- Future app-level wiring (routing bootstrap later)

Must not:

- Render business screens
- Call analysis APIs
- Contain business terminology

---

### `layouts/`

Structural page/report layout helpers and class-name contracts.

Owns:

- Application frame / report sheet / reading column contracts
- Section width roles (reading / medium / wide)

Must not:

- Render business meaning
- Invent spacing or colors outside tokens

---

### `tokens/`

Design Token source of truth (TypeScript).

Owns:

- Core tokens (raw scales)
- Semantic tokens (meaning-first)
- Theme color palettes
- CSS variable name catalog

Must not:

- Contain React components
- Contain screen-specific values

---

### `styles/`

CSS implementation of the Design System.

Owns:

- Token CSS variables
- Light / dark themes
- Reset, typography, layout shell, utilities
- Component stylesheet slot (`styles/components/`)

Must not:

- Encode business rules
- Hardcode values that bypass tokens

Entry: import `@bte/commercial-ui-v3/styles.css` (or `styles/index.css`).

---

### `components/`

Reusable UI components, layered by responsibility.

| Subfolder | Responsibility | When populated |
|-----------|----------------|----------------|
| `base/` | Primitive UI (Button, Text, …) | WP-0002+ |
| `shared/` | Generic composed patterns | WP-0003+ |
| `business/` | BaZi presentation components | WP-0004+ |
| `feedback/` | Foundation feedback shells (Error / Loading boundaries) | WP-0001A |

Must not:

- Perform calculations
- Mutate payloads
- Call engines or knowledge base

---

### `bindings/`

Maps immutable analysis payloads → View Models.

Owns (future):

- Pure transform functions
- Binding contracts

Must not:

- Render HTML
- Style UI
- Contain business inference beyond mapping

Empty until binding Work Packages.

---

### `view_models/`

UI-ready presentation models.

Owns (future):

- Typed View Model interfaces / builders consumed by screens

Must not:

- Render
- Fetch data
- Contain CSS

Empty until View Model Work Packages.

---

### `hooks/`

Presentation-oriented React hooks.

Owns:

- Theme consumer hooks
- Future UI state hooks

Must not:

- Call engines directly
- Encode business rules

---

### `services/`

Presentation infrastructure services (API clients, cache, session — future).

Must not:

- Render
- Own Design Tokens

Empty until needed by later WPs.

---

### `constants/`

UI constants (breakpoints, storage keys shared with UI, foundation enums).

Must not:

- Hold business rule constants (those belong in Knowledge / Engine layers)

---

### `utils/`

Pure presentation helpers (`cx`, formatting helpers later).

Must not:

- Depend on screens or business components

---

### `types/`

Shared TypeScript contracts for the presentation layer.

---

### `theme/`

Theme runtime: DOM application, preference persistence, React `ThemeProvider`.

---

### `config/`

Typed environment configuration (development / staging / production).

Owns architecture for environment selection only.
No business feature flags required at this stage.

---

### `screens/`

Top-level report screens (Executive Summary, Four Pillars, …).

Empty until screen Work Packages. Do not place foundation code here.

---

### `icons/` / `assets/`

SVG icons and static presentation assets.

---

## Public Import Rule

Always import from barrels:

```ts
import { ThemeProvider, AppProviders, cssVar } from "@bte/commercial-ui-v3";
import { ErrorBoundary, LoadingBoundary } from "@bte/commercial-ui-v3";
```

Do not deep-import internal files from outside the package.

---

## Related Documents

- `NAMING_CONVENTIONS.md` — naming rules
- Pack 04 — `01_FOLDER_STRUCTURE.md`, `06_STYLING_STRATEGY.md`, `10_CODING_CONVENTIONS.md`
- Pack 06 — WP-0001 Foundation
