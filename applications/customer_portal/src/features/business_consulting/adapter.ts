import { adaptMarriageView } from "../marriage_consulting/adapter";
import type {
  AssessmentCardVm,
  MarriageMatrixRowVm,
  MarriageViewModel,
  MarriageWarning,
} from "../marriage_consulting/types";
import { HERO_EYEBROW, PERSON_A_LABEL, PERSON_B_LABEL } from "./labels";
import type { BusinessConsultationDto } from "./api";
import type { BusinessReportDto, BusinessViewModel } from "./types";

const GROUPS = [
  { key: "useful_god", title: "Dụng thần và Ngũ Hành", meaning: "Xem người này có bổ sung đúng hành người kia cần, hay đồng thời kích hoạt hành bất lợi.", guidance: "Đối chiếu phần bổ trợ với năng lực thực tế để phân công công việc; nếu có áp lực hai chiều, thống nhất giới hạn trách nhiệm." },
  { key: "cung_phi", title: "Cung Phi", meaning: "Đối chiếu cung bản mệnh và cung từng trụ theo Du Niên; đây là chỉ báo phụ khi xem khả năng phối hợp.", guidance: "Đọc cùng Dụng thần và Can Chi khi cân nhắc cách phối hợp, không dùng riêng Cung Phi để quyết định góp vốn." },
  { key: "stem_branch", title: "Can Chi", meaning: "Các quan hệ hợp, xung, hình, hại và yếu tố cứu giải giúp lý giải phần đồng thuận hoặc ma sát giữa hai lá số.", guidance: "Thống nhất người quyết định cuối cùng, cách phản biện và quy trình giải quyết bất đồng trong công việc." },
  { key: "pattern", title: "Mệnh Cục", meaning: "Mệnh Cục cung cấp bối cảnh của từng lá số; giống hoặc khác mệnh cục chưa đủ để kết luận hợp hay khắc.", guidance: "Dùng bối cảnh này để trao đổi về cách làm việc, rồi kiểm chứng bằng kinh nghiệm và hiệu quả công việc thực tế." },
  { key: "day_master", title: "Nhật Chủ", meaning: "Quan hệ sinh–khắc và âm dương của Nhật Chủ được đọc cùng Dụng thần và các quan hệ Can Chi.", guidance: "Thỏa thuận mức tự chủ của mỗi người và cơ chế kiểm soát chéo khi ra quyết định chung." },
] as const;

function rowsFor(key: string, view: MarriageViewModel): MarriageMatrixRowVm[] {
  if (key === "useful_god" || key === "cung_phi") {
    return view.compatibilityMatrix.find((section) => section.key === key)?.rows || [];
  }
  const rows = view.compatibilityMatrix.find((section) => section.key === "structure")?.rows || [];
  return rows.filter((row) => key === "stem_branch" ? row.key.startsWith("stem_branch") : row.key === key);
}

function verdict(rows: MarriageMatrixRowVm[]): string {
  const available = rows.filter((row) => row.available && row.status !== "unavailable");
  if (!available.length) return "Chưa đủ dữ liệu để đối chiếu";
  const support = available.some((row) => row.status === "supportive");
  const pressure = available.some((row) => row.status === "pressured");
  if (available.some((row) => row.status === "mixed") || (support && pressure)) return "Có cả bổ trợ và điểm cần thỏa thuận";
  if (pressure) return "Có áp lực cần quản lý khi phối hợp";
  if (support) return "Có yếu tố hỗ trợ trong đối chiếu";
  if (available.every((row) => row.status === "reference")) return "Căn cứ tham khảo về bối cảnh hai lá số";
  return "Chưa có xu hướng bổ trợ hoặc áp lực nổi trội";
}

