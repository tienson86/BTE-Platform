export type GoldenWealthStage = {
  id: "WF-01" | "WF-02" | "WF-03" | "WF-04";
  label: string;
  headline: string;
  evidence: string;
  interaction: string;
  narrative: string;
};

export const GOLDEN_WEALTH_STAGES: readonly GoldenWealthStage[] = [
  {
    id: "WF-01",
    label: "Tài vận",
    headline: "Có Thiên Y",
    evidence: "27 · 86",
    interaction: "",
    narrative: "Dãy xuất hiện hai điểm Thiên Y, vì vậy trục tài vận được hình thành rõ.",
  },
  {
    id: "WF-02",
    label: "Tài từ đâu?",
    headline: "Quý nhân & cơ hội",
    evidence: "827",
    interaction: "Sinh Khí → Thiên Y",
    narrative: "Quý nhân, quan hệ hoặc cơ hội có khả năng dẫn tới tài vận.",
  },
  {
    id: "WF-03",
    label: "Tài đi đâu?",
    headline: "Sự nghiệp & lập nghiệp",
    evidence: "278",
    interaction: "Thiên Y → Diên Niên",
    narrative: "Nguồn lực có xu hướng được đưa vào công việc, kinh doanh hoặc phát triển sự nghiệp.",
  },
  {
    id: "WF-04",
    label: "Hậu vận",
    headline: "Thiên Y",
    evidence: "786",
    interaction: "Diên Niên → Thiên Y",
    narrative:
      "Phần cuối dãy quy về Thiên Y. Diên Niên đứng trước cho thấy năng lực và công việc tiếp tục là nguồn dẫn tới tài vận.",
  },
];

export const GOLDEN_WEALTH_STORY = [
  "Quý nhân & cơ hội",
  "Tài",
  "Sự nghiệp",
  "Tài",
] as const;

export const GOLDEN_WEALTH_SYNTHESIS =
  "Dòng tài vận của dãy đi theo hướng: quý nhân và cơ hội mở đường, nguồn lực được đưa vào sự nghiệp, và phần cuối lại quy về khả năng tạo Tài từ chính năng lực nghề nghiệp.";
