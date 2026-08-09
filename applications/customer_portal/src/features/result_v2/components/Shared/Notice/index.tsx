import type { ReactNode } from "react";

export function Notice({
  children,
  tone = "warning",
}: {
  children: ReactNode;
  tone?: "warning" | "danger";
}) {
  return (
    <div className="rv2-notice" data-tone={tone} role="status">
      {children}
    </div>
  );
}
