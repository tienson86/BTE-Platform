/**
 * Environment configuration barrel.
 * Resolves typed presentation environment — no business config.
 */

import { developmentEnvironment } from "./development";
import { productionEnvironment } from "./production";
import { stagingEnvironment } from "./staging";
import {
  ENVIRONMENT_NAMES,
  type EnvironmentConfig,
  type EnvironmentName,
} from "./types";

export { developmentEnvironment } from "./development";
export { stagingEnvironment } from "./staging";
export { productionEnvironment } from "./production";
export { ENVIRONMENT_NAMES } from "./types";
export type { EnvironmentConfig, EnvironmentName } from "./types";

export const environmentCatalog: Record<EnvironmentName, EnvironmentConfig> = {
  development: developmentEnvironment,
  staging: stagingEnvironment,
  production: productionEnvironment,
};

/** Resolve environment config by name (defaults to development). */
export function getEnvironmentConfig(
  name: EnvironmentName | string | undefined = "development",
): EnvironmentConfig {
  if (name === "development" || name === "staging" || name === "production") {
    return environmentCatalog[name];
  }
  return environmentCatalog.development;
}

/**
 * Resolve from a process-like env object.
 * Reads `BTE_CUI_ENV` or `NODE_ENV` when present.
 */
export function resolveEnvironmentName(
  env: Record<string, string | undefined> | undefined = typeof process !== "undefined"
    ? process.env
    : undefined,
): EnvironmentName {
  const explicit = env?.BTE_CUI_ENV?.toLowerCase();
  if (explicit === "development" || explicit === "staging" || explicit === "production") {
    return explicit;
  }
  const nodeEnv = env?.NODE_ENV?.toLowerCase();
  if (nodeEnv === "production") {
    return "production";
  }
  if (nodeEnv === "test" || nodeEnv === "development") {
    return "development";
  }
  if (ENVIRONMENT_NAMES.includes(nodeEnv as EnvironmentName)) {
    return nodeEnv as EnvironmentName;
  }
  return "development";
}

/** Active environment config for the current process. */
export function getActiveEnvironment(
  env?: Record<string, string | undefined>,
): EnvironmentConfig {
  return getEnvironmentConfig(resolveEnvironmentName(env));
}
