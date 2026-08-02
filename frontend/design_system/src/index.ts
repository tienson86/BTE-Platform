/**
 * @bte/design-system — BTE UI Sprint 01 foundation
 * Import styles once: `import "@bte/design-system/styles.css"`
 */

export * from "./tokens";
export * from "./components";
export * from "./layout";
export { cx } from "./utils/cx";

/** Lazy-friendly named groups for code-splitting consumers */
export const designSystemVersion = "1.0.0" as const;
