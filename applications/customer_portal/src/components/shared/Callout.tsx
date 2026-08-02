import type { ReactNode } from "react";
import { BaseCallout } from "../base";
import type { BaseCalloutProps } from "../base";
import { cx } from "../../utils";

export type CalloutProps = BaseCalloutProps & {
  children?: ReactNode;
};

/** Shared callout composed from BaseCallout. */
export function Callout({ children, className, ...rest }: CalloutProps) {
  return (
    <BaseCallout className={cx("cui-shared-box", className)} {...rest}>
      {children}
    </BaseCallout>
  );
}
