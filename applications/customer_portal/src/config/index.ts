/**
 * Config layer barrel — environment + API runtime (TASK_003A).
 */

export * from "./environment";
export {
  getApiRuntimeConfig,
  isMockDataSource,
  readEnv,
  resolveApiBaseUrl,
  resolveDataSource,
  resolveRetries,
  resolveTimeoutMs,
} from "./api";
export type { ApiRuntimeConfig, DataSourceMode } from "./api";
