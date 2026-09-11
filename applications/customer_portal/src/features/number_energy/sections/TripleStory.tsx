import type { ReactNode } from "react";

import { ShellSection } from "../shell/ShellSection";

export function TripleStory(): ReactNode {
  return (
    <ShellSection
      sectionId="P-S04"
      testId="triple-story"
      title="Luận các bộ 3 số"
      subtitle="Hai trường khí liên tiếp kết hợp để hình thành ý nghĩa của từng bộ ba."
    />
  );
}
