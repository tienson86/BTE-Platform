import type { ReactNode } from "react";

import { EMPTY_COPY } from "../catalog";

/**
 * Empty analytical value — production semantics until BZ-UI-03.
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
  value,
}: {
  preview: boolean;
  value?: string | number;
}): ReactNode {
  if (preview && value !== undefined && value !== "") {
    return (
      <span className="bte-rw-value" data-preview="fixture">
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
  tone,
}: {
  value?: number;
  max?: number;
  label: string;
  preview: boolean;
  tone?: string;
}): ReactNode {
  const ready = preview && typeof value === "number";
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
