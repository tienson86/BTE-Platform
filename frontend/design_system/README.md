# @bte/design-system

Shared Design System & Layout Foundation for BTE Platform (UI Sprint 01).

## Install (workspace console)

```json
"@bte/design-system": "file:../../frontend/design_system"
```

```ts
import "@bte/design-system/styles.css";
import { Card, AppLayout, PageHeader } from "@bte/design-system";
```

## Scripts

```bash
cd frontend/design_system
npm install
npm run typecheck
npm run build
```

## Rules

- No hard-coded colors in components — use `--bte-color-*` tokens.
- No random spacing — use `--bte-space-*` scale.
- Screen redesigns belong to later UI sprints; this package is foundation only.
