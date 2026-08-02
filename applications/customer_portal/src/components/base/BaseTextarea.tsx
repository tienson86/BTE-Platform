import type { TextareaHTMLAttributes } from "react";
import { cx } from "../../utils";

export type BaseTextareaProps = TextareaHTMLAttributes<HTMLTextAreaElement> & {
  invalid?: boolean;
};

/** Primitive multiline text input. */
export function BaseTextarea({
  invalid = false,
  className,
  ...rest
}: BaseTextareaProps) {
  return (
    <textarea
      className={cx("cui-base-textarea", "cui-base-control", className)}
      aria-invalid={invalid || undefined}
      {...rest}
    />
  );
}
