import type { ReactNode } from "react";
import { BaseCallout } from "../base";
import type { BaseCalloutProps } from "../base";

export type InsightBoxProps = Omit<BaseCalloutProps, "tone"> & {
  children?: ReactNode;
};

/** Shared insight annotation box. */
export function InsightBox({ children, ...rest }: InsightBoxProps) {
  return (
    <BaseCallout tone="info" className="cui-shared-box" {...rest}>
      {children}
    </BaseCallout>
  );
}
