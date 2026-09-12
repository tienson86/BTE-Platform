import type { ReactNode } from "react";

import {
  GOLDEN_WEALTH_STAGES,
  GOLDEN_WEALTH_STORY,
  GOLDEN_WEALTH_SYNTHESIS,
} from "../goldenWealthFlow";
import type { PresentationWealthFlow, PresentationWealthStage, SlotRenderSource } from "../presentationContract";

const GOLDEN_WEALTH_FLOW: PresentationWealthFlow = {
  stages: GOLDEN_WEALTH_STAGES,
  story: GOLDEN_WEALTH_STORY,
  synthesis: GOLDEN_WEALTH_SYNTHESIS,
};

function FlowConnector(): ReactNode {
  return (
    <span className="ne-wealth-connector" aria-hidden="true">
      <span className="ne-wealth-connector--desktop">→</span>
      <span className="ne-wealth-connector--mobile">↓</span>
    </span>
  );
}

function WealthStageCard({
  stage,
  index,
}: {
  stage: PresentationWealthStage;
  index: number;
}): ReactNode {
  return (
    <article className="ne-wealth-card" data-testid={`wf-stage-${index}`} data-stage-id={stage.id}>
      <p className="ne-wealth-step">{String(index + 1).padStart(2, "0")}</p>
      <h3 className="ne-wealth-label" data-testid={`wf-label-${index}`}>
        {stage.label}
      </h3>
      <p className="ne-wealth-headline" data-testid={`wf-headline-${index}`}>
        {stage.headline}
      </p>
      <p className="ne-wealth-evidence" data-testid={`wf-evidence-${index}`}>
        {stage.evidence}
      </p>
      {stage.interaction ? (
        <p className="ne-wealth-interaction" data-testid={`wf-interaction-${index}`}>
          {stage.interaction}
        </p>
      ) : null}
      <p className="muted ne-wealth-narrative">{stage.narrative}</p>
    </article>
  );
}

export function WealthFlow({
  flow = GOLDEN_WEALTH_FLOW,
  slotSource = "GOLDEN_FIXTURE",
}: {
  flow?: PresentationWealthFlow;
  slotSource?: SlotRenderSource;
}): ReactNode {
  return (
    <section
      className="bte-card ne-wealth-flow"
      data-section="P-S03"
      data-testid="wealth-flow"
      data-slot-source={slotSource}
    >
      <h2>Dòng tài vận</h2>
      <p className="muted">Có Tài không · Tài từ đâu · Tài đi đâu · Hậu vận</p>
      <ol className="ne-wealth-stages" data-testid="wealth-stages">
        {flow.stages.map((stage, index) => (
          <li key={stage.id} className="ne-wealth-item">
            {index > 0 ? <span className="ne-sr-only">tiếp đến</span> : null}
            {index > 0 ? <FlowConnector /> : null}
            <WealthStageCard stage={stage} index={index} />
          </li>
        ))}
      </ol>
      <div className="ne-wealth-story" data-testid="wealth-story">
        <h3 className="ne-wealth-story-title">Câu chuyện tài vận</h3>
        <ol className="ne-wealth-story-flow">
          {flow.story.map((node, index) => (
            <li key={`${node}-${index}`} className="ne-wealth-story-item">
              {index > 0 ? <span className="ne-sr-only">tiếp đến</span> : null}
              {index > 0 ? (
                <span className="ne-wealth-story-arrow" aria-hidden="true">
                  ↓
                </span>
              ) : null}
              <span className="ne-wealth-story-node" data-testid={`wf-story-${index}`}>
                {node}
              </span>
            </li>
          ))}
        </ol>
        <p className="ne-wealth-synthesis" data-testid="wf-synthesis">
          {flow.synthesis}
        </p>
      </div>
    </section>
  );
}
