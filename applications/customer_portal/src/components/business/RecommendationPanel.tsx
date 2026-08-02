import { Callout, StatusBadge } from "../shared";
import type {
  ExecutiveRecommendationViewModel,
  PresentationStatus,
} from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type RecommendationPanelProps = {
  data: ExecutiveRecommendationViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Primary recommendation panel for Executive Summary. */
export function RecommendationPanel({
  data,
  status = "ready",
  className,
}: RecommendationPanelProps) {
  return (
    <section
      className={cx("cui-biz-recommendation", className)}
      aria-label={data.title}
    >
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading recommendation",
          emptyTitle: "No recommendation available",
          unavailableTitle: "Recommendation unavailable",
          errorTitle: "Unable to load recommendation",
        },
        <>
          <Callout tone="info" title={data.title}>
            {data.body}
          </Callout>
          {data.priorityLabel ? (
            <StatusBadge status="info">{data.priorityLabel}</StatusBadge>
          ) : null}
        </>,
      )}
    </section>
  );
}
