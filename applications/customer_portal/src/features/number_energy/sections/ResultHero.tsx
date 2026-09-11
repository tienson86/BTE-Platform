import type { ReactNode } from "react";

import { GOLDEN_PHONE_HERO } from "../goldenHero";

export function ResultHero(): ReactNode {
  const hero = GOLDEN_PHONE_HERO;

  return (
    <section className="bte-card ne-hero" data-section="P-S00" data-testid="result-hero">
      <h2 className="ne-hero__eyebrow">{hero.eyebrow}</h2>
      <p className="ne-hero__type" data-testid="hero-analysis-type">
        {hero.analysisTypeLabel}
      </p>
      <p className="ne-hero__identity" data-testid="hero-identity">
        {hero.displayValue}
      </p>
      <div className="ne-hero__metrics">
        <div className="ui-metric ne-hero__metric" data-testid="hero-score-card">
          <span className="ui-metric-label">Điểm đánh giá</span>
          <span className="ui-metric-value ne-hero__score" data-testid="hero-score">
            {hero.scoreDisplay}
          </span>
          <span className="ne-hero__grade" data-testid="hero-grade">
            {hero.grade}
          </span>
        </div>
        <div className="ui-metric ne-hero__metric" data-testid="hero-primary-card">
          <span className="ui-metric-label">{hero.primaryLabel}</span>
          <span className="ui-metric-value" data-testid="hero-primary-energy">
            {hero.primaryEnergy}
          </span>
          <span className="muted ne-hero__hint">{hero.primaryKeywords}</span>
        </div>
        <div className="ui-metric ne-hero__metric" data-testid="hero-terminal-card">
          <span className="ui-metric-label">{hero.terminalLabel}</span>
          <span className="ui-metric-value" data-testid="hero-terminal-energy">
            {hero.terminalEnergy}
          </span>
          <span className="muted ne-hero__hint">{hero.terminalKeywords}</span>
        </div>
      </div>
      <p className="ne-hero__summary" data-testid="hero-summary">
        {hero.summary}
      </p>
    </section>
  );
}
