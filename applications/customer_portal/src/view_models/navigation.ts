/**
 * Navigation presentation ViewModels — WP-0011.
 * Presentation flow metadata only. No derived reading state.
 */

import type { PresentationStatus } from "./executive_summary";

export type NavigationItemViewModel = {
  id: string;
  label: string;
  href: string;
  active?: boolean;
};

export type NavigationCurrentSectionViewModel = {
  id: string;
  label: string;
};

export type NavigationBreadcrumbItemViewModel = {
  id: string;
  label: string;
  href?: string;
};

export type NavigationBackToTopViewModel = {
  label: string;
  href: string;
  visible: boolean;
};

export type NavigationPrintViewModel = {
  label: string;
  href?: string;
  note?: string;
};

export type NavigationReadyViewModel = {
  status: "ready";
  title?: string;
  railTitle?: string;
  tocTitle?: string;
  items: NavigationItemViewModel[];
  toc: NavigationItemViewModel[];
  currentSection: NavigationCurrentSectionViewModel;
  progress: number;
  breadcrumbs: NavigationBreadcrumbItemViewModel[];
  jumpTargets: NavigationItemViewModel[];
  anchors: NavigationItemViewModel[];
  backToTop: NavigationBackToTopViewModel;
  print: NavigationPrintViewModel;
};

export type NavigationPendingViewModel = {
  status: Exclude<PresentationStatus, "ready" | "error">;
};

export type NavigationErrorViewModel = {
  status: "error";
  errorMessage?: string;
};

export type NavigationViewModel =
  | NavigationReadyViewModel
  | NavigationPendingViewModel
  | NavigationErrorViewModel;
