# Versioning

**Applies to:** BTE Design System (`knowledge/design_system/`)  
**Infrastructure version:** 1.0.0

---

## Purpose

Versioning protects approved UI truth. Once a canonical reference is frozen, it must remain available for comparison, audit, and rollback.

---

## Rules

1. **Never overwrite** a previous canonical file.
2. Each new freeze creates a **new versioned filename**.
3. Status of a file may be annotated in the document body (`DRAFT`, `REVIEW`, `CANONICAL`, `SUPERSEDED`), but the file itself is never deleted to “replace” an older version.
4. Superseded files stay in place; the newer file becomes the active canonical.
5. Infrastructure / docs changes that are not a new UI freeze update `CHANGELOG.md` and the Design System version in `README.md`.

---

## Canonical Version Labels

| Label | Meaning |
|-------|---------|
| **V1** | First frozen canonical for a surface + device |
| **V2** | Second freeze; V1 remains on disk |
| **V3** | Third freeze; V1 and V2 remain on disk |
| **Vn** | Continue sequentially; never reuse a number |

---

## Filename Pattern

```text
CANONICAL_<SURFACE>_<DEVICE>_V<n>.md
```

Examples:

- `CANONICAL_PORTAL_UI_DESKTOP_V1.md`
- `CANONICAL_PORTAL_UI_DESKTOP_V2.md`
- `CANONICAL_PORTAL_UI_TABLET_V1.md`
- `CANONICAL_PORTAL_UI_MOBILE_V1.md`

Matching exports (when present) use the same version token:

```text
CANONICAL_PORTAL_UI_DESKTOP_V2.png
CANONICAL_PORTAL_UI_DESKTOP_V2.svg
```

See `07_exports/export_rule.md`.

---

## What Counts as a New Version

Create a new `Vn+1` when any of the following is approved:

- Structural layout change of the canonical surface
- Section order or major composition change
- Token-level visual system change that alters the frozen look
- Device-class redesign (desktop / tablet / mobile)

Do **not** bump canonical version for:

- Typo fixes in markdown
- Clarifying documentation without visual change
- Checklist wording updates

Those go into `CHANGELOG.md` only.

---

## Active Canonical

For each surface + device, the **highest approved Vn** with status `CANONICAL` is the active source of truth.

Older versions remain historical references.

---

## Forbidden

- Overwriting `…_V1.md` with V2 content
- Renaming an old version to free the name
- Deleting previous canonical markdown or exports after freeze
- Sharing one filename across devices
