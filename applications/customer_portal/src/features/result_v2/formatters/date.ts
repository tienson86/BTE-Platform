/**
 * Date formatting for technical metadata only. Never shown in Hero.
 */

export function formatTechnicalDate(value: unknown): string | null {
  if (value === null || value === undefined) return null;
  const text = String(value).trim();
  return text.length > 0 ? text : null;
}
