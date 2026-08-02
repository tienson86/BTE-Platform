import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

import {
  commercialUiReleaseReady,
  navigationWorkPackageId,
  responsiveAndPolishWorkPackageId,
} from "../../src";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "../..");

function readCss(relativePath: string): string {
  return readFileSync(resolve(rootDir, relativePath), "utf8");
}

describe("WP-0012 Responsive & Polish", () => {
  it("exports WP-0012 identity and release-ready flag", () => {
    expect(responsiveAndPolishWorkPackageId).toBe("WP-0012");
    expect(navigationWorkPackageId).toBe("WP-0011");
    expect(commercialUiReleaseReady).toBe(true);
  });

  it("wires polish stylesheet after component layers", () => {
    const css = readCss("src/styles/index.css");
    expect(css).toContain('./components/navigation/index.css');
    expect(css).toContain('./polish.css');
    expect(css.indexOf('./polish.css')).toBeGreaterThan(
      css.indexOf('./components/navigation/index.css'),
    );
  });

  it("declares responsive type-scale and structural polish tokens", () => {
    const tokens = readCss("src/styles/tokens.css");
    expect(tokens).toContain("--type-scale:");
    expect(tokens).toContain("--border-width:");
    expect(tokens).toContain("--border-width-strong:");
    expect(tokens).toContain("--rail-width:");
    expect(tokens).toContain("--rail-drawer-width:");
    expect(tokens).toContain("--print-margin:");
    expect(tokens).toContain("--type-scale: 0.95");
    expect(tokens).toContain("--type-scale: 0.9");
  });

  it("provides global print, focus, motion, and performance polish", () => {
    const polish = readCss("src/styles/polish.css");
    expect(polish).toContain("@page");
    expect(polish).toContain("size: A4");
    expect(polish).toContain("prefers-reduced-motion");
    expect(polish).toContain("content-visibility");
    expect(polish).toContain(":focus-visible");
    expect(polish).toContain("@media (min-width: 1280px)");
    expect(polish).toContain("@media (max-width: 767px)");
  });

  it("uses tokenized rail widths in layout shell", () => {
    const layout = readCss("src/styles/layout.css");
    expect(layout).toContain("var(--rail-width)");
    expect(layout).toContain("var(--rail-drawer-width)");
    expect(layout).not.toContain("width: 220px");
    expect(layout).not.toContain("min(280px");
  });

  it("keeps navigation touch targets and skip-link focus polish", () => {
    const nav = readCss("src/styles/components/navigation/navigation.css");
    expect(nav).toContain("var(--touch-target-min)");
    expect(nav).toContain(":focus-visible");
    expect(nav).toContain("@media print");
  });

  it("does not introduce business-logic keywords in polish CSS", () => {
    const polish = readCss("src/styles/polish.css");
    expect(polish).not.toMatch(
      /\b(query|lookup|fetch|generate|calculate|derive|evaluate|analyze)\s*\(/i,
    );
  });
});
