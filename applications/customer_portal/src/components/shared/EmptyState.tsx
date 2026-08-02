import type { ReactNode } from "react";
import { BaseEmptyState } from "../base";
import type { BaseEmptyStateProps } from "../base";
import { cx } from "../../utils";

export type EmptyStateProps = BaseEmptyStateProps & { children?: ReactNode };

/** Shared empty state composed from BaseEmptyState. */
export function EmptyState({ className, ...rest }: EmptyStateProps) {
  return <BaseEmptyState className={cx(className)} {...rest} />;
}
