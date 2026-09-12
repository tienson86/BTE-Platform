import type { ReactNode } from "react";

import {
  GOLDEN_ASSESSMENT_FLOW,
  GOLDEN_ASSESSMENT_STORY,
  GOLDEN_ASSESSMENT_TITLE,
  GOLDEN_RECOMMENDATION_STATE,
  GOLDEN_RECOMMENDATION_SUPPORTING,
  GOLDEN_RECOMMENDATION_TITLE,
} from "../goldenAssessment";
import type { PresentationAssessment, SlotRenderSource } from "../presentationContract";

const GOLDEN_ASSESSMENT: PresentationAssessment = {
  title: GOLDEN_ASSESSMENT_TITLE,
  story: GOLDEN_ASSESSMENT_STORY,
  flow: GOLDEN_ASSESSMENT_FLOW,
  recommendationTitle: GOLDEN_RECOMMENDATION_TITLE,
  recommendationState: GOLDEN_RECOMMENDATION_STATE,
  recommendationSupporting: GOLDEN_RECOMMENDATION_SUPPORTING,
};

export function FinalAssessment({
  assessment = GOLDEN_ASSESSMENT,
  slotSource = "GOLDEN_FIXTURE",
}: {
  assessment?: PresentationAssessment;
  slotSource?: SlotRenderSource;
}): ReactNode {
  return (
    <section
      className="bte-card ne-assess"
      data-section="P-S09"
      data-testid="final-assessment"
      data-slot-source={slotSource}
    >
      <div data-testid="assessment-block">
        <h2 data-testid="assessment-title">{assessment.title}</h2>
        <div data-testid="assessment-story">
          {assessment.story.map((paragraph, index) => (
            <p key={`${paragraph}-${index}`} className="ne-assess-story">
              {paragraph}
            </p>
          ))}
        </div>
        <ol className="ne-assess-flow" data-testid="assessment-flow">
          {assessment.flow.map((node, index) => (
            <li key={`${node}-${index}`} className="ne-assess-flow-item">
              {index > 0 ? (
                <span className="ne-assess-flow-arrow" aria-hidden="true">
                  ↓
                </span>
              ) : null}
              <span className="ne-assess-flow-node" data-testid={`assessment-flow-${index}`}>
                {node}
              </span>
            </li>
          ))}
        </ol>
      </div>
      <div className="ne-assess-recommend" data-testid="recommendation-block">
        <h3 className="ne-assess-recommend-title" data-testid="recommendation-title">
          {assessment.recommendationTitle}
        </h3>
        <p className="ne-assess-recommend-state" data-testid="recommendation-state">
          {assessment.recommendationState}
        </p>
        <p className="muted ne-assess-recommend-copy" data-testid="recommendation-supporting">
          {assessment.recommendationSupporting}
        </p>
      </div>
    </section>
  );
}
