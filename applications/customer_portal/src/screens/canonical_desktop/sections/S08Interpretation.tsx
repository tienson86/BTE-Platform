/**
 * S08 — Dashboard Preview Card: LUẬN GIẢI TỔNG HỢP
 */

import type { ReactNode } from "react";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

/**
 * S08 Interpretation — Dashboard preview card.
 */
export function S08Interpretation(): ReactNode {
  const data = useCanonicalDesktop().s08;
  const previewStrengths = data.strengths.items.slice(0, 2);
  const previewWarnings = data.warnings.items.slice(0, 2);

  return (
    <section className="cd-s08 cd-preview-card" aria-labelledby="cd-s08-title">
      <div className="cd-s08__card">
        <h2 id="cd-s08-title" className="cd-s08__title">
          {data.title}
        </h2>

        <div className="cd-s08__exec cd-s08__exec--preview">
          <p className="cd-s08__exec-body">{data.executive.body}</p>
        </div>

        <div className="cd-s08__block">
          <h3 className="cd-s08__block-title cd-s08__block-title--strength">
            {data.strengths.title}
          </h3>
          <ul className="cd-s08__list">
            {previewStrengths.map((item) => (
              <li key={item} className="cd-s08__row">
                <span className="cd-s08__icon cd-s08__icon--strength" aria-hidden="true">
                  ✓
                </span>
                <span className="cd-s08__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="cd-s08__block">
          <h3 className="cd-s08__block-title cd-s08__block-title--warning">
            {data.warnings.title}
          </h3>
          <ul className="cd-s08__list">
            {previewWarnings.map((item) => (
              <li key={item} className="cd-s08__row">
                <span className="cd-s08__icon cd-s08__icon--warning" aria-hidden="true">
                  •
                </span>
                <span className="cd-s08__text">{item}</span>
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
