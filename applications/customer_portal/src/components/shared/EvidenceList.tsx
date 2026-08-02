import type { HTMLAttributes, ReactNode } from "react";
import { BaseStack } from "../base";
import { cx } from "../../utils";

export type EvidenceListProps = HTMLAttributes<HTMLDivElement> & {
  children?: ReactNode;
};

/** Shared list of evidence rows. */
export function EvidenceList({ className, children, ...rest }: EvidenceListProps) {
  return (
    <BaseStack gap="list" className={cx("cui-shared-evidence-list", className)} {...rest}>
      {children}
    </BaseStack>
  );
}
