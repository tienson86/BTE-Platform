import { readFileSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  NavigationScreen,
  ReadingNavigation,
  navigationWorkPackageId,
  type NavigationViewModel,
} from "../../src";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const navigationDir = resolve(rootDir, "src/components/navigation");

afterEach(() => {
  cleanup();
});

const readingJourney = [
  { id: "executive-summary", label: "Executive Summary", href: "#executive-summary" },
  { id: "four-pillars", label: "Four Pillars", href: "#four-pillars" },
  { id: "executive-insight", label: "Executive Insight", href: "#executive-insight" },
  { id: "metrics", label: "Metrics", href: "#metrics" },
  {
    id: "explainable-analysis",
    label: "Explainable Analysis",
    href: "#explainable-analysis",
  },
  {
    id: "consultation-report",
    label: "Consultation Report",
    href: "#consultation-report",
  },
  { id: "appendix", label: "Appendix", href: "#appendix", active: true },
] as const;

const readyFixture: Extract<NavigationViewModel, { status: "ready" }> = {
  status: "ready",
  title: "Reading Navigation",
  railTitle: "Reading Rail",
  tocTitle: "Table of Contents",
  items: readingJourney.map((item) => ({ ...item })),
  toc: readingJourney.map((item) => ({ ...item })),
  currentSection: { id: "appendix", label: "Appendix" },
  progress: 0.86,
  breadcrumbs: [
    { id: "report", label: "Consultation Report", href: "#consultation-report" },
    { id: "appendix", label: "Appendix" },
  ],
  jumpTargets: readingJourney.map((item) => ({ ...item })),
  anchors: readingJourney.map((item) => ({ ...item })),
  backToTop: {
    label: "Back to top",
    href: "#cui-nav-main-content",
    visible: true,
  },
  print: {
    label: "Print navigation",
    href: "#print",
    note: "Print preserves reading order.",
  },
};

const purityForbidden =
  /\b(query|lookup|fetch|generate|calculate|derive|evaluate|analyze)\s*\(/i;

const intersectionObserverForbidden = /IntersectionObserver/;

function listNavigationSources(): string[] {
  return readdirSync(navigationDir)
    .filter((name) => name.endsWith(".tsx") || name.endsWith(".ts"))
    .filter((name) => name !== "index.ts");
}

describe("WP-0011 Navigation", () => {
  it("exports WP-0011 identity", () => {
    expect(navigationWorkPackageId).toBe("WP-0011");
  });

  it("navigation components do not import Base Components directly", () => {
    const offenders: string[] = [];
    for (const name of listNavigationSources()) {
      const source = readFileSync(join(navigationDir, name), "utf8");
      if (/from\s+["']\.\.\/base["']/.test(source) || /from\s+["']\.\.\/base\//.test(source)) {
        offenders.push(name);
      }
    }
    expect(offenders).toEqual([]);
  });

  it("navigation components contain no calculation, derivation, or analysis", () => {
    const offenders: string[] = [];
    for (const name of listNavigationSources()) {
      const source = readFileSync(join(navigationDir, name), "utf8");
      if (purityForbidden.test(source) || intersectionObserverForbidden.test(source)) {
        offenders.push(name);
      }
    }
    const screenSource = readFileSync(
      resolve(rootDir, "src/screens/NavigationScreen.tsx"),
      "utf8",
    );
    const vmSource = readFileSync(
      resolve(rootDir, "src/view_models/navigation.ts"),
      "utf8",
    );
    if (purityForbidden.test(screenSource)) {
      offenders.push("NavigationScreen.tsx");
    }
    if (purityForbidden.test(vmSource)) {
      offenders.push("navigation.ts");
    }
    expect(offenders).toEqual([]);
  });

  it("preserves Pack 06 reading journey order", () => {
    render(
      <ReadingNavigation data={readyFixture}>
        <p>Frozen report content</p>
      </ReadingNavigation>,
    );

    const rail = screen.getByRole("navigation", { name: "Reading Rail" });
    const labels = Array.from(rail.querySelectorAll("a")).map((node) =>
      (node.textContent ?? "").trim(),
    );
    expect(labels).toEqual([
      "Executive Summary",
      "Four Pillars",
      "Executive Insight",
      "Metrics",
      "Explainable Analysis",
      "Consultation Report",
      "Appendix",
    ]);
  });

  it("renders skip link, current section, and children when ready", () => {
    render(
      <NavigationScreen data={readyFixture}>
        <p>Preserved screen content</p>
      </NavigationScreen>,
    );

    expect(screen.getByRole("link", { name: "Skip to content" })).toBeTruthy();
    expect(screen.getByLabelText("Current Section")).toBeTruthy();
    expect(screen.getByText("Preserved screen content")).toBeTruthy();
    expect(screen.getByRole("link", { name: "Back to top" })).toBeTruthy();
  });

  it("hides BackToTop when ViewModel visibility is false", () => {
    render(
      <NavigationScreen
        data={{
          ...readyFixture,
          backToTop: { ...readyFixture.backToTop, visible: false },
        }}
      />,
    );

    expect(screen.queryByRole("link", { name: "Back to top" })).toBeNull();
  });

  it("renders loading and error presentation states", () => {
    const { rerender } = render(<NavigationScreen data={{ status: "loading" }} />);
    expect(screen.getByText("Loading navigation")).toBeTruthy();

    rerender(<NavigationScreen data={{ status: "empty" }} />);
    expect(screen.getByText("No navigation available")).toBeTruthy();

    rerender(<NavigationScreen data={{ status: "unavailable" }} />);
    expect(screen.getByText("Navigation unavailable")).toBeTruthy();

    rerender(
      <NavigationScreen
        data={{ status: "error", errorMessage: "Navigation payload missing" }}
      />,
    );
    expect(screen.getByText("Unable to load navigation")).toBeTruthy();
    expect(screen.getByText("Navigation payload missing")).toBeTruthy();
  });
});
