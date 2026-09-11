import type { ReactNode } from "react";

import { ShellSection } from "../shell/ShellSection";

export function EnergyDistribution(): ReactNode {
  return (
    <ShellSection
      sectionId="P-S05"
      testId="energy-distribution"
      title="Cấu trúc trường khí"
      subtitle="Tám trường khí xuất hiện trong dãy và mức độ lặp lại."
    />
  );
}
