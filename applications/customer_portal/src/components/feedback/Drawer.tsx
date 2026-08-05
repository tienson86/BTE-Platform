import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import { BaseButton } from "../base/BaseButton";

export type DrawerSide = "start" | "end";

export type DrawerProps = HTMLAttributes<HTMLDivElement> & {
  open: boolean;
  title?: ReactNode;
  children?: ReactNode;
  side?: DrawerSide;
  onClose?: () => void;
  closeLabel?: string;
};

/** WP02 Drawer — slide-over panel (caller controls open). */
export function Drawer({
  open,
  title,
  children,
  side = "end",
  onClose,
  closeLabel = "Close",
  className,
  ...rest
}: DrawerProps) {
  if (!open) {
    return null;
  }
  return (
    <div className="cui-drawer-root" data-side={side} role="presentation">
      <button
        type="button"
        className="cui-drawer-backdrop"
        aria-label={closeLabel}
        onClick={onClose}
      />
      <aside
        className={cx("cui-drawer", className)}
        role="dialog"
        aria-modal="true"
        {...rest}
      >
        {title ? <div className="cui-drawer__title">{title}</div> : null}
        <div className="cui-drawer__body">{children}</div>
        {onClose ? (
          <div className="cui-drawer__footer">
            <BaseButton variant="secondary" onClick={onClose}>
              {closeLabel}
            </BaseButton>
          </div>
        ) : null}
      </aside>
    </div>
  );
}
