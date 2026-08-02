/**
 * Commercial UI V3 — public API (WP-0001 … WP-0007).
 * Screens and business components are presentation-only.
 */

export * from "./tokens";
export * from "./theme";
export * from "./layouts";
export * from "./constants";
export * from "./utils";
export * from "./hooks";
export * from "./app";
export * from "./components";
export * from "./config";
export * from "./styles";
export * from "./types";
export * from "./view_models";
export * from "./screens";

export const commercialUiVersion = "3.0.0" as const;
export const workPackageId = "WP-0001" as const;
export const hardeningMissionId = "WP-0001A" as const;
export const baseComponentsWorkPackageId = "WP-0002" as const;
export const sharedComponentsWorkPackageId = "WP-0003" as const;
export const executiveSummaryWorkPackageId = "WP-0004" as const;
export const fourPillarsWorkPackageId = "WP-0005" as const;
export const executiveInsightWorkPackageId = "WP-0006" as const;
export const metricsWorkPackageId = "WP-0007" as const;
