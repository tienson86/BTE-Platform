import type { ReactNode } from "react";
import { BaseCallout } from "../base";
import type { BaseCalloutProps } from "../base";

export type SuccessBoxProps = Omit<BaseCalloutProps, "tone"> & {
  children?: ReactNode;
};

/** Shared success box. */
export function SuccessBox({ children, ...rest }: SuccessBoxProps) {
  return (
    <BaseCallout tone="success" className="cui-shared-box" {...rest}>
      {children}
    </BaseCallout>
  );
}
