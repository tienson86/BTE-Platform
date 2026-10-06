import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { BusinessConsultingPage } from "../../src/features/business_consulting/BusinessConsultingPage";
import { toConsultationBody, validateOccupation, validatePerson } from "../../src/features/business_consulting/request";
import { adaptBusinessView } from "../../src/features/business_consulting/adapter";
import { ResultView } from "../../src/features/business_consulting/ResultView";
import type { BusinessReportDto, BusinessScoreAudit } from "../../src/features/business_consulting/types";
import type { MarriageConsultationDto, MarriageMatrixRowDto } from "../../src/features/marriage_consulting/types";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

const consultation = {
  consultation_id: "BC-TEST-01",
  status: "SUCCESS",
  person_a: { display_name: "An", gender: "male" },
  person_b: { display_name: "Binh", gender: "female" },
  overall_state: "mixed",
  score: null,
  grade: null,
  confidence: { level: "high", overall: 0.82 },
  limitations: [],
  headline: "Có thể hợp tác nếu phân vai rõ",
};

const report = {
  consultation_id: "BC-TEST-01",
  score: null,
  grade: null,
  sections: [
    {
      section_id: "identity",
      title: "Hồ sơ",
      summary: "An và Binh",
      blocks: [],
    },
    {
      section_id: "compatibility_hero",
      title: "Tương hợp tổng thể",
      summary: "Có thể hợp tác nếu phân vai rõ",
      blocks: [
        {
          block_id: "hero-summary",
          kind: "summary",
          title: null,
          body: "Hai người có điểm hỗ trợ nhưng cần thống nhất vai trò và tài chính.",
          semantic_key: null,
          state: "mixed",
          domain: null,
        },
      ],
    },
    {
      section_id: "conclusion",
      title: "Kết luận",
      summary: "Có thể hợp tác nếu phân vai rõ",
      blocks: [
        {
          block_id: "conclusion-opinion",
          kind: "paragraph",
          title: null,
          body: "Nên hợp tác theo vai trò rõ ràng, có quy ước vốn và lợi nhuận.",
          semantic_key: null,
          state: "mixed",
          domain: null,
        },
      ],
    },
  ],
};

const businessScore: BusinessScoreAudit = {
  model_version: "business.compatibility.v1", score: 79.2, coverage: 100, confidence: 0.82,
  provisional: false, recommendation_key: "recommended", recommendation: "Có thể hợp tác",
  advice: "Kiểm chứng năng lực, uy tín và thống nhất vốn góp trước khi triển khai.", reasons: [],
  groups: [
    { key: "useful_god", title: "Dụng thần và Ngũ Hành", configured_weight: 35, effective_weight: 35, score: 74, contribution: 25.9, confidence: 0.82, scored_rows: 2, total_rows: 2, explanation: "Chấm hai chiều bổ trợ." },
    { key: "pattern", title: "Mệnh Cục", configured_weight: 0, effective_weight: 0, score: null, contribution: 0, confidence: 0, scored_rows: 0, total_rows: 1, explanation: "Chỉ dùng làm bối cảnh; không quy đổi thành điểm." },
  ],
  methodology: "Điểm nhóm lấy trung bình theo độ tin cậy dữ liệu.",
  disclaimer: "Điểm tương hợp Bát Tự là chỉ số tham khảo, không phải phần trăm thành công hoặc lợi nhuận.",
};
const scoredReport: BusinessReportDto = {
  ...report, metadata: { consultation_kind: "business" }, business_score: businessScore,
  sections: [...report.sections.filter((section) => section.section_id !== "conclusion"), {
    section_id: "conclusion", title: "Kết luận hợp tác", summary: null,
    blocks: [
      { block_id: "conclusion-opinion", kind: "paragraph", title: "Nhận định chung", body: "Có thể hợp tác. Điểm tương hợp Bát Tự: 79.2/100.", semantic_key: null, state: null, domain: null },
      { block_id: "conclusion-recommendation", kind: "paragraph", title: "Khuyến nghị", body: businessScore.advice, semantic_key: null, state: null, domain: null },
    ],
  }],
};

