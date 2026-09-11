import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { NumberEnergyPage } from "../../src/features/number_energy/NumberEnergyPage";
import {
  FORBIDDEN_PHRASES,
  PRODUCT_TITLE,
  VALIDATION_FALLBACK,
} from "../../src/features/number_energy/labels";
import { PURPOSE_CONTEXTS } from "../../src/features/number_energy/types";
import { APP_NAV_ITEMS } from "../../src/layouts/Navigation";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

const sample103 = {
  success: true,
  message: "Number Energy OK",
  data: {
    occurrences: [
      {
        occurrence_id: "mod-000",
        source_span: [0, 2],
        source_digits: "103",
        pair_digits: "13",
        energy_id: "tian_yi",
        display_name: "Thiên Y",
        strength_rank: 1,
        classification: "supportive",
        classification_label: "trường khí hỗ trợ",
        state: "HIDDEN",
        via_modifier: 0,
        notes: "underlying pair hidden or attenuated by 0",
      },
    ],
    sequence_state: "HIDDEN",
    patterns: [],
    narrative: {
      language: "vi",
      system_name: "Bát Cực Linh Số",
      system_short_name: "Năng lượng số",
      summary:
        "Theo hệ thống Bát Cực Linh Số (Năng lượng số). Dãy này có nền Thiên Y, thiên về tài khí/phúc khí/tình cảm ổn định, nhưng biểu hiện không lộ mạnh vì bị âm trường che.",
      strengths: ["Thiên Y: tài khí/phúc khí"],
      watchouts: ["Thiên Y: quá thiện lương"],
      purpose_focus: "Với số điện thoại, theo hệ thống này nên đọc thiên về giao tiếp.",
      compatibility_note:
        "Không kết luận tương hợp cuối cùng với chủ số khi chưa có dữ liệu Cung Phi hoặc Bát Tự.",
      health_disclaimer:
        "Phần này chỉ mang ý nghĩa tham khảo theo hệ thống Năng lượng số, không phải chẩn đoán y khoa.",
    },
    warnings: [],
    metadata: {
      engine: "number_energy",
      engine_version: "1.0.0",
      knowledge_version: "1.0",
      system_name: "Bát Cực Linh Số",
      system_short_name: "Năng lượng số",
      purpose_context: "phone_number",
      pattern_labels: [],
    },
  },
};

const sample1003 = {
  success: true,
  message: "Number Energy OK",
  data: {
    occurrences: [],
    sequence_state: "UNKNOWN_OR_NOT_DEFINED",
    patterns: [],
    narrative: {
      language: "vi",
      summary:
        "Theo hệ thống Bát Cực Linh Số (Năng lượng số), một phần hoặc toàn bộ dãy số này chưa được định nghĩa trong V1.",
      unknown_notice: "Trạng thái UNKNOWN_OR_NOT_DEFINED: 00 (consecutive modifiers are not frozen in V1).",
      health_disclaimer:
        "Phần này chỉ mang ý nghĩa tham khảo theo hệ thống Năng lượng số, không phải chẩn đoán y khoa.",
      compatibility_note:
        "Không kết luận tương hợp cuối cùng với chủ số khi chưa có dữ liệu Cung Phi hoặc Bát Tự.",
    },
    warnings: [
      {
        code: "UNKNOWN_OR_NOT_DEFINED",
        reason: "consecutive modifiers are not frozen in V1",
        customer_reason:
          "Các số 0 hoặc 5 đứng liền nhau chưa được khóa trong V1, nên không suy diễn thêm quy tắc.",
        source_digits: "00",
        source_span: [1, 2],
      },
    ],
    metadata: {
      engine: "number_energy",
      engine_version: "1.0.0",
      knowledge_version: "1.0",
      system_name: "Bát Cực Linh Số",
      system_short_name: "Năng lượng số",
      purpose_context: "generic_number",
    },
  },
};

