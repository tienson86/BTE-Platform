import type { ReactNode } from "react";

import type { GoldenPreviewState } from "./formModel";
import {
  GOLDEN_ASSESSMENT_FLOW,
  GOLDEN_ASSESSMENT_STORY,
  GOLDEN_ASSESSMENT_TITLE,
  GOLDEN_RECOMMENDATION_STATE,
  GOLDEN_RECOMMENDATION_SUPPORTING,
  GOLDEN_RECOMMENDATION_TITLE,
} from "./goldenAssessment";
import {
  GOLDEN_BASIS_EVIDENCE,
  GOLDEN_BASIS_HELPER,
  GOLDEN_BASIS_HIGHLIGHTS,
  GOLDEN_BASIS_PRINCIPLES,
  GOLDEN_BASIS_TITLE,
} from "./goldenBasis";
import { GOLDEN_ENERGY_DISTRIBUTION } from "./goldenDistribution";
import { GOLDEN_DOMAIN_INSIGHTS } from "./goldenDomains";
import { GOLDEN_PHONE_HERO } from "./goldenHero";
import { GOLDEN_PHONE_PAIRS } from "./goldenPairs";
import { GOLDEN_QUICK_STRUCTURE } from "./goldenQuickStructure";
import {
  GOLDEN_SCORE_BREAKDOWN,
  GOLDEN_SCORE_GRADE,
  GOLDEN_SCORE_NOTE,
  GOLDEN_SCORE_REASONS,
  GOLDEN_SCORE_TOTAL,
} from "./goldenScore";
import { GOLDEN_CAUTIONS, GOLDEN_STRENGTHS } from "./goldenStrengths";
import { GOLDEN_PHONE_TRIPLES } from "./goldenTriples";
import {
  GOLDEN_WEALTH_STAGES,
  GOLDEN_WEALTH_STORY,
  GOLDEN_WEALTH_SYNTHESIS,
} from "./goldenWealthFlow";
import type {
  NumberEnergyPresentationView,
  PresentationAssessment,
  PresentationBasis,
  PresentationFindings,
  PresentationHero,
  PresentationScore,
  PresentationSlotId,
  SlotRenderSource,
} from "./presentationContract";
import { BasisOfAssessment } from "./sections/BasisOfAssessment";
import { DomainInsights } from "./sections/DomainInsights";
import { EnergyDistribution } from "./sections/EnergyDistribution";
import { EnergyMap } from "./sections/EnergyMap";
import { ExpertDetails } from "./sections/ExpertDetails";
import { FinalAssessment } from "./sections/FinalAssessment";
import { QuickStructure } from "./sections/QuickStructure";
import { ResultHero } from "./sections/ResultHero";
import { ScoreBreakdown } from "./sections/ScoreBreakdown";
import { StrengthsCautions } from "./sections/StrengthsCautions";
import { TripleStory } from "./sections/TripleStory";
import { WealthFlow } from "./sections/WealthFlow";

const GOLDEN_FINDINGS: PresentationFindings = {
  strengths: GOLDEN_STRENGTHS,
  cautions: GOLDEN_CAUTIONS,
};

const GOLDEN_SCORE: PresentationScore = {
  totalDisplay: GOLDEN_SCORE_TOTAL,
  grade: GOLDEN_SCORE_GRADE,
  note: GOLDEN_SCORE_NOTE,
  breakdown: GOLDEN_SCORE_BREAKDOWN,
  reasons: GOLDEN_SCORE_REASONS,
};

const GOLDEN_ASSESSMENT: PresentationAssessment = {
  title: GOLDEN_ASSESSMENT_TITLE,
  story: GOLDEN_ASSESSMENT_STORY,
  flow: GOLDEN_ASSESSMENT_FLOW,
  recommendationTitle: GOLDEN_RECOMMENDATION_TITLE,
  recommendationState: GOLDEN_RECOMMENDATION_STATE,
  recommendationSupporting: GOLDEN_RECOMMENDATION_SUPPORTING,
};

const GOLDEN_BASIS: PresentationBasis = {
  title: GOLDEN_BASIS_TITLE,
  helper: GOLDEN_BASIS_HELPER,
  principles: GOLDEN_BASIS_PRINCIPLES,
  highlights: GOLDEN_BASIS_HIGHLIGHTS,
  evidence: GOLDEN_BASIS_EVIDENCE,
};

type ResultSectionProps = {
  goldenPreview?: GoldenPreviewState | null;
  runtimeView?: NumberEnergyPresentationView | null;
  slotSource?: Record<PresentationSlotId, SlotRenderSource> | null;
};

