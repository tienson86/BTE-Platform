/**
 * BaZi Result Workspace V2 — workspace foundation + canonical panel shells.
 */

export { ResultWorkspace } from "./ResultWorkspace";
export type { ResultWorkspaceProps } from "./ResultWorkspace";
export { CanonicalWorkspaceCard } from "./cards/CanonicalWorkspaceCard";
export {
  WorkspaceHeader,
  WorkspaceSidebar,
  WorkspaceTopNav,
} from "./chrome/WorkspaceChrome";
export {
  ACTION_CHIPS,
  EMPTY_COPY,
  FIVE_ELEMENTS,
  INTERPRETATION_BLOCKS,
  NO_RESULT_COPY,
  OVERVIEW_SLOTS,
  SHEN_SHA_NAMES,
  TEN_GODS,
} from "./catalog";
export { adaptBaziWorkspace, WORKSPACE_SOURCE_MAP } from "./adapter";
export type { BaziWorkspaceViewModel } from "./adapter";
export {
  EMPTY_TU_TRU_PILLAR,
  WORKSPACE_BREAKPOINTS,
  WORKSPACE_GRID_COLUMNS,
  WORKSPACE_PANELS,
  WORKSPACE_TOP_NAV,
} from "./layout";
export { PREVIEW_FIXTURE_KIND } from "./previewFixture";
export type {
  TuTruSlotPillar,
  WorkspaceNavItem,
  WorkspacePanelId,
  WorkspacePanelKind,
  WorkspacePanelSpec,
} from "./types";
