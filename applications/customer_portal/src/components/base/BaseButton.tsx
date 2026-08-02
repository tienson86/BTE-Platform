import type { ButtonHTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseSize } from "./types";

export type BaseButtonVariant = "primary" | "secondary" | "ghost" | "danger";

export type BaseButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: BaseButtonVariant;
  size?: BaseSize;
  loading?: boolean;
  children?: ReactNode;
};

/** Primitive action control. Presentation only. */
export function BaseButton({
  variant = "primary",
  size = "md",
  loading = false,
  disabled,
  className,
  children,
  type = "button",
  ...rest
}: BaseButtonProps) {
  return (
    <button
      type={type}
      className={cx("cui-base-button", className)}
      data-variant={variant}
      data-size={size}
      disabled={disabled || loading}
      aria-busy={loading || undefined}
      {...rest}
    >
      {loading ? <span className="cui-base-spinner" data-size="sm" aria-hidden="true" /> : null}
      {children}
    </button>
  );
}
