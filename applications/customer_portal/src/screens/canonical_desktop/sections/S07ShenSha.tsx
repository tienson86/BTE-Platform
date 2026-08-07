/**
 * S07 — Dashboard Preview Card: THẦN SÁT
 * PACK_04: Presentation Adapter list preview + hasMore (fixed height / internal scroll).
 */

import type { ReactNode } from "react";
import { adaptPreviewList, adaptPreviewText } from "../../../presentation";
import { PresentationText } from "../../../components/shared/PresentationText";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

/**
 * S07 Shen Sha — Dashboard preview card.
 */
export function S07ShenSha(): ReactNode {
  const data = useCanonicalDesktop().s07;
  const good = adaptPreviewList(data.good.items, 3);
  const bad = adaptPreviewList(data.bad.items, 2);
  const execLine = adaptPreviewText(data.executive.line2, "summary");
  const hasMore = good.hasMore || bad.hasMore || execLine.hasMore;

  return (
    <section
      className="cd-s07 cd-preview-card"
      data-card-type="list"
      data-has-more={hasMore ? "true" : "false"}
      aria-labelledby="cd-s07-title"
    >
      <div className="cd-s07__card">
        <h2 id="cd-s07-title" className="cd-s07__title ui-line-clamp-2">
          {data.title}
        </h2>

        <div className="cd-s07__exec">
          <PresentationText
            className="cd-s07__exec-line"
            typeRole="summary"
            preview={execLine}
            as="p"
          />
        </div>

        <div className="cd-s07__group">
          <h3 className="cd-s07__group-title cd-s07__group-title--good">
            ● CÁT TINH
          </h3>
          <ul className="cd-s07__list">
            {good.items.map((item) => (
              <li key={item} className="cd-s07__row">
                <span className="cd-s07__icon cd-s07__icon--good" aria-hidden="true">
                  ✓
                </span>
                <span className="cd-s07__text ui-line-clamp-2">{item}</span>
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
            {bad.items.map((item) => (
              <li key={item} className="cd-s07__row">
                <span className="cd-s07__icon cd-s07__icon--bad" aria-hidden="true">
                  ✕
                </span>
                <span className="cd-s07__text ui-line-clamp-2">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <button
          type="button"
          className="cd-preview-cta"
          data-has-more={hasMore ? "true" : "false"}
          aria-label={hasMore ? `${data.link} — còn nội dung đầy đủ` : data.link}
        >
          {data.link}
        </button>
      </div>
    </section>
  );
}
