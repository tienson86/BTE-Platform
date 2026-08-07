/**
 * Guard: Canonical Desktop sections must not import mockData.
 */

import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";

const ROOT = path.resolve(__dirname, "../../src/screens/canonical_desktop");

function listTsx(dir: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === "polish") continue;
      out.push(...listTsx(full));
    } else if (/\.(tsx|ts)$/.test(entry.name) && entry.name !== "mockData.ts") {
      out.push(full);
    }
  }
  return out;
}

describe("Canonical Desktop — no section mockData imports", () => {
  it("sections/shell/rows do not import mockData", () => {
    const files = listTsx(ROOT).filter((f) => {
      const rel = path.relative(ROOT, f).replace(/\\/g, "/");
      return (
        rel.startsWith("sections/") ||
        rel.startsWith("shell/") ||
        rel.startsWith("rows/") ||
        rel === "PortalPage.tsx" ||
        rel === "CanonicalDesktopContext.tsx" ||
        rel === "ModuleHeader.tsx"
      );
    });

    const offenders: string[] = [];
    for (const file of files) {
      const text = readFileSync(file, "utf8");
      if (/from\s+["'].*mockData["']/.test(text) || /CANONICAL_DESKTOP_MOCK/.test(text)) {
        offenders.push(path.relative(ROOT, file));
      }
    }

    expect(offenders).toEqual([]);
  });
});
