import type { HTMLAttributes } from "react";
import { BaseSkeleton, BaseStack } from "../base";
import { cx } from "../../utils";

export type SkeletonSectionProps = HTMLAttributes<HTMLDivElement> & {
  lines?: number;
};

/** Shared section skeleton placeholder. */
export function SkeletonSection({ lines = 3, className, ...rest }: SkeletonSectionProps) {
  return (
    <BaseStack gap="list" className={cx("cui-shared-skeleton-section", className)} {...rest}>
      <BaseSkeleton height="1.5rem" width="40%" />
      {Array.from({ length: lines }, (_, index) => (
        <BaseSkeleton key={index} height="1rem" />
      ))}
    </BaseStack>
  );
}
