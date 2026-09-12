import type { ReactNode } from "react";

import { GOLDEN_DOMAIN_INSIGHTS } from "../goldenDomains";
import type { PresentationDomainCard, SlotRenderSource } from "../presentationContract";

export function DomainInsights({
  domains = GOLDEN_DOMAIN_INSIGHTS,
  slotSource = "GOLDEN_FIXTURE",
}: {
  domains?: readonly PresentationDomainCard[];
  slotSource?: SlotRenderSource;
}): ReactNode {
  return (
    <section
      className="bte-card ne-domains"
      data-section="P-S06"
      data-testid="domain-insights"
      data-slot-source={slotSource}
    >
      <h2>Ảnh hưởng theo lĩnh vực</h2>
      <p className="muted">Tài vận, công việc, quan hệ và các lĩnh vực đời sống liên quan.</p>
      <ol className="ne-domain-list" data-testid="domain-list">
        {domains.map((domain, index) => (
          <li key={`${domain.title}-${index}`} className="ne-domain-card" data-testid={`domain-card-${index}`}>
            <h3 className="ne-domain-title" data-testid={`domain-title-${index}`}>
              {domain.title}
            </h3>
            <p className="ne-domain-conclusion" data-testid={`domain-conclusion-${index}`}>
              {domain.conclusion}
            </p>
            <p className="ne-domain-narrative" data-testid={`domain-narrative-${index}`}>
              {domain.narrative}
            </p>
            {domain.caution ? (
              <p className="muted ne-domain-caution" data-testid={`domain-caution-${index}`}>
                {domain.caution}
              </p>
            ) : null}
          </li>
        ))}
      </ol>
    </section>
  );
}
