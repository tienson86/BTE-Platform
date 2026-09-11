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
      analyzed_input: "103",
    },
    reading: {
      layout: "phone",
      display_number: "103",
      analyzed_number: "103",
      interior_zero_note:
        "Số 0 chỉ nên xuất hiện ở đầu số điện thoại. Khi xuất hiện trong thân số, năng lượng dễ bị che hoặc đứt mạch.",
      pairs: [
        {
          pair_digits: "13",
          display_name: "Thiên Y",
          expression: "Bị che bởi số 0",
          force_label: "lực rất mạnh",
          force_level: 4,
        },
      ],
      groups: [
        {
          display_name: "Thiên Y",
          pairs: ["13"],
          meaning: "Thiên Y thiên về tài vận, tình duyên và phúc khí.",
          watchout: "quá thiện lương",
        },
      ],
      triplets: [],
      dominant: { display_name: "Thiên Y", pairs: ["13"] },
      ending: { pair_digits: "13", display_name: "Thiên Y", note: "Năng lượng kết là cát tinh, hướng kết dãy thuận." },
      supportive_group_count: 1,
      challenging_group_count: 0,
      summary:
        "Số 0 chỉ nên xuất hiện ở đầu số điện thoại. Khi xuất hiện trong thân số, năng lượng dễ bị che hoặc đứt mạch. Phần thân số nghiêng mạnh về Thiên Y, nên thiên về tài khí.",
      notices: [],
      purpose_note:
        "Không phải sim nào nhiều cát tinh cũng phù hợp với mọi người. Cần xét mục đích sử dụng và căn mệnh ở lớp phân tích sau.",
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
      summary: "Chưa đủ dữ liệu V1 để luận phần này",
      unknown_notice: "Chưa đủ dữ liệu V1 để luận phần này",
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
    reading: {
      layout: "generic",
      display_number: "1003",
      analyzed_number: "1003",
      pairs: [],
      groups: [],
      triplets: [],
      dominant: null,
      ending: { pair_digits: null, display_name: null, note: "Chưa đủ dữ liệu V1 để kết luận năng lượng kết." },
      summary: "Chưa đủ dữ liệu V1 để luận phần này",
      notices: ["Chưa đủ dữ liệu V1 để luận phần này"],
      incomplete: true,
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
    reading: {
      layout: "generic",
      pairs: [{ pair_digits: "18", display_name: "Ngũ Quỷ", expression: "Bị che bởi số 0", force_label: "lực rất mạnh", force_level: 4 }],
      groups: [{ display_name: "Ngũ Quỷ", pairs: ["18"], meaning: "Ngũ Quỷ là trường biến động mạnh.", watchout: "bất ổn" }],
      dominant: { display_name: "Ngũ Quỷ", pairs: ["18"] },
      ending: { pair_digits: "18", display_name: "Ngũ Quỷ" },
      summary: "Dãy này có nền Ngũ Quỷ bị che bởi âm trường.",
      challenging_group_count: 1,
      supportive_group_count: 0,
    },
  },
};

const sample0328278786 = {
  success: true,
  message: "Number Energy OK",
  data: {
    occurrences: [],
    sequence_state: "NORMAL",
    patterns: [],
    narrative: {
      health_disclaimer:
        "Phần này chỉ mang ý nghĩa tham khảo theo hệ thống Năng lượng số, không phải chẩn đoán y khoa.",
    },
    warnings: [],
    metadata: { knowledge_version: "1.0", purpose_context: "phone_number", analyzed_input: "328278786" },
    reading: {
      layout: "phone",
      display_number: "0328278786",
      analyzed_number: "328278786",
      leading_zero: true,
      leading_zero_note: "Sim này có đầu số 0 hợp lệ.",
      pairs: [
        { pair_digits: "32", display_name: "Họa Hại", force_label: "lực nhẹ", force_level: 1 },
        { pair_digits: "28", display_name: "Sinh Khí", force_label: "lực nhẹ", force_level: 1 },
        { pair_digits: "82", display_name: "Sinh Khí", force_label: "lực nhẹ", force_level: 1 },
        { pair_digits: "27", display_name: "Thiên Y", force_label: "lực nhẹ", force_level: 1 },
        { pair_digits: "78", display_name: "Diên Niên", force_label: "lực mạnh", force_level: 3 },
        { pair_digits: "87", display_name: "Diên Niên", force_label: "lực mạnh", force_level: 3 },
        { pair_digits: "78", display_name: "Diên Niên", force_label: "lực mạnh", force_level: 3 },
        { pair_digits: "86", display_name: "Thiên Y", force_label: "lực mạnh", force_level: 3 },
      ],
      groups: [
        { display_name: "Diên Niên", pairs: ["78", "87", "78"], meaning: "Diên Niên là trường của sự nghiệp và sự ổn định.", watchout: "cứng, cố chấp" },
        { display_name: "Sinh Khí", pairs: ["28", "82"], meaning: "Sinh Khí thiên về quý nhân.", watchout: "thiếu quyết đoán" },
        { display_name: "Thiên Y", pairs: ["27", "86"], meaning: "Thiên Y thiên về tài vận.", watchout: "quá thiện lương" },
        { display_name: "Họa Hại", pairs: ["32"], meaning: "Họa Hại là trường của ngôn ngữ.", watchout: "nóng lời" },
      ],
      triplets: [
        { digits: "328", left_name: "Họa Hại", right_name: "Sinh Khí" },
        { digits: "282", left_name: "Sinh Khí", right_name: "Sinh Khí" },
        { digits: "827", left_name: "Sinh Khí", right_name: "Thiên Y" },
        { digits: "278", left_name: "Thiên Y", right_name: "Diên Niên" },
        { digits: "787", left_name: "Diên Niên", right_name: "Diên Niên" },
        { digits: "878", left_name: "Diên Niên", right_name: "Diên Niên" },
        { digits: "786", left_name: "Diên Niên", right_name: "Thiên Y" },
      ],
      dominant: { display_name: "Diên Niên", pairs: ["78", "87", "78"] },
      ending: {
        pair_digits: "86",
        display_name: "Thiên Y",
        note: "Năng lượng kết là cát tinh, hướng kết dãy thuận.",
      },
      supportive_group_count: 3,
      challenging_group_count: 1,
      supportive_balance_note: "Cấu trúc cát tinh khá cân bằng.",
      lifted: true,
      lifted_note:
        "Hung tinh được cát tinh phía sau nâng đỡ, nên ảnh hưởng bất lợi có cơ hội được kéo về hướng tốt hơn.",
      force_notes: ["Cát tinh có hỗ trợ nhưng chưa đủ lực áp chế hoàn toàn."],
      summary:
        "Sim này có đầu số 0 hợp lệ. Phần thân số nghiêng mạnh về Diên Niên, đi cùng Sinh Khí và Thiên Y, nên thiên về ổn định, trách nhiệm, quý nhân và tài khí. Điểm cần lưu ý là Họa Hại xuất hiện ở đầu phần thân số; tuy nhiên phía sau có Sinh Khí nâng đỡ nên ảnh hưởng được làm mềm hơn.",
      notices: [],
      purpose_note:
        "Không phải sim nào nhiều cát tinh cũng phù hợp với mọi người. Cần xét mục đích sử dụng và căn mệnh ở lớp phân tích sau.",
    },
  },
};

