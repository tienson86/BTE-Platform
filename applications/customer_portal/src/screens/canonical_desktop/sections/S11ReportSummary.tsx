/**
 * S11 — Dashboard Preview Card: BÁO CÁO TỔNG KẾT
 */

import type { ReactNode } from "react";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

/**
 * S11 Report Summary — Dashboard preview card.
 */
export function S11ReportSummary(): ReactNode {
  const data = useCanonicalDesktop().s11;
  const previewStrengths = data.strengths.items.slice(0, 2);
  const previewAttention = data.attention.items.slice(0, 2);
  const previewRecs = data.recommendations.items.slice(0, 2);

  return (
    <section className="cd-s11 cd-preview-card" aria-labelledby="cd-s11-title">
      <div className="cd-s11__card">
        <h2 id="cd-s11-title" className="cd-s11__title">
          {data.title}
        </h2>

        <div className="cd-s11__exec cd-s11__exec--preview">
          <h3 className="cd-s11__exec-title">{data.executive.title}</h3>
          <p className="cd-s11__exec-body">{data.executive.body}</p>
        </div>

        <div className="cd-s11__block">
          <h3 className="cd-s11__block-title cd-s11__block-title--strength">
            {data.strengths.title}
          </h3>
          <ul className="cd-s11__list">
            {previewStrengths.map((item) => (
              <li key={item} className="cd-s11__row">
                <span className="cd-s11__icon cd-s11__icon--strength" aria-hidden="true">
                  ✓
                </span>
                <span className="cd-s11__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="cd-s11__block">
          <h3 className="cd-s11__block-title cd-s11__block-title--attention">
            {data.attention.title}
          </h3>
          <ul className="cd-s11__list">
            {previewAttention.map((item) => (
              <li key={item} className="cd-s11__row">
                <span className="cd-s11__icon cd-s11__icon--attention" aria-hidden="true">
                  •
                </span>
                <span className="cd-s11__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="cd-s11__block">
          <h3 className="cd-s11__block-title cd-s11__block-title--recommend">
            {data.recommendations.title}
          </h3>
          <ul className="cd-s11__list">
            {previewRecs.map((item) => (
              <li key={item} className="cd-s11__row">
                <span className="cd-s11__icon cd-s11__icon--recommend" aria-hidden="true">
                  →
                </span>
                <span className="cd-s11__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <button type="button" className="cd-preview-cta">
          {data.link}
        </button>
      </div>
    </section>
  );
}

/** Portal export alias — keep S11LearningPanel name for shell stability. */
export const S11LearningPanel = S11ReportSummary;
