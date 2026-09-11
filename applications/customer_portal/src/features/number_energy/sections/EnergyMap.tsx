import type { ReactNode } from "react";

import { GOLDEN_PHONE_PAIRS, type GoldenPairCard } from "../goldenPairs";

function PairCard({ pair, index }: { pair: GoldenPairCard; index: number }): ReactNode {
  const tone = pair.categoryLabel === "Hung" ? "caution" : "support";

  return (
    <article
      className="ne-pair-card"
      data-testid={`pair-card-${index}`}
      data-pair-digits={pair.digits}
      data-pair-tone={tone}
    >
      <p className="ne-pair-digits" data-testid={`pair-digits-${index}`}>
        {pair.digits}
      </p>
      <p className="ne-pair-energy" data-testid={`pair-energy-${index}`}>
        {pair.energyLabel}
      </p>
      <div className="ne-pair-strength" aria-label={pair.strengthLabel}>
        {pair.strengthDots.map((filled, dotIndex) => (
          <span
            key={`${pair.digits}-dot-${dotIndex}`}
            className="ne-pair-dot"
            data-filled={filled ? "true" : "false"}
          />
        ))}
        <span className="ne-pair-strength-label" data-testid={`pair-strength-${index}`}>
          {pair.strengthLabel}
        </span>
      </div>
      <p className="ne-pair-category" data-testid={`pair-category-${index}`}>
        {pair.categoryLabel}
      </p>
      <p className="muted ne-pair-keywords">{pair.keywords}</p>
    </article>
  );
}

export function EnergyMap(): ReactNode {
  return (
    <section className="bte-card ne-energy-map" data-section="P-S01" data-testid="energy-map">
      <h2>Cấu trúc dãy số</h2>
      <p className="muted">Các cặp số được đọc liên tiếp theo thứ tự xuất hiện trong dãy.</p>
      <ol className="ne-pair-strip" data-testid="pair-strip">
        {GOLDEN_PHONE_PAIRS.map((pair, index) => (
          <li key={`pair-${index}-${pair.digits}`} className="ne-pair-item">
            {index > 0 ? (
              <span className="ne-pair-connector" aria-hidden="true">
                →
              </span>
            ) : null}
            <PairCard pair={pair} index={index} />
          </li>
        ))}
      </ol>
    </section>
  );
}
