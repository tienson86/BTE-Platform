import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { MarriageConsultingPage } from "../../src/features/marriage_consulting/MarriageConsultingPage";
import { adaptMarriageView } from "../../src/features/marriage_consulting/adapter";
import { ResultView } from "../../src/features/marriage_consulting/ResultView";
import { FORBIDDEN_ID_PATTERN, FORBIDDEN_SCORE_PATTERN, PRODUCT_TITLE } from "../../src/features/marriage_consulting/labels";
import { DEFAULT_PERSON_A, DEFAULT_PERSON_B, EMPTY_PERSON, toConsultationBody, validatePerson } from "../../src/features/marriage_consulting/request";
import { APP_NAV_ITEMS } from "../../src/layouts/Navigation";
import type { MarriageConsultationDto, MarriageReportDto, MarriageWarning } from "../../src/features/marriage_consulting/types";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

const consultation: MarriageConsultationDto = {
  consultation_id: "MC-19870121-TEST01",
  status: "SUCCESS",
  person_a: { display_name: "An", gender: "male" },
  person_b: { display_name: "Binh", gender: "female" },
  overall_state: "mixed",
  score: null,
  grade: null,
  confidence: { level: "high", overall: 0.82 },
  limitations: ["birth_time_quality"],
  headline: "Có một số điểm cần điều chỉnh",
};

const report: MarriageReportDto = {
  consultation_id: "MC-19870121-TEST01",
  score: null,
  grade: null,
  sections: [
    {
      section_id: "identity",
      title: "Hồ sơ cặp đôi",
      summary: "An và Binh",
      blocks: [{ block_id: "identity-header", kind: "headline", title: "Hồ sơ", body: "An (Nam) và Binh (Nữ)", semantic_key: null, state: null, domain: null }],
    },
    {
      section_id: "executive_summary",
      title: "Tóm tắt tư vấn",
      summary: "Có một số điểm cần điều chỉnh",
      blocks: [{ block_id: "exec", kind: "summary", title: "Tóm tắt", body: "Cấu trúc hiện cho thấy vừa có điểm hỗ trợ, vừa có điểm tạo áp lực.", semantic_key: null, state: "mixed", domain: null }],
    },
    {
      section_id: "compatibility_hero",
      title: "Tương hợp tổng thể",
      summary: "Có một số điểm cần điều chỉnh",
      blocks: [
        { block_id: "hero-state", kind: "decision_state", title: "Có một số điểm cần điều chỉnh", body: "Cấu trúc hiện cho thấy vừa có điểm hỗ trợ, vừa có điểm tạo áp lực.", semantic_key: null, state: "mixed", domain: null },
        { block_id: "hero-summary", kind: "summary", title: null, body: "Cấu trúc hiện cho thấy vừa có điểm hỗ trợ, vừa có điểm tạo áp lực.", semantic_key: null, state: null, domain: null },
        { block_id: "hero-s", kind: "highlight", title: "Điểm hỗ trợ", body: "Ngũ hành đang nâng đỡ", semantic_key: null, state: null, domain: null },
        { block_id: "hero-r", kind: "highlight", title: "Điểm cần lưu ý", body: "Can Chi có điểm căng", semantic_key: null, state: null, domain: null },
      ],
    },
    {
      section_id: "strengths",
      title: "Điểm hỗ trợ then chốt",
      summary: null,
      blocks: [{ block_id: "s1", kind: "highlight", title: "Ngũ hành đang nâng đỡ nền tảng chung.", body: "Ngũ hành đang nâng đỡ nền tảng chung.", semantic_key: null, state: null, domain: "five_elements" }],
    },
    {
      section_id: "risks",
      title: "Điểm cần điều chỉnh",
      summary: null,
      blocks: [{ block_id: "r1", kind: "highlight", title: "Can Chi có điểm cần phối hợp rõ hơn.", body: "Can Chi có điểm cần phối hợp rõ hơn.", semantic_key: null, state: null, domain: "stem_branch" }],
    },
    {
      section_id: "domain_analysis",
      title: "Hiểu vì sao",
      summary: null,
      blocks: [
        { block_id: "d1", kind: "domain_summary", title: "Ngũ hành", body: "Lớp ngũ hành đang hỗ trợ.", semantic_key: null, state: "supportive", domain: "five_elements" },
        { block_id: "d2", kind: "domain_summary", title: "Can Chi", body: "Lớp can chi có điểm cần điều chỉnh.", semantic_key: null, state: "mixed", domain: "stem_branch" },
        { block_id: "d3", kind: "domain_summary", title: "Thập thần", body: "Lớp thập thần tương đối cân.", semantic_key: null, state: "balanced", domain: "ten_gods" },
        { block_id: "d4", kind: "domain_summary", title: "Tài chính", body: "Lớp tài chính cần quy ước chi tiêu.", semantic_key: null, state: "mixed", domain: "finance" },
      ],
    },
    {
      section_id: "action_plan",
      title: "Kế hoạch hành động",
      summary: null,
      blocks: [
        {
          block_id: "a1",
          kind: "recommendation",
          title: "Giữ nhịp hỗ trợ đã có",
          body: "Ưu tiên cao. Giữ nhịp trao đổi đều. Khi nào: Áp dụng thường xuyên. Giúp hai người dễ phối hợp hơn.",
          semantic_key: null,
          state: null,
          domain: "five_elements",
        },
      ],
    },
    {
      section_id: "confidence_limitations",
      title: "Độ tin cậy và giới hạn",
      summary: null,
      blocks: [{ block_id: "c1", kind: "confidence", title: null, body: "Độ tin cậy của hồ sơ ở mức cao trên dữ liệu hiện có.", semantic_key: null, state: null, domain: null }],
    },
    {
      section_id: "conclusion",
      title: "Kết luận",
      summary: "Có một số điểm cần điều chỉnh",
      blocks: [{ block_id: "k1", kind: "paragraph", title: null, body: "Có một số điểm cần điều chỉnh. Nên xử lý điểm căng trước.", semantic_key: null, state: "mixed", domain: null }],
    },
    {
      section_id: "appendix",
      title: "Phụ lục phương pháp",
      summary: null,
      blocks: [{ block_id: "ap1", kind: "methodology", title: "Cách đọc hồ sơ", body: "Không dùng điểm số tương hợp vì mô hình điểm hiện chưa khả dụng.", semantic_key: null, state: null, domain: null, visibility: "customer" }],
    },
  ],
};

