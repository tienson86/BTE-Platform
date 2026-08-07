/**
 * S08 — Dashboard Preview Card: LUẬN GIẢI TỔNG HỢP
 * PACK_04: Presentation Adapter preview + hasMore (fixed height).
 */

import type { ReactNode } from "react";
import { adaptInterpretationPreview } from "../../../presentation";
import { PresentationText } from "../../../components/shared/PresentationText";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

/**
 * S08 Interpretation — Dashboard preview card.
 */
export function S08Interpretation(): ReactNode {
  const data = useCanonicalDesktop().s08;
  const preview = adaptInterpretationPreview({
    executiveBody: data.executive.body,
    strengths: data.strengths.items,
    warnings: data.warnings.items,
    cardType: "preview",
  });

  return (
    <section
      className="cd-s08 cd-preview-card"
      data-card-type="preview"
      data-has-more={preview.hasMore ? "true" : "false"}
      aria-labelledby="cd-s08-title"
    >
      <div className="cd-s08__card">
        <h2 id="cd-s08-title" className="cd-s08__title ui-line-clamp-2">
          {data.title}
        </h2>

        <div className="cd-s08__exec cd-s08__exec--preview">
          <PresentationText
            className="cd-s08__exec-body"
            typeRole="summary"
            preview={preview.executive}
            as="p"
          />
        </div>

        <div className="cd-s08__block">
          <h3 className="cd-s08__block-title cd-s08__block-title--strength">
            {data.strengths.title}
          </h3>
          <ul className="cd-s08__list">
            {preview.strengths.items.map((item) => (
              <li key={item} className="cd-s08__row">
                <span className="cd-s08__icon cd-s08__icon--strength" aria-hidden="true">
                  ✓
                </span>
                <span className="cd-s08__text ui-line-clamp-2">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="cd-s08__block">
          <h3 className="cd-s08__block-title cd-s08__block-title--warning">
            {data.warnings.title}
          </h3>
          <ul className="cd-s08__list">
            {preview.warnings.items.map((item) => (
              <li key={item} className="cd-s08__row">
                <span className="cd-s08__icon cd-s08__icon--warning" aria-hidden="true">
                  •
                </span>
                <span className="cd-s08__text ui-line-clamp-2">{item}</span>
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
