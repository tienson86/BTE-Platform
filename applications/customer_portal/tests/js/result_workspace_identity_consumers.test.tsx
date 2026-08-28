import { readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { cleanup, render } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import type { AnalysisDataDto, CanonicalIdentityDto } from "../../src/models";
import {
  EMPTY_COPY,
  ResultWorkspace,
  adaptBaziWorkspace,
} from "../../src/features/result_workspace";
import { WORKSPACE_FIELD_OWNERS } from "../../src/features/result_workspace/adapter";

afterEach(() => {
  cleanup();
});

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/features/result_workspace");

const IDENTITY: CanonicalIdentityDto = {
  person: {
    full_name: "Nguyen Tien Son",
    gender: "male",
    solar_birth: "21/01/1987",
    lunar_birth: "22/12/Bính Dần",
    birth_time: "04:30",
    birth_place: "Ha Noi",
    timezone: "Asia/Ho_Chi_Minh",
  },
  four_pillars: {
    year: {
      stem: "Bính",
      branch: "Dần",
      can_chi: "Bính Dần",
      nayin_element: "Hỏa",
      cung_phi: "Cấn",
    },
    month: {
      stem: "Tân",
      branch: "Sửu",
      can_chi: "Tân Sửu",
      nayin_element: "Thổ",
      cung_phi: "Khôn",
    },
    day: {
      stem: "Canh",
      branch: "Ngọ",
      can_chi: "Canh Ngọ",
      nayin_element: "Thổ",
      cung_phi: "Khôn",
    },
    hour: {
      stem: "Mậu",
      branch: "Dần",
      can_chi: "Mậu Dần",
      nayin_element: "Thổ",
      cung_phi: "Cấn",
    },
  },
  bone_weight: { weight: "", classification: "", rating: "", summary: "" },
  luck: {
    current_cycle: "Nhâm Thân",
    current_cycle_ganzhi: "Nhâm Thân",
    current_cycle_age: "40",
    current_year: "2026",
  },
  interpretation: {
    observation_id: "sec-observation",
    reasoning_id: "sec-reasoning",
    recommendation_id: "sec-recommendation",
    conclusion_id: "sec-conclusion",
    conclusion: "Kết luận đã công bố.",
    action: { next_action: "Giữ nhịp làm việc." },
    section_keys: ["sec-observation", "sec-reasoning", "sec-recommendation", "sec-conclusion"],
  },
};

function payload(identity: CanonicalIdentityDto = IDENTITY): AnalysisDataDto {
  return {
    identity,
    narrative_result: {
      sections: [
        { id: "sec-observation", paragraphs: [{ text: "Quan sát từ narrative." }] },
        { id: "sec-reasoning", paragraphs: [{ text: "Lý giải từ narrative." }] },
        { id: "sec-recommendation", paragraphs: [{ text: "Khuyến nghị từ narrative." }] },
      ],
    },
    luck: {
      available: true,
      cycles: [
        { gan_zhi: "Canh Ngọ", age_start: 22, age_end: 31 },
        { gan_zhi: "Nhâm Thân", age_start: 32, age_end: 41 },
      ],
    },
    customer: { full_name: "DO-NOT-USE-CUSTOMER" },
    calendar: {
      solar_date: "DO-NOT-USE-CALENDAR",
      lunar_date: "DO-NOT-USE-LUNAR",
      year_can_chi: "Giáp Tý",
      month_can_chi: "Ất Sửu",
      day_can_chi: "Bính Dần",
      hour_can_chi: "Đinh Mão",
      cung_phi: "Ly",
    },
    bazi: {
      year_pillar: { stem: "Giáp", branch: "Tý" },
      month_pillar: { stem: "Ất", branch: "Sửu" },
      day_pillar: { stem: "Bính", branch: "Dần" },
      hour_pillar: { stem: "Đinh", branch: "Mão" },
    },
  };
}

describe("BZ-ID-04A Workspace Identity Consumers", () => {
  it("header uses identity.person only", () => {
    const viewModel = adaptBaziWorkspace(payload(), {
      analysisId: "chart-1",
      input: { full_name: "INPUT-NAME", timezone: "UTC", hour: 9, minute: 0 },
    });
    expect(viewModel?.person.name.value).toBe("Nguyen Tien Son");
    expect(viewModel?.person.gender.value).toBe("male");
    expect(viewModel?.person.solarDate.value).toBe("21/01/1987");
    expect(viewModel?.person.lunarDate.value).toBe("22/12/Bính Dần");
    expect(viewModel?.person.birthTime.value).toBe("04:30");
    expect(viewModel?.person.location.value).toBe("Ha Noi");
    expect(viewModel?.person.timezone.value).toBe("Asia/Ho_Chi_Minh");
    expect(viewModel?.person.name.source).toBe("identity.person.full_name");
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-slot='profile']")?.textContent).toContain("Nguyen Tien Son");
    expect(container.querySelector("[data-slot='gender']")?.textContent).toContain("male");
    expect(container.textContent).not.toContain("DO-NOT-USE-CUSTOMER");
    expect(container.textContent).not.toContain("INPUT-NAME");
  });

  it("TuTruPanel uses identity.four_pillars without calendar or bazi fallback", () => {
    const viewModel = adaptBaziWorkspace(payload());
    expect(viewModel?.fourPillars.year).toEqual({
      stem: "Bính",
      branch: "Dần",
      canChi: "Bính Dần",
      napAm: "Hỏa",
      cungPhi: "Cấn",
    });
    expect(viewModel?.fourPillars.month.canChi).toBe("Tân Sửu");
    expect(viewModel?.fourPillars.day.canChi).toBe("Canh Ngọ");
    expect(viewModel?.fourPillars.hour.canChi).toBe("Mậu Dần");
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    const tuTru = container.querySelector("[data-panel='tu-tru']");
    expect(tuTru?.textContent).toContain("Bính Dần");
    expect(tuTru?.textContent).not.toContain("Giáp Tý");
    expect(tuTru?.textContent).not.toContain("Đinh Mão");
  });

  it("changing hour identity only changes the hour row", () => {
    const base = payload();
    const shifted = payload({
      ...IDENTITY,
      four_pillars: {
        ...IDENTITY.four_pillars,
        hour: {
          stem: "Kỷ",
          branch: "Mão",
          can_chi: "Kỷ Mão",
          nayin_element: "Thổ",
          cung_phi: "Chấn",
        },
      },
    });
    const before = adaptBaziWorkspace(base)?.fourPillars;
    const after = adaptBaziWorkspace(shifted)?.fourPillars;
    expect(after?.year).toEqual(before?.year);
    expect(after?.month).toEqual(before?.month);
    expect(after?.day).toEqual(before?.day);
    expect(after?.hour.canChi).toBe("Kỷ Mão");
    expect(before?.hour.canChi).toBe("Mậu Dần");
  });

  it("BoneWeight uses identity and shows empty copy when unpublished", () => {
    const viewModel = adaptBaziWorkspace(payload());
    expect(viewModel?.boneWeight.amount.available).toBe(false);
    expect(viewModel?.boneWeight.amount.source).toBe("identity.bone_weight.weight");
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-panel='bone-weight']")?.textContent).toContain(EMPTY_COPY);
    const published = adaptBaziWorkspace(
      payload({
        ...IDENTITY,
        bone_weight: { weight: "3.2", classification: "Trung", rating: "B", summary: "S10" },
      }),
    );
    expect(published?.boneWeight.amount.value).toBe("3.2");
    expect(published?.boneWeight.classification.value).toBe("Trung");
    expect(published?.boneWeight.interpretation.value).toBe("S10");
  });

  it("Luck prefers identity.luck over the luck slice for published fields", () => {
    const viewModel = adaptBaziWorkspace(payload());
    expect(viewModel?.luck.ganZhi.value).toBe("Nhâm Thân");
    expect(viewModel?.luck.ganZhi.source).toBe("identity.luck.current_cycle_ganzhi");
    expect(viewModel?.luck.ageRange.value).toBe("40");
    expect(viewModel?.luck.currentYear.value).toBe("2026");
    expect(viewModel?.luck.cycles.map((cycle) => cycle.ganZhi)).toEqual(["Canh Ngọ", "Nhâm Thân"]);
  });

  it("Interpretation uses identity section ids and narrative body only", () => {
    const viewModel = adaptBaziWorkspace(payload());
    expect(viewModel?.interpretation.observationId.value).toBe("sec-observation");
    expect(viewModel?.interpretation.observe.value).toBe("Quan sát từ narrative");
    expect(viewModel?.interpretation.reason.value).toBe("Lý giải từ narrative");
    expect(viewModel?.interpretation.advice.value).toBe("Khuyến nghị từ narrative");
    expect(viewModel?.conclusion.overall.value).toBe("Kết luận đã công bố.");
    expect(viewModel?.conclusion.action.value).toBe("Giữ nhịp làm việc.");
  });

  it("does not read calendar, customer, or frontend lookup tables for identity", () => {
    const adapter = readFileSync(join(ROOT, "adapter/baziWorkspaceAdapter.ts"), "utf8");
    expect(adapter).not.toMatch(/data\.calendar/);
    expect(adapter).not.toMatch(/data\.customer/);
    expect(adapter).not.toMatch(/year_can_chi/);
    expect(adapter).not.toMatch(/nayin_lookup|hoa_giap|cung_phi_lookup|01_nap_am|ha_nguyen/);
    expect(adapter).not.toMatch(/joinStemBranch/);
    expect(adapter).toContain("identity.person");
    expect(adapter).toContain("identity.four_pillars");
    expect(WORKSPACE_FIELD_OWNERS["person.name"]).toBe("identity.person.full_name");
    expect(WORKSPACE_FIELD_OWNERS["four_pillars.hour"]).toBe("identity.four_pillars.hour");
  });

  it("empty identity fields show Chưa có dữ liệu without inference", () => {
    const viewModel = adaptBaziWorkspace({ identity: {} });
    expect(viewModel?.person.name.available).toBe(false);
    expect(viewModel?.fourPillars.year.canChi).toBe("");
    expect(viewModel?.luck.ganZhi.available).toBe(false);
    expect(viewModel?.conclusion.overall.available).toBe(false);
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-slot='profile']")?.textContent).toContain(EMPTY_COPY);
    expect(container.querySelector("[data-slot='conclusion-overall']")?.textContent).toContain(
      EMPTY_COPY,
    );
  });
});