const warnings: MarriageWarning[] = [
  { code: "DOMAIN_UNAVAILABLE", description: "This domain does not have enough structural data.", affected_domain: "interaction" },
  { code: "DOMAIN_UNAVAILABLE", description: "This domain does not have enough structural data.", affected_domain: "family" },
  { code: "DOMAIN_UNAVAILABLE", description: "This domain does not have enough structural data.", affected_domain: "children" },
  { code: "TIMING_UNAVAILABLE", description: "Timing coverage is not available for this consultation.", affected_domain: "luck" },
];

function envelope<T>(data: T, extraWarnings: MarriageWarning[] = warnings) {
  return { status: "SUCCESS", data, warnings: extraWarnings, errors: [] };
}

function mockApi(options?: { fail?: boolean; retryable?: boolean }) {
  vi.stubGlobal(
    "fetch",
    vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (options?.fail) {
        return jsonResponse(
          {
            status: "FAILED",
            data: null,
            warnings: [],
            errors: [
              {
                code: "INTERNAL_ERROR",
                stage: "runtime",
                message: "An unexpected error occurred.",
                retryable: options.retryable ?? true,
                consultation_id: null,
              },
            ],
          },
          500,
        );
      }
      if (init?.method === "POST") {
        const body = JSON.parse(String(init.body || "{}")) as { person_a?: { gender?: string; birth_date?: string } };
        expect(body.person_a?.gender).toBe("female");
        expect(body.person_a?.birth_date).toBe("1987-01-21");
        return jsonResponse(envelope(consultation), 201);
      }
      if (url.includes("/report")) {
        return jsonResponse(envelope(report));
      }
      return jsonResponse(envelope(consultation));
    }),
  );
}

