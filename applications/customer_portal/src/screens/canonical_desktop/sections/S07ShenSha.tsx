/**
 * S07 — Dashboard Preview Card: THẦN SÁT
 */

import type { ReactNode } from "react";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

/**
 * S07 Shen Sha — Dashboard preview card.
 */
export function S07ShenSha(): ReactNode {
  const data = useCanonicalDesktop().s07;
  const previewGood = data.good.items.slice(0, 3);
  const previewBad = data.bad.items.slice(0, 2);

  return (
    <section className="cd-s07 cd-preview-card" aria-labelledby="cd-s07-title">
      <div className="cd-s07__card">
        <h2 id="cd-s07-title" className="cd-s07__title">
          {data.title}
        </h2>

        <div className="cd-s07__exec">
          <p className="cd-s07__exec-line">{data.executive.line2}</p>
        </div>

        <div className="cd-s07__group">
          <h3 className="cd-s07__group-title cd-s07__group-title--good">
            ● CÁT TINH
          </h3>
          <ul className="cd-s07__list">
            {previewGood.map((item) => (
              <li key={item} className="cd-s07__row">
                <span className="cd-s07__icon cd-s07__icon--good" aria-hidden="true">
                  ✓
                </span>
                <span className="cd-s07__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <hr className="cd-s07__divider" />

        <div className="cd-s07__group">
          <h3 className="cd-s07__group-title cd-s07__group-title--bad">
            ● HUNG TINH
          </h3>
          <ul className="cd-s07__list">
            {previewBad.map((item) => (
              <li key={item} className="cd-s07__row">
                <span className="cd-s07__icon cd-s07__icon--bad" aria-hidden="true">
                  ✕
                </span>
                <span className="cd-s07__text">{item}</span>
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
