/**
 * Production narrative provider. Pack05 is retired from production flags.
 * Archive access is PACK05_LEGACY (read-only), not a production switch.
 */

export const NARRATIVE_PROVIDER_QUERY = "provider";
export const NARRATIVE_PROVIDER_DEFAULT = "v2";
export const NARRATIVE_PROVIDERS = ["v2"] as const;

export type NarrativeProvider = (typeof NARRATIVE_PROVIDERS)[number];

type EnvBag = Record<string, string | undefined>;

declare global {
  interface Window {
    __BTE_NARRATIVE_PROVIDER__?: string;
    __BTE_PACK05_LEGACY__?: string;
  }
}

/**
 * True when value is a production provider. Pack05 is not allowed.
 */
export function isNarrativeProvider(value: unknown): value is NarrativeProvider {
  return value === "v2";
}

function normalizeProvider(value: unknown): NarrativeProvider | null {
  if (typeof value !== "string") return null;
  const next = value.trim().toLowerCase();
  if (next === "pack05" || next === "auto") {
    return null;
  }
  return isNarrativeProvider(next) ? next : null;
}

function readQueryProvider(search: string): NarrativeProvider | null {
  const raw = search.startsWith("?") ? search.slice(1) : search;
  return normalizeProvider(new URLSearchParams(raw).get(NARRATIVE_PROVIDER_QUERY));
}

function readBootProvider(): NarrativeProvider | null {
  if (typeof window === "undefined") return null;
  return normalizeProvider(window.__BTE_NARRATIVE_PROVIDER__);
}

function readEnvProvider(env?: EnvBag): NarrativeProvider | null {
  const bag =
    env ??
    ({
      ...(typeof process !== "undefined" ? process.env : {}),
      ...((() => {
        try {
          return (import.meta as ImportMeta & { env?: EnvBag }).env;
        } catch {
          return undefined;
        }
      })() ?? {}),
    } as EnvBag);
  return (
    normalizeProvider(bag.NARRATIVE_PROVIDER) ??
    normalizeProvider(bag.VITE_NARRATIVE_PROVIDER)
  );
}

/**
 * Resolve the production provider. Pack05 flags are ignored.
 */
export function resolveNarrativeProvider(
  search: string = typeof window !== "undefined" ? window.location.search : "",
  env?: EnvBag,
): NarrativeProvider {
  return (
    readQueryProvider(search) ??
    readBootProvider() ??
    readEnvProvider(env) ??
    NARRATIVE_PROVIDER_DEFAULT
  );
}
