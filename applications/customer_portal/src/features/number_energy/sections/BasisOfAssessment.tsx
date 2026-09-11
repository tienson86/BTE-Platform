import type { ReactNode } from "react";

import {
  GOLDEN_BASIS_EVIDENCE,
  GOLDEN_BASIS_HELPER,
  GOLDEN_BASIS_HIGHLIGHTS,
  GOLDEN_BASIS_PRINCIPLES,
  GOLDEN_BASIS_TITLE,
} from "../goldenBasis";

export function BasisOfAssessment(): ReactNode {
  return (
    <section className="bte-card ne-basis" data-section="P-S10" data-testid="basis-of-assessment">
      <h2>{GOLDEN_BASIS_TITLE}</h2>
      <p className="muted ne-basis-helper" data-testid="basis-helper">
        {GOLDEN_BASIS_HELPER}
      </p>
      <ul className="ne-basis-principles" data-testid="basis-principles">
        {GOLDEN_BASIS_PRINCIPLES.map((principle, index) => (
          <li key={principle} data-testid={`basis-principle-${index}`}>
            {principle}
          </li>
        ))}
      </ul>
      <dl className="ne-basis-highlights" data-testid="basis-highlights">
        {GOLDEN_BASIS_HIGHLIGHTS.map((row, index) => (
          <div key={row.label} className="ne-basis-highlight">
            <dt data-testid={`basis-highlight-label-${index}`}>{row.label}</dt>
            <dd data-testid={`basis-highlight-value-${index}`}>{row.value}</dd>
          </div>
        ))}
      </dl>
      <div className="ne-basis-evidence" data-testid="basis-evidence">
        {GOLDEN_BASIS_EVIDENCE.map((group, groupIndex) => (
          <div key={group.group} className="ne-basis-group">
            <h3 className="ne-basis-group-title" data-testid={`basis-group-${groupIndex}`}>
              {group.group}
            </h3>
            <ul className="ne-basis-items">
              {group.items.map((item, itemIndex) => (
                <li key={item} data-testid={`basis-item-${groupIndex}-${itemIndex}`}>
                  {item}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}
