/**
 * N-REL-01 Portal production switch.
 * Provider flag, fallback, rollback, ResultStore, presentation selection, rendering.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import { CommercialDashboardPage } from "../../src/screens/commercial_dashboard";
import { adaptOverviewCard } from "../../src/screens/commercial_dashboard/overviewAdapter";
import { adaptInterpretationCard } from "../../src/screens/commercial_dashboard/interpretationAdapter";
import { adaptActionPlanCard } from "../../src/screens/commercial_dashboard/actionPlanAdapter";
import { adaptNarrativeV2Presentation } from "../../src/adapters/narrativeV2PresentationAdapter";
import type { AnalysisDataDto } from "../../src/models";
import { resolveNarrativeProvider } from "../../src/resultState/narrativeProvider";
import { selectNarrativePresentation } from "../../src/resultState/narrativePresentationSelection";
import {
  getNarrativeFallbackCount,
  resetNarrativeFallbackCount,
  setNarrativeMonitorSink,
  type NarrativeMonitorEvent,
} from "../../src/resultState/narrativeReleaseMonitor";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..", "..", "..");
const PRESENTATION = JSON.parse(
  readFileSync(
    resolve(ROOT, "implementation/narrative_v2/n_imp_09a/case0001_presentation_v2_1.json"),
    "utf8",
  ),
) as Record<string, unknown>;

const PACK05_IDENTITY = "Pack05 identity stays independent";
const CONSULTING = (PRESENTATION.interpretation as { consulting_flow: string }).consulting_flow;
const HEADLINE = (PRESENTATION.overview as { headline: string }).headline;
const PRIORITY = (PRESENTATION.action_plan as { top_priority: { title: string } }).top_priority.title;

const ANALYSIS = {
  analysis_id: "ana-nrel01-0001",
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
    summary: { identity: PACK05_IDENTITY, priority_recommendation: "Pack05 priority" },
    sections: [
      {
        intent: "overview",
        title: "Tóm tắt điều hành",
        paragraphs: [{ text: "Pack05 overview sentence for rollback." }],
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

const FORBIDDEN = [
  "pipeline_trace",
  "source_unit_ids",
  "NR-REL-001",
  "rule_id",
  "Traceback",
  "engines.narrative_v2",
];

const events: NarrativeMonitorEvent[] = [];

beforeEach(() => {
  events.length = 0;
  resetNarrativeFallbackCount();
  setNarrativeMonitorSink((event) => {
    events.push(event);
  });
});

afterEach(() => {
  setNarrativeMonitorSink(null);
  resetNarrativeFallbackCount();
  cleanup();
});

describe("N-REL-01 provider switch", () => {
  it("defaults to v2 and accepts pack05 / auto without rebuild", () => {
    expect(resolveNarrativeProvider("", {})).toBe("v2");
    expect(resolveNarrativeProvider("?provider=pack05", {})).toBe("pack05");
    expect(resolveNarrativeProvider("?provider=v2", {})).toBe("v2");
    expect(resolveNarrativeProvider("?provider=auto", {})).toBe("auto");
    expect(resolveNarrativeProvider("", { NARRATIVE_PROVIDER: "pack05" })).toBe("pack05");
  });

  it("query override wins over env so rollback does not need a rebuild", () => {
    expect(resolveNarrativeProvider("?provider=pack05", { NARRATIVE_PROVIDER: "v2" })).toBe("pack05");
    expect(resolveNarrativeProvider("?provider=v2", { NARRATIVE_PROVIDER: "pack05" })).toBe("v2");
  });
});

describe("N-REL-01 presentation selection", () => {
  it("renders NarrativeV2Presentation when provider=v2", () => {
    const selected = selectNarrativePresentation(ANALYSIS, "v2");
    expect(selected.selected).toBe("v2");
    expect(selected.fallback).toBe(false);
    expect(selected.presentationVersion).toBe("bte.presentation.v2.1");
    expect(selected.overview.insight).toBe(HEADLINE);
    expect(selected.interpretation.lead).toBe(CONSULTING);
    expect(selected.actionPlan.priority?.title).toBe(PRIORITY);
  });

  it("keeps Pack05 when provider=pack05", () => {
    const selected = selectNarrativePresentation(ANALYSIS, "pack05");
    expect(selected.selected).toBe("pack05");
    expect(selected.fallback).toBe(false);
    expect(selected.interpretation.lead).toContain("Pack05 overview sentence");
    expect(selected.overview.insight).toBe(adaptOverviewCard(ANALYSIS).insight);
  });

  it("does not compose or join V2 interpretation fields", () => {
    const selected = selectNarrativePresentation(ANALYSIS, "v2");
    const observation = (PRESENTATION.interpretation as { observation: string }).observation;
    const reasoning = (PRESENTATION.interpretation as { reasoning: string }).reasoning;
    expect(selected.interpretation.lead).not.toBe(`${observation} ${reasoning}`);
    expect(selected.interpretation.lead).toBe(CONSULTING);
    const observationZone = selected.interpretation.zones.find((zone) => zone.id === "observation");
    expect(observationZone?.body).toBe(observation);
  });
});

describe("N-REL-01 fallback", () => {
  it("falls back to Pack05 when V2 presentation is invalid", () => {
    const invalid = {
      ...ANALYSIS,
      narrative_v2_shadow: {
        status: "ok",
        presentation: { metadata: { version: "bte.presentation.v2" } },
        error: null,
      },
    } as AnalysisDataDto;
    const selected = selectNarrativePresentation(invalid, "v2");
    expect(selected.selected).toBe("pack05");
    expect(selected.fallback).toBe(true);
    expect(selected.fallbackReason).toBe("incompatible_presentation_version");
    expect(selected.interpretation.lead).toContain("Pack05 overview sentence");
    expect(getNarrativeFallbackCount()).toBe(1);
  });

  it("falls back to Pack05 when V2 is missing", () => {
    const missing = { ...ANALYSIS, narrative_v2_shadow: undefined } as AnalysisDataDto;
    const selected = selectNarrativePresentation(missing, "v2");
    expect(selected.selected).toBe("pack05");
    expect(selected.fallback).toBe(true);
    expect(adaptInterpretationCard(missing).lead).toBe(selected.interpretation.lead);
  });

  it("records a monitor event without personal data", () => {
    selectNarrativePresentation(ANALYSIS, "v2");
    expect(events).toHaveLength(1);
    const event = events[0];
    expect(event.provider).toBe("v2");
    expect(event.selected).toBe("v2");
    expect(event.presentation_version).toBe("bte.presentation.v2.1");
    expect(event.fallback).toBe(false);
    expect(JSON.stringify(event)).not.toContain("CASE-0001");
    expect(JSON.stringify(event)).not.toContain("1987");
    expect(JSON.stringify(event)).not.toContain(CONSULTING.slice(0, 24));
  });
});

describe("N-REL-01 rollback", () => {
  it("CASE-0001 pack05 → v2 → pack05 all succeed on the same ResultStore payload", () => {
    const first = selectNarrativePresentation(ANALYSIS, "pack05");
    const second = selectNarrativePresentation(ANALYSIS, "v2");
    const third = selectNarrativePresentation(ANALYSIS, "pack05");
    expect(first.selected).toBe("pack05");
    expect(second.selected).toBe("v2");
    expect(third.selected).toBe("pack05");
    expect(first.interpretation.lead).toBe(third.interpretation.lead);
    expect(second.interpretation.lead).toBe(CONSULTING);
    expect(ANALYSIS.narrative_v2_shadow?.presentation).toBe(PRESENTATION);
    expect((ANALYSIS.narrative_result as { contract: string }).contract).toBe(
      "pack05_narrative_result_v1",
    );
  });
});

describe("N-REL-01 ResultStore independence", () => {
  it("keeps Pack05 and Narrative V2 as separate layers", () => {
    expect(ANALYSIS.narrative_result).not.toBe(ANALYSIS.narrative_v2_shadow);
    expect((ANALYSIS.narrative_result as { contract: string }).contract).toBe(
      "pack05_narrative_result_v1",
    );
    const view = adaptNarrativeV2Presentation(ANALYSIS.narrative_v2_shadow);
    expect(view.ok).toBe(true);
    expect(view.version).toBe("bte.presentation.v2.1");
    const pack05 = adaptActionPlanCard(ANALYSIS);
    const v2 = selectNarrativePresentation(ANALYSIS, "v2").actionPlan;
    expect(v2.priority?.title).not.toBe(pack05.priority?.title);
  });
});

describe("N-REL-01 portal rendering", () => {
  it("uses the existing Commercial Dashboard, not the shadow review page", () => {
    const { container } = render(
      <CommercialDashboardPage
        analysis={ANALYSIS}
        resultSource="current"
        layoutMode="live"
        narrativeProvider="v2"
      />,
    );
    expect(container.querySelector('[data-dashboard="commercial-v1"]')).toBeTruthy();
    expect(container.querySelector('[data-narrative-surface="production"]')).toBeTruthy();
    expect(container.querySelector('[data-narrative-provider="v2"]')).toBeTruthy();
    expect(container.querySelector("[data-narrative-v2-shadow]")).toBeNull();
    expect(container.textContent).toContain(CONSULTING);
    expect(container.textContent).toContain(HEADLINE);
    expect(container.textContent).toContain(PRIORITY);
  });

  it("renders Pack05 on the same dashboard when provider=pack05", () => {
    const { container } = render(
      <CommercialDashboardPage
        analysis={ANALYSIS}
        resultSource="current"
        layoutMode="live"
        narrativeProvider="pack05"
      />,
    );
    expect(container.querySelector('[data-narrative-provider="pack05"]')).toBeTruthy();
    expect(container.querySelector('[data-narrative-fallback="false"]')).toBeTruthy();
    expect(container.textContent).toContain("Pack05 overview sentence for rollback.");
    expect(container.textContent).not.toContain(CONSULTING);
  });

  it("does not interrupt the customer or leak internals on fallback", () => {
    const leaked = {
      ...ANALYSIS,
      narrative_v2_shadow: {
        status: "error",
        error: "incompatible_presentation_version",
        presentation: null,
        pipeline_trace: "secret-trace",
        source_unit_ids: ["NR-REL-001"],
      },
    } as AnalysisDataDto;
    const { container } = render(
      <CommercialDashboardPage
        analysis={leaked}
        resultSource="current"
        layoutMode="live"
        narrativeProvider="v2"
      />,
    );
    expect(container.querySelector('[data-narrative-provider="pack05"]')).toBeTruthy();
    expect(container.querySelector('[data-narrative-fallback="true"]')).toBeTruthy();
    expect(container.textContent).not.toMatch(/incompatible_presentation_version|partial JSON|stack/i);
    const html = container.innerHTML;
    for (const token of FORBIDDEN) {
      expect(html).not.toContain(token);
    }
  });
});

describe("N-REL-01 regression", () => {
  it("Pack05 adapters remain callable and unchanged for rollback", () => {
    const overview = adaptOverviewCard(ANALYSIS);
    const interpretation = adaptInterpretationCard(ANALYSIS);
    const action = adaptActionPlanCard(ANALYSIS);
    expect(overview.insight).toMatch(/Thân vượng|Canh/);
    expect(interpretation.lead).toContain("Pack05 overview sentence");
    expect(action.title).toBe("KẾ HOẠCH HÀNH ĐỘNG");
  });

  it("does not join V2 overview headline and summary", () => {
    const selected = selectNarrativePresentation(ANALYSIS, "v2");
    const summary = (PRESENTATION.overview as { summary: string }).summary;
    expect(selected.overview.insight).toBe(HEADLINE);
    expect(selected.overview.insight).not.toContain(summary);
  });
});
