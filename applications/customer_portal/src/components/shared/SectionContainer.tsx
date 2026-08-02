import type { HTMLAttributes, ReactNode } from "react";
import { BaseContainer, BaseStack } from "../base";
import type { BaseContainerWidth, BaseSpacing } from "../base";
import { cx } from "../../utils";

export type SectionContainerProps = HTMLAttributes<HTMLElement> & {
  width?: BaseContainerWidth;
  gap?: BaseSpacing;
  children?: ReactNode;
};

/** Shared section shell with reading-width container. */
export function SectionContainer({
  width = "reading",
  gap = "block",
  className,
  children,
  ...rest
}: SectionContainerProps) {
  return (
    <BaseContainer
      as="section"
      width={width}
      className={cx("cui-shared-section-container", className)}
      {...rest}
    >
      <BaseStack gap={gap}>{children}</BaseStack>
    </BaseContainer>
  );
}
