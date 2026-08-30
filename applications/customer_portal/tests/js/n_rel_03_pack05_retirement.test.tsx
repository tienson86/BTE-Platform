/**
 * N-REL-03 Pack05 retirement. Production is Narrative V2. Pack05 is archive.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import { CommercialDashboardPage } from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";
import { resolveNarrativeProvider } from "../../src/resultState/narrativeProvider";
import { isPack05LegacyEnabled } from "../../src/resultState/pack05Legacy";
import { selectNarrativePresentation } from "../../src/resultState/narrativePresentationSelection";
import {
  resetNarrativeFallbackCount,
  setNarrativeMonitorSink,
} from "../../src/resultState/narrativeReleaseMonitor";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..", "..", "..");
const PRESENTATION = JSON.parse(
  readFileSync(
    resolve(ROOT, "implementation/narrative_v2/n_imp_09a/case0001_presentation_v2_1.json"),
    "utf8",
  ),
) as Record<string, unknown>;

const CONSULTING = (PRESENTATION.interpretation as { consulting_flow: string }).consulting_flow;
const HEADLINE = (PRESENTATION.overview as { headline: string }).headline;
const PRIORITY = (PRESENTATION.action_plan as { top_priority: { title: string } }).top_priority.title;
const PACK05_IDENTITY = "Historical Pack05 stays in the store";

const ANALYSIS = {
  analysis_id: "ana-nrel03-0001",
  identity: {
    person: { full_name: "CASE-0001", gender: "male", solar_birth: "1987-01-21" },
  },
  bazi: { day_master: "Canh", day_master_element: "Kim" },
  strength: { strength_level: "strong" },
  useful_god: {
    useful_display: "Hỏa",
    unfavorable_display: "Canh, Tân",
  },
  temperature: { balancing_need_label: "Cần ôn ấm" },
  narrative_result: {
    contract: "pack05_narrative_result_v1",
    status: "ok",
    summary: { identity: PACK05_IDENTITY, priority_recommendation: "Pack05 archive" },
    sections: [
      {
        intent: "overview",
        title: "Tóm tắt điều hành",
        paragraphs: [{ text: "Người định khung. Lịch sử Pack05 không bị xóa." }],
      },
    ],
  },
  narrative_v2_shadow: {
    status: "ok",
    portal_connection: "true_shadow",
    replaces_pack05: false,
    presentation: PRESENTATION,
    error: null,
  },
} as AnalysisDataDto;

beforeEach(() => {
  resetNarrativeFallbackCount();
  setNarrativeMonitorSink(() => undefined);
});

afterEach(() => {
  setNarrativeMonitorSink(null);
  resetNarrativeFallbackCount();
  cleanup();
});

describe("N-REL-03 provider removal", () => {
  it("cannot select Pack05 through production flags", () => {
    expect(resolveNarrativeProvider("", {})).toBe("v2");
    expect(resolveNarrativeProvider("?provider=pack05", {})).toBe("v2");
    expect(resolveNarrativeProvider("?provider=auto", {})).toBe("v2");
    expect(resolveNarrativeProvider("?provider=v2", {})).toBe("v2");
    expect(resolveNarrativeProvider("", { NARRATIVE_PROVIDER: "pack05" })).toBe("v2");
    expect(resolveNarrativeProvider("?provider=pack05", { NARRATIVE_PROVIDER: "pack05" })).toBe("v2");
  });
});

describe("N-REL-03 legacy access", () => {
  it("PACK05_LEGACY is read-only and is not a production switch", () => {
    expect(isPack05LegacyEnabled("", {})).toBe(false);
    expect(isPack05LegacyEnabled("?legacy=pack05", {})).toBe(true);
    expect(isPack05LegacyEnabled("", { PACK05_LEGACY: "1" })).toBe(true);
    expect(resolveNarrativeProvider("?legacy=pack05", { PACK05_LEGACY: "pack05" })).toBe("v2");
  });
});

describe("N-REL-03 history", () => {
  it("keeps stored Pack05 after production V2 selection", () => {
    const before = ANALYSIS.narrative_result;
    const selected = selectNarrativePresentation(ANALYSIS, "pack05");
    expect(selected.selected).toBe("v2");
    expect(selected.fallback).toBe(false);
    expect(ANALYSIS.narrative_result).toBe(before);
    expect((ANALYSIS.narrative_result as { contract: string }).contract).toBe(
      "pack05_narrative_result_v1",
    );
    expect(ANALYSIS.narrative_v2_shadow?.replaces_pack05).toBe(false);
    expect(
      ((ANALYSIS.narrative_result as { sections: { paragraphs: { text: string }[] }[] }).sections[0]
        .paragraphs[0].text),
    ).toContain("Người định khung");
  });
});

describe("N-REL-03 portal", () => {
  it("always renders Narrative V2 on the Commercial Dashboard", () => {
    const { container } = render(
      <CommercialDashboardPage
        analysis={ANALYSIS}
        resultSource="current"
        layoutMode="live"
        narrativeProvider="pack05"
      />,
    );
    expect(container.querySelector('[data-narrative-provider="v2"]')).toBeTruthy();
    expect(container.querySelector('[data-narrative-provider="pack05"]')).toBeNull();
    expect(container.querySelector('[data-narrative-fallback="true"]')).toBeNull();
    expect(container.textContent).toContain(CONSULTING);
    expect(container.textContent).toContain(HEADLINE);
    expect(container.textContent).toContain(PRIORITY);
    expect(container.querySelector("[data-narrative-v2-shadow]")).toBeNull();
  });

  it("does not fall back to Pack05 when V2 is missing", () => {
    const missing = { ...ANALYSIS, narrative_v2_shadow: undefined } as AnalysisDataDto;
    const selected = selectNarrativePresentation(missing, "v2");
    expect(selected.selected).toBe("v2");
    expect(selected.fallback).toBe(false);
    expect(selected.interpretation.lead).toBe("");
    expect(selected.interpretation.available).toBe(false);
  });
});

describe("N-REL-03 regression", () => {
  it("renders V2 consulting_flow without joining Pack05", () => {
    const selected = selectNarrativePresentation(ANALYSIS, "v2");
    expect(selected.interpretation.lead).toBe(CONSULTING);
    expect(selected.interpretation.lead).not.toContain("Người định khung");
    expect(selected.overview.insight).toBe(HEADLINE);
  });
});
