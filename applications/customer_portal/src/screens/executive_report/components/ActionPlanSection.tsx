/**
 * Action plan from NarrativeV2Presentation.action_plan. Wording unchanged.
 */

import type { ReactNode } from "react";
import type { NarrativeV2ActionView } from "../../../adapters/narrativeV2PresentationAdapter";
import { REPORT_ACTION_LABEL, REPORT_SECTION } from "../copy";
import { PrintCallout } from "../print/PrintCallout";
import { ReportSectionHeader } from "./ReportPrimitives";

type ActionPlanSectionProps = {
  readonly plan: NarrativeV2ActionView | null;
};

/**
 * Top Priority dominant, then actions, warnings, current period.
 */
export function ActionPlanSection({ plan }: ActionPlanSectionProps): ReactNode {
  if (!plan) return null;
  const priority = plan.top_priority?.title ? plan.top_priority : null;
  const actions = plan.actions.filter((item) => item.title || item.description);
  const warnings = plan.warnings.filter((item) => item.title || item.description);
  const period =
    plan.current_period?.title || plan.current_period?.description ? plan.current_period : null;
  if (!priority && !actions.length && !warnings.length && !period) return null;
  return (
    <section
      className="bte-er__section bte-er__action"
      data-report-section="action-plan"
      data-report-level="primary"
    >
      <ReportSectionHeader title={REPORT_SECTION.action} level="primary" />
      {priority ? (
        <PrintCallout label={REPORT_ACTION_LABEL.priority} tone="priority">
          <p
            className="bte-er__priority-title"
            data-action-priority-title="true"
            data-report-level="executive"
          >
            {priority.title}
          </p>
          {priority.description ? (
            <p className="bte-er__body" data-action-priority-description="true">
              {priority.description}
            </p>
          ) : null}
        </PrintCallout>
      ) : null}
      {actions.length ? (
        <div className="bte-er__plan-block" data-action-block="actions">
          <h3 className="bte-er__subhead">{REPORT_ACTION_LABEL.actions}</h3>
          <ol className="bte-er__plan-list">
            {actions.map((item, index) => (
              <li key={`${item.title}-${index}`} className="bte-er__plan-item">
                {item.title ? <p className="bte-er__plan-title">{item.title}</p> : null}
                {item.description ? <p className="bte-er__body">{item.description}</p> : null}
              </li>
            ))}
          </ol>
        </div>
      ) : null}
      {warnings.length ? (
        <div className="bte-er__plan-block" data-action-block="warnings">
          <h3 className="bte-er__subhead">{REPORT_ACTION_LABEL.warnings}</h3>
          <ul className="bte-er__plan-list">
            {warnings.map((item, index) => (
              <li key={`${item.title}-${index}`} className="bte-er__plan-item">
                {item.title ? <p className="bte-er__plan-title">{item.title}</p> : null}
                {item.description ? <p className="bte-er__body">{item.description}</p> : null}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
      {period ? (
        <div className="bte-er__plan-block" data-action-block="period">
          <h3 className="bte-er__subhead">{REPORT_ACTION_LABEL.period}</h3>
          {period.title ? <p className="bte-er__plan-title">{period.title}</p> : null}
          {period.description ? <p className="bte-er__body">{period.description}</p> : null}
        </div>
      ) : null}
    </section>
  );
}
