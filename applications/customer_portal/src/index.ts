/**
 * Commercial UI V3 — Foundation public API (WP-0001 / WP-0001A).
 * No business screens. No business components. No bindings.
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

export const commercialUiVersion = "3.0.0" as const;
export const workPackageId = "WP-0001" as const;
export const hardeningMissionId = "WP-0001A" as const;
export const baseComponentsWorkPackageId = "WP-0002" as const;
export const sharedComponentsWorkPackageId = "WP-0003" as const;
