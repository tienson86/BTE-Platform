/**
 * Mobile expand/collapse chrome. Presentation only. No data changes.
 */

import { useState, type ReactNode } from "react";

type MobileToggleProps = {
  readonly open: boolean;
  readonly label: string;
  readonly onToggle: () => void;
};

/**
 * Thumb-zone disclosure control. Hidden on desktop via CSS.
 */
export function MobileToggle({ open, label, onToggle }: MobileToggleProps): ReactNode {
  return (
    <button
      type="button"
      className="bte-mobile-toggle"
      data-thumb-zone="true"
      aria-expanded={open}
      onClick={onToggle}
    >
      {open ? "Thu gọn" : label}
    </button>
  );
}

/**
 * Local open state for mobile disclosure. Desktop CSS ignores it.
 */
export function useMobileOpen(): {
  readonly open: boolean;
  readonly toggle: () => void;
} {
  const [open, setOpen] = useState(false);
  return {
    open,
    toggle: () => setOpen((value) => !value),
  };
}
