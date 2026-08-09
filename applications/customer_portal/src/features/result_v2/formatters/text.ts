/**
 * Text formatting only — trim, stringify, no consulting rewrite.
 */

export function trimText(value: unknown): string | null {
  if (value === null || value === undefined) return null;
  const text = String(value).trim();
  return text.length > 0 ? text : null;
}

export function requiredText(value: unknown): string {
  return trimText(value) ?? "";
}

export function stringifyMetaValue(value: unknown): string | null {
  if (value === null || value === undefined) return null;
  if (typeof value === "string") return trimText(value);
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  return null;
}
