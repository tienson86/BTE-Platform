/**
 * BZ-UI-01 Result Workspace V2 — presentation contracts.
 * Layout only. No engine, API, or calculation types.
 */

export type WorkspacePanelId =
  | "tu-tru"
  | "overview"
  | "five-elements"
  | "ten-gods"
  | "destiny"
  | "shen-sha"
  | "bone-weight"
  | "luck-cycles"
  | "interpretation"
  | "conclusion";

export type WorkspacePanelKind = "canonical-tu-tru" | "canonical-shell";

export type WorkspacePanelSpec = {
  readonly id: WorkspacePanelId;
  readonly title: string;
  readonly span: 3 | 4 | 6 | 10;
  readonly kind: WorkspacePanelKind;
  readonly row: 1 | 2 | 3 | 4;
};

export type WorkspaceNavItem = {
  readonly id: string;
  readonly label: string;
  readonly href: string;
  readonly active?: boolean;
};

export type TuTruSlotPillar = {
  readonly canChi: string;
  readonly napAm: string;
  readonly cungPhi: string;
};
