import type { ReactNode } from "react";
import { BaseStack, BaseSurface, BaseText } from "../base";
import { cx } from "../../utils";

export type HighlightBoxProps = {
  title?: ReactNode;
  children?: ReactNode;
  className?: string;
};

/** Shared highlight annotation box. */
export function HighlightBox({ title, children, className }: HighlightBoxProps) {
  return (
    <BaseSurface variant="callout" className={cx("cui-shared-box", className)}>
      <BaseStack gap="list">
        {title ? <BaseText variant="subsection">{title}</BaseText> : null}
        {children ? (
          <BaseText variant="body" tone="secondary">
            {children}
          </BaseText>
        ) : null}
      </BaseStack>
    </BaseSurface>
  );
}
