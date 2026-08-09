import { memo } from "react";
import type { ChromeModel, SummaryModel } from "../../adapter/PortalResultModel";
import { Button } from "../Shared/Button";
import { SectionHeader } from "../Shared/SectionHeader";

export type ExecutiveSummaryProps = {
  model: SummaryModel;
  chrome: ChromeModel;
  onJumpToRecommendations?: () => void;
};

export const ExecutiveSummary = memo(function ExecutiveSummary({
  model,
  chrome,
  onJumpToRecommendations,
}: ExecutiveSummaryProps) {
  return (
    <section className="rv2-section" id="rv2-Summary" tabIndex={-1} aria-labelledby="rv2-summary-title">
      <SectionHeader id="rv2-summary-title">{model.title}</SectionHeader>
      <ul className="rv2-summary__list">
        {model.bullets.map((bullet) => (
          <li key={bullet}>{bullet}</li>
        ))}
      </ul>
      {onJumpToRecommendations ? (
        <Button variant="text" onClick={onJumpToRecommendations}>
          {chrome.section_recommendation}
        </Button>
      ) : null}
    </section>
  );
});
