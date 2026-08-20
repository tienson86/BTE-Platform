/**
 * Canonical Useful God V1.0 presentation helpers.
 * Copy published Ten God · stem · element. Do not derive Can/Hành here.
 */

export type CanonicalUsefulGodSource = {
  readonly useful_god?: unknown;
  readonly overall_useful_god?: unknown;
  readonly overall_incomplete?: unknown;
  readonly useful_display?: unknown;
  readonly useful_ten_god?: unknown;
  readonly useful_stem?: unknown;
  readonly useful_element?: unknown;
  readonly favorable_gods?: unknown;
  readonly unfavorable_gods?: unknown;
  readonly favorable_display?: unknown;
  readonly unfavorable_display?: unknown;
  readonly winning_rule_id?: unknown;
  readonly winning_rule_group?: unknown;
  readonly climate_candidate?: unknown;
  readonly climate_display?: unknown;
  readonly climate_preference_label?: unknown;
  readonly short_reason?: unknown;
  readonly reason_archetype?: unknown;
  readonly hy_role_status?: unknown;
  readonly ky_scope_note?: unknown;
};

export const OVERALL_INCOMPLETE_MESSAGE =
  "Chưa đủ căn cứ xác định Dụng thần tổng thể";

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function text(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function listText(value: unknown): string {
  if (Array.isArray(value)) {
    return value.map((item) => text(item)).filter(Boolean).join(", ");
  }
  return text(value);
}

export function canonicalUsefulGodPayload(
  data: { readonly useful_god?: unknown } | null | undefined,
): CanonicalUsefulGodSource {
  return asRecord(data?.useful_god) as CanonicalUsefulGodSource;
}

export function canonicalUsefulDisplay(
  useful: CanonicalUsefulGodSource | null | undefined,
  fallback = "",
): string {
  if (useful?.overall_incomplete) {
    return text(useful?.useful_display) || OVERALL_INCOMPLETE_MESSAGE;
  }
  return text(useful?.useful_display) || fallback;
}

export function canonicalUsefulShortReason(
  useful: CanonicalUsefulGodSource | null | undefined,
  fallback = "",
): string {
  return text(useful?.short_reason) || fallback;
}

export function canonicalClimatePreferenceLabel(
  useful: CanonicalUsefulGodSource | null | undefined,
): string {
  return text(useful?.climate_preference_label);
}

export function canonicalFavorableDisplay(
  useful: CanonicalUsefulGodSource | null | undefined,
  fallback = "",
): string {
  // Copy published customer Hỷ. Do not fall back to internal favorable_gods
  // (that list still contains the Overall Dụng token).
  return text(useful?.favorable_display) || fallback;
}

export function canonicalUnfavorableDisplay(
  useful: CanonicalUsefulGodSource | null | undefined,
  fallback = "",
): string {
  return (
    text(useful?.unfavorable_display) || listText(useful?.unfavorable_gods) || fallback
  );
}
