import type { ReactNode } from "react";

export function Tag({ children }: { children: ReactNode }) {
  return <span className="rv2-tag">{children}</span>;
}
