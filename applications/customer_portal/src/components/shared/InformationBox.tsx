import type { ReactNode } from "react";
import { BaseCallout } from "../base";
import type { BaseCalloutProps } from "../base";

export type InformationBoxProps = Omit<BaseCalloutProps, "tone"> & {
  children?: ReactNode;
};

/** Shared informational box. */
export function InformationBox({ children, ...rest }: InformationBoxProps) {
  return (
    <BaseCallout tone="info" className="cui-shared-box" {...rest}>
      {children}
    </BaseCallout>
  );
}
