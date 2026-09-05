/**
 * CP-BUG-002 — Technical Information must not show Tốn when Tứ Trụ Year is Khôn.
 */

import { describe, expect, it } from "vitest";

import { bindPersonalCungPhiIdentity } from "../../src/adapters/personalCungPhi";
import { adaptIdentityHeader } from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const SON_STALE_CALENDAR = {
  identity: { person: { gender: "male" } },
  calendar: {
    cung_phi: "Tốn",
    menh_quai: "Tốn",
    hanh_cung: "Mộc",
    nhom_trach: "Đông Tứ Trạch",
    house_group: "Đông Tứ Trạch",
    calendar_rule_version: "G1-10C",
    ganzhi_routing: {
      year: { cung_phi: "Khôn", source_nguyen: "Hạ Nguyên", ganzhi: "Bính Dần" },
    },
  },
  bazi: {
    year_pillar: { stem: "Bính", branch: "Dần", cung_phi: "Khôn" },
  },
  feng_shui: {
    cung_phi: "Tốn",
    gua_name: "Tốn",
    menh_quai: "Tốn",
    nhom_trach: "Đông Tứ Trạch",
  },
} as AnalysisDataDto;

describe("CP-BUG-002 personal Cung Phi routing", () => {
  it("does not keep Tốn on Technical Information when Year Cung is Khôn", () => {
    const header = adaptIdentityHeader(SON_STALE_CALENDAR);
    expect(header.pillars.year.cungPhi).toBe("Khôn");
    expect(header.status.cungPhi).toBe("Khôn");
    expect(header.status.menhQuai).toBe("Khôn");
    expect(header.status.hanhCung).toBe("Thổ");
    expect(header.status.nhomTrach).toBe("Tây Tứ Trạch");
    expect(header.status.cungPhi).not.toBe("Tốn");
    expect(header.status.nhomTrach).not.toBe("Đông Tứ Trạch");
  });

  it("derives Hành Cung and Nhóm Trạch from the canonical palace", () => {
    const identity = bindPersonalCungPhiIdentity(SON_STALE_CALENDAR as Record<string, unknown>, "male");
    expect(identity).toEqual({
      cungPhi: "Khôn",
      menhQuai: "Khôn",
      hanhCung: "Thổ",
      nhomTrach: "Tây Tứ Trạch",
    });
  });

  it("does not let a later current payload keep stale Tốn over Year routing", () => {
    const identity = bindPersonalCungPhiIdentity(
      {
        ...SON_STALE_CALENDAR,
        calendar: {
          ...SON_STALE_CALENDAR.calendar,
          cung_phi: "Tốn",
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
});
