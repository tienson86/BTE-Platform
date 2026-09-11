import type { ReactNode } from "react";

import { ShellSection } from "../shell/ShellSection";

export function BasisOfAssessment(): ReactNode {
  return (
    <ShellSection
      sectionId="P-S10"
      testId="basis-of-assessment"
      title="Cơ sở đánh giá"
      subtitle="Phần nền tảng cho khách hàng; chi tiết kỹ thuật mặc định không hiện."
    />
  );
}