function matrixRow(key: string, label: string, status = "supportive"): MarriageMatrixRowDto {
  return {
    key, label, status, available: true, confidence: 0.82,
    value_a: "Giáp · Dương Mộc", value_b: "Bính · Dương Hỏa",
    relationship: "Có quan hệ tương sinh.", basis: "Đối chiếu từ hai lá số.", score_effect: 3,
  };
}

const evidenceConsultation: MarriageConsultationDto = {
  ...consultation,
  score: 78,
  grade: "B",
  compatibility_matrix: {
    version: "test",
    sections: [
      { key: "useful_god", title: "Ngũ Hành và Dụng/Hỷ thần", description: "Nhu cầu hai lá số", rows: [matrixRow("a_to_b", "Người Nữ bổ trợ Người Nam"), matrixRow("b_to_a", "Người Nam bổ trợ Người Nữ", "pressured")] },
      { key: "cung_phi", title: "Cung Phi hai lá số", description: "Cung bản mệnh và từng trụ", rows: [matrixRow("personal", "Cung Phi bản mệnh"), { ...matrixRow("hour", "Cung Phi trụ giờ"), available: false, status: "unavailable", confidence: 0, score_effect: null }] },
      { key: "structure", title: "Nhật Chủ và cấu trúc Bát Tự", description: "Can Chi và Mệnh Cục", rows: [matrixRow("day_master", "Nhật Chủ"), matrixRow("stem_branch_1", "Thiên Can hợp"), matrixRow("pattern", "Mệnh Cục", "reference"), matrixRow("ten_gods_a_to_b", "Vai trò Nữ → Nam")] },
      { key: "married_life", title: "Đời sống sau kết hôn", description: "", rows: [matrixRow("children", "Phối hợp nuôi dạy con")] },
    ],
  },
};

function envelope<T>(data: T) {
  return { status: "SUCCESS", data, warnings: [], errors: [] };
}

