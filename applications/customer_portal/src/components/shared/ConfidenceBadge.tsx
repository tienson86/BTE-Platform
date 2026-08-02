import type { ReactNode } from "react";
import { BaseBadge } from "../base";
import type { BaseBadgeProps } from "../base";

export type ConfidenceLevel = "low" | "medium" | "high";

export type ConfidenceBadgeProps = Omit<BaseBadgeProps, "tone" | "children"> & {
  level?: ConfidenceLevel;
  children?: ReactNode;
};

const LEVEL_TONE = {
  low: "warning",
  medium: "info",
  high: "success",
} as const;

/** Shared confidence indicator badge. */
export function ConfidenceBadge({
  level = "medium",
  children,
  ...rest
}: ConfidenceBadgeProps) {
  return (
    <BaseBadge tone={LEVEL_TONE[level]} {...rest}>
      {children ?? level}
    </BaseBadge>
  );
}
