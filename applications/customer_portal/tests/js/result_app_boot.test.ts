/**
 * Result boot helpers — ResultStore → PortalPage props.
 */

import { describe, expect, it } from "vitest";
import { resolveResultBoot, toAnalyzeRequest } from "../../src/entries/resultBoot";

describe("resultBoot helpers", () => {
  it("maps ResultStore input to AnalyzeChartRequest", () => {
    const request = toAnalyzeRequest({
      year: 1990,
      month: 8,
      day: 15,
      hour: 10,
      minute: 30,
      gender: "male",
      full_name: "Nguyễn Văn A",
      birth_place: "Hà Nội",
      timezone: "Asia/Ho_Chi_Minh",
    });

    expect(request).toEqual({
      year: 1990,
      month: 8,
      day: 15,
      hour: 10,
      minute: 30,
      gender: "male",
      timezone: "Asia/Ho_Chi_Minh",
      full_name: "Nguyễn Văn A",
      birth_place: "Hà Nội",
      customer_id: null,
    });
  });

  it("returns null when birth date is incomplete", () => {
    expect(toAnalyzeRequest({ year: 1990, month: 8 })).toBeNull();
    expect(toAnalyzeRequest(null)).toBeNull();
  });

  it("uses fixture preview only when ?preview=1", () => {
    const empty = resolveResultBoot(null);
    expect(empty.request).toBeNull();
    expect(empty.previewFallback).toBe(false);
    expect(empty.resultSource).toBe("empty");
    expect(empty.initialData).toBeUndefined();

    const preview = resolveResultBoot(null, "?preview=1");
    expect(preview.previewFallback).toBe(true);
    expect(preview.resultSource).toBe("preview");
  });

  it("adapts stored engine payload for production mode", () => {
    const boot = resolveResultBoot({
      input: {
        year: 1990,
        month: 8,
        day: 15,
        hour: 10,
        minute: 30,
        gender: "male",
        full_name: "Nguyễn Văn A",
      },
      data: {
        analysis_id: "req-boot-1",
        useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
        useful_god: {
          useful_display: "Hỏa · Đinh · Chính Quan",
          favorable_display: "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng",
        },
        bazi: {
          day_master: "Bính",
          day_master_element: "Hỏa",
          year_pillar: { stem: "Canh", branch: "Ngọ" },
          month_pillar: { stem: "Giáp", branch: "Ngọ" },
          day_pillar: { stem: "Bính", branch: "Dần" },
          hour_pillar: { stem: "Tân", branch: "Tỵ" },
        },
        customer: { full_name: "Nguyễn Văn A", gender: "male" },
      },
    });

    expect(boot.previewFallback).toBe(false);
    expect(boot.request).toBeNull();
    expect(boot.initialData?.source).toBe("api");
    expect(boot.initialData?.s03.pillars[0].stem.han).toBe("庚");
    expect(boot.initialData?.s00.profile.name).toBe("Nguyễn Văn A");
  });
});
