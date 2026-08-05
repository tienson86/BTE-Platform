import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import { BaseButton } from "../base/BaseButton";

export type DialogProps = HTMLAttributes<HTMLDivElement> & {
  open: boolean;
  title?: ReactNode;
  children?: ReactNode;
  onClose?: () => void;
  closeLabel?: string;
};

/** WP02 Dialog — presentational modal dialog (caller controls open). */
export function Dialog({
  open,
  title,
  children,
  onClose,
  closeLabel = "Close",
  className,
  ...rest
}: DialogProps) {
  if (!open) {
    return null;
  }
  return (
    <div className="cui-dialog-root" role="presentation">
      <button
        type="button"
        className="cui-dialog-backdrop"
        aria-label={closeLabel}
        onClick={onClose}
      />
      <div
        className={cx("cui-dialog", className)}
        role="dialog"
        aria-modal="true"
        aria-label={typeof title === "string" ? title : undefined}
        {...rest}
      >
        {title ? <div className="cui-dialog__title">{title}</div> : null}
        <div className="cui-dialog__body">{children}</div>
        {onClose ? (
          <div className="cui-dialog__footer">
            <BaseButton variant="secondary" onClick={onClose}>
              {closeLabel}
            </BaseButton>
          </div>
        ) : null}
      </div>
    </div>
  );
}
