/**
 * N-IMP-10 Portal shadow integration tests.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import { CommercialDashboardPage } from "../../src/screens/commercial_dashboard";
import { NarrativeV2ShadowPage } from "../../src/screens/narrative_v2_shadow";
import {
  adaptNarrativeV2Presentation,
  PRESENTATION_V2_1,
} from "../../src/adapters/narrativeV2PresentationAdapter";
import { resolveResultSurface } from "../../src/resultState/narrativeV2Shadow";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..", "..", "..");
const PRESENTATION = JSON.parse(
  readFileSync(
    resolve(ROOT, "implementation/narrative_v2/n_imp_09a/case0001_presentation_v2_1.json"),
    "utf8",
  ),
) as Record<string, unknown>;

const ANALYSIS = {
  analysis_id: "ana-nimp10-0001",
  identity: {
    person: { full_name: "CASE-0001", gender: "male", solar_birth: "1987-01-21" },
  },
  narrative_result: {
    contract: "pack05_narrative_result_v1",
    status: "ok",
    summary: { identity: "Pack05 identity", priority_recommendation: "Pack05 priority" },
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
  "evidence.strength.level",
  "NR-REL-001",
  "knowledge.pattern.chinh_an",
  "pipeline_trace",
  "source_unit_ids",
  "runtime_metrics",
];

afterEach(cleanup);

describe("N-IMP-10 narrative v2 shadow", () => {
  it("PS1 production /result surface is default", () => {
    expect(resolveResultSurface("", "/result")).toBe("production");
    expect(resolveResultSurface("?preview=1", "/result")).toBe("production");
    const { container } = render(
      <CommercialDashboardPage analysis={ANALYSIS} resultSource="current" layoutMode="live" />,
    );
    expect(container.querySelector('[data-narrative-surface="production"]')).toBeTruthy();
    expect(container.querySelector("[data-narrative-v2-shadow]")).toBeNull();
  });

  it("PS2 shadow loads only with explicit flag", () => {
    expect(resolveResultSurface("?narrative=v2-shadow", "/result")).toBe("v2-shadow");
    const { container } = render(<NarrativeV2ShadowPage analysis={ANALYSIS} mode="v2-shadow" />);
    expect(container.querySelector("[data-narrative-v2-shadow='true']")).toBeTruthy();
    expect(container.textContent).toContain("Narrative V2 — Shadow Review");
  });

  it("PS3 Portal reads Presentation v2.1 only", () => {
    const view = adaptNarrativeV2Presentation(ANALYSIS.narrative_v2_shadow);
    expect(view.ok).toBe(true);
    expect(view.version).toBe(PRESENTATION_V2_1);
    const bad = adaptNarrativeV2Presentation({
      status: "ok",
      presentation: { ...PRESENTATION, metadata: { version: "bte.presentation.v2", status: "partial" } },
    });
    expect(bad.ok).toBe(false);
    expect(bad.error).toBe("incompatible_presentation_version");
  });

  it("PS4 consulting_flow renders unchanged", () => {
    const { container } = render(<NarrativeV2ShadowPage analysis={ANALYSIS} />);
    const flow = container.querySelector("[data-v2-consulting-flow]");
    expect(flow?.textContent).toBe(
      (PRESENTATION.interpretation as { consulting_flow: string }).consulting_flow,
    );
  });

  it("PS5 structured interpretation renders unchanged", () => {
    const { container } = render(<NarrativeV2ShadowPage analysis={ANALYSIS} />);
    const meaning = container.querySelector('[data-v2-structured-field="meaning"] p');
    expect(meaning?.textContent).toBe(
      (PRESENTATION.interpretation as { meaning: string }).meaning,
    );
  });

  it("PS6 Action Plan renders unchanged", () => {
    const { container } = render(<NarrativeV2ShadowPage analysis={ANALYSIS} />);
    const priority = container.querySelector("[data-v2-top-priority]");
    const action = PRESENTATION.action_plan as {
      top_priority: { title: string; description: string };
    };
    expect(priority?.textContent).toContain(action.top_priority.title);
    expect(priority?.textContent).toContain(action.top_priority.description);
  });

  it("PS7 Portal does not compose Narrative", () => {
    const source = readFileSync(
      resolve(ROOT, "applications/customer_portal/src/adapters/narrativeV2PresentationAdapter.ts"),
      "utf8",
    );
    expect(source).not.toMatch(/consulting_flow.*=.*overview/);
    expect(source).not.toMatch(/\.join\(/);
    const { container } = render(<NarrativeV2ShadowPage analysis={ANALYSIS} />);
    const flow = container.querySelector("[data-v2-consulting-flow]")?.textContent ?? "";
    const observation = (PRESENTATION.interpretation as { observation: string }).observation;
    const reasoning = (PRESENTATION.interpretation as { reasoning: string }).reasoning;
    expect(flow).not.toBe(`${observation} ${reasoning}`);
  });

  it("PS8 missing Summary fields are not invented", () => {
    const { container } = render(<NarrativeV2ShadowPage analysis={ANALYSIS} />);
    expect(container.querySelector('[data-v2-overview-missing="identity"]')?.textContent).toContain(
      "Không có trong Presentation",
    );
    expect(container.textContent).not.toMatch(/Nhật Chủ được suy ra/);
  });

  it("PS9 Commercial null is handled safely", () => {
    const { container } = render(<NarrativeV2ShadowPage analysis={ANALYSIS} />);
    expect(container.querySelector("[data-v2-commercial]")?.textContent).toContain("Chưa có");
  });

  it("PS10 internal ids are not exposed", () => {
    const leaked = {
      ...ANALYSIS,
      narrative_v2_shadow: {
        ...ANALYSIS.narrative_v2_shadow,
        pipeline_trace: "secret",
        presentation: PRESENTATION,
      },
    } as AnalysisDataDto;
    const { container } = render(<NarrativeV2ShadowPage analysis={leaked} />);
    const html = container.innerHTML;
    for (const token of FORBIDDEN) {
      expect(html).not.toContain(token);
    }
  });

  it("PS13 missing shadow does not mount production as V2", () => {
    const { container } = render(
      <NarrativeV2ShadowPage analysis={{ analysis_id: "x" } as AnalysisDataDto} />,
    );
    expect(container.querySelector("[data-v2-error]")).toBeTruthy();
    expect(container.querySelector('[data-dashboard="commercial-v1"]')).toBeNull();
  });

  it("PS14 version is validated", () => {
    const view = adaptNarrativeV2Presentation({
      status: "ok",
      presentation: { metadata: { version: "nope" } },
    });
    expect(view.ok).toBe(false);
  });

  it("PS18 same Presentation yields the same shadow rendering", () => {
    const first = render(<NarrativeV2ShadowPage analysis={ANALYSIS} />);
    const html = first.container.innerHTML;
    cleanup();
    const second = render(<NarrativeV2ShadowPage analysis={ANALYSIS} />);
    expect(second.container.innerHTML).toBe(html);
  });

  it("comparison mode is explicit and internal", () => {
    expect(resolveResultSurface("?narrative=v2-compare", "/result")).toBe("v2-compare");
    const { container } = render(<NarrativeV2ShadowPage analysis={ANALYSIS} mode="v2-compare" />);
    expect(container.querySelector("[data-v2-compare]")).toBeTruthy();
    expect(container.textContent).toContain("CURRENT PRODUCTION");
    expect(container.textContent).toContain("NARRATIVE V2 SHADOW");
  });
});
