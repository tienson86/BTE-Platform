import type { ReactNode } from "react";

import {
  GOLDEN_BASIS_EVIDENCE,
  GOLDEN_BASIS_HELPER,
  GOLDEN_BASIS_HIGHLIGHTS,
  GOLDEN_BASIS_PRINCIPLES,
  GOLDEN_BASIS_TITLE,
} from "../goldenBasis";
import type { PresentationBasis, SlotRenderSource } from "../presentationContract";

const GOLDEN_BASIS: PresentationBasis = {
  title: GOLDEN_BASIS_TITLE,
  helper: GOLDEN_BASIS_HELPER,
  principles: GOLDEN_BASIS_PRINCIPLES,
  highlights: GOLDEN_BASIS_HIGHLIGHTS,
  evidence: GOLDEN_BASIS_EVIDENCE,
};

export function BasisOfAssessment({
  basis = GOLDEN_BASIS,
  slotSource = "GOLDEN_FIXTURE",
}: {
  basis?: PresentationBasis;
  slotSource?: SlotRenderSource;
}): ReactNode {
  return (
    <section
      className="bte-card ne-basis"
      data-section="P-S10"
      data-testid="basis-of-assessment"
      data-slot-source={slotSource}
    >
      <h2>{basis.title}</h2>
      <p className="muted ne-basis-helper" data-testid="basis-helper">
        {basis.helper}
      </p>
      <ul className="ne-basis-principles" data-testid="basis-principles">
        {basis.principles.map((principle, index) => (
          <li key={`${principle}-${index}`} data-testid={`basis-principle-${index}`}>
            {principle}
          </li>
        ))}
      </ul>
      <dl className="ne-basis-highlights" data-testid="basis-highlights">
        {basis.highlights.map((row, index) => (
          <div key={`${row.label}-${index}`} className="ne-basis-highlight">
            <dt data-testid={`basis-highlight-label-${index}`}>{row.label}</dt>
            <dd data-testid={`basis-highlight-value-${index}`}>{row.value}</dd>
          </div>
        ))}
      </dl>
      <div className="ne-basis-evidence" data-testid="basis-evidence">
        {basis.evidence.map((group, groupIndex) => (
          <div key={`${group.group}-${groupIndex}`} className="ne-basis-group">
            <h3 className="ne-basis-group-title" data-testid={`basis-group-${groupIndex}`}>
              {group.group}
            </h3>
            <ul className="ne-basis-items">
              {group.items.map((item, itemIndex) => (
                <li key={`${item}-${itemIndex}`} data-testid={`basis-item-${groupIndex}-${itemIndex}`}>
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
