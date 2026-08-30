/**
 * Luck / timing from canonical Luck adapter. No tốt/xấu inference.
 */

import type { ReactNode } from "react";
import type { LuckView } from "../../commercial_dashboard/types";
import { REPORT_LUCK_LABEL, REPORT_SECTION } from "../copy";
import { ReportSectionHeader } from "./ReportPrimitives";

type LuckSectionProps = {
  readonly luck: LuckView;
};

/**
 * Khởi vận, current Đại Vận, timeline, next Đại Vận.
 */
export function LuckSection({ luck }: LuckSectionProps): ReactNode {
  if (!luck.available) return null;
  const start = [luck.direction, luck.startAge].filter(Boolean).join(" · ");
  return (
    <section
      className="bte-er__section bte-er__luck"
      data-report-section="luck"
      data-report-level="detailed"
      data-viz="timeline"
    >
      <ReportSectionHeader title={REPORT_SECTION.luck} level="detailed" />
      {start ? (
        <div className="bte-er__luck-block" data-luck-section="start">
          <h3 className="bte-er__subhead">{REPORT_LUCK_LABEL.start}</h3>
          <p className="bte-er__body">{start}</p>
        </div>
      ) : null}
      {luck.current ? (
        <div className="bte-er__luck-block" data-luck-section="current">
          <h3 className="bte-er__subhead">{REPORT_LUCK_LABEL.current}</h3>
          <p className="bte-er__luck-current">
            <span data-luck-current-name="true">{luck.current.ganZhi}</span>
            {luck.current.yearRange ? (
              <span data-luck-current-years="true"> · {luck.current.yearRange}</span>
            ) : null}
          </p>
        </div>
      ) : null}
      {luck.cycles.length ? (
        <div className="bte-er__luck-block" data-luck-section="timeline">
          <h3 className="bte-er__subhead">{REPORT_LUCK_LABEL.timeline}</h3>
          <ol className="bte-er__timeline" data-viz-chart="timeline">
            {luck.cycles.map((cycle) => (
              <li
                key={`${cycle.ganZhi}-${cycle.yearRange}`}
                className="bte-er__timeline-item"
                data-luck-current={cycle.isCurrent ? "true" : undefined}
              >
                <span className="bte-er__timeline-name">{cycle.ganZhi}</span>
                {cycle.yearRange ? (
                  <span className="bte-er__caption">{cycle.yearRange}</span>
                ) : null}
              </li>
            ))}
          </ol>
        </div>
      ) : null}
      {luck.next ? (
        <div className="bte-er__luck-block" data-luck-section="next">
          <h3 className="bte-er__subhead">{REPORT_LUCK_LABEL.next}</h3>
          <p className="bte-er__body">
            {luck.next.ganZhi}
            {luck.next.yearRange ? ` · ${luck.next.yearRange}` : ""}
          </p>
        </div>
      ) : null}
    </section>
  );
}
