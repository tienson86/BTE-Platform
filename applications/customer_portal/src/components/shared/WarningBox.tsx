import type { ReactNode } from "react";
import { BaseCallout } from "../base";
import type { BaseCalloutProps } from "../base";

export type WarningBoxProps = Omit<BaseCalloutProps, "tone"> & {
  children?: ReactNode;
};

/** Shared warning box. */
export function WarningBox({ children, ...rest }: WarningBoxProps) {
  return (
    <BaseCallout tone="warning" className="cui-shared-box" {...rest}>
      {children}
    </BaseCallout>
  );
}
