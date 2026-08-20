/**
 * Canonical Useful God V1.0 presentation helpers.
 * Copy published Ten God · stem · element. Do not derive Can/Hành here.
 */

export type CanonicalUsefulGodSource = {
  readonly useful_god?: unknown;
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
};

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
  return text(useful?.useful_display) || text(useful?.useful_god) || fallback;
}

export function canonicalFavorableDisplay(
  useful: CanonicalUsefulGodSource | null | undefined,
  fallback = "",
): string {
  return text(useful?.favorable_display) || listText(useful?.favorable_gods) || fallback;
}

export function canonicalUnfavorableDisplay(
  useful: CanonicalUsefulGodSource | null | undefined,
  fallback = "",
): string {
  return (
    text(useful?.unfavorable_display) || listText(useful?.unfavorable_gods) || fallback
  );
}