export function adaptBusinessView(
  consultation: BusinessConsultationDto,
  report: BusinessReportDto,
  warnings: MarriageWarning[],
  occupation: string,
): BusinessViewModel {
  const source = adaptMarriageView(consultation, report, warnings);
  const personAName = consultation.person_a.display_name || PERSON_A_LABEL;
  const personBName = consultation.person_b.display_name || PERSON_B_LABEL;
  const directionalLabels: Record<string, string> = {
    a_to_b: `${personAName} bổ trợ ${personBName}`,
    b_to_a: `${personBName} bổ trợ ${personAName}`,
    ten_gods_a_to_b: `Vai trò ${personAName} → ${personBName}`,
    ten_gods_b_to_a: `Vai trò ${personBName} → ${personAName}`,
  };
  const view = {
    ...source,
    personAName,
    personBName,
    // Reuse structural evidence, not the marriage-specific life domains or score.
    score: null,
    grade: null,
    scoreDomains: [],
    compatibilityMatrix: source.compatibilityMatrix
      .filter((section) => ["useful_god", "cung_phi", "structure"].includes(section.key))
      .map((section) => ({
        ...section,
        rows: section.rows.map((row) => ({ ...row, label: directionalLabels[row.key] || row.label })),
      })),
  };
  const cards: AssessmentCardVm[] = GROUPS.map((group) => {
    const rows = rowsFor(group.key, view);
    return {
      questionId: group.key,
      question: group.title,
      answer: verdict(rows),
      meaning: group.meaning,
      supportingFacts: rows.map((row) => `${row.label}: ${personAName} — ${row.personA}; ${personBName} — ${row.personB}. ${row.relationship} Cơ sở: ${row.basis}`),
      quickGuidance: rows.some((row) => row.available && row.status !== "unavailable") ? group.guidance : "Bổ sung dữ liệu lá số trước khi luận phần này.",
      confidence: "",
      limitations: [],
      technicalExplanation: "",
    };
  });
  const coreRows = ["useful_god", "stem_branch", "day_master"].flatMap((key) => rowsFor(key, view));
  const supportive = coreRows.find((row) => row.available && row.status === "supportive");
  const pressured = coreRows.find((row) => row.available && ["pressured", "mixed"].includes(row.status));
  const overall = `Đối chiếu nền tảng hợp tác: ${verdict(coreRows).toLocaleLowerCase("vi")}.`;
  return {
    ...view,
    businessScore: report.metadata?.consultation_kind === "business" ? report.business_score || null : null,
    heroEyebrow: HERO_EYEBROW,
    heroHeadline: overall,
    heroSummary: overall,
    executiveSummary: overall,
    assessmentCards: report.metadata?.consultation_kind === "business" ? source.assessmentCards : cards,
    unavailableNote: "Dẫn chứng hiện phản ánh tương tác giữa hai lá số. Mức phù hợp với ngành/nghề đã chọn cần được đánh giá thêm theo chuyên môn và điều kiện kinh doanh.",
    timingSummary: null,
    actions: report.metadata?.consultation_kind === "business" ? source.actions : cards.filter((card) => rowsFor(card.questionId, view).some((row) => row.available && row.status !== "unavailable"))
      .filter((card) => card.questionId !== "cung_phi")
      .map((card) => ({ key: card.questionId, title: `Phối hợp theo ${card.question}`, what: card.question, objective: card.quickGuidance, outcome: "", when: "", priority: "", priorityLabel: "" })),
    conclusion: overall,
    finalOpinion: report.metadata?.consultation_kind === "business" ? source.finalOpinion : {
      overall,
      strongestStrength: supportive ? `${supportive.label}: ${supportive.relationship}` : "Chưa có yếu tố hỗ trợ nổi trội đủ dữ liệu để kết luận.",
      mainAttention: pressured ? `${pressured.label}: ${pressured.relationship}` : "Cần đọc đầy đủ các hàng đối chiếu và phần thiếu dữ liệu trước khi quyết định hợp tác.",
      recommendation: `Trước khi hợp tác trong lĩnh vực ${occupation}, thống nhất vai trò, vốn góp, quyền quyết định, phân chia lợi ích và cách xử lý bất đồng; kiểm chứng bằng một giai đoạn làm việc thử.`,
    },
  };
}
