import type { ReactNode } from "react";

import { ShellSection } from "../shell/ShellSection";

export function WealthFlow(): ReactNode {
  return (
    <ShellSection
      sectionId="P-S03"
      testId="wealth-flow"
      title="Dòng tài vận"
      subtitle="Có Tài không · Tài từ đâu · Tài đi đâu · Hậu vận"
    />
  );
}
