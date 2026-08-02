import {
  InformationBox,
  SectionHeader,
  SectionSurface,
  StatusBadge,
} from "../shared";
import type { BalancePanelViewModel } from "../../view_models/metrics";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { MetricIndicator } from "./MetricIndicator";
import { renderPresentationGate } from "./presentationGate";

export type BalancePanelProps = {
  data: BalancePanelViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Balance indicators panel — presentation only. */
export function BalancePanel({
  data,
  status = "ready",
  className,
}: BalancePanelProps) {
  const title = data.title ?? "Balance Indicators";

  return (
    <section className={cx("cui-biz-balance-panel", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading balance indicators",
          emptyTitle: "No balance indicators available",
          unavailableTitle: "Balance indicators unavailable",
          errorTitle: "Unable to load balance indicators",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader
            title={title}
            level={2}
            actions={<StatusBadge status="info">Balance</StatusBadge>}
          />
          <InformationBox title="Balance Summary">{data.summary}</InformationBox>
          <div className="cui-biz-balance-panel__indicators">
            {data.indicators.map((indicator) => (
              <MetricIndicator key={indicator.id} data={indicator} />
            ))}
          </div>
        </SectionSurface>,
      )}
    </section>
  );
}
