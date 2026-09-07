import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { MarriageConsultingPage } from "../../src/features/marriage_consulting/MarriageConsultingPage";
import { adaptMarriageView } from "../../src/features/marriage_consulting/adapter";
import { FORBIDDEN_ID_PATTERN, FORBIDDEN_SCORE_PATTERN } from "../../src/features/marriage_consulting/labels";
import type { MarriageConsultationDto, MarriageReportDto, MarriageWarning } from "../../src/features/marriage_consulting/types";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

const consultation: MarriageConsultationDto = {
  consultation_id: "MC-19870121-B08G01",
  status: "SUCCESS",
  person_a: { display_name: "Nguyễn Thị Ánh", gender: "female" },
  person_b: { display_name: "Trần Văn Bình".padEnd(80, "n"), gender: "male" },
  overall_state: "mixed",
  score: null,
  grade: null,
  confidence: { level: "medium", overall: 0.64 },
  limitations: ["birth_time_unknown"],
  headline: "Có một số điểm cần điều chỉnh",
};

const report: MarriageReportDto = {
  consultation_id: "MC-19870121-B08G01",
  score: null,
  grade: null,
  sections: [
    {
      section_id: "identity",
      title: "Hồ sơ cặp đôi",
      summary: "Nguyễn Thị Ánh và Trần Văn Bình",
      blocks: [{ block_id: "identity-header", kind: "headline", title: "Hồ sơ", body: "Nguyễn Thị Ánh và Trần Văn Bình", semantic_key: null, state: null, domain: null }],
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
          body: "Ưu tiên cao. Giữ nhịp trao đổi đều.",
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
      blocks: [{ block_id: "c1", kind: "confidence", title: null, body: "Giờ sinh chưa đủ nên độ tin cậy bị giới hạn.", semantic_key: null, state: null, domain: null }],
    },
    {
      section_id: "conclusion",
      title: "Kết luận",
      summary: "Có một số điểm cần điều chỉnh",
      blocks: [{ block_id: "k1", kind: "paragraph", title: null, body: "Có một số điểm cần điều chỉnh.", semantic_key: null, state: "mixed", domain: null }],
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
  { code: "BIRTH_TIME_UNKNOWN", description: "Giờ sinh chưa rõ. Đây là giới hạn dữ liệu, không phải rủi ro hôn nhân.", affected_domain: null },
  { code: "DOMAIN_UNAVAILABLE", description: "This domain does not have enough structural data.", affected_domain: "family" },
];

function envelope<T>(data: T) {
  return { status: "SUCCESS" as const, data, warnings, errors: [] };
}

describe("TV1-B08 Marriage Consulting UI golden presentation", () => {
  it("adapter keeps score/grade null and omits empty unavailable domain cards", () => {
    const view = adaptMarriageView(consultation, report, warnings);
    expect(view.score).toBeNull();
    expect(view.grade).toBeNull();
    expect(view.domains.map((item) => item.domain)).toEqual(["five_elements", "stem_branch"]);
    expect(view.domains.some((item) => item.domain === "family")).toBe(false);
    expect(view.domains.some((item) => item.domain === "interaction")).toBe(false);
    expect(FORBIDDEN_SCORE_PATTERN.test(JSON.stringify(view))).toBe(false);
    expect(FORBIDDEN_ID_PATTERN.test(JSON.stringify({ ...view, expertTrace: null }))).toBe(false);
    expect(view.personAName).toContain("Nguyễn");
  });

  it("renders unicode names, warnings, actions, and no fake score", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (init?.method === "POST") {
          return new Response(JSON.stringify(envelope(consultation)), {
            status: 201,
            headers: { "Content-Type": "application/json" },
          });
        }
        if (url.includes("/report")) {
          return new Response(JSON.stringify(envelope(report)), {
            status: 200,
            headers: { "Content-Type": "application/json" },
          });
        }
        return new Response(JSON.stringify(envelope(consultation)), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        });
      }),
    );
    render(<MarriageConsultingPage />);
    fireEvent.change(screen.getByLabelText("Họ tên", { selector: "#person-a-full-name" }), {
      target: { value: "Nguyễn Thị Ánh" },
    });
    fireEvent.click(screen.getAllByLabelText("Nữ")[0]!);
    fireEvent.change(screen.getByLabelText("Ngày sinh dương lịch", { selector: "#person-a-birth-date" }), {
      target: { value: "21011987" },
    });
    fireEvent.change(screen.getByLabelText("Họ tên", { selector: "#person-b-full-name" }), {
      target: { value: "Trần Văn Bình" },
    });
    fireEvent.click(screen.getAllByLabelText("Nam")[1]!);
    fireEvent.change(screen.getByLabelText("Ngày sinh dương lịch", { selector: "#person-b-birth-date" }), {
      target: { value: "15051990" },
    });
    fireEvent.submit(screen.getByTestId("marriage-form"));
    await waitFor(() => expect(screen.getByTestId("marriage-result")).toBeTruthy());
    expect(screen.getByTestId("couple-names").textContent).toContain("Nguyễn");
    expect(screen.queryByText(/\/100/)).toBeNull();
    expect(screen.queryByText(/Grade/)).toBeNull();
    expect(screen.getByTestId("action-plan")).toBeTruthy();
    expect(screen.getAllByTestId("warning-note").length).toBeGreaterThan(0);
    expect(screen.getByTestId("domain-analysis").querySelector('[data-domain="family"]')).toBeNull();
    expect(screen.getByTestId("expert-mode")).toBeTruthy();
    fireEvent.click(screen.getByTestId("expert-mode").querySelector("summary")!);
    expect(screen.queryByText(/82%/)).toBeNull();
  });
});