function mockApi(result: MarriageConsultationDto = consultation): void {
  vi.stubGlobal(
    "fetch",
    vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/business/history")) return jsonResponse(envelope({ items: [], next_cursor: null }));
      if (init?.method === "POST") {
        const body = JSON.parse(String(init.body || "{}"));
        expect(body.person_a.gender).toBe("male");
        expect(body.person_b.gender).toBe("female");
        expect(body.request_meta.client).toContain("occupation=technology");
        expect(body.options.include_score).toBe(true);
        return jsonResponse(envelope(result), 201);
      }
      if (url.includes("/report")) {
        return jsonResponse(envelope(report));
      }
      return jsonResponse(envelope(result));
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
  fireEvent.change(screen.getByTestId("occupation-select"), { target: { value: "technology" } });
  fireEvent.change(screen.getByLabelText("Họ tên", { selector: "#person-a-full-name" }), { target: { value: "An" } });
  fireEvent.change(screen.getByLabelText("Giới tính", { selector: "#person-a-gender" }), { target: { value: "male" } });
  fireEvent.change(screen.getByLabelText("Ngày sinh dương lịch", { selector: "#person-a-birth-date" }), {
    target: { value: "21011987" },
  });
  fireEvent.change(screen.getByLabelText("Họ tên", { selector: "#person-b-full-name" }), { target: { value: "Binh" } });
  fireEvent.change(screen.getByLabelText("Giới tính", { selector: "#person-b-gender" }), { target: { value: "female" } });
  fireEvent.change(screen.getByLabelText("Ngày sinh dương lịch", { selector: "#person-b-birth-date" }), {
    target: { value: "15051990" },
  });
}

describe("Business Consulting UI", () => {
  it("renders occupation and gender controls", () => {
    render(<BusinessConsultingPage />);
    expect(screen.getByTestId("business-title").textContent).toContain("Tư vấn hợp tác");
    expect(screen.getByTestId("occupation-select")).toBeTruthy();
    expect(screen.getByLabelText("Giới tính", { selector: "#person-a-gender" })).toBeTruthy();
    expect(screen.getByLabelText("Giới tính", { selector: "#person-b-gender" })).toBeTruthy();
  });

  it("validates required occupation and gender", () => {
    render(<BusinessConsultingPage />);
    fireEvent.submit(screen.getByTestId("business-form"));
    expect(screen.getByTestId("error-state").textContent).toContain("Thiếu thông tin bắt buộc");
    expect(screen.getByTestId("business-context").textContent).toContain("Vui lòng chọn ngành/nghề");
    expect(validateOccupation("technology")).toBe("");
    expect(validatePerson({ full_name: "", gender: "male", birth_date: "21/01/1987", birth_time: "", birth_place: "" })).toEqual({});
  });

  it("posts selected genders and occupation metadata", async () => {
    mockApi();
    render(<BusinessConsultingPage />);
    fillValidForm();
    fireEvent.submit(screen.getByTestId("business-form"));
    await waitFor(() => expect(screen.getByTestId("business-result")).toBeTruthy());
    const body = toConsultationBody(
      { full_name: "An", gender: "male", birth_date: "21/01/1987", birth_time: "", birth_place: "" },
      { full_name: "Binh", gender: "female", birth_date: "15/05/1990", birth_time: "", birth_place: "" },
      "technology",
    );
    expect(body?.person_a.birth_date).toBe("1987-01-21");
    expect(body?.request_meta?.client).toContain("occupation=technology");
    expect(screen.getByTestId("business-occupation").textContent).toContain("Công nghệ - phần mềm");
  });

  it("shows the same structural evidence across tabs using partner names and business guidance", async () => {
    mockApi(evidenceConsultation);
    render(<BusinessConsultingPage />);
    fillValidForm();
    fireEvent.submit(screen.getByTestId("business-form"));
    await waitFor(() => expect(screen.getByTestId("compatibility-matrix")).toBeTruthy());
    expect(screen.getByTestId("matrix-section-useful_god").textContent).toContain("An bổ trợ Binh");
    expect(screen.queryByText("Người Nữ bổ trợ Người Nam")).toBeNull();
    for (const key of ["useful_god", "cung_phi", "stem_branch", "pattern", "day_master"]) {
      expect(screen.getByTestId(`assessment-card-${key}`)).toBeTruthy();
    }
    fireEvent.click(screen.getByRole("tab", { name: "Cung Phi hai lá số" }));
    expect(screen.getByTestId("matrix-section-cung_phi").textContent).toContain("Cung Phi trụ giờ");
    expect(screen.getByTestId("matrix-section-cung_phi").textContent).toContain("Thiếu dữ liệu");
    fireEvent.click(screen.getByRole("tab", { name: "Nhật Chủ và cấu trúc Bát Tự" }));
    const structure = screen.getByTestId("matrix-section-structure");
    expect(structure.textContent).toContain("Nhật Chủ");
    expect(structure.textContent).toContain("Thiên Can hợp");
    expect(structure.textContent).toContain("Mệnh Cục");
    expect(structure.textContent).toContain("Vai trò An → Binh");
    expect(screen.getByTestId("conclusion-recommendation").textContent).toContain("Công nghệ - phần mềm");
    expect(screen.queryByText("Đời sống sau kết hôn")).toBeNull();
  });

  it("keeps calculated evidence unchanged and does not present the marriage score as a business score", () => {
    const view = adaptBusinessView(evidenceConsultation, report, [], "Công nghệ - phần mềm");
    const row = view.compatibilityMatrix[0].rows[0];
    expect(row.personA).toBe(evidenceConsultation.compatibility_matrix!.sections[0].rows[0].value_a);
    expect(row.relationship).toBe(evidenceConsultation.compatibility_matrix!.sections[0].rows[0].relationship);
    expect(row.basis).toBe("Đối chiếu từ hai lá số.");
    expect(view.assessmentCards[0].answer).toContain("Có cả bổ trợ");
    expect(view.assessmentCards[3].answer).toContain("tham khảo");
    expect(view.score).toBeNull();
    expect(view.businessScore).toBeNull();
    expect(view.grade).toBeNull();
    expect(view.compatibilityMatrix).toHaveLength(3);
  });

  it("displays the backend business score, advice and auditable breakdown instead of the marriage score", () => {
    const view = adaptBusinessView(evidenceConsultation, scoredReport, [], "Sản xuất");
    expect(view.score).toBeNull();
    expect(view.businessScore).toEqual(businessScore);
    render(<ResultView view={view} occupation="Sản xuất" />);
    expect(screen.getByTestId("business-score-value").textContent).toContain("79,2");
    expect(screen.getByTestId("business-score-recommendation").textContent).toBe("Có thể hợp tác");
    expect(screen.getByTestId("conclusion-score").textContent).toContain("79,2 / 100");
    expect(screen.getByTestId("conclusion-recommendation").textContent).toContain(businessScore.advice);
    expect(screen.getByRole("table", { name: "Đóng góp của từng nhóm đối chiếu" }).textContent).toContain("35%");
    expect(screen.getAllByText("Không chấm")).toHaveLength(2);
    expect(screen.getAllByText(businessScore.disclaimer)).toHaveLength(2);
  });

  it("marks partial scores and does not display a missing score as zero", () => {
    const partial = { ...businessScore, score: null, coverage: 35, provisional: true, recommendation_key: "insufficient", recommendation: "Chưa đủ dữ liệu để khuyến nghị hợp tác", reasons: ["Bổ sung nhóm lõi còn thiếu."] };
    const view = adaptBusinessView(evidenceConsultation, { ...scoredReport, business_score: partial }, [], "Sản xuất");
    render(<ResultView view={view} occupation="Sản xuất" />);
    expect(screen.getByTestId("business-score-value").textContent).toBe("Chưa đủ dữ liệu");
    expect(screen.getByTestId("conclusion-score").textContent).toContain("Chưa đủ dữ liệu để chấm điểm");
    expect(screen.queryByRole("meter")).toBeNull();
    expect(screen.getAllByText("Bổ sung nhóm lõi còn thiếu.")).toHaveLength(2);
  });

  it("labels provisional points without changing their value", () => {
    const view = adaptBusinessView(evidenceConsultation, { ...scoredReport, business_score: { ...businessScore, provisional: true, coverage: 98 } }, [], "Sản xuất");
    render(<ResultView view={view} occupation="Sản xuất" />);
    expect(screen.getByText("Điểm tạm tính")).toBeTruthy();
    expect(screen.getByTestId("conclusion-score").textContent).toContain("79,2 / 100 (tạm tính)");
  });

  it("does not infer support from unavailable evidence or fabricate missing matrix rows", () => {
    const missing = adaptBusinessView(consultation, report, [], "Sản xuất");
    expect(missing.compatibilityMatrix).toEqual([]);
    expect(missing.assessmentCards.every((card) => card.answer === "Chưa đủ dữ liệu để đối chiếu")).toBe(true);
    expect(missing.actions).toEqual([]);
    const partial = structuredClone(evidenceConsultation);
    partial.person_a.gender = "male";
    partial.person_b.gender = "male";
    for (const section of partial.compatibility_matrix!.sections) {
      for (const row of section.rows) row.available = false;
    }
    const view = adaptBusinessView(partial, report, [], "Sản xuất");
    expect(view.assessmentCards.every((card) => card.answer === "Chưa đủ dữ liệu để đối chiếu")).toBe(true);
    expect(view.finalOpinion.overall).toContain("chưa đủ dữ liệu");
    expect(view.compatibilityMatrix[0].rows[0].label).toBe("An bổ trợ Binh");
  });

  it("saves once, reloads history, and reopens the same occupation without creating a new consultation", async () => {
    let saved = false;
    const item = { consultation_id: consultation.consultation_id, display_identity: "An / Binh", created_at: "2026-10-05T02:00:00Z", saved_at: "2026-10-05T02:10:00Z", occupation: "technology", occupation_label: "Công nghệ - phần mềm" };
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/business/history")) return jsonResponse(envelope({ items: saved ? [item] : [], next_cursor: null }));
      if (url.endsWith("/save")) { saved = true; return jsonResponse(envelope(item)); }
      if (init?.method === "POST") return jsonResponse(envelope(evidenceConsultation), 201);
      if (url.includes("/report")) return jsonResponse(envelope(scoredReport));
      return jsonResponse(envelope({ ...evidenceConsultation, business_context: { ...item, saved_at: saved ? item.saved_at : null } }));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<BusinessConsultingPage />);
    fillValidForm(); fireEvent.submit(screen.getByTestId("business-form"));
    await screen.findByRole("button", { name: "Lưu hồ sơ" });
    fireEvent.click(screen.getByRole("button", { name: "Lưu hồ sơ" }));
    await screen.findByRole("button", { name: "Đã lưu hồ sơ" });
    expect(screen.getByTestId("business-history").textContent).toContain("An / Binh");
    fireEvent.click(screen.getByRole("button", { name: "Tư vấn hợp tác mới" }));
    expect(screen.getByTestId("business-form")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Mở hồ sơ" }));
    await screen.findByRole("button", { name: "Đã lưu hồ sơ" });
    expect(screen.getByTestId("business-occupation").textContent).toContain("Công nghệ - phần mềm");
    expect(screen.getByTestId("business-score-value").textContent).toContain("79,2");
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST" && init.body)).toHaveLength(1);
    expect(fetchMock.mock.calls.filter(([input]) => String(input).endsWith("/save"))).toHaveLength(1);
  });

  it("downloads actual PDF and DOCX blobs using the selected profile id", async () => {
    const revoke = vi.fn(); const create = vi.fn(() => "blob:business-report");
    const NativeURL = URL;
    vi.stubGlobal("URL", class extends NativeURL { static createObjectURL = create; static revokeObjectURL = revoke; });
    const clicks: string[] = [];
    vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(function (this: HTMLAnchorElement) { clicks.push(this.download); });
    mockApi(evidenceConsultation);
    const baseFetch = globalThis.fetch;
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/export/")) {
        const format = url.endsWith("/pdf") ? "pdf" : "docx";
        return new Response(format === "pdf" ? "%PDF-1.4" : "PK-DOCX", { headers: { "Content-Type": format === "pdf" ? "application/pdf" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "Content-Disposition": `attachment; filename="BTE_TuVanHopTac.${format}"` } });
      }
      return baseFetch(input, init);
    }));
    render(<BusinessConsultingPage />); fillValidForm(); fireEvent.submit(screen.getByTestId("business-form"));
    await screen.findByRole("button", { name: "Tải PDF" });
    fireEvent.click(screen.getByRole("button", { name: "Tải PDF" }));
    await waitFor(() => expect(clicks).toContain("BTE_TuVanHopTac.pdf"));
    await waitFor(() => expect((screen.getByRole("button", { name: "Tải DOCX" }) as HTMLButtonElement).disabled).toBe(false));
    fireEvent.click(screen.getByRole("button", { name: "Tải DOCX" }));
    await waitFor(() => expect(clicks).toContain("BTE_TuVanHopTac.docx"));
    expect(create).toHaveBeenCalledTimes(2);
    expect(vi.mocked(fetch).mock.calls.some(([input]) => String(input).includes(`/business/${consultation.consultation_id}/export/pdf`))).toBe(true);
    await new Promise((resolve) => setTimeout(resolve, 1100));
    expect(revoke).toHaveBeenCalledTimes(2);
  });

  it("reports failed saving and rejects an error response instead of downloading it", async () => {
    mockApi(evidenceConsultation);
    const baseFetch = globalThis.fetch;
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith("/save") || url.includes("/export/")) return jsonResponse({ status: "FAILED", data: null, errors: [] }, 500);
      return baseFetch(input, init);
    }));
    render(<BusinessConsultingPage />); fillValidForm(); fireEvent.submit(screen.getByTestId("business-form"));
    await screen.findByRole("button", { name: "Lưu hồ sơ" });
    fireEvent.click(screen.getByRole("button", { name: "Lưu hồ sơ" }));
    await screen.findByText("Chưa lưu được hồ sơ hợp tác. Vui lòng thử lại.");
    expect(screen.queryByRole("button", { name: "Đã lưu hồ sơ" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "Tải PDF" }));
    await screen.findByText("Không tải được báo cáo hợp tác. Vui lòng thử lại.");
    expect((screen.getByRole("button", { name: "Tải PDF" }) as HTMLButtonElement).disabled).toBe(false);
  });
});
