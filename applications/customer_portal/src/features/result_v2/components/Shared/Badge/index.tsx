import type { ReactNode } from "react";

export type ResultV2BadgeTone = "neutral" | "warning" | "danger" | "success";

export function Badge({
  children,
  tone = "neutral",
}: {
  children: ReactNode;
  tone?: ResultV2BadgeTone;
}) {
  return (
    <span className="rv2-badge" data-tone={tone}>
      {children}
    </span>
  );
}
