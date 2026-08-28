import type { ReactNode } from "react";

import { EMPTY_COPY } from "../catalog";

/**
 * Empty analytical value — field exists on the page but is not published.
 */
export function EmptyValue(): ReactNode {
  return (
    <span className="bte-rw-empty" data-empty="true">
      {EMPTY_COPY}
    </span>
  );
}

export function SlotValue({
  preview,
  bound,
  value,
}: {
  preview?: boolean;
  bound?: boolean;
  value?: string | number | null;
}): ReactNode {
  const ready = (preview || bound) && value !== undefined && value !== null && value !== "";
  if (ready) {
    return (
      <span
        className="bte-rw-value"
        data-preview={preview ? "fixture" : undefined}
        data-bound={bound && !preview ? "canonical" : undefined}
      >
        {value}
      </span>
    );
  }
  return <EmptyValue />;
}

export function VisualMeter({
  value,
  max = 100,
  label,
  preview,
  bound,
  tone,
}: {
  value?: number | null;
  max?: number;
  label: string;
  preview?: boolean;
  bound?: boolean;
  tone?: string;
}): ReactNode {
  const ready = (preview || bound) && typeof value === "number";
  const pct = ready ? Math.max(0, Math.min(100, (value / max) * 100)) : 0;
  return (
    <div
      className="bte-rw-meter"
      role="meter"
      aria-label={label}
      aria-valuemin={0}
      aria-valuemax={max}
      aria-valuenow={ready ? value : undefined}
      aria-valuetext={ready ? `${value} / ${max}` : EMPTY_COPY}
      data-empty={ready ? "false" : "true"}
      data-tone={tone}
    >
      <div className="bte-rw-meter__fill" style={{ width: `${pct}%` }} />
    </div>
  );
}
