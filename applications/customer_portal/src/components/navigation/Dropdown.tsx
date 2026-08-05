import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import { BaseButton } from "../base/BaseButton";

export type DropdownProps = HTMLAttributes<HTMLDivElement> & {
  label: ReactNode;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children?: ReactNode;
};

/** WP02 Dropdown — disclosure pattern (caller may control open). */
export function Dropdown({
  label,
  open,
  onOpenChange,
  children,
  className,
  ...rest
}: DropdownProps) {
  const uncontrolled = open === undefined;
  return (
    <div className={cx("cui-dropdown", className)} data-open={open || undefined} {...rest}>
      <BaseButton
        variant="secondary"
        size="sm"
        aria-expanded={open ?? undefined}
        aria-haspopup="menu"
        onClick={() => onOpenChange?.(!(open ?? false))}
      >
        {label}
      </BaseButton>
      {(uncontrolled || open) && children ? (
        <div className="cui-dropdown__panel" role="menu">
          {children}
        </div>
      ) : null}
    </div>
  );
}
