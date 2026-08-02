import type { HTMLAttributes, ReactNode } from "react";
import { BaseText } from "../base";
import { cx } from "../../utils";

export type CitationRowProps = HTMLAttributes<HTMLDivElement> & {
  citation: ReactNode;
  source?: ReactNode;
};

/** Shared citation row. */
export function CitationRow({ citation, source, className, ...rest }: CitationRowProps) {
  return (
    <div className={cx("cui-shared-citation-row", className)} {...rest}>
      <BaseText variant="body">{citation}</BaseText>
      {source ? (
        <BaseText variant="metadata" tone="muted">
          {source}
        </BaseText>
      ) : null}
    </div>
  );
}
