import type { ReactNode } from "react";

import {
  GOLDEN_ASSESSMENT_FLOW,
  GOLDEN_ASSESSMENT_STORY,
  GOLDEN_ASSESSMENT_TITLE,
  GOLDEN_RECOMMENDATION_STATE,
  GOLDEN_RECOMMENDATION_SUPPORTING,
  GOLDEN_RECOMMENDATION_TITLE,
} from "../goldenAssessment";

export function FinalAssessment(): ReactNode {
  return (
    <section className="bte-card ne-assess" data-section="P-S09" data-testid="final-assessment">
      <div data-testid="assessment-block">
        <h2 data-testid="assessment-title">{GOLDEN_ASSESSMENT_TITLE}</h2>
        <div data-testid="assessment-story">
          {GOLDEN_ASSESSMENT_STORY.map((paragraph) => (
            <p key={paragraph} className="ne-assess-story">
              {paragraph}
            </p>
          ))}
        </div>
        <ol className="ne-assess-flow" data-testid="assessment-flow">
          {GOLDEN_ASSESSMENT_FLOW.map((node, index) => (
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
          {GOLDEN_RECOMMENDATION_TITLE}
        </h3>
        <p className="ne-assess-recommend-state" data-testid="recommendation-state">
          {GOLDEN_RECOMMENDATION_STATE}
        </p>
        <p className="muted ne-assess-recommend-copy" data-testid="recommendation-supporting">
          {GOLDEN_RECOMMENDATION_SUPPORTING}
        </p>
      </div>
    </section>
  );
}
