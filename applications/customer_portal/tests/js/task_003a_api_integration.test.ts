/**
 * TASK_003A — API client + adapter integration tests (mocked fetch).
 */

import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiClient, ApiError, resetApiClient } from "../../src/api";
import { adaptAnalysisToBaZiResult } from "../../src/adapters";
import { AnalyzeService, resetAnalyzeService } from "../../src/services";
import type { AnalysisDataDto } from "../../src/models";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  resetApiClient();
  resetAnalyzeService();
});

describe("TASK_003A API client", () => {
  it("parses success envelope from POST /analyze", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      statusText: "OK",
      text: async () =>
        JSON.stringify({
          success: true,
          message: "Analyze OK",
          data: { bazi: { day_master: "Canh" } },
          request_id: "req-1",
        }),
    });
    vi.stubGlobal("fetch", fetchMock);

    const client = new ApiClient({
      baseUrl: "http://127.0.0.1:8000/api/v1",
      timeoutMs: 5000,
      retries: 0,
    });

    const result = await client.post<{
      success: boolean;
      data: { bazi: { day_master: string } };
      request_id: string;
    }>("/analyze", { year: 1990, month: 5, day: 15 });

    expect(result.success).toBe(true);
    expect(result.data.bazi.day_master).toBe("Canh");
    expect(result.request_id).toBe("req-1");
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe("http://127.0.0.1:8000/api/v1/analyze");
    expect(init.method).toBe("POST");
  });

  it("maps 401 to unauthorized ApiError", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 401,
        statusText: "Unauthorized",
        text: async () =>
          JSON.stringify({
            success: false,
            message: "Unauthorized",
            code: "unauthorized",
          }),
      }),
    );

    const client = new ApiClient({
      baseUrl: "http://127.0.0.1:8000/api/v1",
      retries: 0,
    });

    await expect(client.get("/admin/dashboard")).rejects.toMatchObject({
      kind: "unauthorized",
      status: 401,
    } satisfies Partial<ApiError>);
  });

  it("maps network failure to network ApiError", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new TypeError("Failed to fetch")),
    );

    const client = new ApiClient({
      baseUrl: "http://127.0.0.1:8000/api/v1",
      retries: 0,
    });

    await expect(client.get("/health")).rejects.toMatchObject({
      kind: "network",
    } satisfies Partial<ApiError>);
  });
});

describe("TASK_003A BaZi adapter", () => {
  it("maps analyze data into BaZi Result ViewModel", () => {
    const data: AnalysisDataDto = {
      bazi: {
        year_pillar: {
          stem: "Canh",
          branch: "Ngọ",
          hidden_stems: ["Đinh"],
          nap_am: "Lư Trung Hỏa",
          truong_sinh: "Đế Vượng",
          ten_god: "Tỷ Kiên",
        },
        month_pillar: { stem: "Tân", branch: "Tỵ", ten_god: "Kiếp Tài" },
        day_pillar: { stem: "Canh", branch: "Thìn", ten_god: "Nhật Chủ" },
        hour_pillar: { stem: "Tân", branch: "Tỵ", ten_god: "Thiên Ấn" },
        day_master: "Canh",
        ten_gods: ["Tỷ Kiên", "Kiếp Tài", "Thiên Ấn"],
      },
      calendar: {
        year_can_chi: "Canh Ngọ",
        day_can_chi: "Canh Thìn",
      },
      customer: {
        full_name: "Nguyễn Văn A",
        gender: "male",
        birth_place: "Hà Nội",
      },
      score: {
        wuxing_series: [
          { label: "Kim", value: 4 },
          { label: "Mộc", value: 2 },
          { label: "Thủy", value: 1 },
          { label: "Hỏa", value: 2 },
          { label: "Thổ", value: 1 },
        ],
        ten_god_series: [{ label: "Thiên Ấn", value: 2 }],
        strength_score: 72,
        recommendation: "Củng cố thế cục",
      },
      strength: {
        strength_level: "strong",
        strength_score: 72,
        confidence: 0.9,
        reasoning: "Thân được sinh phù trợ.",
      },
    };

    const vm = adaptAnalysisToBaZiResult(data, {
      request: {
        year: 1990,
        month: 8,
        day: 15,
        hour: 9,
        minute: 30,
        full_name: "Nguyễn Văn A",
        birth_place: "Hà Nội",
        gender: "male",
      },
      requestId: "req-adapter",
    });

    expect(vm.status).toBe("ready");
    expect(vm.profile.fullName).toBe("Nguyễn Văn A");
    expect(vm.profile.gender).toBe("Nam");
    expect(vm.pillars).toHaveLength(4);
    expect(vm.pillars[0]?.heavenlyStem).toBe("Canh");
    expect(vm.fiveElements.find((el) => el.id === "kim")?.score).toBe(4);
    expect(vm.tenGods[0]?.name).toBe("Thiên Ấn");
    expect(vm.strength.label).toBe("THÂN VƯỢNG");
    expect(vm.metadata.chartId).toBe("req-adapter");
  });
});

describe("TASK_003A AnalyzeService with mocked fetch", () => {
  it("returns adapted ViewModel from analyze envelope", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        statusText: "OK",
        text: async () =>
          JSON.stringify({
            success: true,
            message: "OK",
            request_id: "svc-1",
            data: {
              bazi: {
                year_pillar: { stem: "Giáp", branch: "Tý" },
                month_pillar: { stem: "Ất", branch: "Sửu" },
                day_pillar: { stem: "Bính", branch: "Dần" },
                hour_pillar: { stem: "Đinh", branch: "Mão" },
                day_master: "Bính",
              },
              strength: {
                strength_level: "balanced",
                strength_score: 50,
                reasoning: "Cân bằng",
              },
              score: { wuxing_series: [], ten_god_series: [] },
              customer: { full_name: "Test User", gender: "female" },
            },
          }),
      }),
    );

    const service = new AnalyzeService({
      client: new ApiClient({
        baseUrl: "http://127.0.0.1:8000/api/v1",
        retries: 0,
      }),
    });

    const request = {
      year: 1990,
      month: 1,
      day: 1,
      full_name: "Test User",
      gender: "female",
    } as const;

    const response = await service.analyze(request);
    const vm = adaptAnalysisToBaZiResult(response.data, {
      request,
      requestId: response.request_id,
    });

    expect(vm.profile.fullName).toBe("Test User");
    expect(vm.pillars[2]?.heavenlyStem).toBe("Bính");
    expect(vm.strength.label).toBe("CÂN BẰNG");
  });
});
