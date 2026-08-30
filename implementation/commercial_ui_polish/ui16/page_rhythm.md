# UI-16 Page Rhythm

Designed for later A4 portrait PDF (UI-17). This sprint is HTML preview only.

## Page geometry

- Size: A4 portrait
- Margins: 18mm / 16mm / 22mm / 16mm
- Header/footer safe area reserved via `@page` margin
- Sheet max-width 210mm in screen preview

## Break rules

| Block | Rule |
|-------|------|
| Cover | `page-break-after: always` |
| Section titles | `break-after: avoid` |
| Sections | `break-inside: avoid` where the block is short |
| Top Priority callout | `break-inside: avoid` |
| Finding cards | `break-inside: avoid` |
| Action items | `break-inside: avoid` |
| Supporting tables | `break-inside: avoid` |

## Vertical rhythm

Section padding uses the UI-13 spacing scale (`--bte-space-32` to `--bte-space-96`). Executive blocks use larger type and whitespace. Supporting analysis uses smaller sans type so it does not compete with Level 1–2 reading.

## Print preview

`@media print` hides the portal header and the preview banner, removes sheet shadow, and keeps paper white for contrast.
