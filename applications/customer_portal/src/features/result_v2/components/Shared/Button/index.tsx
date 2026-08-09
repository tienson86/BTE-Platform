import type { ButtonHTMLAttributes, ReactNode } from "react";

export type ResultV2ButtonVariant = "primary" | "secondary" | "text";

export type ResultV2ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ResultV2ButtonVariant;
  children: ReactNode;
};

export function Button({
  variant = "primary",
  type = "button",
  children,
  ...rest
}: ResultV2ButtonProps) {
  return (
    <button type={type} className="rv2-button" data-variant={variant} {...rest}>
      {children}
    </button>
  );
}
