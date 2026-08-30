/**
 * Interpretation: consulting_flow first, structured zones below. No concatenation.
 */

import type { ReactNode } from "react";
import type { NarrativeV2InterpretationView } from "../../../adapters/narrativeV2PresentationAdapter";
import { REPORT_DETAIL_LABEL, REPORT_SECTION } from "../copy";
import { ReportSectionHeader } from "./ReportPrimitives";

type InterpretationSectionProps = {
  readonly interpretation: NarrativeV2InterpretationView | null;
};

const DETAIL_KEYS = [
  "observation",
  "reasoning",
  "meaning",
  "impact",
  "recommendation",
  "closing",
] as const;

/**
 * Primary consulting narrative, then optional structured disclosure.
 */
export function InterpretationSection({ interpretation }: InterpretationSectionProps): ReactNode {
  if (!interpretation) return null;
  const flow = interpretation.consulting_flow;
  const details = DETAIL_KEYS.flatMap((key) => {
    const text = interpretation[key];
    return text ? [{ key, label: REPORT_DETAIL_LABEL[key], text }] : [];
  });
  if (!flow && !details.length) return null;
  return (
    <section
      className="bte-er__section bte-er__interpretation"
      data-report-section="interpretation"
    >
      <ReportSectionHeader title={REPORT_SECTION.interpretation} level="primary" />
      {flow ? (
        <p
          className="bte-er__narrative"
          data-consulting-flow="true"
          data-report-level="executive"
        >
          {flow}
        </p>
      ) : null}
      {details.length ? (
        <div className="bte-er__detail" data-report-level="detailed">
          <h3 className="bte-er__subhead">{REPORT_SECTION.interpretationDetail}</h3>
          {details.map((item) => (
            <section key={item.key} className="bte-er__zone" data-interpretation-zone={item.key}>
              <h4 className="bte-er__zone-title">{item.label}</h4>
              <p className="bte-er__body">{item.text}</p>
            </section>
          ))}
        </div>
      ) : null}
    </section>
  );
}