export function ResultSection({
  goldenPreview = null,
  runtimeView = null,
  slotSource = null,
}: ResultSectionProps): ReactNode {
  const isGolden = goldenPreview !== null;
  const hero = boundSlot("P-S00", slotSource, presentHero(runtimeView?.hero), GOLDEN_PHONE_HERO);
  const pairs = boundSlot("P-S01", slotSource, runtimeView?.pairs, GOLDEN_PHONE_PAIRS);
  const quick = boundSlot("P-S02", slotSource, runtimeView?.quick_structure, GOLDEN_QUICK_STRUCTURE);
  const wealth = boundSlot("P-S03", slotSource, runtimeView?.wealth_flow, {
    stages: GOLDEN_WEALTH_STAGES,
    story: GOLDEN_WEALTH_STORY,
    synthesis: GOLDEN_WEALTH_SYNTHESIS,
  });
  const triples = boundSlot(
    "P-S04",
    slotSource,
    nonempty(runtimeView?.triples),
    GOLDEN_PHONE_TRIPLES,
  );
  const distribution = boundSlot(
    "P-S05",
    slotSource,
    runtimeView?.distribution,
    GOLDEN_ENERGY_DISTRIBUTION,
  );
  const domains = boundSlot(
    "P-S06",
    slotSource,
    nonempty(runtimeView?.domains),
    GOLDEN_DOMAIN_INSIGHTS,
  );
  const findings = boundSlot(
    "P-S07",
    slotSource,
    presentFindings(runtimeView?.findings),
    GOLDEN_FINDINGS,
  );
  const score = boundSlot("P-S08", slotSource, presentScore(runtimeView?.score), GOLDEN_SCORE);
  const assessment = boundSlot(
    "P-S09",
    slotSource,
    presentAssessment(runtimeView?.assessment),
    GOLDEN_ASSESSMENT,
  );
  const basis = boundSlot("P-S10", slotSource, presentBasis(runtimeView?.basis), GOLDEN_BASIS);

  return (
    <div
      className="ne-result"
      data-testid="result-section"
      data-preview-state={isGolden ? (runtimeView ? "runtime" : "golden") : "idle"}
      hidden={!isGolden}
    >
      <ResultHero
        hero={hero}
        slotSource={
          slotSource?.["P-S00"] === "RUNTIME" && presentHero(runtimeView?.hero)
            ? "RUNTIME"
            : "GOLDEN_FIXTURE"
        }
      />
      <EnergyMap pairs={pairs} slotSource={slotSource?.["P-S01"] ?? "GOLDEN_FIXTURE"} />
      <QuickStructure structure={quick} slotSource={slotSource?.["P-S02"] ?? "GOLDEN_FIXTURE"} />
      <WealthFlow flow={wealth} slotSource={slotSource?.["P-S03"] ?? "GOLDEN_FIXTURE"} />
      <TripleStory
        triples={triples}
        slotSource={
          slotSource?.["P-S04"] === "RUNTIME" && nonempty(runtimeView?.triples)
            ? "RUNTIME"
            : "GOLDEN_FIXTURE"
        }
      />
      <div className="ne-shell-row ne-shell-row--5-7">
        <EnergyDistribution
          rows={distribution}
          slotSource={slotSource?.["P-S05"] ?? "GOLDEN_FIXTURE"}
        />
        <DomainInsights
          domains={domains}
          slotSource={
            slotSource?.["P-S06"] === "RUNTIME" && nonempty(runtimeView?.domains)
              ? "RUNTIME"
              : "GOLDEN_FIXTURE"
          }
        />
      </div>
      <StrengthsCautions
        findings={findings}
        slotSource={
          slotSource?.["P-S07"] === "RUNTIME" && presentFindings(runtimeView?.findings)
            ? "RUNTIME"
            : "GOLDEN_FIXTURE"
        }
      />
      <div className="ne-shell-row ne-shell-row--5-7">
        <ScoreBreakdown
          score={score}
          slotSource={
            slotSource?.["P-S08"] === "RUNTIME" && presentScore(runtimeView?.score)
              ? "RUNTIME"
              : "GOLDEN_FIXTURE"
          }
        />
        <FinalAssessment
          assessment={assessment}
          slotSource={
            slotSource?.["P-S09"] === "RUNTIME" && presentAssessment(runtimeView?.assessment)
              ? "RUNTIME"
              : "GOLDEN_FIXTURE"
          }
        />
      </div>
      <BasisOfAssessment
        basis={basis}
        slotSource={
          slotSource?.["P-S10"] === "RUNTIME" && presentBasis(runtimeView?.basis)
            ? "RUNTIME"
            : "GOLDEN_FIXTURE"
        }
      />
      <ExpertDetails />
    </div>
  );
}

function boundSlot<T>(
  slot: PresentationSlotId,
  slotSource: Record<PresentationSlotId, SlotRenderSource> | null,
  runtimeValue: T | null | undefined,
  golden: T,
): T {
  if (!slotSource || slotSource[slot] !== "RUNTIME" || runtimeValue == null) {
    return golden;
  }
  return runtimeValue;
}

function presentHero(value: PresentationHero | null | undefined): PresentationHero | null {
  if (!value) {
    return null;
  }
  if (
    !value.displayValue ||
    !value.scoreDisplay ||
    !value.grade ||
    !value.primaryEnergy ||
    !value.terminalEnergy ||
    !value.summary
  ) {
    return null;
  }
  return value;
}

function nonempty<T>(value: readonly T[] | null | undefined): readonly T[] | null {
  return value && value.length > 0 ? value : null;
}

function presentFindings(value: PresentationFindings | null | undefined): PresentationFindings | null {
  if (!value) {
    return null;
  }
  if (value.strengths.length === 0 && value.cautions.length === 0) {
    return null;
  }
  return value;
}

function presentScore(value: PresentationScore | null | undefined): PresentationScore | null {
  if (!value) {
    return null;
  }
  if (!value.totalDisplay || !value.grade || value.breakdown.length === 0) {
    return null;
  }
  return value;
}

function presentAssessment(
  value: PresentationAssessment | null | undefined,
): PresentationAssessment | null {
  if (!value) {
    return null;
  }
  if (!value.title || value.story.length === 0 || !value.recommendationState) {
    return null;
  }
  return value;
}

function presentBasis(value: PresentationBasis | null | undefined): PresentationBasis | null {
  if (!value) {
    return null;
  }
  if (value.evidence.length === 0) {
    return null;
  }
  return value;
}
