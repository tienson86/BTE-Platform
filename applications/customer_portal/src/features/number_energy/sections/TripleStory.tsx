import type { ReactNode } from "react";

import { GOLDEN_PHONE_TRIPLES, type GoldenTripleCard } from "../goldenTriples";

function TripleCard({ triple, index }: { triple: GoldenTripleCard; index: number }): ReactNode {
  const compact = triple.priority === "compact";

  return (
    <article
      className="ne-triple-card"
      data-testid={`triple-card-${index}`}
      data-triple-digits={triple.digits}
      data-priority={triple.priority}
    >
      <p className="ne-triple-digits" data-testid={`triple-digits-${index}`}>
        {triple.digits}
      </p>
      <p className="ne-triple-flow" data-testid={`triple-flow-${index}`}>
        <span data-testid={`triple-source-${index}`}>{triple.sourceLabel}</span>
        <span className="ne-sr-only"> tiếp đến </span>
        <span className="ne-triple-arrow" aria-hidden="true">
          →
        </span>
        <span data-testid={`triple-target-${index}`}>{triple.targetLabel}</span>
      </p>
      <h3 className="ne-triple-title" data-testid={`triple-title-${index}`}>
        {triple.title}
      </h3>
      {compact ? null : (
        <>
          <p className="ne-triple-narrative">{triple.narrative}</p>
          <p className="muted ne-triple-domains">{triple.domains}</p>
        </>
      )}
    </article>
  );
}

export function TripleStory(): ReactNode {
  return (
    <section className="bte-card ne-triple-story" data-section="P-S04" data-testid="triple-story">
      <h2>Luận các bộ 3 số</h2>
      <p className="muted">Hai trường khí liên tiếp kết hợp để hình thành ý nghĩa của từng bộ ba.</p>
      <ol className="ne-triple-list" data-testid="triple-list">
        {GOLDEN_PHONE_TRIPLES.map((triple, index) => (
          <li key={`${triple.digits}-${index}`} className="ne-triple-item" data-priority={triple.priority}>
            <TripleCard triple={triple} index={index} />
          </li>
        ))}
      </ol>
    </section>
  );
}
