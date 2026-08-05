/**
 * Layout infrastructure helpers — Pack 01 / Pack 02 Grid.
 * No business rendering. Structural class names only.
 * Kept for Commercial UI report-frame compatibility.
 */

export const layoutClassNames = {
  applicationFrame: "cui-application-frame",
  topBar: "cui-top-bar",
  readingRail: "cui-reading-rail",
  reportSheet: "cui-report-sheet",
  contentGrid: "cui-content-grid",
  readingColumn: "cui-reading-column",
  wideColumn: "cui-wide-column",
  mediumColumn: "cui-medium-column",
  pageFooter: "cui-page-footer",
  surfaceBackground: "cui-surface-background",
  surfacePaper: "cui-surface-paper",
  surfaceSection: "cui-surface-section",
  surfaceCallout: "cui-surface-callout",
  surfaceOverlay: "cui-surface-overlay",
} as const;

export type LayoutClassName =
  (typeof layoutClassNames)[keyof typeof layoutClassNames];

/** Section width roles from Pack 02 — 02_GRID_SYSTEM §12. */
export const sectionWidthRoles = {
  reading: "reading",
  medium: "medium",
  wide: "wide",
} as const;

export type SectionWidthRole =
  (typeof sectionWidthRoles)[keyof typeof sectionWidthRoles];

export function sectionWidthClass(role: SectionWidthRole): string {
  switch (role) {
    case "wide":
      return layoutClassNames.wideColumn;
    case "medium":
      return layoutClassNames.mediumColumn;
    case "reading":
    default:
      return layoutClassNames.readingColumn;
  }
}