const sample108 = {
  success: true,
  message: "Number Energy OK",
  data: {
    occurrences: [
      {
        occurrence_id: "mod-000",
        source_span: [0, 2],
        source_digits: "108",
        pair_digits: "18",
        energy_id: "wu_gui",
        display_name: "Ngũ Quỷ",
        strength_rank: 1,
        classification: "challenging",
        classification_label: "trường khí cần kiểm soát",
        state: "HIDDEN",
        via_modifier: 0,
        notes: "expert only",
      },
    ],
    sequence_state: "HIDDEN",
    patterns: [],
    narrative: {
      summary: "Dãy này có nền Ngũ Quỷ bị che bởi âm trường.",
      health_disclaimer:
        "Phần này chỉ mang ý nghĩa tham khảo theo hệ thống Năng lượng số, không phải chẩn đoán y khoa.",
    },
    warnings: [],
    metadata: {
      engine: "number_energy",
      knowledge_version: "1.0",
      purpose_context: "generic_number",
    },
  },
};

function mockFetch(payload: unknown, status = 200): void {
  vi.stubGlobal(
    "fetch",
    vi.fn(() =>
      Promise.resolve({
        ok: status >= 200 && status < 300,
        status,
        text: () => Promise.resolve(JSON.stringify(payload)),
      }),
    ),
  );
}

async function submitNumber(value: string, context?: string): Promise<void> {
  fireEvent.change(screen.getByLabelText("Dãy số"), { target: { value } });
  if (context) {
    fireEvent.change(screen.getByLabelText("Ngữ cảnh sử dụng"), { target: { value: context } });
  }
  fireEvent.submit(screen.getByTestId("number-energy-form"));
}

