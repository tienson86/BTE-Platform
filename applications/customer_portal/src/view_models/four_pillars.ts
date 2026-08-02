/**
 * Four Pillars presentation ViewModels — WP-0005.
 * Presentation-ready data only. No engine entities.
 */

import type { PresentationStatus } from "./executive_summary";

export type PillarKind = "year" | "month" | "day" | "hour";

export type HeavenlyStemCellViewModel = {
  label: string;
  symbol?: string;
  elementLabel?: string;
  tenGodLabel?: string;
};

export type EarthlyBranchCellViewModel = {
  label: string;
  symbol?: string;
  elementLabel?: string;
  animalLabel?: string;
};

export type HiddenStemItemViewModel = {
  id: string;
  label: string;
  tenGodLabel?: string;
};

export type PillarViewModel = {
  kind: PillarKind;
  title: string;
  isDayMaster?: boolean;
  stem: HeavenlyStemCellViewModel;
  branch: EarthlyBranchCellViewModel;
  hiddenStems: HiddenStemItemViewModel[];
  tenGodLabels?: string[];
  naYin?: string;
  lifeStage?: string;
};

export type ChartMetadataItemViewModel = {
  id: string;
  label: string;
  value: string;
};

export type ChartLegendItemViewModel = {
  id: string;
  label: string;
  description: string;
};

export type FourPillarsTransitionViewModel = {
  label: string;
  href?: string;
};

export type FourPillarsReadyViewModel = {
  status: "ready";
  title?: string;
  overview?: string;
  pillars: PillarViewModel[];
  metadata: ChartMetadataItemViewModel[];
  legend: ChartLegendItemViewModel[];
  transition?: FourPillarsTransitionViewModel;
};

export type FourPillarsPendingViewModel = {
  status: Exclude<PresentationStatus, "ready" | "error">;
};

export type FourPillarsErrorViewModel = {
  status: "error";
  errorMessage?: string;
};

export type FourPillarsViewModel =
  | FourPillarsReadyViewModel
  | FourPillarsPendingViewModel
  | FourPillarsErrorViewModel;
