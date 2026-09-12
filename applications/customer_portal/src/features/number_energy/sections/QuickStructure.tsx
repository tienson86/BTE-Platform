import type { ReactNode } from "react";

import { GOLDEN_QUICK_STRUCTURE } from "../goldenQuickStructure";
import type { PresentationQuickStructure, SlotRenderSource } from "../presentationContract";

export function QuickStructure({
  structure = GOLDEN_QUICK_STRUCTURE,
  slotSource = "GOLDEN_FIXTURE",
}: {
  structure?: PresentationQuickStructure;
  slotSource?: SlotRenderSource;
}): ReactNode {
  return (
    <section
      className="bte-card ne-quick-structure"
      data-section="P-S02"
      data-testid="quick-structure"
      data-slot-source={slotSource}
    >
      <h2>Cấu trúc nhanh</h2>
      <p className="muted">Nhìn nhanh cát tinh, hung tinh, chủ đạo và năng lượng kết — chưa phải điểm số.</p>
      <div className="ne-quick-grid">
        <div className="ui-metric ne-quick-card" data-testid="qs-favorable">
          <span className="ui-metric-label">{structure.favorableLabel}</span>
          <span className="ui-metric-value" data-testid="qs-favorable-value">
            {structure.favorableValue}
          </span>
        </div>
        <div className="ui-metric ne-quick-card" data-testid="qs-challenging">
          <span className="ui-metric-label">{structure.challengingLabel}</span>
          <span className="ui-metric-value" data-testid="qs-challenging-value">
            {structure.challengingValue}
          </span>
        </div>
        <div className="ui-metric ne-quick-card" data-testid="qs-primary">
          <span className="ui-metric-label">{structure.primaryLabel}</span>
          <span className="ui-metric-value" data-testid="qs-primary-value">
            {structure.primaryValue}
          </span>
        </div>
        <div className="ui-metric ne-quick-card" data-testid="qs-terminal">
          <span className="ui-metric-label">{structure.terminalLabel}</span>
          <span className="ui-metric-value" data-testid="qs-terminal-value">
            {structure.terminalValue}
          </span>
        </div>
      </div>
      <p className="ne-quick-summary" data-testid="qs-summary">
        {structure.summary}
      </p>
    </section>
  );
}
