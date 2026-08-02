import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import type { ReactElement } from "react";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  AppProviders,
  ErrorBoundary,
  LoadingBoundary,
  STYLES_ENTRY,
  ThemeProvider,
  commercialUiVersion,
  getEnvironmentConfig,
  hardeningMissionId,
  resolveEnvironmentName,
  useTheme,
  workPackageId,
} from "../../src";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "../..");

const REQUIRED_BARRELS = [
  "src/components/base/index.ts",
  "src/components/shared/index.ts",
  "src/components/business/index.ts",
  "src/components/feedback/index.ts",
  "src/layouts/index.ts",
  "src/tokens/index.ts",
  "src/styles/index.ts",
  "src/hooks/index.ts",
  "src/utils/index.ts",
  "src/types/index.ts",
  "src/constants/index.ts",
  "src/app/index.ts",
  "src/config/index.ts",
  "src/theme/index.ts",
] as const;

function ThemeProbe(): ReactElement {
  const { mode, toggleMode, preference } = useTheme();
  return (
    <div>
      <span data-testid="mode">{mode}</span>
      <span data-testid="preference">{preference}</span>
      <button type="button" onClick={toggleMode}>
        toggle
      </button>
    </div>
  );
}

describe("WP-0001A Foundation Hardening", () => {
  afterEach(() => {
    cleanup();
    document.documentElement.removeAttribute("data-theme");
    document.documentElement.style.colorScheme = "";
  });

  it("exposes hardening identity without breaking WP-0001 version", () => {
    expect(commercialUiVersion).toBe("3.0.0");
    expect(workPackageId).toBe("WP-0001");
    expect(hardeningMissionId).toBe("WP-0001A");
  });

  it("provides barrel exports for every public module", () => {
    for (const relative of REQUIRED_BARRELS) {
      expect(existsSync(resolve(rootDir, relative)), relative).toBe(true);
    }
  });

  it("documents foundation architecture and naming conventions", () => {
    const readme = readFileSync(resolve(rootDir, "src/README.md"), "utf8");
    const naming = readFileSync(resolve(rootDir, "src/NAMING_CONVENTIONS.md"), "utf8");
    expect(readme).toContain("### `app/`");
    expect(readme).toContain("### `tokens/`");
    expect(readme).toContain("### `components/`");
    expect(naming).toContain("Components");
    expect(naming).toContain("View Models");
    expect(naming).toContain("Bindings");
  });

  it("resolves typed environment configurations", () => {
    expect(getEnvironmentConfig("development").diagnostics).toBe(true);
    expect(getEnvironmentConfig("staging").name).toBe("staging");
    expect(getEnvironmentConfig("production").strictMode).toBe(false);
    expect(resolveEnvironmentName({ NODE_ENV: "production" })).toBe("production");
    expect(resolveEnvironmentName({ BTE_CUI_ENV: "staging" })).toBe("staging");
  });

  it("exports styles barrel entry constants", () => {
    expect(STYLES_ENTRY).toBe("./index.css");
  });

  it("renders LoadingBoundary fallback when loading", () => {
    render(
      <LoadingBoundary loading label="Preparing report">
        <p>content</p>
      </LoadingBoundary>,
    );
    expect(screen.getByRole("status").textContent).toContain("Preparing report");
    expect(screen.queryByText("content")).toBeNull();
  });

  it("renders children when LoadingBoundary is not loading", () => {
    render(
      <LoadingBoundary loading={false}>
        <p>ready</p>
      </LoadingBoundary>,
    );
    expect(screen.getByText("ready")).toBeTruthy();
  });

  it("ThemeProvider initializes mode and supports toggle", () => {
    render(
      <ThemeProvider initialPreference="light">
        <ThemeProbe />
      </ThemeProvider>,
    );
    expect(screen.getByTestId("mode").textContent).toBe("light");
    expect(document.documentElement.getAttribute("data-theme")).toBe("light");
    fireEvent.click(screen.getByRole("button", { name: "toggle" }));
    expect(screen.getByTestId("mode").textContent).toBe("dark");
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
  });

  it("AppProviders compose ThemeProvider and ErrorBoundary", () => {
    render(
      <AppProviders themePreference="dark">
        <ThemeProbe />
      </AppProviders>,
    );
    expect(screen.getByTestId("mode").textContent).toBe("dark");
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
  });

  it("ErrorBoundary shows fallback UI on render error", () => {
    function Boom(): ReactElement {
      throw new Error("boom");
    }

    const spy = vi.spyOn(console, "error").mockImplementation(() => undefined);
    render(
      <ErrorBoundary>
        <Boom />
      </ErrorBoundary>,
    );
    expect(screen.getByRole("alert").textContent).toContain("Something went wrong");
    spy.mockRestore();
  });
});
