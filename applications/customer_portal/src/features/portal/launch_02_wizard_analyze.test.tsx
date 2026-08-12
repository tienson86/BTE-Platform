import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ApiClient } from "../../api";
import { AnalyzeService, resetAnalyzeService } from "../../services";
import { PortalApp } from "./PortalApp";
import { draftToAnalyzeRequest } from "./wizardAnalyzeRequest";
import type { WizardDraft } from "./pages/AnalysisWizard";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  resetAnalyzeService();
});

beforeEach(() => {
  resetAnalyzeService();
});

const SAMPLE_DRAFT: WizardDraft = {
  name: "Nguyễn Văn An",
  place: "Hà Nội",
  year: "1990",
  month: "5",
  day: "15",
  hour: "10",
  minute: "30",
  gender: "male",
  calendar: "solar",
};

const SUCCESS_BODY = {
  success: true,
  message: "Analyze OK",
  request_id: "anl_launch02_1",
  data: {
    pipeline: [
      "calendar",
      "bazi",
      "pattern",
      "score",
      "interpretation",
      "report",
      "narrative",
    ],
    stage: "analyze",
    bazi: {
      day_master: "Bính",
      year_pillar: { stem: "Giáp", branch: "Tý" },
      month_pillar: { stem: "Ất", branch: "Sửu" },
      day_pillar: { stem: "Bính", branch: "Dần" },
      hour_pillar: { stem: "Đinh", branch: "Mão" },
    },
    customer: {
      full_name: "Nguyễn Văn An",
      birth_place: "Hà Nội",
      timezone: "Asia/Ho_Chi_Minh",
      gender: "male",
    },
    narrative_result: {
      contract: "pack05_narrative_result_v1",
      status: "partial_insufficient",
      summary: {
        identity: "Nhật chủ Bính · Cách cục Thực Thương",
        strengths: ["Quyết đoán có nguồn chứng"],
        weaknesses: ["Cần cân bằng cảm xúc"],
        priority_recommendation: "Ưu tiên phát huy Thủy",
        next_action: "Giữ nhịp ổn định trong 90 ngày",
        insufficient_flags: [],
      },
      sections: [],
      recommendations: [],
    },
  },
};

function okResponse(body: unknown = SUCCESS_BODY) {
  return {
    ok: true,
    status: 200,
    statusText: "OK",
    text: async () => JSON.stringify(body),
  };
}

function errorResponse(body: unknown) {
  return {
    ok: false,
    status: 500,
    statusText: "Error",
    text: async () => JSON.stringify(body),
  };
}

function createTestService(): AnalyzeService {
  return new AnalyzeService({
    client: new ApiClient({
      baseUrl: "http://127.0.0.1:8000/api/v1",
      retries: 0,
    }),
  });
}

describe("LAUNCH-02 draftToAnalyzeRequest", () => {
  it("maps wizard draft to POST /api/v1/analyze birth payload", () => {
    expect(draftToAnalyzeRequest(SAMPLE_DRAFT)).toEqual({
      year: 1990,
      month: 5,
      day: 15,
      hour: 10,
      minute: 30,
      gender: "male",
      timezone: "Asia/Ho_Chi_Minh",
      full_name: "Nguyễn Văn An",
      birth_place: "Hà Nội",
    });
  });

  it("returns null for invalid birth fields", () => {
    expect(draftToAnalyzeRequest({ ...SAMPLE_DRAFT, year: "abc" })).toBeNull();
  });
});

describe("LAUNCH-02 wizard → POST /api/v1/analyze", () => {
  it("submits correct payload, shows loading, and navigates to result with analysis id", async () => {
    let resolveFetch!: (value: ReturnType<typeof okResponse>) => void;
    const fetchMock = vi.fn().mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveFetch = resolve;
        }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const service = createTestService();
    render(<PortalApp initialRoute="analyze-chart" analyzeService={service} />);

    fireEvent.click(screen.getByRole("button", { name: "Bắt đầu phân tích" }));

    expect(await screen.findByText("Đang tạo phân tích...")).toBeTruthy();
    const dashboardBtn = screen.getByRole("button", { name: "Về tổng quan" }) as HTMLButtonElement;
    expect(dashboardBtn.disabled).toBe(true);
    expect(document.querySelector('[data-analyze-status="loading"]')).toBeTruthy();

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledTimes(1);
    });

    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe("http://127.0.0.1:8000/api/v1/analyze");
    expect(init.method).toBe("POST");
    expect(JSON.parse(String(init.body))).toEqual({
      year: 1990,
      month: 5,
      day: 15,
      hour: 10,
      minute: 30,
      gender: "male",
      timezone: "Asia/Ho_Chi_Minh",
      full_name: "Nguyễn Văn An",
      birth_place: "Hà Nội",
    });

    resolveFetch(okResponse());

    expect(await screen.findByRole("button", { name: "Lưu báo cáo" }, { timeout: 5000 })).toBeTruthy();
    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-id")).toBe("anl_launch02_1");
    expect(root?.getAttribute("data-analysis-source")).toBe("api");
    expect(root?.getAttribute("data-has-analysis-result")).toBe("true");
  });

  it("prevents duplicate submission while loading", async () => {
    let resolveFetch!: (value: ReturnType<typeof okResponse>) => void;
    const fetchMock = vi.fn().mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveFetch = resolve;
        }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const service = createTestService();
    render(<PortalApp initialRoute="analyze-chart" analyzeService={service} />);

    const start = screen.getByRole("button", { name: "Bắt đầu phân tích" });
    fireEvent.click(start);
    fireEvent.click(start);
    fireEvent.click(start);

    expect(await screen.findByText("Đang tạo phân tích...")).toBeTruthy();
    expect(fetchMock).toHaveBeenCalledTimes(1);

    resolveFetch(okResponse());
    await screen.findByRole("button", { name: "Lưu báo cáo" }, { timeout: 5000 });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("keeps wizard data and shows Vietnamese error on API failure", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      errorResponse({ success: false, message: "Lỗi máy chủ tạm thời." }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const service = createTestService();
    render(<PortalApp initialRoute="analyze-chart" analyzeService={service} />);
    fireEvent.click(screen.getByRole("button", { name: "Bắt đầu phân tích" }));

    expect(await screen.findByRole("alert")).toBeTruthy();
    expect(screen.getByText("Không tạo được phân tích")).toBeTruthy();
    expect(screen.getByText("Lỗi máy chủ tạm thời.")).toBeTruthy();
    expect(screen.getByText(/Chưa tạo được phân tích cho Nguyễn Văn An/)).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Lưu báo cáo" })).toBeNull();
    expect(fetchMock).toHaveBeenCalledTimes(1);

    expect(screen.getByLabelText("Các bước phân tích")).toBeTruthy();
    expect(document.querySelector('[data-analyze-status="error"]')).toBeTruthy();
  });

  it("real submit path does not depend on portalDemoReport", async () => {
    const fetchMock = vi.fn().mockResolvedValue(okResponse());
    vi.stubGlobal("fetch", fetchMock);

    const service = createTestService();
    render(<PortalApp initialRoute="analyze-chart" analyzeService={service} />);
    fireEvent.click(screen.getByRole("button", { name: "Bắt đầu phân tích" }));

    await screen.findByRole("button", { name: "Lưu báo cáo" }, { timeout: 5000 });
    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-source")).toBe("api");
    expect(root?.getAttribute("data-analysis-id")).toBeTruthy();
    expect(root?.getAttribute("data-analysis-source")).not.toBe("demo");
  });
});
