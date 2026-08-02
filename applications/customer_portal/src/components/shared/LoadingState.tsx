import type { ReactNode } from "react";
import { BaseLoadingState } from "../base";
import type { BaseLoadingStateProps } from "../base";
import { cx } from "../../utils";

export type LoadingStateProps = BaseLoadingStateProps & { children?: ReactNode };

/** Shared loading state. */
export function LoadingState({ className, ...rest }: LoadingStateProps) {
  return <BaseLoadingState className={cx(className)} {...rest} />;
}
