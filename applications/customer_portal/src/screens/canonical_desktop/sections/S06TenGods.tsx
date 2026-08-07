/**
 * S06 — Dashboard Preview Card: THẬP THẦN
 */

import type { ReactNode } from "react";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

/**
 * S06 Ten Gods — Dashboard preview card.
 */
export function S06TenGods(): ReactNode {
  const data = useCanonicalDesktop().s06;
  const previewGods = [...data.gods]
    .sort((a, b) => Number.parseFloat(b.score) - Number.parseFloat(a.score))
    .slice(0, 4);

  return (
    <section className="cd-s06 cd-preview-card" aria-labelledby="cd-s06-title">
      <div className="cd-s06__card">
        <h2 id="cd-s06-title" className="cd-s06__title">
          {data.title}
        </h2>

        <p className="cd-s06__preview-label">Tóm tắt Thập thần nổi bật</p>

        <ul className="cd-s06__preview-list">
          {previewGods.map((god) => (
            <li key={god.name} className="cd-s06__preview-row">
              <span
                className="cd-s06__dot"
                style={{ background: god.color }}
                aria-hidden="true"
              />
              <span className="cd-s06__preview-name">{god.name}</span>
              <span className="cd-s06__preview-score">{god.score}</span>
            </li>
          ))}
        </ul>

        <button type="button" className="cd-preview-cta">
          {data.link}
        </button>
      </div>
    </section>
  );
}
