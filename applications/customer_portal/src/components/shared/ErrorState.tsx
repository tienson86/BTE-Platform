import type { ReactNode } from "react";
import { BaseErrorState } from "../base";
import type { BaseErrorStateProps } from "../base";
import { cx } from "../../utils";

export type ErrorStateProps = BaseErrorStateProps & { children?: ReactNode };

/** Shared error state. */
export function ErrorState({ className, ...rest }: ErrorStateProps) {
  return <BaseErrorState className={cx(className)} {...rest} />;
}
