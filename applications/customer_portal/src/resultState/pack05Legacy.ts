/**
 * Pack05 legacy archive flag. Read-only. Not a production provider.
 */

export const PACK05_LEGACY_QUERY = "legacy";
export const PACK05_LEGACY_VALUE = "pack05";

type EnvBag = Record<string, string | undefined>;

/**
 * True when Pack05 may be read as a historical archive.
 * Never selects Pack05 for production Portal rendering.
 */
export function isPack05LegacyEnabled(
  search: string = typeof window !== "undefined" ? window.location.search : "",
  env?: EnvBag,
): boolean {
  const raw = search.startsWith("?") ? search.slice(1) : search;
  const query = new URLSearchParams(raw).get(PACK05_LEGACY_QUERY);
  if (query === PACK05_LEGACY_VALUE || query === "1" || query === "true") {
    return true;
  }
  if (typeof window !== "undefined" && window.__BTE_PACK05_LEGACY__) {
    const boot = window.__BTE_PACK05_LEGACY__.trim().toLowerCase();
    if (boot === "1" || boot === "true" || boot === "pack05") return true;
  }
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
  const flag = (bag.PACK05_LEGACY ?? bag.VITE_PACK05_LEGACY ?? "").trim().toLowerCase();
  return flag === "1" || flag === "true" || flag === "pack05";
}
