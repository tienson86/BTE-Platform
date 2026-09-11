import type { ReactNode } from "react";

import { ShellSection } from "../shell/ShellSection";

export function StrengthsCautions(): ReactNode {
  return (
    <ShellSection
      sectionId="P-S07"
      testId="strengths-cautions"
      title="Điểm mạnh và điểm cần lưu ý"
      subtitle="Hai mặt của dãy số, không chỉ phần thuận."
    />
  );
}
