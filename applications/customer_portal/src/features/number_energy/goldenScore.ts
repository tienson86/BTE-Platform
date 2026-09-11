export type GoldenScoreDimension = {
  label: string;
  earned: number;
  max: number;
};

export type GoldenScoreReason = {
  title: string;
  copy: string;
};

export const GOLDEN_SCORE_TOTAL = "82 / 100";
export const GOLDEN_SCORE_GRADE = "TỐT";

export const GOLDEN_SCORE_NOTE =
  "Đây là điểm minh họa của bản dựng tĩnh, chưa phải điểm đã được đối chiếu khi hệ thống vận hành.";

export const GOLDEN_SCORE_BREAKDOWN: readonly GoldenScoreDimension[] = [
  { label: "Cấu trúc năng lượng", earned: 21, max: 25 },
  { label: "Dòng tài vận", earned: 22, max: 25 },
  { label: "Công việc & trợ lực", earned: 17, max: 20 },
  { label: "Ổn định & rủi ro", earned: 10, max: 15 },
  { label: "Năng lượng kết", earned: 12, max: 15 },
];

export const GOLDEN_SCORE_REASONS: readonly GoldenScoreReason[] = [
  {
    title: "Cấu trúc Cát giữ vai trò chủ đạo",
    copy: "Sinh Khí, Thiên Y và Diên Niên chiếm phần lớn thân số.",
  },
  {
    title: "Dòng Tài có nguồn rõ",
    copy: "Sinh Khí → Thiên Y cho thấy quý nhân và cơ hội có khả năng dẫn tới Tài.",
  },
  {
    title: "Công việc là trục mạnh",
    copy: "Diên Niên xuất hiện liên tiếp và tiếp tục dẫn tới Thiên Y ở phần cuối dãy.",
  },
  {
    title: "Họa Hại cần được sử dụng đúng cách",
    copy: "Họa Hại xuất hiện ở đầu thân số, nhưng tổ hợp tiếp theo là Họa Hại → Sinh Khí, giúp khả năng giao tiếp có hướng phát huy tích cực.",
  },
];
