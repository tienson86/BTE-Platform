import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { afterEach, describe, expect, it, vi } from "vitest";

import { NUMBER_ENERGY_CONTRACT_FREEZE } from "../../src/features/number_energy/presentationContract";
import {
  NUMBER_ENERGY_RUNTIME_STATUS,
  createNumberEnergyRuntimeController,
} from "../../src/features/number_energy/runtimeController";
import type { NumberEnergyRuntimeResult } from "../../src/features/number_energy/runtimeClient";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

const FORBIDDEN_ERROR_TOKENS = [
  "energy_id",
  "source_span",
  "Traceback",
  "HIDDEN",
  "verified_by_runtime",
  "occurrence_id",
];

function featureSource(fileName: string): string {
  const here = dirname(fileURLToPath(import.meta.url));
  return readFileSync(resolve(here, `../../src/features/number_energy/${fileName}`), "utf8");
}

function entrySource(): string {
  const here = dirname(fileURLToPath(import.meta.url));
  return readFileSync(resolve(here, "../../src/entries/numberEnergyApp.tsx"), "utf8");
}

function runtimeData(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    purpose_context: "phone_number",
    metadata: { input_raw: "141319", purpose_context: "phone_number" },
    pair_occurrences: [
      {
        pair_digits: "14",
        display_name: "Sinh Khí",
        category: "CAT",
        category_label: "Cát",
        strength_label: "Nhẹ",
        strength_visual: [true, false, false, false],
      },
    ],
    pair_summary: {
      pair_count: 1,
      supportive_pair_count: 1,
      challenging_pair_count: 0,
    },
    ...overrides,
  };
}

function deferredAnalyze(): {
  analyze: (input: { purpose_context: string; input: string }) => Promise<NumberEnergyRuntimeResult>;
  resolve: (result: NumberEnergyRuntimeResult) => void;
} {
  let resolvePromise: ((result: NumberEnergyRuntimeResult) => void) | undefined;
  const analyze = vi.fn(
    () =>
      new Promise<NumberEnergyRuntimeResult>((resolve) => {
        resolvePromise = resolve;
      }),
  );
  return {
    analyze,
    resolve: (result) => {
      if (!resolvePromise) {
        throw new Error("analyze was not called");
      }
      resolvePromise(result);
    },
  };
}

