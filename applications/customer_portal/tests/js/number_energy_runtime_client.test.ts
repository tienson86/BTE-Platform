import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { afterEach, describe, expect, it, vi } from "vitest";

import {
  DEFAULT_NUMBER_ENERGY_RUNTIME_API,
  NUMBER_ENERGY_RUNTIME_ERROR_CODE,
  analyzeNumberEnergyRuntime,
  numberEnergyRuntimeApiUrl,
} from "../../src/features/number_energy/runtimeClient";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  delete (window as Window & { __BTE_NUMBER_ENERGY_API__?: string }).__BTE_NUMBER_ENERGY_API__;
});

const PAGE_FILES = [
  "NumberEnergyPage.tsx",
  "index.ts",
  "ResultSection.tsx",
  "InputSection.tsx",
] as const;

type FetchInit = {
  method?: string;
  headers?: Record<string, string>;
  body?: string;
};

function featureSource(fileName: string): string {
  const here = dirname(fileURLToPath(import.meta.url));
  return readFileSync(resolve(here, `../../src/features/number_energy/${fileName}`), "utf8");
}

function entrySource(): string {
  const here = dirname(fileURLToPath(import.meta.url));
  return readFileSync(resolve(here, "../../src/entries/numberEnergyApp.tsx"), "utf8");
}

function stubJsonResponse(body: unknown, status = 200): void {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      text: async () => JSON.stringify(body),
    }),
  );
}

function stubTextResponse(text: string, status = 200): void {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      text: async () => text,
    }),
  );
}

describe("Number Energy RB07 runtime client", () => {
  it("POSTs the live analyze contract to the default endpoint", async () => {
    stubJsonResponse({
      success: true,
      data: { pair_occurrences: [], verified_by_runtime: true },
    });
    const result = await analyzeNumberEnergyRuntime({
      purpose_context: "phone_number",
      input: "141319",
    });
    const fetchMock = fetch as unknown as ReturnType<typeof vi.fn>;
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, init] = fetchMock.mock.calls[0] as [string, FetchInit];
    expect(url).toBe(DEFAULT_NUMBER_ENERGY_RUNTIME_API);
    expect(url).toBe("/api/v1/number-energy/analyze");
    expect(init.method).toBe("POST");
    expect(init.headers).toEqual({
      Accept: "application/json",
      "Content-Type": "application/json",
    });
    expect(JSON.parse(init.body ?? "{}")).toEqual({
      number: "141319",
      purpose_context: "phone_number",
    });
    expect(result).toEqual({
      ok: true,
      data: { pair_occurrences: [], verified_by_runtime: true },
    });
  });

  it("uses window.__BTE_NUMBER_ENERGY_API__ when set", async () => {
    (
      window as Window & { __BTE_NUMBER_ENERGY_API__?: string }
    ).__BTE_NUMBER_ENERGY_API__ = "https://runtime.test/number-energy/analyze";
    expect(numberEnergyRuntimeApiUrl()).toBe("https://runtime.test/number-energy/analyze");
    stubJsonResponse({ success: true, data: { chain: { primary_energy_label: "Diên Niên" } } });
    await analyzeNumberEnergyRuntime({
      purpose_context: "phone_number",
      input: "141319",
    });
    const fetchMock = fetch as unknown as ReturnType<typeof vi.fn>;
    expect(fetchMock.mock.calls[0]?.[0]).toBe("https://runtime.test/number-energy/analyze");
  });

  it("falls back to /api/v1/number-energy/analyze when window config is absent", () => {
    expect(numberEnergyRuntimeApiUrl()).toBe("/api/v1/number-energy/analyze");
  });

  it("lets apiUrl override window config", async () => {
    (
      window as Window & { __BTE_NUMBER_ENERGY_API__?: string }
    ).__BTE_NUMBER_ENERGY_API__ = "https://runtime.test/from-window";
    stubJsonResponse({ success: true, data: { pair_summary: { pair_count: 1 } } });
    await analyzeNumberEnergyRuntime({
      purpose_context: "car_plate",
      input: "51A12345",
      apiUrl: "https://runtime.test/override",
    });
    const fetchMock = fetch as unknown as ReturnType<typeof vi.fn>;
    expect(fetchMock.mock.calls[0]?.[0]).toBe("https://runtime.test/override");
  });

  it("returns a structured HTTP error without leaking raw payload text", async () => {
    stubJsonResponse(
      { success: false, detail: "Traceback (most recent call last): engine dump" },
      500,
    );
    const result = await analyzeNumberEnergyRuntime({
      purpose_context: "phone_number",
      input: "141319",
    });
    expect(result.ok).toBe(false);
    if (result.ok) {
      return;
    }
    expect(result.error.code).toBe(NUMBER_ENERGY_RUNTIME_ERROR_CODE.HTTP_ERROR);
    expect(result.error.status).toBe(500);
    expect(result.error.message).toBe("Không thể hoàn tất phân tích lúc này.");
    expect(JSON.stringify(result)).not.toContain("Traceback");
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("returns a structured error for invalid JSON", async () => {
    stubTextResponse("<html>upstream</html>", 200);
    const result = await analyzeNumberEnergyRuntime({
      purpose_context: "phone_number",
      input: "141319",
    });
    expect(result).toEqual({
      ok: false,
      error: {
        code: NUMBER_ENERGY_RUNTIME_ERROR_CODE.INVALID_JSON,
        message: "Không thể đọc kết quả phân tích.",
        status: 200,
      },
    });
  });

  it("returns a structured error when data is missing", async () => {
    stubJsonResponse({ success: true, message: "Number Energy OK" });
    const result = await analyzeNumberEnergyRuntime({
      purpose_context: "phone_number",
      input: "141319",
    });
    expect(result).toEqual({
      ok: false,
      error: {
        code: NUMBER_ENERGY_RUNTIME_ERROR_CODE.MISSING_DATA,
        message: "Kết quả phân tích chưa đầy đủ.",
        status: 200,
      },
    });
  });

  it("does not call the presentation adapter or hardcode the Golden phone", () => {
    const source = featureSource("runtimeClient.ts");
    expect(source).not.toContain("adaptNumberEnergyPresentation");
    expect(source).not.toContain("presentationAdapter");
    expect(source).not.toContain("from \"./api\"");
    expect(source).not.toContain("ResultView");
    expect(source).not.toContain("0328278786");
    expect(source).not.toContain("GOLDEN_");
  });

  it("is not imported by the frozen page, barrel, or app entry", () => {
    for (const fileName of PAGE_FILES) {
      const source = featureSource(fileName);
      expect(source).not.toContain("runtimeClient");
      expect(source).not.toContain("analyzeNumberEnergyRuntime");
    }
    expect(entrySource()).not.toContain("runtimeClient");
    expect(entrySource()).not.toContain("analyzeNumberEnergyRuntime");
  });
});
