import type { HTMLAttributes, ReactNode } from "react";
import { BaseText } from "../base";
import { cx } from "../../utils";

export type FooterNoteProps = HTMLAttributes<HTMLElement> & {
  children?: ReactNode;
};

/** Shared footer note / disclaimer. */
export function FooterNote({ className, children, ...rest }: FooterNoteProps) {
  return (
    <footer className={cx("cui-shared-footer-note", className)} {...rest}>
      <BaseText variant="metadata" tone="muted">
        {children}
      </BaseText>
    </footer>
  );
}
