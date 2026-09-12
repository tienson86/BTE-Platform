import type { ReactNode } from "react";

import {
  GOLDEN_SCORE_BREAKDOWN,
  GOLDEN_SCORE_GRADE,
  GOLDEN_SCORE_NOTE,
  GOLDEN_SCORE_REASONS,
  GOLDEN_SCORE_TOTAL,
} from "../goldenScore";
import type { PresentationScore, PresentationScoreDimension, SlotRenderSource } from "../presentationContract";

const GOLDEN_SCORE: PresentationScore = {
  totalDisplay: GOLDEN_SCORE_TOTAL,
  grade: GOLDEN_SCORE_GRADE,
  note: GOLDEN_SCORE_NOTE,
  breakdown: GOLDEN_SCORE_BREAKDOWN,
  reasons: GOLDEN_SCORE_REASONS,
};

function formatPoints(earned: number, max: number): string {
  return `${earned} / ${max}`;
}

function ScoreDimensionRow({
  dimension,
  index,
}: {
  dimension: PresentationScoreDimension;
  index: number;
}): ReactNode {
  const points = formatPoints(dimension.earned, dimension.max);
  const remainder = Math.max(dimension.max - dimension.earned, 0);
  return (
    <li key={`${dimension.label}-${index}`} className="ne-score-row" data-testid={`score-row-${index}`}>
      <div className="ne-score-row-head">
        <span className="ne-score-dim-label" data-testid={`score-dim-label-${index}`}>
          {dimension.label}
        </span>
        <span className="ne-score-dim-points" data-testid={`score-dim-points-${index}`}>
          {points}
        </span>
      </div>
      <div
        className="ne-score-bar"
        role="meter"
        aria-label={`${dimension.label} ${points}`}
        aria-valuemin={0}
        aria-valuemax={dimension.max}
        aria-valuenow={dimension.earned}
        aria-valuetext={points}
      >
        <span className="ne-score-bar-fill" style={{ flexGrow: dimension.earned }} aria-hidden="true" />
        <span className="ne-score-bar-rest" style={{ flexGrow: remainder }} aria-hidden="true" />
      </div>
    </li>
  );
}

export function ScoreBreakdown({
  score = GOLDEN_SCORE,
  slotSource = "GOLDEN_FIXTURE",
}: {
  score?: PresentationScore;
  slotSource?: SlotRenderSource;
}): ReactNode {
  return (
    <section
      className="bte-card ne-score"
      data-section="P-S08"
      data-testid="score-breakdown"
      data-slot-source={slotSource}
    >
      <h2>Điểm đánh giá</h2>
      <p className="muted">
        Điểm tổng hợp được hình thành từ cấu trúc năng lượng, dòng tài vận, công việc, độ ổn định và
        phần cuối dãy.
      </p>
      <div className="ne-score-total" data-testid="score-total-card">
        <p className="ne-score-total-value" data-testid="score-total">
          {score.totalDisplay}
        </p>
        <p className="ne-score-grade" data-testid="score-grade">
          {score.grade}
        </p>
        {score.note ? (
          <p className="muted ne-score-note" data-testid="score-static-note">
            {score.note}
          </p>
        ) : null}
      </div>
      <ol className="ne-score-list" data-testid="score-dimension-list">
        {score.breakdown.map((dimension, index) => (
          <ScoreDimensionRow key={`${dimension.label}-${index}`} dimension={dimension} index={index} />
        ))}
      </ol>
      <div className="ne-score-reasons" data-testid="score-reasons">
        <h3 className="ne-score-reasons-title">Vì sao dãy số đạt mức này?</h3>
        <ol className="ne-score-reason-list" data-testid="score-reason-list">
          {score.reasons.map((reason, index) => (
            <li key={`${reason.title}-${index}`} className="ne-score-reason" data-testid={`score-reason-card-${index}`}>
              <h4 className="ne-score-reason-title" data-testid={`score-reason-title-${index}`}>
                {reason.title}
              </h4>
              <p className="ne-score-reason-copy" data-testid={`score-reason-copy-${index}`}>
                {reason.copy}
              </p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
