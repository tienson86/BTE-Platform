/**
 * S06 — Dashboard Preview Card: THẬP THẦN
 * PACK_04: Presentation Adapter list preview + hasMore (fixed height / internal scroll).
 */

import type { ReactNode } from "react";
import { adaptPreviewList } from "../../../presentation";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

/**
 * S06 Ten Gods — Dashboard preview card.
 */
export function S06TenGods(): ReactNode {
  const data = useCanonicalDesktop().s06;
  const ranked = [...data.gods].sort(
    (a, b) => Number.parseFloat(b.score) - Number.parseFloat(a.score),
  );
  const preview = adaptPreviewList(ranked, 4);

  return (
    <section
      className="cd-s06 cd-preview-card"
      data-card-type="list"
      data-has-more={preview.hasMore ? "true" : "false"}
      aria-labelledby="cd-s06-title"
    >
      <div className="cd-s06__card">
        <h2 id="cd-s06-title" className="cd-s06__title ui-line-clamp-2">
          {data.title}
        </h2>

        <p className="cd-s06__preview-label">{data.visibleLabel || "Lộ can"}</p>

        <ul className="cd-s06__preview-list">
          {preview.items.map((god) => (
            <li key={god.name} className="cd-s06__preview-row">
              <span
                className="cd-s06__dot"
                style={{ background: god.color }}
                aria-hidden="true"
              />
              <span className="cd-s06__preview-name ui-line-clamp-1">{god.name}</span>
              <span className="cd-s06__preview-score">{god.score}</span>
            </li>
          ))}
        </ul>

        {data.hiddenGods && data.hiddenGods.length ? (
          <>
            <p className="cd-s06__preview-label">{data.hiddenLabel || "Tàng can"}</p>
            <ul className="cd-s06__preview-list">
              {data.hiddenGods.slice(0, 6).map((god) => (
                <li key={`hidden-${god.name}`} className="cd-s06__preview-row">
                  <span
                    className="cd-s06__dot"
                    style={{ background: god.color }}
                    aria-hidden="true"
                  />
                  <span className="cd-s06__preview-name ui-line-clamp-1">{god.name}</span>
                </li>
              ))}
            </ul>
          </>
        ) : null}

        {data.note ? <p className="cd-s06__note">{data.note}</p> : null}

        <button
          type="button"
          className="cd-preview-cta"
          data-has-more={preview.hasMore ? "true" : "false"}
          aria-label={
            preview.hasMore ? `${data.link} — còn ${preview.totalCount - preview.items.length} mục` : data.link
          }
        >
          {data.link}
        </button>
      </div>
    </section>
  );
}
