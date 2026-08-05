/**
 * API runtime configuration — no hardcoded production URLs (TASK_003A).
 */

export type DataSourceMode = "api" | "mock";

export type ApiRuntimeConfig = {
  readonly baseUrl: string;
  readonly timeoutMs: number;
  readonly retries: number;
  readonly dataSource: DataSourceMode;
};

type EnvBag = Record<string, string | undefined>;

function readImportMetaEnv(): EnvBag | undefined {
  try {
    const meta = import.meta as ImportMeta & { env?: EnvBag };
    return meta.env;
  } catch {
    return undefined;
  }
}

function readProcessEnv(): EnvBag | undefined {
  if (typeof process === "undefined") {
    return undefined;
  }
  return process.env as EnvBag;
}

/** Read a single env key from Vite `import.meta.env` or `process.env`. */
export function readEnv(key: string, env?: EnvBag): string | undefined {
  const bag = env ?? { ...readProcessEnv(), ...readImportMetaEnv() };
  const value = bag[key];
  if (value === undefined || value === "") {
    return undefined;
  }
  return value;
}

function isBrowser(): boolean {
  return typeof window !== "undefined" && typeof window.document !== "undefined";
}

function isTestRuntime(env?: EnvBag): boolean {
  const bag = env ?? { ...readProcessEnv(), ...readImportMetaEnv() };
  if (bag.VITEST === "true" || bag.VITEST === "1") {
    return true;
  }
  if (bag.NODE_ENV === "test") {
    return true;
  }
  return false;
}

function normalizeBaseUrl(raw: string): string {
  return raw.replace(/\/+$/, "");
}

/**
 * Resolve API base URL.
 * Prefer VITE_API_BASE_URL / BTE_API_BASE_URL; otherwise same-origin portal proxy.
 */
export function resolveApiBaseUrl(env?: EnvBag): string {
  const vite = readEnv("VITE_API_BASE_URL", env);
  if (vite) {
    return normalizeBaseUrl(vite);
  }

  const bte = readEnv("BTE_API_BASE_URL", env);
  if (bte) {
    const trimmed = normalizeBaseUrl(bte);
    if (/\/api\/v1$/i.test(trimmed)) {
      return trimmed;
    }
    return `${trimmed}/api/v1`;
  }

  // Same-origin FastAPI portal proxy (legacy static client uses `/backend` + path).
  if (isBrowser()) {
    return "/backend/api/v1";
  }

  return "http://127.0.0.1:8000/api/v1";
}

export function resolveDataSource(env?: EnvBag): DataSourceMode {
  const explicit = readEnv("VITE_DATA_SOURCE", env) ?? readEnv("BTE_DATA_SOURCE", env);
  if (explicit === "mock" || explicit === "api") {
    return explicit;
  }
  // Preserve existing screen tests without network calls.
  if (isTestRuntime(env)) {
    return "mock";
  }
  return "api";
}

export function resolveTimeoutMs(env?: EnvBag): number {
  const raw = readEnv("VITE_API_TIMEOUT_MS", env) ?? readEnv("BTE_API_TIMEOUT_MS", env);
  const parsed = raw ? Number(raw) : NaN;
  if (Number.isFinite(parsed) && parsed > 0) {
    return parsed;
  }
  return 30_000;
}

export function resolveRetries(env?: EnvBag): number {
  const raw = readEnv("VITE_API_RETRIES", env) ?? readEnv("BTE_API_RETRIES", env);
  const parsed = raw ? Number(raw) : NaN;
  if (Number.isFinite(parsed) && parsed >= 0) {
    return Math.floor(parsed);
  }
  return 2;
}

/** Active API runtime config. */
export function getApiRuntimeConfig(env?: EnvBag): ApiRuntimeConfig {
  return {
    baseUrl: resolveApiBaseUrl(env),
    timeoutMs: resolveTimeoutMs(env),
    retries: resolveRetries(env),
    dataSource: resolveDataSource(env),
  };
}

export function isMockDataSource(env?: EnvBag): boolean {
  return resolveDataSource(env) === "mock";
}
