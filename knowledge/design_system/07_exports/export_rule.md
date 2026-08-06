# Export Rule

**Status:** Active  
**Version:** 1.0.0  
**Location:** `knowledge/design_system/07_exports/`

---

## Purpose

Define how design artifacts are exported and named for BTE Design System freezes.

Exports support review, audit, and implementation alignment. They do not replace canonical markdown documentation.

---

## Supported Formats

| Format | Use | Notes |
|--------|-----|-------|
| **SVG** | Vector UI chrome, icons, logos, diagrams | Preferred for scalable UI elements |
| **PDF** | Printable full-page canonical / review packs | Preserve fonts when possible |
| **PNG** | Raster snapshots for review and visual diff | Use sufficient resolution for 1:1 review |
| **FIG** | Figma source (or Figma export package) | Source of truth for editable design files when used |

Do not invent one-off formats for canonical freezes without updating this document.

---

## Folder Placement

```text
07_exports/
├── export_rule.md
├── desktop/
├── tablet/
└── mobile/
```

Place files only in the matching device folder.

---

## Export Naming

### Canonical UI freezes

```text
CANONICAL_<SURFACE>_<DEVICE>_V<n>.<ext>
```

Examples:

- `CANONICAL_PORTAL_UI_DESKTOP_V2.png`
- `CANONICAL_PORTAL_UI_DESKTOP_V2.svg`
- `CANONICAL_PORTAL_UI_DESKTOP_V2.pdf`
- `CANONICAL_PORTAL_UI_TABLET_V1.fig`
- `CANONICAL_PORTAL_UI_MOBILE_V1.png`

### Section or partial exports (optional)

```text
CANONICAL_<SURFACE>_<DEVICE>_V<n>_<SECTION>.<ext>
```

Example:

- `CANONICAL_PORTAL_UI_DESKTOP_V2_S11.png`

### Asset exports (non-canonical)

Use descriptive `snake_case` names under `06_assets/…` categories. Do not place non-canonical decorative assets in `07_exports/` unless they are part of a freeze pack.

---

## Versioning

- Export version token must match the markdown canonical version (`V1`, `V2`, `V3`, …)
- **Never overwrite** a previous export with the same version name
- If a corrected re-export is required for the same version, append a revision suffix only after governance approval, e.g. `_R2` — prefer bumping to the next canonical version for material visual changes

See `../versioning.md`.

---

## Quality Rules

| Format | Minimum expectation |
|--------|---------------------|
| PNG | Sharp at intended review zoom; no UI chrome from unrelated apps |
| SVG | Clean paths; no editor junk layers |
| PDF | Complete page(s); readable type |
| FIG | Linked to the freeze; document page / frame name in the companion markdown |

---

## Workflow

1. Approve visual freeze
2. Export to the correct device folder with versioned name
3. Reference the export path from the matching `05_canonical/…` markdown
4. Run the device review checklist in `08_reviews/`
5. Log in `CHANGELOG.md` when a new freeze export is added

---

## Out of Scope

- Generating assets as part of documentation-only infrastructure tasks
- Redesigning Portal or Consoles
