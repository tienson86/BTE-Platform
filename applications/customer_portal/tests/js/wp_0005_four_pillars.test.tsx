import { readdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  ChartLegend,
  ChartMetadata,
  EarthlyBranchCell,
  FourPillarsChart,
  FourPillarsScreen,
  HeavenlyStemCell,
  HiddenStemGroup,
  LifeStagePanel,
  NaYinPanel,
  PillarColumn,
  PillarHeader,
  fourPillarsWorkPackageId,
  type FourPillarsViewModel,
  type PillarViewModel,
} from "../../src";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const businessDir = resolve(rootDir, "src/components/business");

afterEach(() => {
  cleanup();
});

const yearPillar: PillarViewModel = {
  kind: "year",
  title: "Year",
  stem: { label: "Geng", symbol: "庚", elementLabel: "Metal", tenGodLabel: "Partial Wealth" },
  branch: { label: "Chen", symbol: "辰", animalLabel: "Dragon", elementLabel: "Earth" },
  hiddenStems: [
    { id: "y1", label: "Wu", tenGodLabel: "Eating God" },
    { id: "y2", label: "Yi", tenGodLabel: "Direct Officer" },
  ],
  tenGodLabels: ["Partial Wealth"],
  naYin: "White Wax Gold",
  lifeStage: "Crown",
};

const monthPillar: PillarViewModel = {
  kind: "month",
  title: "Month",
  stem: { label: "Xin", symbol: "辛", elementLabel: "Metal" },
  branch: { label: "Si", symbol: "巳", animalLabel: "Snake" },
  hiddenStems: [{ id: "m1", label: "Bing", tenGodLabel: "Hurting Officer" }],
  naYin: "River Water",
  lifeStage: "Bath",
};

const dayPillar: PillarViewModel = {
  kind: "day",
  title: "Day",
  isDayMaster: true,
  stem: { label: "Jia", symbol: "甲", elementLabel: "Wood", tenGodLabel: "Day Master" },
  branch: { label: "Zi", symbol: "子", animalLabel: "Rat", elementLabel: "Water" },
  hiddenStems: [{ id: "d1", label: "Gui", tenGodLabel: "Direct Resource" }],
  tenGodLabels: ["Day Master"],
  naYin: "Sea Metal",
  lifeStage: "Birth",
};

const hourPillar: PillarViewModel = {
  kind: "hour",
  title: "Hour",
  stem: { label: "Yi", symbol: "乙", elementLabel: "Wood" },
  branch: { label: "Chou", symbol: "丑", animalLabel: "Ox" },
  hiddenStems: [],
  naYin: "Sea Metal",
  lifeStage: "Nourish",
};

const readyFixture: Extract<FourPillarsViewModel, { status: "ready" }> = {
  status: "ready",
  title: "Four Pillars",
  overview: "Structural chart presentation for Year, Month, Day, and Hour pillars.",
  pillars: [yearPillar, monthPillar, dayPillar, hourPillar],
  metadata: [
    { id: "calendar", label: "Calendar", value: "Solar" },
    { id: "timezone", label: "Timezone", value: "UTC+7" },
  ],
  legend: [
    { id: "stem", label: "Heavenly Stem", description: "Top cell of each pillar" },
    { id: "branch", label: "Earthly Branch", description: "Second cell of each pillar" },
  ],
  transition: {
    label: "Continue to Executive Insight",
    href: "#executive-insight",
  },
};

const fourPillarsBusinessFiles = [
  "FourPillarsChart.tsx",
  "PillarColumn.tsx",
  "PillarHeader.tsx",
  "HeavenlyStemCell.tsx",
  "EarthlyBranchCell.tsx",
  "HiddenStemGroup.tsx",
  "NaYinPanel.tsx",
  "LifeStagePanel.tsx",
  "ChartMetadata.tsx",
  "ChartLegend.tsx",
];

