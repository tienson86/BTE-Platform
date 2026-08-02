import type { HTMLAttributes, ReactNode } from "react";
import { BaseSurface, BaseStack } from "../base";
import type { BaseSpacing, BaseSurfaceVariant } from "../base";
import { cx } from "../../utils";

export type SectionSurfaceProps = HTMLAttributes<HTMLDivElement> & {
  variant?: BaseSurfaceVariant;
  gap?: BaseSpacing;
  children?: ReactNode;
};

/** Shared surfaced section block. */
export function SectionSurface({
  variant = "section",
  gap = "paragraph",
  className,
  children,
  ...rest
}: SectionSurfaceProps) {
  return (
    <BaseSurface variant={variant} className={cx(className)} {...rest}>
      <BaseStack gap={gap}>{children}</BaseStack>
    </BaseSurface>
  );
}
