/**
 * S07 — Dashboard Preview Card: THẦN SÁT
 * PACK_04: Presentation Adapter list preview + hasMore (fixed height / internal scroll).
 * Copies engine presence + evidence. Does not classify Cát/Hung.
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
  const preview = adaptPreviewList(
    data.items.map((item) => item.name),
    5,
  );
  const execLine = adaptPreviewText(data.executive.line1, "summary");
  const hasMore = preview.hasMore || execLine.hasMore;
  const rows = preview.items
    .map((name) => data.items.find((item) => item.name === name))
    .filter((item): item is (typeof data.items)[number] => Boolean(item));

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

        <ul className="cd-s07__list">
          {rows.map((item) => (
            <li key={item.name} className="cd-s07__entry">
              <span className="cd-s07__name ui-line-clamp-2">{item.name}</span>
              <span className="cd-s07__presence ui-line-clamp-2">{item.presence}</span>
              {item.evidence ? (
                <span className="cd-s07__evidence ui-line-clamp-2">{item.evidence}</span>
              ) : null}
            </li>
          ))}
        </ul>

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
