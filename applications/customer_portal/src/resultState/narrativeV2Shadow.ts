/**
 * Narrative V2 shadow flag. Production /result ignores this.
 */

export const NARRATIVE_V2_QUERY = "narrative";
export const NARRATIVE_V2_SHADOW_VALUE = "v2-shadow";
export const NARRATIVE_V2_COMPARE_VALUE = "v2-compare";

export type ResultNarrativeSurface = "production" | "v2-shadow" | "v2-compare";

/**
 * Resolve which Result surface to mount. Default is production Narrative V2.
 */
export function resolveResultSurface(
  search: string,
  pathname: string = "/result",
): ResultNarrativeSurface {
  const path = pathname.replace(/\/+$/, "") || "/";
  if (path !== "/result") {
    return "production";
  }
  const raw = search.startsWith("?") ? search.slice(1) : search;
  const mode = new URLSearchParams(raw).get(NARRATIVE_V2_QUERY);
  if (mode === NARRATIVE_V2_SHADOW_VALUE) {
    return "v2-shadow";
  }
  if (mode === NARRATIVE_V2_COMPARE_VALUE) {
    return "v2-compare";
  }
  return "production";
}
