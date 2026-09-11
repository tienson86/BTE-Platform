import type { ReactNode } from "react";

import { ShellSection } from "../shell/ShellSection";

export function ScoreBreakdown(): ReactNode {
  return (
    <ShellSection
      sectionId="P-S08"
      testId="score-breakdown"
      title="Điểm đánh giá"
      subtitle="Điểm tổng hợp sẽ được trình bày sau khi khóa Static Golden UI, chưa nối runtime."
    />
  );
}
