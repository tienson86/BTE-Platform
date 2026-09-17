/**
 * CP-BUG-002 — personal Cung Phi must follow lunar year + gender.
 */

import { describe, expect, it } from "vitest";

import { bindPersonalCungPhiIdentity } from "../../src/adapters/personalCungPhi";
import { adaptIdentityHeader } from "../../src/screens/commercial_dashboard";
import { adaptBaziWorkspace } from "../../src/features/result_workspace/adapter/baziWorkspaceAdapter";
import type { AnalysisDataDto } from "../../src/models";

const SON_PRE_TET_LUNAR_1986 = {
  identity: { person: { gender: "male" } },
  calendar: {
    lunar_year: 1986,
    cung_phi: "Khôn",
    menh_quai: "Khôn",
    hanh_cung: "Thổ",
    nhom_trach: "Tây Tứ Trạch",
    house_group: "Tây Tứ Trạch",
    calendar_rule_version: "G1-10C",
    ganzhi_routing: {
      year: { cung_phi: "Khôn", source_nguyen: "Hạ Nguyên", ganzhi: "Bính Dần" },
    },
  },
  bazi: {
    year_pillar: { stem: "Bính", branch: "Dần", cung_phi: "Khôn" },
  },
  feng_shui: {
    cung_phi: "Khôn",
    gua_name: "Khôn",
    menh_quai: "Khôn",
    nhom_trach: "Tây Tứ Trạch",
  },
} as AnalysisDataDto;

describe("CP-BUG-002 personal Cung Phi routing", () => {
  it("uses lunar 1986 Khôn for a male born before Lunar New Year 1987", () => {
    const header = adaptIdentityHeader(SON_PRE_TET_LUNAR_1986);
    expect(header.pillars.year.cungPhi).toBe("Khôn");
    expect(header.status.cungPhi).toBe("Khôn");
    expect(header.status.menhQuai).toBe("Khôn");
    expect(header.status.hanhCung).toBe("Thổ");
    expect(header.status.nhomTrach).toBe("Tây Tứ Trạch");
  });

  it("derives Hành Cung and Nhóm Trạch from the canonical palace", () => {
    const identity = bindPersonalCungPhiIdentity(SON_PRE_TET_LUNAR_1986 as Record<string, unknown>, "male");
    expect(identity).toEqual({
      cungPhi: "Khôn",
      menhQuai: "Khôn",
      hanhCung: "Thổ",
      nhomTrach: "Tây Tứ Trạch",
    });
  });

  it("does not let technical Year routing override canonical personal Cung Phi", () => {
    const identity = bindPersonalCungPhiIdentity(
      {
        ...SON_PRE_TET_LUNAR_1986,
        calendar: {
          ...SON_PRE_TET_LUNAR_1986.calendar,
          cung_phi: "Khôn",
        },
      } as Record<string, unknown>,
      "male",
    );
    expect(identity.cungPhi).toBe("Khôn");
  });

  it("keeps 1966 female personal Cấn instead of Year male palace Đoài", () => {
    const identity = bindPersonalCungPhiIdentity(
      {
        identity: { person: { gender: "female" } },
        calendar: {
          cung_phi: "Cấn",
          menh_quai: "Cấn",
          nhom_trach: "Tây Tứ Trạch",
          ganzhi_routing: {
            year: { cung_phi: "Đoài", source_nguyen: "Trung Nguyên", ganzhi: "Bính Ngọ" },
          },
        },
        bazi: { year_pillar: { cung_phi: "Đoài" } },
      },
      "female",
    );
    expect(identity).toEqual({
      cungPhi: "Cấn",
      menhQuai: "Cấn",
      hanhCung: "Thổ",
      nhomTrach: "Tây Tứ Trạch",
    });
  });

  it("uses canonical personal Cung Phi in the Tứ Trụ Year row", () => {
    const workspace = adaptBaziWorkspace({
      identity: {
        person: { gender: "female" },
        four_pillars: {
          year: { can_chi: "Đinh Mão", cung_phi: "Khôn" },
        },
      },
      bazi: {
        year_pillar: { stem: "Đinh", branch: "Mão", cung_phi: "Tốn" },
      },
      calendar: { cung_phi: "Khôn" },
    } as AnalysisDataDto);

    if (!workspace) throw new Error("expected Bazi workspace");
    expect(workspace.fourPillars.year.cungPhi).toBe("Khôn");
  });
});
