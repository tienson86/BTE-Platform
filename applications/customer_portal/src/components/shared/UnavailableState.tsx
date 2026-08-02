import type { ReactNode } from "react";
import { BaseUnavailableState } from "../base";
import type { BaseUnavailableStateProps } from "../base";
import { cx } from "../../utils";

export type UnavailableStateProps = BaseUnavailableStateProps & { children?: ReactNode };

/** Shared unavailable state. */
export function UnavailableState({ className, ...rest }: UnavailableStateProps) {
  return <BaseUnavailableState className={cx(className)} {...rest} />;
}
