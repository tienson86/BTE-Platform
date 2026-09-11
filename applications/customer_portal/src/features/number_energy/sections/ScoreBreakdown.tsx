import type { ReactNode } from "react";

import {
  GOLDEN_SCORE_BREAKDOWN,
  GOLDEN_SCORE_GRADE,
  GOLDEN_SCORE_NOTE,
  GOLDEN_SCORE_REASONS,
  GOLDEN_SCORE_TOTAL,
} from "../goldenScore";

function formatPoints(earned: number, max: number): string {
  return `${earned} / ${max}`;
}

export function ScoreBreakdown(): ReactNode {
  return (
    <section className="bte-card ne-score" data-section="P-S08" data-testid="score-breakdown">
      <h2>Điểm đánh giá</h2>
      <p className="muted">
        Điểm tổng hợp được hình thành từ cấu trúc năng lượng, dòng tài vận, công việc, độ ổn định và
        phần cuối dãy.
      </p>
      <div className="ne-score-total" data-testid="score-total-card">
        <p className="ne-score-total-value" data-testid="score-total">
          {GOLDEN_SCORE_TOTAL}
        </p>
        <p className="ne-score-grade" data-testid="score-grade">
          {GOLDEN_SCORE_GRADE}
        </p>
        <p className="muted ne-score-note" data-testid="score-static-note">
          {GOLDEN_SCORE_NOTE}
        </p>
      </div>
      <ol className="ne-score-list" data-testid="score-dimension-list">
        {GOLDEN_SCORE_BREAKDOWN.map((dimension, index) => {
          const points = formatPoints(dimension.earned, dimension.max);
          const remainder = dimension.max - dimension.earned;
          return (
            <li
              key={dimension.label}
              className="ne-score-row"
              data-testid={`score-row-${index}`}
            >
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
        })}
      </ol>
      <div className="ne-score-reasons" data-testid="score-reasons">
        <h3 className="ne-score-reasons-title">Vì sao dãy số đạt mức này?</h3>
        <ol className="ne-score-reason-list" data-testid="score-reason-list">
          {GOLDEN_SCORE_REASONS.map((reason, index) => (
            <li key={reason.title} className="ne-score-reason" data-testid={`score-reason-card-${index}`}>
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
