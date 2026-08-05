import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type ToastTone = "neutral" | "success" | "warning" | "danger" | "info";

export type ToastProps = HTMLAttributes<HTMLDivElement> & {
  tone?: ToastTone;
  title?: ReactNode;
  children?: ReactNode;
  open?: boolean;
};

/** WP02 Toast — presentational toast surface (host manages open state). */
export function Toast({
  tone = "info",
  title,
  children,
  open = true,
  className,
  role = "status",
  ...rest
}: ToastProps) {
  if (!open) {
    return null;
  }
  return (
    <div
      className={cx("cui-toast", className)}
      data-tone={tone}
      role={role}
      {...rest}
    >
      {title ? <p className="cui-toast__title">{title}</p> : null}
      {children ? <div className="cui-toast__body">{children}</div> : null}
    </div>
  );
}
