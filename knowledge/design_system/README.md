# BTE Design System

**Version:** 1.0.0  
**Status:** Infrastructure  
**Scope:** Documentation + folder architecture only

---

## Purpose

The BTE Design System is the single source of truth for every user interface across the BTE Platform:

- Customer Portal
- Analysis Console
- Admin Console
- Future Mobile App

This repository tree defines principles, tokens, components, layouts, canonical references, assets, exports, and review checklists.

It does **not** replace application code. Implementation must follow these documents; documents must not silently diverge from approved canonical UI.

---

## Structure

```text
knowledge/design_system/
├── README.md
├── CHANGELOG.md
├── versioning.md
├── 00_design_principles/
├── 01_tokens/
├── 02_icons/
├── 03_components/
├── 04_layouts/
├── 05_canonical/
│   ├── desktop/
│   ├── tablet/
│   └── mobile/
├── 06_assets/
│   ├── bagua/
│   ├── tutru/
│   ├── icons/
│   ├── logos/
│   ├── illustrations/
│   └── backgrounds/
├── 07_exports/
│   ├── desktop/
│   ├── tablet/
│   └── mobile/
└── 08_reviews/
```

| Folder | Role |
|--------|------|
| `00_design_principles/` | Product and visual principles |
| `01_tokens/` | Color, type, radius, shadow, spacing scale |
| `02_icons/` | Icon system documentation |
| `03_components/` | Component contracts (docs only in V1.0) |
| `04_layouts/` | Grids, spacing, breakpoints |
| `05_canonical/` | Frozen canonical UI references by device |
| `06_assets/` | Approved static assets (folders prepared; assets added later) |
| `07_exports/` | Export rules and exported design artifacts |
| `08_reviews/` | Device review checklists |

---

## Naming Convention

### Folders

- Numbered prefixes for top-level order: `00_`, `01_`, …
- Lowercase `snake_case` for folder names
- Device folders: `desktop`, `tablet`, `mobile`

### Documents

- Topic docs: `lowercase_snake_case.md` (e.g. `desktop_grid.md`)
- Canonical docs: `CANONICAL_<SURFACE>_<DEVICE>_V<n>.md`
  - Example: `CANONICAL_PORTAL_UI_DESKTOP_V2.md`
- Checklists: `<device>_review_checklist.md`
- Root governance: `README.md`, `CHANGELOG.md`, `versioning.md`

### Assets & exports

See `07_exports/export_rule.md` for file naming of SVG, PDF, PNG, and FIG.

---

## Versioning

Rules live in [`versioning.md`](./versioning.md).

Summary:

- Canonical files are versioned (`V1`, `V2`, `V3`, …)
- **Never overwrite** a previous canonical file
- New major visual freeze → new versioned file
- Design System infrastructure version is tracked in `CHANGELOG.md`

---

## Workflow

1. **Define / update tokens or principles** in `00_` / `01_`
2. **Document components and layouts** in `03_` / `04_`
3. **Freeze canonical** under `05_canonical/<device>/` with a new versioned markdown file
4. **Store exports** under `07_exports/<device>/` following `export_rule.md`
5. **Review** using checklists in `08_reviews/`
6. **Log** the change in `CHANGELOG.md`

No step may redesign live Portal/Console UI by editing this tree alone. Implementation changes are separate tasks.

---

## Review Process

1. Author prepares docs and (when applicable) exports
2. Reviewer runs the matching checklist:
   - Desktop → `08_reviews/desktop_review_checklist.md`
   - Tablet → `08_reviews/tablet_review_checklist.md`
   - Mobile → `08_reviews/mobile_review_checklist.md`
3. Canonical status is granted only after checklist pass
4. Failed items are fixed or a new version file is opened — previous canonical files remain untouched

---

## Out of Scope (V1.0 Infrastructure)

- Redesigning UI
- Modifying Portal, Console, or shared components
- Creating new layouts in application code
- Moving screens
- Generating graphics or binary assets

---

## Related

- Existing UI master references may live under `knowledge/ui_master/`
- This Design System is the long-term home for cross-product UI standards
