# Commercial UI V3 — Naming Conventions

Version: 1.0.0  
Status: Foundation Hardening (WP-0001A)  
Authority: Pack 04 — Coding Conventions + this document

These rules are mandatory for WP-0002 through WP-0012.
No local exceptions without Architecture approval.

---

## 1. Folders

| Rule | Example |
|------|---------|
| kebab-case | `view_models/` is the sole historical exception (snake_case plural noun, Pack 04) |
| One responsibility per folder | `components/base/` |
| Forbidden names | `misc/`, `common/`, `temp/`, `helpers/`, `old/`, `new/`, `backup/` |

Use Pack 04 folder names exactly. Do not invent parallel trees.

---

## 2. Files

| Kind | Pattern | Example |
|------|---------|---------|
| Component module | `PascalCase.tsx` | `ErrorBoundary.tsx` |
| Hook module | `camelCase.ts` / `useX.ts` | `useTheme.ts` |
| Utility module | `camelCase.ts` | `cx.ts` |
| Constants module | `camelCase.ts` or domain noun | `breakpoints.ts` |
| Types module | `camelCase.ts` or `types.ts` | `environment.ts` |
| Barrel | `index.ts` only | `components/base/index.ts` |
| Stylesheet | `kebab-case.css` | `tokens.css` |
| Test | `*_foundation.test.ts` or `*.test.ts(x)` | `wp_0001a_hardening.test.tsx` |

One primary export per file when practical.

---

## 3. Components

| Rule | Example |
|------|---------|
| PascalCase | `LoadingBoundary` |
| Prefix by layer when ambiguous | `BaseButton`, `SharedCallout`, `ExecutiveHero` |
| No business verbs in base/shared | Avoid `CalculateScoreButton` |
| Feedback / foundation shells | `ErrorBoundary`, `LoadingBoundary` |

Props types: `ComponentNameProps` (PascalCase).

---

## 4. Hooks

| Rule | Example |
|------|---------|
| `use` + PascalCase remainder | `useTheme`, `useThemeMode` |
| camelCase file name matching export | `useTheme.ts` → `useTheme` |
| Presentation only | No engine calls |

---

## 5. Utilities

| Rule | Example |
|------|---------|
| camelCase functions | `cx`, `resolveBreakpoint` |
| Pure when possible | No hidden DOM mutation unless documented (`applyThemeMode`) |

---

## 6. Constants

| Rule | Example |
|------|---------|
| UPPER_SNAKE_CASE for exported constants | `THEME_STORAGE_KEY`, `REQUIRED_SEMANTIC_CSS_VARS` |
| `as const` objects for catalogs | `layoutClassNames`, `breakpoints` |

---

## 7. View Models

| Rule | Example |
|------|---------|
| PascalCase + `ViewModel` suffix | `ExecutiveSummaryViewModel` |
| File: domain snake file under `view_models/` | `executive_summary.ts` → `ExecutiveSummaryViewModel` |
| No HTML / CSS in View Models | Data only |

---

## 8. Bindings

| Rule | Example |
|------|---------|
| Verb + domain + `Binding` or `to*ViewModel` | `toExecutiveSummaryViewModel` |
| Pure functions | Input payload → View Model |
| File names: snake_case matching domain | `executive_summary_binding.ts` |

---

## 9. Types / Interfaces

| Rule | Example |
|------|---------|
| PascalCase | `ThemeMode`, `EnvironmentName` |
| Prefer `type` for unions; `interface` for object contracts when extending | `ThemeColorPalette` |
| Props: `*Props`; context: `*ContextValue` | `ThemeContextValue` |

---

## 10. CSS

| Rule | Example |
|------|---------|
| Custom properties: kebab-case, semantic | `--surface-report-paper` |
| Foundation layout classes: `cui-` prefix | `.cui-report-sheet` |
| Typography classes: `cui-type-*` | `.cui-type-body` |
| No hardcoded colors / spacing in components | `var(--space-block)` only |

---

## 11. Design Tokens (TypeScript)

| Rule | Example |
|------|---------|
| snake_case keys in token objects | `space_section`, `surface_report_paper` |
| CSS mirror: kebab-case | `--space-section` |
| Never expose core tokens to components | Consume semantic / CSS vars |

---

## 12. Import Paths

Public consumers must use barrels:

```ts
// Correct
import { ThemeProvider } from "@bte/commercial-ui-v3";
import { cx } from "@bte/commercial-ui-v3";

// Forbidden outside package internals
import { cx } from "@bte/commercial-ui-v3/src/utils/cx";
```

Import order (Pack 04):

1. Framework (React)
2. Third-party
3. Application / package barrels
4. Business → Shared → Base
5. Styles

---

## 13. Export Rules

- Prefer named exports
- Default exports only for documented entry points (none required in foundation)
- Every public folder exposes `index.ts`

---

## 14. Forbidden Patterns

- Inventing folder names outside Pack 04
- Mixing business logic into components
- Deep imports bypassing barrels
- Hardcoded visual values
- `any` without Architecture approval
- Abbreviated opaque names (`btn1`, `data2`, `tmp`)

---

## Freeze

After Architecture Review of WP-0001A, these conventions are binding for all Commercial UI V3 implementation.