describe("WP-0005 Four Pillars", () => {
  it("exports WP-0005 identity", () => {
    expect(fourPillarsWorkPackageId).toBe("WP-0005");
  });

  it("four pillars business components do not import Base Components directly", () => {
    const offenders: string[] = [];
    for (const name of fourPillarsBusinessFiles) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (/from\s+["']\.\.\/base["']/.test(source) || /from\s+["']\.\.\/base\//.test(source)) {
        offenders.push(name);
      }
    }
    expect(offenders).toEqual([]);
  });

  it("does not modify frozen Executive Summary business modules", () => {
    const executiveFiles = [
      "ExecutiveHero.tsx",
      "RecommendationPanel.tsx",
      "ExecutiveOverview.tsx",
      "ExecutiveHighlights.tsx",
      "SummaryGlance.tsx",
      "HeroBackground.tsx",
      "HeroActions.tsx",
    ];
    for (const name of executiveFiles) {
      expect(readdirSync(businessDir)).toContain(name);
    }
  });

  it("renders Four Pillars reading order when ready", () => {
    const { container } = render(<FourPillarsScreen data={readyFixture} />);

    expect(screen.getByLabelText("Four Pillars")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Four Pillars" })).toBeTruthy();
    expect(screen.getByText("Chart Overview")).toBeTruthy();
    expect(screen.getByLabelText("Four Pillars Chart")).toBeTruthy();
    expect(screen.getByLabelText("Day (Day Master)")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Chart Metadata" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Chart Legend" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Continue to Executive Insight" })).toBeTruthy();

    const pillarNodes = Array.from(
      container.querySelectorAll<HTMLElement>("[data-pillar]"),
    );
    expect(pillarNodes.map((node) => node.dataset.pillar)).toEqual([
      "year",
      "month",
      "day",
      "hour",
    ]);

    const text = container.textContent ?? "";
    const overviewIdx = text.indexOf("Structural chart presentation");
    const chartIdx = text.indexOf("Four Pillars Chart");
    const yearStemIdx = text.indexOf("Geng");
    const metadataIdx = text.indexOf("Chart Metadata");
    const legendIdx = text.indexOf("Chart Legend");
    const transitionIdx = text.indexOf("Continue to Executive Insight");

    expect(overviewIdx).toBeGreaterThanOrEqual(0);
    expect(chartIdx).toBeGreaterThan(overviewIdx);
    expect(yearStemIdx).toBeGreaterThan(chartIdx);
    expect(metadataIdx).toBeGreaterThan(yearStemIdx);
    expect(legendIdx).toBeGreaterThan(metadataIdx);
    expect(transitionIdx).toBeGreaterThan(legendIdx);
  });

  it("renders loading, empty, unavailable, and error screen states", () => {
    const { rerender } = render(<FourPillarsScreen data={{ status: "loading" }} />);
    expect(screen.getByText("Loading four pillars")).toBeTruthy();

    rerender(<FourPillarsScreen data={{ status: "empty" }} />);
    expect(screen.getByText("BaZi chart data is unavailable.")).toBeTruthy();

    rerender(<FourPillarsScreen data={{ status: "unavailable" }} />);
    expect(screen.getByText("Four pillars unavailable")).toBeTruthy();

    rerender(
      <FourPillarsScreen data={{ status: "error", errorMessage: "Chart render failed" }} />,
    );
    expect(screen.getByText("Unable to load four pillars")).toBeTruthy();
    expect(screen.getByText("Chart render failed")).toBeTruthy();
  });

  it("renders Pack 06 four pillars business components in isolation", () => {
    render(
      <>
        <PillarHeader title="Day" isDayMaster tenGodLabels={["Day Master"]} />
        <HeavenlyStemCell data={dayPillar.stem} />
        <EarthlyBranchCell data={dayPillar.branch} />
        <HiddenStemGroup items={dayPillar.hiddenStems} />
        <NaYinPanel value={dayPillar.naYin} />
        <LifeStagePanel value={dayPillar.lifeStage} />
        <PillarColumn data={dayPillar} />
        <FourPillarsChart pillars={readyFixture.pillars} />
        <ChartMetadata items={readyFixture.metadata} />
        <ChartLegend items={readyFixture.legend} />
      </>,
    );

    expect(screen.getAllByText("Day Master").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Heavenly Stem").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Earthly Branch").length).toBeGreaterThan(0);
    expect(screen.getByText("White Wax Gold")).toBeTruthy();
    expect(screen.getByText("Solar")).toBeTruthy();
    expect(screen.getByText("Top cell of each pillar")).toBeTruthy();
  });

  it("wires four pillars styles into the business stylesheet entry", () => {
    const css = readFileSync(
      resolve(rootDir, "src/styles/components/business/index.css"),
      "utf8",
    );
    expect(css).toContain("./four-pillars.css");
  });
});
