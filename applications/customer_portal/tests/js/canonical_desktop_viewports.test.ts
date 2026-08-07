/**
 * Desktop viewport band verification — 1366 / 1600 / 1920.
 * Frozen layout tokens only (no redesign).
 */

import { readFileSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";

const CSS = readFileSync(
  path.resolve(__dirname, "../../src/styles/canonical-desktop.css"),
  "utf8",
);

function token(name: string): number {
  const match = CSS.match(new RegExp(`${name}:\\s*(\\d+)px`));
  if (!match) {
    throw new Error(`Missing CSS token ${name}`);
  }
  return Number(match[1]);
}

describe("Desktop V2 viewport band", () => {
  it("keeps content max-width 1600 with fluid columns for 1366–1920", () => {
    const contentW = token("--cd-content-w");
    const sidebarW = token("--cd-sidebar-w");
    const pad = token("--cd-pad");

    expect(contentW).toBe(1600);
    expect(sidebarW).toBe(280);
    expect(pad).toBe(32);

    // Available main column at each viewport (sidebar reserved).
    const mainAt = (viewport: number) => viewport - sidebarW;

    expect(mainAt(1366)).toBeGreaterThan(1000);
    expect(mainAt(1600)).toBe(1320);
    expect(mainAt(1920)).toBe(1640);

    // Content never exceeds token; at 1920 main is wider than max so it centers.
    expect(mainAt(1920)).toBeGreaterThan(contentW);
    expect(CSS).toContain("max-width: var(--cd-content-w)");
    expect(CSS).toContain("minmax(0, 1fr)");
  });
});
