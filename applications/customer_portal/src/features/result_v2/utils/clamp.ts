/**
 * List clamps — PX-2 formatting only.
 */

import { trimText } from "../formatters/text";

export const SUMMARY_BULLET_MAX = 5;

export function clampSummaryBullets(values: unknown): string[] {
  if (!Array.isArray(values)) return [];
  const bullets: string[] = [];
  for (const item of values) {
    if (bullets.length >= SUMMARY_BULLET_MAX) break;
    const text = trimText(item);
    if (text) bullets.push(text);
  }
  return bullets;
}
