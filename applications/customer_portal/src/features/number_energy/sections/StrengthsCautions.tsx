import type { ReactNode } from "react";

import { GOLDEN_CAUTIONS, GOLDEN_STRENGTHS } from "../goldenStrengths";
import type { PresentationFindings, SlotRenderSource } from "../presentationContract";

const GOLDEN_FINDINGS: PresentationFindings = {
  strengths: GOLDEN_STRENGTHS,
  cautions: GOLDEN_CAUTIONS,
};

export function StrengthsCautions({
  findings = GOLDEN_FINDINGS,
  slotSource = "GOLDEN_FIXTURE",
}: {
  findings?: PresentationFindings;
  slotSource?: SlotRenderSource;
}): ReactNode {
  return (
    <section
      className="bte-card ne-findings"
      data-section="P-S07"
      data-testid="strengths-cautions"
      data-slot-source={slotSource}
    >
      <h2>Điểm mạnh và điểm cần lưu ý</h2>
      <p className="muted">Hai mặt của dãy số, không chỉ phần thuận.</p>
      <div className="ne-findings-grid" data-testid="findings-grid">
        <div className="ne-findings-column" data-testid="strengths-column">
          <h3 className="ne-findings-heading">Điểm mạnh</h3>
          <ol className="ne-finding-list" data-testid="strength-list">
            {findings.strengths.map((finding, index) => (
              <li key={`${finding.title}-${index}`} className="ne-finding-item" data-testid={`strength-card-${index}`}>
                <h4 className="ne-finding-title" data-testid={`strength-title-${index}`}>
                  {finding.title}
                </h4>
                <p className="ne-finding-copy" data-testid={`strength-copy-${index}`}>
                  {finding.copy}
                </p>
              </li>
            ))}
          </ol>
        </div>
        <div className="ne-findings-column ne-findings-column--caution" data-testid="cautions-column">
          <h3 className="ne-findings-heading">Điểm cần lưu ý</h3>
          <ol className="ne-finding-list" data-testid="caution-list">
            {findings.cautions.map((finding, index) => (
              <li
                key={`${finding.title}-${index}`}
                className="ne-finding-item ne-finding-item--caution"
                data-testid={`caution-card-${index}`}
              >
                <h4 className="ne-finding-title" data-testid={`caution-title-${index}`}>
                  {finding.title}
                </h4>
                <p className="ne-finding-copy" data-testid={`caution-copy-${index}`}>
                  {finding.copy}
                </p>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </section>
  );
}
