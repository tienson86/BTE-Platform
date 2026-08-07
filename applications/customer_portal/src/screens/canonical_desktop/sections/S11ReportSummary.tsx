/**
 * S11 — Dashboard Preview Card: BÁO CÁO TỔNG KẾT
 * PACK_04: Presentation Adapter preview + hasMore (fixed height).
 */

import type { ReactNode } from "react";
import { adaptReportSummaryPreview } from "../../../presentation";
import { PresentationText } from "../../../components/shared/PresentationText";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

/**
 * S11 Report Summary — Dashboard preview card.
 */
export function S11ReportSummary(): ReactNode {
  const data = useCanonicalDesktop().s11;
  const preview = adaptReportSummaryPreview({
    executiveTitle: data.executive.title,
    executiveBody: data.executive.body,
    strengths: data.strengths.items,
    attention: data.attention.items,
    recommendations: data.recommendations.items,
    cardType: "preview",
  });

  return (
    <section
      className="cd-s11 cd-preview-card"
      data-card-type="preview"
      data-has-more={preview.hasMore ? "true" : "false"}
      aria-labelledby="cd-s11-title"
    >
      <div className="cd-s11__card">
        <h2 id="cd-s11-title" className="cd-s11__title ui-line-clamp-2">
          {data.title}
        </h2>

        <div className="cd-s11__exec cd-s11__exec--preview">
          <PresentationText
            className="cd-s11__exec-title"
            typeRole="subtitle"
            preview={preview.executive.title}
            as="h3"
          />
          <PresentationText
            className="cd-s11__exec-body"
            typeRole="summary"
            preview={preview.executive.body}
            as="p"
          />
        </div>

        <div className="cd-s11__block">
          <h3 className="cd-s11__block-title cd-s11__block-title--strength">
            {data.strengths.title}
          </h3>
          <ul className="cd-s11__list">
            {preview.strengths.items.map((item) => (
              <li key={item} className="cd-s11__row">
                <span className="cd-s11__icon cd-s11__icon--strength" aria-hidden="true">
                  ✓
                </span>
                <span className="cd-s11__text ui-line-clamp-2">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="cd-s11__block">
          <h3 className="cd-s11__block-title cd-s11__block-title--attention">
            {data.attention.title}
          </h3>
          <ul className="cd-s11__list">
            {preview.attention.items.map((item) => (
              <li key={item} className="cd-s11__row">
                <span className="cd-s11__icon cd-s11__icon--attention" aria-hidden="true">
                  •
                </span>
                <span className="cd-s11__text ui-line-clamp-2">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="cd-s11__block">
          <h3 className="cd-s11__block-title cd-s11__block-title--recommend">
            {data.recommendations.title}
          </h3>
          <ul className="cd-s11__list">
            {preview.recommendations.items.map((item) => (
              <li key={item} className="cd-s11__row">
                <span className="cd-s11__icon cd-s11__icon--recommend" aria-hidden="true">
                  →
                </span>
                <span className="cd-s11__text ui-line-clamp-2">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <button
          type="button"
          className="cd-preview-cta"
          data-has-more={preview.hasMore ? "true" : "false"}
          aria-label={
            preview.hasMore ? `${data.link} — còn nội dung đầy đủ` : data.link
          }
        >
          {data.link}
        </button>
      </div>
    </section>
  );
}

/** Portal export alias — keep S11LearningPanel name for shell stability. */
export const S11LearningPanel = S11ReportSummary;