const FORBIDDEN_UI_TOKENS = [
  "UNKNOWN_OR_NOT_DEFINED",
  "NORMAL",
  "HIDDEN",
  "AMPLIFIED",
  "REPEATED",
  "CONTROLLED",
  "strength_rank",
  "classification",
  "source_digits",
  "occurrence_id",
];

function visibleResultText(): string {
  return screen.getByTestId("number-energy-result").textContent || "";
}

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

  it("posts digits and purpose_context then shows pair chips, not engine tokens", async () => {
    mockFetch(sample103);
    render(<NumberEnergyPage />);
    await submitNumber("103", "phone_number");
    await waitFor(() => expect(screen.getByTestId("number-energy-result")).toBeTruthy());
    const post = vi.mocked(fetch).mock.calls[0];
    expect(String(post?.[0])).toContain("/backend/api/v1/number-energy/analyze");
    const body = JSON.parse(String(post?.[1]?.body));
    expect(body).toEqual({ number: "103", purpose_context: "phone_number" });
    expect(screen.getByTestId("pair-chip").textContent).toContain("13");
    expect(screen.getByTestId("pair-chip").textContent).toContain("Thiên Y");
    expect(screen.getByTestId("interior-zero-note").textContent).toContain("Số 0 chỉ nên xuất hiện ở đầu");
    expect(screen.getByTestId("narrative-summary").textContent).toContain("Thiên Y");
    expect(screen.getByTestId("health-disclaimer").textContent).toContain("không phải chẩn đoán y khoa");
    expect(screen.getByTestId("knowledge-version").textContent).toBe("1.0");
    const visible = visibleResultText();
    for (const token of FORBIDDEN_UI_TOKENS) {
      expect(visible).not.toContain(token);
    }
  });

  it("renders unknown as Vietnamese incomplete copy, not raw tokens", async () => {
    mockFetch(sample1003);
    render(<NumberEnergyPage />);
    await submitNumber("1003");
    await waitFor(() => expect(screen.getByTestId("number-energy-result")).toBeTruthy());
    expect(visibleResultText()).toContain("Chưa đủ dữ liệu V1");
    expect(visibleResultText()).not.toContain("UNKNOWN_OR_NOT_DEFINED");
    expect(screen.getByTestId("health-disclaimer").textContent).toContain("không phải chẩn đoán y khoa");
  });

  it("shows hung tinh by name without English classification", async () => {
    mockFetch(sample108);
    render(<NumberEnergyPage />);
    await submitNumber("108");
    await waitFor(() => expect(screen.getByTestId("number-energy-result")).toBeTruthy());
    expect(screen.getByTestId("pair-chip").textContent).toContain("Ngũ Quỷ");
    expect(visibleResultText()).not.toContain("challenging");
    expect(visibleResultText()).not.toContain("expert only");
  });

  it("renders phone reading for 0328278786", async () => {
    mockFetch(sample0328278786);
    render(<NumberEnergyPage />);
    await submitNumber("0328278786", "phone_number");
    await waitFor(() => expect(screen.getByTestId("number-energy-result")).toBeTruthy());
    expect(screen.getByTestId("analyzed-number").textContent).toBe("328278786");
    expect(screen.getByTestId("dominant-energy").textContent).toContain("Diên Niên");
    expect(screen.getByTestId("ending-pair").textContent).toContain("86");
    expect(screen.getByTestId("ending-pair").textContent).toContain("Thiên Y");
    expect(screen.getByTestId("lifted-note").textContent).toContain("nâng đỡ");
    expect(visibleResultText()).not.toContain("NEUTRALIZED");
    expect(visibleResultText()).not.toContain("UNKNOWN_OR_NOT_DEFINED");
    const chips = screen.getAllByTestId("pair-chip").map((node) => node.textContent);
    expect(chips[0]).toContain("32");
    expect(chips[0]).toContain("Họa Hại");
    expect(chips[chips.length - 1]).toContain("86");
    expect(chips[chips.length - 1]).toContain("Thiên Y");
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