function jsonResponse(payload: unknown, status = 200): Response {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function fillValidForm(): void {
  fireEvent.change(screen.getByLabelText("Họ tên", { selector: "#person-a-full-name" }), { target: { value: "An" } });
  fireEvent.change(screen.getByLabelText("Ngày sinh dương lịch", { selector: "#person-a-birth-date" }), {
    target: { value: "21011987" },
  });
  fireEvent.change(screen.getByLabelText("Họ tên", { selector: "#person-b-full-name" }), { target: { value: "Binh" } });
  fireEvent.change(screen.getByLabelText("Ngày sinh dương lịch", { selector: "#person-b-birth-date" }), {
    target: { value: "15051990" },
  });
}

describe("TV1-B07 Marriage Consulting UI", () => {
  it("1 route heading loads", () => {
    render(<MarriageConsultingPage />);
    expect(screen.getByTestId("marriage-title").textContent).toBe(PRODUCT_TITLE);
    expect(screen.getByTestId("consulting-family").textContent).toContain("Tư vấn");
  });

  it("2-5 person forms use fixed genders and allow unknown branch-hour birth time", () => {
    render(<MarriageConsultingPage />);
    expect(screen.getByRole("heading", { name: "Người Nữ (Phụ nữ)" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Người Nam (Đàn ông)" })).toBeTruthy();
    expect(screen.queryByText("Giới tính")).toBeNull();
    expect(DEFAULT_PERSON_A.gender).toBe("female");
    expect(DEFAULT_PERSON_B.gender).toBe("male");
    expect((screen.getAllByLabelText("Giờ sinh")[0] as HTMLSelectElement).value).toBe("");
    expect((screen.getAllByLabelText("Giờ sinh")[1] as HTMLSelectElement).value).toBe("");
    fireEvent.change(screen.getAllByLabelText("Giờ sinh")[0]!, { target: { value: "06:00" } });
    expect((screen.getAllByLabelText("Giờ sinh")[0] as HTMLSelectElement).value).toBe("06:00");
    expect(screen.getAllByText("Giờ Mão (05:00-06:59)")).toHaveLength(2);
    expect(validatePerson({ ...EMPTY_PERSON, gender: "male", birth_date: "21/01/1987" })).toEqual({});
  });

  it("6 validation errors for missing date", () => {
    render(<MarriageConsultingPage />);
    fireEvent.submit(screen.getByTestId("marriage-form"));
    expect(screen.getByTestId("error-state").textContent).toContain("Thiếu thông tin bắt buộc");
    expect(screen.getByTestId("person-a-panel").textContent).toContain("Vui lòng nhập ngày sinh dương lịch");
  });

  it("7 API request contract posts person_a and person_b", async () => {
    mockApi();
    render(<MarriageConsultingPage />);
    fillValidForm();
    fireEvent.submit(screen.getByTestId("marriage-form"));
    await waitFor(() => expect(screen.getByTestId("marriage-result")).toBeTruthy());
    const fetchMock = vi.mocked(fetch);
    const post = fetchMock.mock.calls.find((call) => String(call[1]?.method) === "POST");
    expect(post).toBeTruthy();
    const body = JSON.parse(String(post?.[1]?.body));
    expect(body.person_a.gender).toBe("female");
    expect(body.person_b.gender).toBe("male");
    expect(body.person_a.birth_time).toBeUndefined();
    expect(body.options.include_score).toBe(true);
    expect(toConsultationBody(
      { full_name: "An", gender: "female", birth_date: "21/01/1987", birth_time: "", birth_place: "" },
      { full_name: "Binh", gender: "male", birth_date: "15/05/1990", birth_time: "", birth_place: "" },
    )?.person_a.birth_date).toBe("1987-01-21");
  });

  it("8 loading state appears while waiting", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => new Promise<Response>(() => undefined)),
    );
    render(<MarriageConsultingPage />);
    fillValidForm();
    fireEvent.submit(screen.getByTestId("marriage-form"));
    expect(await screen.findByTestId("loading-state")).toBeTruthy();
  });

  it("9-20 successful semantic journey rendering", async () => {
    mockApi();
    render(<MarriageConsultingPage />);
    fillValidForm();
    fireEvent.submit(screen.getByTestId("marriage-form"));
    await waitFor(() => expect(screen.getByTestId("marriage-result")).toBeTruthy());
    expect(screen.getByTestId("compatibility-hero").getAttribute("data-semantic-only")).toBe("true");
    expect(screen.queryByText(/82%/)).toBeNull();
    expect(screen.queryByText(/\/100/)).toBeNull();
    expect(screen.queryByText(/Grade/)).toBeNull();
    expect(screen.getByTestId("hero-headline").textContent).toContain("điều chỉnh");
    expect(screen.getByTestId("executive-summary").textContent).toContain("điểm hỗ trợ");
    expect(screen.queryByTestId("detailed-analysis")).toBeNull();
    expect(screen.queryByTestId("key-strengths")).toBeNull();
    expect(screen.queryByTestId("key-risks")).toBeNull();
    expect(screen.queryByTestId("expert-mode")).toBeNull();
    expect(screen.queryByText("Xem chế độ chuyên gia")).toBeNull();
    expect(screen.queryByText("Giải thích kỹ thuật")).toBeNull();
    expect(screen.queryByText("Phụ lục phương pháp")).toBeNull();
    expect(screen.queryByTestId("domain-card")).toBeNull();
    expect(screen.queryByTestId("domain-analysis")).toBeNull();
    expect(screen.queryByTestId("action-plan")).toBeNull();
    expect(screen.getByTestId("relationship-guidance").textContent).toContain("Giữ nhịp hỗ trợ đã có");
    expect(screen.getByTestId("relationship-guidance").textContent).toContain("Giữ nhịp trao đổi đều");
    expect(screen.getByTestId("relationship-guidance").textContent).toContain("Giúp hai người dễ phối hợp hơn");
    expect(screen.getByTestId("guidance-scope")).toBeTruthy();
    expect(screen.queryByText("Ưu tiên cao")).toBeNull();
    expect(screen.queryByText(/decision_trace/)).toBeNull();
  });

  it("10-12 adapter never invents score or grade", () => {
    const view = adaptMarriageView(consultation, report, warnings);
    expect(view.score).toBeNull();
    expect(view.grade).toBeNull();
    expect(FORBIDDEN_SCORE_PATTERN.test(JSON.stringify(view))).toBe(false);
  });

  it("renders an explainable structural score when the API provides one", () => {
    const scoredConsultation: MarriageConsultationDto = {
      ...consultation,
      score: 72.4,
      grade: "B",
      domain_scores: [
        { domain: "five_elements", score: 78, weight: 20, available: true },
        { domain: "stem_branch", score: 66, weight: 18, available: true },
        { domain: "children", score: null, weight: 4, available: false },
      ],
    };
    const scoredReport: MarriageReportDto = { ...report, score: 72.4, grade: "B" };
    const view = adaptMarriageView(scoredConsultation, scoredReport, []);

    render(<ResultView view={view} />);

    expect(screen.getByTestId("overall-score").textContent).toContain("72.4/100");
    expect(screen.getByTestId("overall-grade").textContent).toContain("B");
    expect(screen.getByTestId("domain-scores").textContent).toContain("Ngũ hành");
    expect(screen.getByTestId("domain-scores").textContent).not.toContain("Con cái");
  });

  it("renders the auditable comparison matrix and switches sections", () => {
    const matrixConsultation: MarriageConsultationDto = {
      ...consultation,
      compatibility_matrix: {
        version: "marriage.compatibility_matrix.v1@1.0.0",
        sections: [
          {
            key: "useful_god",
            title: "Ngũ Hành và Dụng/Hỷ thần",
            description: "Đối chiếu nhu cầu và phần người kia có.",
            rows: [
              {
                key: "a_to_b",
                label: "Người Nữ bổ trợ Người Nam",
                value_a: "Có: Hỏa 4",
                value_b: "Dụng: Hỏa; Hỷ: Mộc",
                relationship: "Bổ đúng nhu cầu: Hỏa.",
                status: "supportive",
                confidence: 0.82,
                basis: "Đối chiếu phân bố Ngũ Hành.",
                score_effect: null,
                available: true,
              },
            ],
          },
          {
            key: "cung_phi",
            title: "Cung Phi hai lá số",
            description: "Ghép từng cặp cung theo cùng trụ.",
            rows: [
              {
                key: "month",
                label: "Cung Phi trụ tháng",
                value_a: "Càn",
                value_b: "Đoài",
                relationship: "Sinh Khí: Quan hệ hỗ trợ.",
                status: "supportive",
                confidence: 0.82,
                basis: "Tra ma trận Du Niên 8×8.",
                score_effect: 2,
                available: true,
              },
            ],
          },
        ],
      },
    };
    const view = adaptMarriageView(matrixConsultation, report, []);

    render(<ResultView view={view} />);

    expect(screen.getByTestId("compatibility-matrix").textContent).toContain("Bổ đúng nhu cầu: Hỏa");
    fireEvent.click(screen.getByRole("tab", { name: "Cung Phi hai lá số" }));
    expect(screen.getByTestId("matrix-section-cung_phi").textContent).toContain("Càn");
    expect(screen.getByTestId("matrix-section-cung_phi").textContent).toContain("Đoài");
    expect(screen.getByTestId("matrix-section-cung_phi").textContent).toContain("Sinh Khí");
    expect(screen.getByTestId("matrix-section-cung_phi").textContent).toContain("Ảnh hưởng kỹ thuật: +2");
  });

  it("21 customer mode hides technical ids", () => {
    const view = adaptMarriageView(consultation, report, warnings);
    expect(FORBIDDEN_ID_PATTERN.test(JSON.stringify(view))).toBe(false);
  });

  it("22 customer receives one unified report without an expert seam", async () => {
    mockApi();
    render(<MarriageConsultingPage />);
    fillValidForm();
    fireEvent.submit(screen.getByTestId("marriage-form"));
    await waitFor(() => expect(screen.getByTestId("marriage-result")).toBeTruthy());
    expect(screen.queryByTestId("expert-mode")).toBeNull();
    expect(screen.queryByTestId("expert-trace")).toBeNull();
    expect(screen.getByTestId("relationship-guidance")).toBeTruthy();
    expect(vi.mocked(fetch).mock.calls.some(([input]) => String(input).includes("expert=true"))).toBe(false);
  });

  it("24 error rendering is customer-safe and retryable", async () => {
    mockApi({ fail: true, retryable: true });
    render(<MarriageConsultingPage />);
    fillValidForm();
    fireEvent.submit(screen.getByTestId("marriage-form"));
    const alert = await screen.findByTestId("error-state");
    expect(alert.textContent).toContain("Không thể hoàn tất phân tích lúc này");
    expect(alert.textContent).not.toContain("Traceback");
    expect(screen.getByTestId("retry-analysis")).toBeTruthy();
  });

  it("B07B fetch rejection exits loading with a controlled error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.reject(new TypeError("Failed to fetch"))),
    );
    render(<MarriageConsultingPage />);
    fillValidForm();
    fireEvent.submit(screen.getByTestId("marriage-form"));
    const alert = await screen.findByTestId("error-state");
    expect(alert.textContent).toContain("Không thể hoàn tất phân tích lúc này");
    expect(screen.queryByTestId("loading-state")).toBeNull();
    expect(screen.getByTestId("retry-analysis")).toBeTruthy();
    const post = vi.mocked(fetch).mock.calls.find((call) => String(call[1]?.method) === "POST");
    expect(String(post?.[0])).not.toBe("http://127.0.0.1/backend/api/v1/consulting/marriage");
    expect(String(post?.[0])).toContain("/backend/api/v1/consulting/marriage");
  });

  it("25 mobile layout stacks people via CSS", () => {
    const here = dirname(fileURLToPath(import.meta.url));
    const css = readFileSync(resolve(here, "../../static/css/marriage_consulting.css"), "utf8");
    expect(css).toContain("grid-template-columns: minmax(0, 1fr) minmax(0, 1fr)");
    expect(css).toContain("@media (max-width: 768px)");
    expect(css).toContain(".mc-people");
  });

  it("26 keyboard and accessibility basics", () => {
    render(<MarriageConsultingPage />);
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe(PRODUCT_TITLE);
    expect(screen.getByTestId("person-a-panel").querySelector("label")).toBeTruthy();
    const date = screen.getByLabelText("Ngày sinh dương lịch", { selector: "#person-a-birth-date" });
    expect(date.getAttribute("aria-describedby")).toBe("person-a-birth-date-error");
    expect(screen.getByTestId("submit-marriage").tagName).toBe("BUTTON");
  });

  it("27 existing three destinations stay; Marriage remains the last primary item", () => {
    expect(APP_NAV_ITEMS.slice(0, 3).map((item) => item.href)).toEqual([
      "/good-date",
      "/choose-date",
      "/analyze",
    ]);
    expect(APP_NAV_ITEMS).toHaveLength(5);
    expect(APP_NAV_ITEMS[3]).toEqual({
      id: "number-energy",
      label: "Tư vấn năng lượng số",
      href: "/number-energy",
    });
    expect(APP_NAV_ITEMS[4]).toEqual({
      id: "marriage-consulting",
      label: "Tư vấn hôn nhân",
      href: "/marriage-consulting",
    });
  });
});
