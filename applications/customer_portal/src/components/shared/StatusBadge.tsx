import type { ReactNode } from "react";
import { BaseBadge } from "../base";
import type { BaseBadgeProps, BaseTone } from "../base";

export type StatusBadgeProps = Omit<BaseBadgeProps, "tone" | "children"> & {
  status?: BaseTone;
  children?: ReactNode;
};

/** Shared status badge mapped to semantic tones. */
export function StatusBadge({ status = "neutral", children, ...rest }: StatusBadgeProps) {
  return (
    <BaseBadge tone={status} {...rest}>
      {children}
    </BaseBadge>
  );
}
