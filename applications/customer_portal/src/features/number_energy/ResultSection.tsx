import type { ReactNode } from "react";

import type { GoldenPreviewState } from "./formModel";
import { BasisOfAssessment } from "./sections/BasisOfAssessment";
import { DomainInsights } from "./sections/DomainInsights";
import { EnergyDistribution } from "./sections/EnergyDistribution";
import { EnergyMap } from "./sections/EnergyMap";
import { FinalAssessment } from "./sections/FinalAssessment";
import { QuickStructure } from "./sections/QuickStructure";
import { ResultHero } from "./sections/ResultHero";
import { ScoreBreakdown } from "./sections/ScoreBreakdown";
import { StrengthsCautions } from "./sections/StrengthsCautions";
import { TripleStory } from "./sections/TripleStory";
import { WealthFlow } from "./sections/WealthFlow";

type ResultSectionProps = {
  goldenPreview?: GoldenPreviewState | null;
};

export function ResultSection({ goldenPreview = null }: ResultSectionProps): ReactNode {
  const isGolden = goldenPreview !== null;

  return (
    <div
      className="ne-result"
      data-testid="result-section"
      data-preview-state={isGolden ? "golden" : "idle"}
      hidden={!isGolden}
    >
      <ResultHero />
      <EnergyMap />
      <QuickStructure />
      <WealthFlow />
      <TripleStory />
      <div className="ne-shell-row ne-shell-row--5-7">
        <EnergyDistribution />
        <DomainInsights />
      </div>
      <StrengthsCautions />
      <div className="ne-shell-row ne-shell-row--5-7">
        <ScoreBreakdown />
        <FinalAssessment />
      </div>
      <BasisOfAssessment />
    </div>
  );
}
