import type { HTMLAttributes } from "react";
import { BaseSkeleton, BaseStack, BaseSurface } from "../base";
import { cx } from "../../utils";

export type SkeletonMetricProps = HTMLAttributes<HTMLDivElement>;

/** Shared metric card skeleton. */
export function SkeletonMetric({ className, ...rest }: SkeletonMetricProps) {
  return (
    <BaseSurface variant="section" className={cx("cui-shared-skeleton-metric", className)} {...rest}>
      <BaseStack gap="inline">
        <BaseSkeleton height="0.75rem" width="45%" />
        <BaseSkeleton height="1.75rem" width="30%" />
      </BaseStack>
    </BaseSurface>
  );
}