describe("Number Energy RB08 runtime controller", () => {
  it("starts idle and does not call the runtime client", () => {
    const analyze = vi.fn();
    const controller = createNumberEnergyRuntimeController({ analyze });
    expect(controller.getState()).toEqual({
      status: NUMBER_ENERGY_RUNTIME_STATUS.idle,
      view: null,
      adapterResult: null,
      slotSource: null,
      gaps: [],
      error: null,
    });
    expect(analyze).not.toHaveBeenCalled();
  });

  it("submits once with normalized input, then exposes adapter view", async () => {
    const analyze = vi.fn().mockResolvedValue({
      ok: true,
      data: runtimeData(),
    });
    const controller = createNumberEnergyRuntimeController({ analyze });
    const loadingPromise = controller.submit({
      purpose_context: "phone_number",
      input: "141 319",
    });
    expect(controller.getState().status).toBe(NUMBER_ENERGY_RUNTIME_STATUS.loading);
    const state = await loadingPromise;
    expect(analyze).toHaveBeenCalledTimes(1);
    expect(analyze).toHaveBeenCalledWith({
      purpose_context: "phone_number",
      input: "141319",
    });
    expect(state.status).toBe(NUMBER_ENERGY_RUNTIME_STATUS.success);
    expect(state.view).not.toBeNull();
    expect(state.adapterResult?.freezeLabel).toBe(NUMBER_ENERGY_CONTRACT_FREEZE);
    expect(state.slotSource).toEqual(state.adapterResult?.slotSource);
    expect(state.view?.pairs[0]?.digits).toBe("14");
    expect(state.error).toBeNull();
  });

  it("exposes a safe error state on API failure without a partial view", async () => {
    const analyze = vi.fn().mockResolvedValue({
      ok: false,
      error: {
        code: "HTTP_ERROR",
        message: "Không thể hoàn tất phân tích lúc này.",
        status: 500,
      },
    });
    const controller = createNumberEnergyRuntimeController({ analyze });
    const state = await controller.submit({
      purpose_context: "phone_number",
      input: "141319",
    });
    expect(state.status).toBe(NUMBER_ENERGY_RUNTIME_STATUS.error);
    expect(state.view).toBeNull();
    expect(state.adapterResult).toBeNull();
    expect(state.slotSource).toBeNull();
    expect(state.gaps).toEqual([]);
    expect(state.error).toEqual({
      code: "HTTP_ERROR",
      message: "Không thể hoàn tất phân tích lúc này.",
    });
    for (const token of FORBIDDEN_ERROR_TOKENS) {
      expect(JSON.stringify(state.error)).not.toContain(token);
    }
  });

  it("keeps success when adapter records a missing-slot RUNTIME_GAP", async () => {
    const analyze = vi.fn().mockResolvedValue({
      ok: true,
      data: runtimeData({ pair_occurrences: undefined }),
    });
    const controller = createNumberEnergyRuntimeController({ analyze });
    const state = await controller.submit({
      purpose_context: "phone_number",
      input: "141319",
    });
    expect(state.status).toBe(NUMBER_ENERGY_RUNTIME_STATUS.success);
    expect(state.gaps.some((item) => item.id === "G19")).toBe(true);
    expect(state.slotSource?.["P-S01"]).toBe("GOLDEN_FIXTURE");
    expect(state.view?.pairs.map((item) => item.digits)).toEqual([
      "32",
      "28",
      "82",
      "27",
      "78",
      "87",
      "78",
      "86",
    ]);
  });

  it("reset returns to idle and drops runtime view", async () => {
    const analyze = vi.fn().mockResolvedValue({
      ok: true,
      data: runtimeData(),
    });
    const controller = createNumberEnergyRuntimeController({ analyze });
    await controller.submit({
      purpose_context: "phone_number",
      input: "141319",
    });
    controller.reset();
    expect(controller.getState()).toEqual({
      status: NUMBER_ENERGY_RUNTIME_STATUS.idle,
      view: null,
      adapterResult: null,
      slotSource: null,
      gaps: [],
      error: null,
    });
  });

  it("ignores a stale response after a newer submit", async () => {
    const first = deferredAnalyze();
    const secondData = runtimeData({
      metadata: { input_raw: "222222", purpose_context: "phone_number" },
      pair_occurrences: [
        {
          pair_digits: "22",
          display_name: "Diên Niên",
          category: "CAT",
          category_label: "Cát",
          strength_label: "Mạnh",
          strength_visual: [true, true, true, false],
        },
      ],
    });
    const analyze = vi
      .fn()
      .mockImplementationOnce(first.analyze)
      .mockResolvedValueOnce({ ok: true, data: secondData });
    const controller = createNumberEnergyRuntimeController({ analyze });
    const stale = controller.submit({
      purpose_context: "phone_number",
      input: "141319",
    });
    const latest = controller.submit({
      purpose_context: "phone_number",
      input: "222222",
    });
    const latestState = await latest;
    first.resolve({
      ok: true,
      data: runtimeData(),
    });
    await stale;
    expect(analyze).toHaveBeenCalledTimes(2);
    expect(latestState.status).toBe(NUMBER_ENERGY_RUNTIME_STATUS.success);
    expect(controller.getState().view?.pairs[0]?.digits).toBe("22");
    expect(controller.getState()).toBe(latestState);
  });

  it("does not fetch when input is invalid", async () => {
    const analyze = vi.fn();
    const controller = createNumberEnergyRuntimeController({ analyze });
    const state = await controller.submit({
      purpose_context: "phone_number",
      input: "  ",
    });
    expect(analyze).not.toHaveBeenCalled();
    expect(state.status).toBe(NUMBER_ENERGY_RUNTIME_STATUS.error);
    expect(state.view).toBeNull();
    expect(state.error?.message).toBe("Dữ liệu phân tích chưa hợp lệ.");
  });

  it("is not imported by the default entry, barrel, or InputSection", () => {
    const source = featureSource("runtimeController.ts");
    expect(source).toContain("adaptNumberEnergyPresentation");
    expect(source).toContain("analyzeNumberEnergyRuntime");
    expect(featureSource("index.ts")).not.toContain("runtimeController");
    expect(featureSource("InputSection.tsx")).not.toContain("runtimeController");
    expect(featureSource("InputSection.tsx")).not.toContain("useNumberEnergyRuntime");
    expect(entrySource()).not.toContain("runtimeController");
    expect(entrySource()).not.toContain("useNumberEnergyRuntime");
    expect(entrySource()).not.toContain("runtimeMode");
  });
});
