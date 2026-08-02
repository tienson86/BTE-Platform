/**
 * Class-name join utility for layout / foundation helpers.
 * No styling decisions — presentation plumbing only.
 */

export function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}
