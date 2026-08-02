import type { AnchorHTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseLinkProps = AnchorHTMLAttributes<HTMLAnchorElement> & {
  children?: ReactNode;
};

/** Primitive text link. Presentation only. */
export function BaseLink({ className, children, ...rest }: BaseLinkProps) {
  return (
    <a className={cx("cui-base-link", className)} {...rest}>
      {children}
    </a>
  );
}
