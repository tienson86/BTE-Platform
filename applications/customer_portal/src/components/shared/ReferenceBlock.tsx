import type { HTMLAttributes, ReactNode } from "react";
import { BaseStack, BaseText } from "../base";
import { cx } from "../../utils";

export type ReferenceBlockProps = HTMLAttributes<HTMLElement> & {
  title?: ReactNode;
  children?: ReactNode;
};

/** Shared reference block container. */
export function ReferenceBlock({
  title = "References",
  className,
  children,
  ...rest
}: ReferenceBlockProps) {
  return (
    <BaseStack
      as="section"
      gap="list"
      className={cx("cui-shared-reference-block", className)}
      {...rest}
    >
      <BaseText variant="section">{title}</BaseText>
      {children}
    </BaseStack>
  );
}
