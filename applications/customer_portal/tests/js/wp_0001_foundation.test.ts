import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

import {
  REQUIRED_SEMANTIC_CSS_VARS,
  coreGrid,
  coreSpacing,
  semanticMotion,
  semanticSpacing,
  semanticTypography,
  themeColorCatalog,
} from "../../src/tokens";
import {
  applyThemeMode,
  getThemePalette,
  resolveThemeMode,
  toggleThemeMode,
} from "../../src/theme";
import { resolveBreakpoint, spacingScaleFactor } from "../../src/constants/breakpoints";
import { layoutClassNames, sectionWidthClass } from "../../src/layouts";
import { cx } from "../../src/utils/cx";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "../..");

function readCss(relativePath: string): string {
  return readFileSync(resolve(rootDir, relativePath), "utf8");
}

describe("WP-0001 Design Tokens", () => {
  it("exposes the 8-point spacing scale from Pack 02", () => {
    expect(coreSpacing).toEqual({
      space_0: 0,
      space_1: 4,
      space_2: 8,
      space_3: 12,
      space_4: 16,
      space_5: 24,
      space_6: 32,
      space_7: 48,
      space_8: 64,
      space_9: 96,
      space_10: 120,
    });
  });

  it("maps semantic spacing to the core scale", () => {
    expect(semanticSpacing.inline).toBe(8);
    expect(semanticSpacing.paragraph).toBe(24);
    expect(semanticSpacing.block).toBe(48);
    expect(semanticSpacing.section).toBe(96);
    expect(semanticSpacing.chapter).toBe(120);
  });

  it("defines nine typography roles", () => {
    expect(Object.keys(semanticTypography)).toEqual([
      "display",
      "page_title",
      "chapter",
      "section",
      "subsection",
      "body_large",
      "body",
      "caption",
      "metadata",
    ]);
  });

  it("defines grid metrics from Pack 02", () => {
    expect(coreGrid.desktop_columns).toBe(12);
    expect(coreGrid.desktop_margin).toBe(48);
    expect(coreGrid.desktop_gutter).toBe(24);
    expect(coreGrid.desktop_report_max_width).toBe(1360);
    expect(coreGrid.desktop_reading_max_width).toBe(760);
    expect(coreGrid.desktop_wide_max_width).toBe(1080);
    expect(coreGrid.breakpoint_mobile_max).toBe(767);
    expect(coreGrid.breakpoint_desktop_min).toBe(1440);
  });

  it("exposes semantic motion tokens", () => {
    expect(semanticMotion.fast).toBe("120ms");
    expect(semanticMotion.normal).toBe("200ms");
    expect(semanticMotion.slow).toBe("320ms");
  });
});

describe("WP-0001 Theme Infrastructure", () => {
  it("resolves system preference to light/dark", () => {
    expect(resolveThemeMode("system", false)).toBe("light");
    expect(resolveThemeMode("system", true)).toBe("dark");
    expect(resolveThemeMode("dark", false)).toBe("dark");
  });

  it("provides light and dark palettes with required semantic keys", () => {
    const required = [
      "surface_report_paper",
      "text_primary",
      "border_divider",
      "accent_primary",
      "feedback_success",
      "elevation_soft",
      "focus_ring",
    ] as const;

    for (const mode of ["light", "dark"] as const) {
      const palette = getThemePalette(mode);
      for (const key of required) {
        expect(palette[key]).toBeTruthy();
      }
      expect(themeColorCatalog[mode]).toBe(palette);
    }
  });

  it("applies and toggles data-theme on a root element", () => {
    const root = {
      attrs: new Map<string, string>(),
      style: { colorScheme: "" },
      setAttribute(name: string, value: string) {
        this.attrs.set(name, value);
      },
      getAttribute(name: string) {
        return this.attrs.get(name) ?? null;
      },
    };

    applyThemeMode("dark", root as unknown as HTMLElement);
    expect(root.getAttribute("data-theme")).toBe("dark");
    expect(root.style.colorScheme).toBe("dark");

    const next = toggleThemeMode(root as unknown as HTMLElement);
    expect(next).toBe("light");
    expect(root.getAttribute("data-theme")).toBe("light");
  });
});

describe("WP-0001 CSS Variable Integration", () => {
  it("declares every required semantic CSS variable in tokens.css", () => {
    const css = readCss("src/styles/tokens.css");
    for (const name of REQUIRED_SEMANTIC_CSS_VARS) {
      expect(css.includes(`${name}:`)).toBe(true);
    }
  });

  it("declares dark theme overrides", () => {
    const css = readCss("src/styles/themes/dark.css");
    expect(css).toContain('[data-theme="dark"]');
    expect(css).toContain("--surface-report-paper:");
    expect(css).toContain("--text-primary:");
    expect(css).toContain("--accent-primary:");
  });

  it("wires foundation styles through index.css", () => {
    const css = readCss("src/styles/index.css");
    expect(css).toContain('./tokens.css');
    expect(css).toContain('./themes/light.css');
    expect(css).toContain('./themes/dark.css');
    expect(css).toContain('./typography.css');
    expect(css).toContain('./layout.css');
    expect(css).toContain('./utilities.css');
  });

  it("includes reduced-motion and focus foundations", () => {
    const tokens = readCss("src/styles/tokens.css");
    const reset = readCss("src/styles/reset.css");
    expect(tokens).toContain("prefers-reduced-motion");
    expect(reset).toContain(":focus-visible");
    expect(reset).toContain("var(--focus-ring)");
  });
});

describe("WP-0001 Layout & Responsive Foundations", () => {
  it("exposes layout shell class names", () => {
    expect(layoutClassNames.applicationFrame).toBe("cui-application-frame");
    expect(layoutClassNames.reportSheet).toBe("cui-report-sheet");
    expect(layoutClassNames.readingColumn).toBe("cui-reading-column");
  });

  it("maps section width roles to columns", () => {
    expect(sectionWidthClass("reading")).toBe("cui-reading-column");
    expect(sectionWidthClass("medium")).toBe("cui-medium-column");
    expect(sectionWidthClass("wide")).toBe("cui-wide-column");
  });

  it("resolves breakpoints per Pack 02", () => {
    expect(resolveBreakpoint(375)).toBe("mobile");
    expect(resolveBreakpoint(900)).toBe("tablet");
    expect(resolveBreakpoint(1360)).toBe("laptop");
    expect(resolveBreakpoint(1600)).toBe("desktop");
  });

  it("uses Pack 02 responsive spacing scale factors", () => {
    expect(spacingScaleFactor).toEqual({
      desktop: 1,
      laptop: 0.9,
      tablet: 0.8,
      mobile: 0.7,
    });
  });

  it("declares shell and surface classes in layout.css", () => {
    const css = readCss("src/styles/layout.css");
    expect(css).toContain(".cui-application-frame");
    expect(css).toContain(".cui-report-sheet");
    expect(css).toContain(".cui-content-grid");
    expect(css).toContain(".cui-surface-callout");
    expect(css).toContain(".cui-surface-paper");
  });
});

describe("WP-0001 Utilities", () => {
  it("joins class names safely", () => {
    expect(cx("a", false, null, undefined, "b")).toBe("a b");
  });
});
