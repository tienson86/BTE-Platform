import type { ReactNode } from "react";

import { ShellSection } from "../shell/ShellSection";

export function DomainInsights(): ReactNode {
  return (
    <ShellSection
      sectionId="P-S06"
      testId="domain-insights"
      title="Ảnh hưởng theo lĩnh vực"
      subtitle="Tài vận, công việc, quan hệ và các lĩnh vực đời sống liên quan."
    />
  );
}
