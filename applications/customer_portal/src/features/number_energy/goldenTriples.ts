export type TriplePriority = "featured" | "standard" | "compact";

export type GoldenTripleCard = {
  digits: string;
  sourceLabel: string;
  targetLabel: string;
  title: string;
  narrative: string;
  domains: string;
  priority: TriplePriority;
};

export const GOLDEN_PHONE_TRIPLES: readonly GoldenTripleCard[] = [
  {
    digits: "328",
    sourceLabel: "Họa Hại",
    targetLabel: "Sinh Khí",
    title: "Khẩu tài tốt",
    narrative:
      "Khả năng giao tiếp và diễn đạt là điểm mạnh của tổ hợp này. Lời nói có giá trị và dễ được người khác lắng nghe, tiếp nhận.",
    domains: "Giao tiếp · Công việc",
    priority: "standard",
  },
  {
    digits: "282",
    sourceLabel: "Sinh Khí",
    targetLabel: "Sinh Khí",
    title: "Quý nhân và cơ hội được tăng cường",
    narrative:
      "Sinh Khí được tiếp nối, làm nổi bật khả năng gặp người hỗ trợ, cơ hội và những mối quan hệ thuận lợi.",
    domains: "Quý nhân · Cơ hội",
    priority: "standard",
  },
  {
    digits: "827",
    sourceLabel: "Sinh Khí",
    targetLabel: "Thiên Y",
    title: "Quý nhân mang đến Tài vận",
    narrative: "Quý nhân, quan hệ hoặc cơ hội có khả năng dẫn tới tài vận.",
    domains: "Tài vận · Quý nhân",
    priority: "featured",
  },
  {
    digits: "278",
    sourceLabel: "Thiên Y",
    targetLabel: "Diên Niên",
    title: "Tài đi vào sự nghiệp",
    narrative:
      "Nguồn lực có xu hướng được đưa vào công việc, kinh doanh hoặc phát triển sự nghiệp.",
    domains: "Tài vận · Công việc",
    priority: "featured",
  },
  {
    digits: "787",
    sourceLabel: "Diên Niên",
    targetLabel: "Diên Niên",
    title: "Năng lực nghề nghiệp được tăng cường",
    narrative: "Diên Niên được tiếp nối, làm nổi bật năng lực làm việc, trách nhiệm và khả năng tổ chức.",
    domains: "Công việc · Năng lực",
    priority: "compact",
  },
  {
    digits: "878",
    sourceLabel: "Diên Niên",
    targetLabel: "Diên Niên",
    title: "Năng lực nghề nghiệp được tăng cường",
    narrative: "Diên Niên tiếp tục xuất hiện, cho thấy công việc và năng lực nghề nghiệp là chủ đề được duy trì rõ trong dãy.",
    domains: "Công việc · Năng lực",
    priority: "compact",
  },
  {
    digits: "786",
    sourceLabel: "Diên Niên",
    targetLabel: "Thiên Y",
    title: "Năng lực nghề nghiệp tạo Tài",
    narrative: "Tài vận chủ yếu đến từ năng lực làm việc, chuyên môn và sự nghiệp.",
    domains: "Tài vận · Công việc",
    priority: "featured",
  },
];
