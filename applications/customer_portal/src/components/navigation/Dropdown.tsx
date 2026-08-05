import { useState, type HTMLAttributes, type ReactNode } from "react";
import { cx } from "../../utils";

export type DropdownProps = HTMLAttributes<HTMLDivElement> & {
  label: ReactNode;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children?: ReactNode;
};

/** WP02 Dropdown — disclosure pattern (no Base imports; WP-0011). */
export function Dropdown({
  label,
  open,
  onOpenChange,
  children,
  className,
  ...rest
}: DropdownProps) {
  const [internalOpen, setInternalOpen] = useState(false);
  const isControlled = open !== undefined;
  const isOpen = isControlled ? open : internalOpen;

  const setOpen = (next: boolean) => {
    if (!isControlled) {
      setInternalOpen(next);
    }
    onOpenChange?.(next);
  };

  return (
    <div className={cx("cui-dropdown", className)} data-open={isOpen || undefined} {...rest}>
      <button
        type="button"
        className="cui-base-button"
        data-variant="secondary"
        data-size="sm"
        aria-expanded={isOpen}
        aria-haspopup="menu"
        onClick={() => setOpen(!isOpen)}
      >
        {label}
      </button>
      {isOpen && children ? (
        <div className="cui-dropdown__panel" role="menu">
          {children}
        </div>
      ) : null}
    </div>
  );
}
