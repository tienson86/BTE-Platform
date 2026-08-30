/**
 * Display-only date/time formatting for the executive report.
 * Does not infer missing calendar values.
 */

const ISO_STAMP =
  /^(\d{4})-(\d{2})-(\d{2})(?:[T\s](\d{2}):(\d{2})(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2})?)?/;

/**
 * Format a published ISO date as DD/MM/YYYY. Keep 24-hour time when present.
 * Unrecognized values pass through unchanged.
 */
export function formatPublishedDate(value: string): string {
  const trimmed = value.trim();
  if (!trimmed) return "";
  const match = trimmed.match(ISO_STAMP);
  if (!match) return trimmed;
  const date = `${match[3]}/${match[2]}/${match[1]}`;
  if (match[4] && match[5]) {
    return `${date} ${match[4]}:${match[5]}`;
  }
  return date;
}