describe("Number Energy V1 UI", () => {
  it("renders the form, empty state, and purpose contexts", () => {
    render(<NumberEnergyPage />);
    expect(screen.getByTestId("number-energy-title").textContent).toBe(PRODUCT_TITLE);
    expect(screen.getByTestId("number-energy-form")).toBeTruthy();
    expect(screen.getByTestId("empty-state")).toBeTruthy();
    const select = screen.getByLabelText("Ngữ cảnh sử dụng") as HTMLSelectElement;
    expect(Array.from(select.options).map((item) => item.value)).toEqual([...PURPOSE_CONTEXTS]);
    expect(APP_NAV_ITEMS).toHaveLength(4);
  });

  it("rejects empty input without calling the API", () => {
    mockFetch(sample103);
    render(<NumberEnergyPage />);
    fireEvent.submit(screen.getByTestId("number-energy-form"));
    expect(screen.getByTestId("error-state").textContent).toContain("Vui lòng nhập dãy số");
    expect(vi.mocked(fetch).mock.calls).toHaveLength(0);
  });

  it("rejects overlong digit strings without calling the API", () => {
    mockFetch(sample103);
    render(<NumberEnergyPage />);
    fireEvent.change(screen.getByLabelText("Dãy số"), { target: { value: "1".repeat(129) } });
    fireEvent.submit(screen.getByTestId("number-energy-form"));
    expect(screen.getByTestId("error-state").textContent).toContain("vượt quá độ dài");
    expect(vi.mocked(fetch).mock.calls).toHaveLength(0);
  });

  it("shows loading while the request is in flight", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => new Promise<Response>(() => undefined)),
    );
    render(<NumberEnergyPage />);
    await submitNumber("103");
    expect(await screen.findByTestId("loading-state")).toBeTruthy();
    expect(screen.getByTestId("submit-number-energy")).toHaveProperty("disabled", true);
  });

  it("posts digits and purpose_context then shows API result", async () => {
    mockFetch(sample103);
    render(<NumberEnergyPage />);
    await submitNumber("103", "phone_number");
    await waitFor(() => expect(screen.getByTestId("number-energy-result")).toBeTruthy());
    const post = vi.mocked(fetch).mock.calls[0];
    expect(String(post?.[0])).toContain("/backend/api/v1/number-energy/analyze");
    const body = JSON.parse(String(post?.[1]?.body));
    expect(body).toEqual({ number: "103", purpose_context: "phone_number" });
    expect(screen.getByTestId("sequence-state").textContent).toBe("HIDDEN");
    expect(screen.getByTestId("occurrence-item").textContent).toContain("Thiên Y");
    expect(screen.getByTestId("classification-label").textContent).toBe("trường khí hỗ trợ");
    expect(screen.getByTestId("narrative-summary").textContent).toContain("Thiên Y");
    expect(screen.getByTestId("health-disclaimer").textContent).toContain("không phải chẩn đoán y khoa");
    expect(screen.getByTestId("knowledge-version").textContent).toBe("1.0");
    expect(screen.getByTestId("narrative-strengths")).toBeTruthy();
    expect(screen.getByTestId("narrative-watchouts")).toBeTruthy();
    expect(document.body.textContent).not.toContain("underlying pair hidden");
  });

  it("renders unknown state, warning, and health disclaimer from the API payload", async () => {
    mockFetch(sample1003);
    render(<NumberEnergyPage />);
    await submitNumber("1003");
    await waitFor(() => expect(screen.getByTestId("number-energy-result")).toBeTruthy());
    expect(screen.getByTestId("sequence-state").textContent).toBe("UNKNOWN_OR_NOT_DEFINED");
    expect(screen.getByTestId("unknown-notice").textContent).toContain("UNKNOWN_OR_NOT_DEFINED");
    expect(screen.getByTestId("warnings-card").textContent).toContain("chưa được khóa trong V1");
    expect(screen.getByTestId("warnings-card").textContent).not.toContain(
      "consecutive modifiers are not frozen",
    );
    expect(screen.getByTestId("health-disclaimer").textContent).toContain("không phải chẩn đoán y khoa");
  });

  it("renders hung tinh as trường khí cần kiểm soát from the API label", async () => {
    mockFetch(sample108);
    render(<NumberEnergyPage />);
    await submitNumber("108");
    await waitFor(() => expect(screen.getByTestId("number-energy-result")).toBeTruthy());
    expect(screen.getByTestId("classification-label").textContent).toBe("trường khí cần kiểm soát");
    expect(screen.getByTestId("occurrence-item").textContent).not.toContain("challenging");
    expect(document.body.textContent).not.toContain("expert only");
  });

  it("shows a Vietnamese message on API 422", async () => {
    mockFetch({ success: false, message: "number input must contain digits 0-9 only" }, 422);
    render(<NumberEnergyPage />);
    await submitNumber("103");
    const alert = await screen.findByTestId("error-state");
    expect(alert.textContent).toContain(VALIDATION_FALLBACK);
    expect(alert.textContent).not.toContain("digits 0-9");
  });

  it("shows a customer-safe message on HTTP 500", async () => {
    mockFetch({ success: false, message: "Number energy analysis failed: boom" }, 500);
    render(<NumberEnergyPage />);
    await submitNumber("103");
    const alert = await screen.findByTestId("error-state");
    expect(alert.textContent).toContain("Không thể hoàn tất phân tích lúc này");
    expect(alert.textContent).not.toContain("boom");
    expect(screen.getByTestId("retry-analysis")).toBeTruthy();
  });

  it("shows a customer-safe message on server failure", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.reject(new TypeError("Failed to fetch"))),
    );
    render(<NumberEnergyPage />);
    await submitNumber("103");
    const alert = await screen.findByTestId("error-state");
    expect(alert.textContent).toContain("Không thể hoàn tất phân tích lúc này");
    expect(screen.getByTestId("retry-analysis")).toBeTruthy();
  });

  it("does not invent medical diagnosis copy", async () => {
    mockFetch(sample103);
    render(<NumberEnergyPage />);
    await submitNumber("103");
    await waitFor(() => expect(screen.getByTestId("number-energy-result")).toBeTruthy());
    const blob = document.body.textContent?.toLowerCase() || "";
    for (const phrase of FORBIDDEN_PHRASES) {
      expect(blob).not.toContain(phrase);
    }
    expect(blob).not.toContain("%");
  });

  it("uses token-based layout without traffic-light colors", () => {
    const here = dirname(fileURLToPath(import.meta.url));
    const css = readFileSync(resolve(here, "../../static/css/number_energy.css"), "utf8");
    expect(css).toContain("var(--space-6)");
    expect(css).toContain("@media (max-width: 1024px)");
    expect(css).toContain("@media (max-width: 768px)");
    expect(css).not.toContain("#ff0000");
    expect(css).not.toContain("traffic");
  });
});
