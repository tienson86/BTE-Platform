import type { HTMLAttributes } from "react";
import { BaseSkeleton, BaseStack } from "../base";
import { cx } from "../../utils";

export type SkeletonParagraphProps = HTMLAttributes<HTMLDivElement> & {
  lines?: number;
};

/** Shared paragraph skeleton. */
export function SkeletonParagraph({
  lines = 4,
  className,
  ...rest
}: SkeletonParagraphProps) {
  return (
    <BaseStack gap="inline" className={cx("cui-shared-skeleton-paragraph", className)} {...rest}>
      {Array.from({ length: lines }, (_, index) => (
        <BaseSkeleton
          key={index}
          height="1rem"
          width={index === lines - 1 ? "70%" : "100%"}
        />
      ))}
    </BaseStack>
  );
}
