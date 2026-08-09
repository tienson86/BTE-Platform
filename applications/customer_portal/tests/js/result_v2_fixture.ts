import type { CanonicalReportInput } from "../../src/features/result_v2/adapter/reportInput";

export const resultV2ReadyReport: CanonicalReportInput = {
  success: true,
  report_pipeline_version: "1.0.0",
  presentation: {
    identity: {
      full_name: "Nguyễn Văn An",
      headline: "Ưu tiên môi trường ổn định trước khi mở rộng trách nhiệm",
      one_line_summary: "Giai đoạn này nên củng cố năng lực cốt lõi rồi mới tăng tốc.",
      consultation_status: "ready",
    },
    summary: {
      bullets: [
        "Nên chọn công việc có nhịp độ rõ ràng và người dẫn dắt đáng tin.",
        "Giữ kỷ luật chi tiêu trước khi mở rộng đầu tư.",
        "Ưu tiên quan hệ cộng tác hơn cạnh tranh ngắn hạn.",
        "Giữ nhịp nghỉ ngơi đều đặn để duy trì sức bền.",
        "Ba tháng tới phù hợp để hoàn thiện hơn là bung sức.",
        "Dòng thừa sẽ bị cắt.",
      ],
    },
    recommendations: [
      {
        id: "rec-career-1",
        domain: "career",
        title: "Chọn môi trường có cấu trúc",
        reason: "Năng lực phát huy tốt hơn khi vai trò và kỳ vọng được nói rõ.",
        expected_result: "Giảm hao tổn và tăng độ tin cậy trong công việc.",
        action: "Lọc cơ hội theo mức rõ ràng của vai trò trước khi nhận thêm việc.",
        detail: "Trong 90 ngày, ghi lại ba tiêu chí môi trường rồi đối chiếu từng đề xuất.",
        priority: 1,
      },
      {
        id: "rec-wealth-1",
        domain: "wealth",
        title: "Giữ biên an toàn tiền mặt",
        reason: "Biến động thu nhập dễ làm lệch kế hoạch nếu không có đệm.",
        expected_result: "An tâm hơn khi ra quyết định lớn.",
        action: "Giữ một khoản dự phòng trước khi tăng chi đầu tư.",
        priority: 2,
      },
    ],
    warnings: [
      {
        title: "Tránh nhận quá nhiều việc cùng lúc",
        body: "Dồn trách nhiệm sẽ làm giảm chất lượng quyết định.",
        mitigation: "Chỉ nhận thêm việc khi ba ưu tiên hiện tại đã có nhịp ổn.",
        severity: "attention",
      },
    ],
    domains: {
      career: {
        available: true,
        intro: "Sự nghiệp cần nền tảng trước tăng tốc.",
        recommendation_ids: ["rec-career-1"],
        analysis_preview: "Cấu trúc lá số ủng hộ công việc có quy trình rõ.",
        analysis_detail: "Khi môi trường hỗn loạn, hiệu suất giảm rõ rệt.",
      },
      wealth: { available: true, recommendation_ids: ["rec-wealth-1"] },
      relationship: { available: false },
      health: { available: false },
      luck: { available: false },
    },
    charts: [
      {
        title: "Cân bằng ngũ hành",
        caption: "Biểu đồ minh họa phần hỗ trợ cho định hướng đã nêu.",
        asset_ref: "chart-balance",
        table: {
          headers: ["Nhóm", "Mức"],
          rows: [
            ["Ổn định", "Cao"],
            ["Biến động", "Trung"],
          ],
        },
      },
    ],
    technical: {
      calendar: "Dương lịch",
      pillars: "Giáp Tý · Ất Sửu · Bính Dần · Đinh Mão",
      timezone: "Múi giờ Việt Nam",
      schema: "1.0.0",
      ids: "HS-demo",
    },
    knowledge: [
      {
        title: "Nhật chủ",
        teaser: "Nhật chủ là trục nhận diện trong buổi tư vấn.",
        body: "Hiểu nhật chủ giúp đọc các lĩnh vực đời sống nhất quán hơn.",
      },
    ],
    appendix: {
      scope: "Buổi tư vấn này tập trung định hướng gần.",
      reread: "Nên đọc lại tóm tắt sau 90 ngày.",
      limits: "Không thay thế tư vấn y tế hoặc pháp lý.",
    },
    cta: {
      primary: { enabled: true },
      secondary: { enabled: true },
    },
  },
  canonical_report_artifact: {
    success: true,
    artifact_id: "art-1",
    mime_type: "application/json",
    metadata: { render_version: "1.0.0" },
    content: "<html>must-not-render</html>",
  },
};
