import type { HTMLAttributes, ReactNode } from "react";
import { BaseText } from "../base";
import { cx } from "../../utils";

export type EvidenceRowProps = HTMLAttributes<HTMLDivElement> & {
  label: ReactNode;
  detail?: ReactNode;
  meta?: ReactNode;
};

/** Shared evidence presentation row. */
export function EvidenceRow({ label, detail, meta, className, ...rest }: EvidenceRowProps) {
  return (
    <div className={cx("cui-shared-evidence-row", className)} {...rest}>
      <div>
        <BaseText variant="body">{label}</BaseText>
        {detail ? (
          <BaseText variant="caption" tone="secondary">
            {detail}
          </BaseText>
        ) : null}
      </div>
      {meta ? (
        <BaseText variant="metadata" tone="muted">
          {meta}
        </BaseText>
      ) : null}
    </div>
  );
}
